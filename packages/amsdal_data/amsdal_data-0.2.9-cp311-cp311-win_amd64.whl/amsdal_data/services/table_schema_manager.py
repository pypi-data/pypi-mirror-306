import amsdal_glue as glue
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.utils.singleton import Singleton

from amsdal_data.aliases.using import LAKEHOUSE_DB_ALIAS
from amsdal_data.errors import RegisterTableError
from amsdal_data.transactions.manager import AmsdalTransactionManager


class TableSchemasManager(metaclass=Singleton):
    def __init__(self) -> None:
        from amsdal_data.application import DataApplication

        self._operation_manager = DataApplication().operation_manager

    def register_table(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        """
        Creates a new table in the database through connection.
        """
        existing_schema = self._get_existing_schema(schema, using=using)

        if existing_schema:
            self._update_table(schema, existing_schema, using=using)
        else:
            self._create_table(schema, using=using)

    def unregister_table(
        self,
        address: Address,
        *,
        using: str | None = None,
    ) -> None:
        schema_reference = glue.SchemaReference(name=address.class_name, version=address.class_version)

        if using == LAKEHOUSE_DB_ALIAS:
            result = self._operation_manager.perform_schema_command_lakehouse(
                command=glue.SchemaCommand(
                    mutations=[glue.DeleteSchema(schema_reference=schema_reference)],
                    root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                    transaction_id=AmsdalTransactionManager().transaction_id,
                ),
            )
        else:
            result = self._operation_manager.perform_schema_command(
                command=glue.SchemaCommand(
                    mutations=[glue.DeleteSchema(schema_reference=schema_reference)],
                    root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                    transaction_id=AmsdalTransactionManager().transaction_id,
                ),
            )

        if not result.success:
            msg = f'Failed to unregister schema: {result.message}'
            raise RegisterTableError(msg) from result.exception

    def _get_existing_schema(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> glue.Schema | None:
        if using == LAKEHOUSE_DB_ALIAS:
            _query = self._operation_manager.schema_query_lakehouse
        else:
            _query = self._operation_manager.schema_query

        result = _query(
            filters=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(field=glue.Field(name='name'), table_name='amsdal_schema_registry'),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(schema.name),
                ),
            ),
        )

        if result.success:
            return result.schemas[0] if result.schemas else None

        msg = f'Error while getting schema {schema.name}: {result.message}'
        raise RegisterTableError(msg) from result.exception

    def _create_table(
        self,
        schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        if using == LAKEHOUSE_DB_ALIAS:
            _command = self._operation_manager.perform_schema_command_lakehouse
        else:
            _command = self._operation_manager.perform_schema_command

        result = _command(
            glue.SchemaCommand(
                root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalTransactionManager().transaction_id,
                mutations=[
                    glue.RegisterSchema(schema=schema),
                ],
            ),
        )

        if not result.success:
            msg = f'Error while creating schema {schema.name}: {result.message}'
            raise RegisterTableError(msg) from result.exception

    def _update_table(
        self,
        schema: glue.Schema,
        existing_schema: glue.Schema,
        *,
        using: str | None = None,
    ) -> None:
        schema_reference = glue.SchemaReference(name=schema.name, version=existing_schema.version)
        mutations: list[glue.SchemaMutation] = []
        new_property_names = [_prop.name for _prop in schema.properties]
        existing_property_names = [existing_prop.name for existing_prop in existing_schema.properties]

        for existing_prop in existing_schema.properties:
            if existing_prop.name not in new_property_names:
                mutations.append(
                    glue.DeleteProperty(schema_reference=schema_reference, property_name=existing_prop.name)
                )
                continue

            new_prop = schema.properties[new_property_names.index(existing_prop.name)]

            # it's all the JSON field
            if existing_prop.type is list:
                existing_prop.type = dict

            if new_prop.type is list:
                new_prop.type = dict

            if existing_prop != new_prop:
                mutations.append(glue.UpdateProperty(schema_reference=schema_reference, property=new_prop))

        for new_prop in schema.properties:
            if new_prop.name not in existing_property_names:
                mutations.append(glue.AddProperty(schema_reference=schema_reference, property=new_prop))

        new_index_names = [index.name for index in schema.indexes or []]
        existing_index_names = [existing_index.name for existing_index in existing_schema.indexes or []]

        for existing_index in existing_schema.indexes or []:
            if existing_index.name not in new_index_names:
                mutations.append(glue.DeleteIndex(schema_reference=schema_reference, index_name=existing_index.name))
                continue

            new_index = (schema.indexes or [])[new_index_names.index(existing_index.name)]

            if existing_index != new_index:
                mutations.append(glue.DeleteIndex(schema_reference=schema_reference, index_name=existing_index.name))
                mutations.append(glue.AddIndex(schema_reference=schema_reference, index=new_index))

        for new_index in schema.indexes or []:
            if new_index.name not in existing_index_names:
                mutations.append(glue.AddIndex(schema_reference=schema_reference, index=new_index))

        new_constraint_names = [constraint.name for constraint in schema.constraints or []]
        existing_constraint_names = [
            existing_constraint.name for existing_constraint in existing_schema.constraints or []
        ]

        for existing_constraint in existing_schema.constraints or []:
            if existing_constraint.name not in new_constraint_names:
                mutations.append(
                    glue.DeleteConstraint(schema_reference=schema_reference, constraint_name=existing_constraint.name)
                )
                continue

            new_constraint = (schema.constraints or [])[new_constraint_names.index(existing_constraint.name)]

            if existing_constraint != new_constraint:
                mutations.append(
                    glue.DeleteConstraint(
                        schema_reference=schema_reference,
                        constraint_name=existing_constraint.name,
                    ),
                )
                mutations.append(glue.AddConstraint(schema_reference=schema_reference, constraint=new_constraint))

        for new_constraint in schema.constraints or []:
            if new_constraint.name not in existing_constraint_names:
                mutations.append(glue.AddConstraint(schema_reference=schema_reference, constraint=new_constraint))

        if not mutations:
            return

        if using == LAKEHOUSE_DB_ALIAS:
            _command = self._operation_manager.perform_schema_command_lakehouse
        else:
            _command = self._operation_manager.perform_schema_command

        result = _command(
            glue.SchemaCommand(
                mutations=mutations,
                root_transaction_id=AmsdalTransactionManager().get_root_transaction_id(),
                transaction_id=AmsdalTransactionManager().transaction_id,
            ),
        )

        if not result.success:
            msg = f'Error while updating schema {schema.name}: {result.message}'
            raise RegisterTableError(msg) from result.exception
