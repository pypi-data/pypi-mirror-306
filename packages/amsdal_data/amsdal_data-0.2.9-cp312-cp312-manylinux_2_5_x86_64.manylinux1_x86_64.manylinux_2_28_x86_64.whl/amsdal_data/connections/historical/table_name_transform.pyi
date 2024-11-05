import amsdal_glue as glue
from _typeshed import Incomplete
from amsdal_data.connections.historical.command_builder import build_historical_table_name as build_historical_table_name
from amsdal_data.connections.historical.schema_version_manager import HistoricalSchemaVersionManager as HistoricalSchemaVersionManager

class TableNameTransform:
    query: Incomplete
    schema_version_manager: Incomplete
    def __init__(self, query: glue.QueryStatement) -> None: ...
    def transform(self) -> glue.QueryStatement: ...
    @classmethod
    def _process_table_names(cls, query: glue.QueryStatement) -> glue.QueryStatement: ...
    @classmethod
    def process_table_name(cls, table: glue.SchemaReference | glue.SubQueryStatement) -> None: ...
