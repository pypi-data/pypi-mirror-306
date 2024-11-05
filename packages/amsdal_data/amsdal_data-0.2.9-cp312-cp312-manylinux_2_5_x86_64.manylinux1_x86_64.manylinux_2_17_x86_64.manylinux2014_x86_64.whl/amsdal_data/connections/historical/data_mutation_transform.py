import time
from collections.abc import Sequence
from copy import copy
from typing import TYPE_CHECKING
from typing import Any
from typing import Union

import amsdal_glue as glue
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.metadata import Metadata
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.identifier import get_identifier

from amsdal_data.connections.constants import METADATA_KEY
from amsdal_data.connections.constants import METADATA_TABLE
from amsdal_data.connections.constants import OBJECT_ID
from amsdal_data.connections.constants import OBJECT_VERSION
from amsdal_data.connections.constants import PRIMARY_PARTITION_KEY
from amsdal_data.connections.constants import REFERENCE_TABLE
from amsdal_data.connections.constants import SECONDARY_PARTITION_KEY
from amsdal_data.connections.constants import TRANSACTION_TABLE
from amsdal_data.connections.historical.data_query_transform import METADATA_TABLE_ALIAS
from amsdal_data.connections.historical.data_query_transform import NEXT_VERSION_FIELD
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager
from amsdal_data.connections.historical.table_name_transform import TableNameTransform

if TYPE_CHECKING:
    from amsdal_data.connections.postgresql_historical import PostgresHistoricalConnection
    from amsdal_data.connections.sqlite_historical import SqliteHistoricalConnection


