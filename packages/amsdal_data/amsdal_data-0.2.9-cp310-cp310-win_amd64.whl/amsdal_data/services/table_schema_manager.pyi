import amsdal_glue as glue
from _typeshed import Incomplete
from amsdal_data.aliases.using import LAKEHOUSE_DB_ALIAS as LAKEHOUSE_DB_ALIAS
from amsdal_data.errors import RegisterTableError as RegisterTableError
from amsdal_data.transactions.manager import AmsdalTransactionManager as AmsdalTransactionManager
from amsdal_utils.models.data_models.address import Address as Address
from amsdal_utils.utils.singleton import Singleton

class TableSchemasManager(metaclass=Singleton):
    _operation_manager: Incomplete
    def __init__(self) -> None: ...
    def register_table(self, schema: glue.Schema, *, using: str | None = None) -> None:
        """
        Creates a new table in the database through connection.
        """
    def unregister_table(self, address: Address, *, using: str | None = None) -> None: ...
    def _get_existing_schema(self, schema: glue.Schema, *, using: str | None = None) -> glue.Schema | None: ...
    def _create_table(self, schema: glue.Schema, *, using: str | None = None) -> None: ...
    def _update_table(self, schema: glue.Schema, existing_schema: glue.Schema, *, using: str | None = None) -> None: ...