class DataMutationTransform:
    def __init__(
        self,
        connection: Union['SqliteHistoricalConnection', 'PostgresHistoricalConnection'],
        mutation: DataMutation,
    ) -> None:
        self.connection = connection
        self.mutation = copy(mutation)
        self._data: list[glue.Data] | None = None

    @property
    def is_internal_tables(self) -> bool:
        return self.mutation.schema.name in (METADATA_TABLE, REFERENCE_TABLE, TRANSACTION_TABLE)

    @property
    def data(self) -> list[glue.Data] | None:
        return self._data

    def transform(self) -> Sequence[DataMutation]:
        if self.is_internal_tables:
            return [self.mutation]

        if isinstance(self.mutation, glue.InsertData):
            return self._transform_insert_data(self.mutation)
        if isinstance(self.mutation, glue.UpdateData):
            return self._transform_update_data(self.mutation)
        if isinstance(self.mutation, glue.DeleteData):
            return self._transform_delete_data(self.mutation)

        msg = f'Unsupported mutation type: {type(self.mutation)}'
        raise ValueError(msg)

    def _transform_insert_data(self, mutation: glue.InsertData) -> Sequence[DataMutation]:
        self._process_data(mutation.schema, mutation.data, is_insert=True)
        self._data = mutation.data

        return self._build_insert_mutations(mutation.schema, mutation.data)

    def _transform_update_data(self, mutation: glue.UpdateData) -> Sequence[DataMutation]:
        # AMSDAL ORM always put whole object in update mutation
        self._process_data(mutation.schema, [mutation.data])
        self._data = [mutation.data]

        return self._build_insert_mutations(mutation.schema, [mutation.data])

    def _transform_delete_data(self, mutation: glue.DeleteData) -> Sequence[DataMutation]:
        stored_items = self.connection.query(
            glue.QueryStatement(
                table=mutation.schema,
                where=mutation.query,
            ),
        )
        self._process_data(mutation.schema, stored_items, mark_as_deleted=True)
        self._data = stored_items

        return self._build_insert_mutations(mutation.schema, stored_items)

    def _process_data(
        self,
        schema_reference: glue.SchemaReference,
        data: list[glue.Data],
        *,
        is_insert: bool = False,
        mark_as_deleted: bool = False,
    ) -> None:
        from amsdal_data.transactions.manager import AmsdalTransactionManager

        for _data in data:
            _metadata = Metadata(**_data.data[METADATA_KEY])

            if mark_as_deleted:
                _metadata.is_deleted = True
                _metadata.updated_at = round(time.time() * 1000)

                if _transaction := AmsdalTransactionManager().transaction_object:
                    _metadata.transaction = _transaction.address

            if (
                _metadata.address.object_version
                in (
                    Versions.LATEST,
                    glue.Version.LATEST,
                )
                or mark_as_deleted
            ):
                if is_insert:
                    current_version = None
                    new_version = get_identifier()
                else:
                    current_version = self._resolve_current_version(
                        glue.SchemaReference(name=schema_reference.name, version=glue.Version.ALL),
                        object_id=_data.data[PRIMARY_PARTITION_KEY],
                    )
                    new_version = get_identifier()

                _metadata.prior_version = current_version
                _metadata.address.object_version = new_version

            _data.data[METADATA_KEY] = _metadata.model_dump(exclude={'next_version'})
            _data.data[SECONDARY_PARTITION_KEY] = _metadata.address.object_version

    @classmethod
    def _build_insert_mutations(cls, schema: glue.SchemaReference, data: list[glue.Data]) -> Sequence[glue.InsertData]:
        schema_version_manager = HistoricalSchemaVersionManager()
        TableNameTransform.process_table_name(schema)
        _mutations = []

        for _data in data:
            _item = copy(_data.data)
            _metadata_data = _item.pop(METADATA_KEY)
            _metadata_object = Metadata(**_metadata_data)

            for _ref, _class_name_attr, _class_version_attr in (
                (_metadata_object.address, 'class_name', 'class_version'),
                (_metadata_object.class_schema_reference.ref, 'class_name', 'class_version'),
                (_metadata_object.class_schema_reference.ref, 'object_id', 'object_version'),
                (getattr(_metadata_object.class_meta_schema_reference, 'ref', None), 'class_name', 'class_version'),
                (getattr(_metadata_object.class_meta_schema_reference, 'ref', None), 'object_id', 'object_version'),
            ):
                if not _ref:
                    continue

                _class_name = getattr(_ref, _class_name_attr)
                _class_version = getattr(_ref, _class_version_attr)

                if _class_version in (Versions.LATEST, glue.Version.LATEST, ''):
                    _class_version = (
                        schema_version_manager.get_latest_schema_version(
                            _class_name,
                        )
                        or Versions.LATEST
                    )

                    setattr(_ref, _class_version_attr, _class_version)

            _metadata = _metadata_object.model_dump(exclude={'next_version'})
            _metadata[PRIMARY_PARTITION_KEY] = get_identifier()
            _metadata[OBJECT_ID] = _item[PRIMARY_PARTITION_KEY]
            _metadata[OBJECT_VERSION] = _item[SECONDARY_PARTITION_KEY]

            _inserts = [
                glue.InsertData(schema=schema, data=[glue.Data(data=_item)]),
                glue.InsertData(
                    schema=glue.SchemaReference(name=METADATA_TABLE, version=glue.Version.LATEST),
                    data=[glue.Data(data=_metadata)],
                ),
            ]
            _references: list[glue.Data] = []
            cls._generate_references(_metadata_object.address, _item, _references)

            if _references:
                _inserts.append(
                    glue.InsertData(
                        schema=glue.SchemaReference(name=REFERENCE_TABLE, version=glue.Version.LATEST),
                        data=_references,
                    ),
                )

            _mutations.extend(_inserts)

        return _mutations

    def _resolve_current_version(
        self,
        schema_reference: glue.SchemaReference,
        object_id: str,
    ) -> str | None:
        _query = glue.QueryStatement(
            table=schema_reference,
            where=glue.Conditions(
                glue.Condition(
                    field=glue.FieldReference(
                        field=glue.Field(name=PRIMARY_PARTITION_KEY),
                        table_name=schema_reference.name,
                    ),
                    lookup=glue.FieldLookup.EQ,
                    value=glue.Value(value=object_id),
                ),
                glue.Conditions(
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=NEXT_VERSION_FIELD),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                        lookup=glue.FieldLookup.ISNULL,
                        value=glue.Value(value=True),
                    ),
                    glue.Condition(
                        field=glue.FieldReference(
                            field=glue.Field(name=NEXT_VERSION_FIELD),
                            table_name=METADATA_TABLE_ALIAS,
                        ),
                        lookup=glue.FieldLookup.EQ,
                        value=glue.Value(value=''),
                    ),
                    connector=glue.FilterConnector.OR,
                ),
            ),
            limit=glue.LimitQuery(limit=1),
        )

        _data = self.connection.query(_query)

        if not _data:
            return None

        return _data[0].data[SECONDARY_PARTITION_KEY]

    @classmethod
    def _generate_references(
        cls,
        address: Address,
        data: Any,
        reference_buffer: list[glue.Data],
    ) -> None:
        if cls._is_reference(data):
            reference_buffer.append(
                glue.Data(
                    data={
                        PRIMARY_PARTITION_KEY: get_identifier(),
                        'from_address': address.model_dump(),
                        'to_address': data['ref'],
                    },
                ),
            )
        elif isinstance(data, list):
            for data_value in data:
                cls._generate_references(address, data_value, reference_buffer)

        elif isinstance(data, dict):
            for data_value in data.values():
                cls._generate_references(address, data_value, reference_buffer)

    @staticmethod
    def _is_reference(data: Any) -> bool:
        return isinstance(data, dict) and ['ref'] == list(data.keys()) and isinstance(data['ref'], dict)
