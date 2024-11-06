from .columns import TableColumnBronze, TableColumnSilver
from datetime import datetime


class DataTableBronze:
    def __init__(self, schema_name, table_prefixo, table_name, columns=[]):
        self.columns = columns
        self.schema_name = schema_name
        self.table_name = table_name
        self.table_prefixo = table_prefixo

    def add_column(
        self, name: str, data_type: str, nullable: bool, column_type: str = ""
    ):
        column = TableColumnBronze(name, "", data_type, nullable, column_type)
        self.columns.append(column)

    def getPk(self):
        for column in self.columns:
            if column.column_type.upper() == "PK":
                return column
        return None

    def getNoPk(self):
        non_pk_columns = []
        for column in self.columns:
            if column.column_type.upper() != "PK":
                non_pk_columns.append(column)
        return non_pk_columns


class DataTableSilver:
    def __init__(self, schema_name, table_prefixo, table_name, columns=[]):
        self.schema_name = schema_name
        self.table_prefixo = table_prefixo
        self.table_name = table_name
        self.columns = columns
        setattr(self, f"{self.table_prefixo}_dh_carga", datetime.now())

    def add_column(
        self, name: str, data_type: str, nullable: bool, column_type: str = ""
    ):
        column = TableColumnSilver(name, data_type, nullable, column_type)
        self.columns.append(column)

    def getPk(self):
        for column in self.columns:
            if column.column_type == "PK":
                return column
        return None


class DataTableSilverHub(DataTableSilver):
    def __init__(self, schema_name, table_prefixo, table_name, columns=[]):
        super().__init__(schema_name, table_prefixo, table_name, columns)


class DataTableSilverLink(DataTableSilver):
    def __init__(self, schema_name, table_prefixo, table_name, columns=[]):
        super().__init__(schema_name, table_prefixo, table_name, columns)


class DataTableSilverSatellite(DataTableSilver):
    def __init__(self, schema_name, table_prefixo, table_name, columns=[]):
        super().__init__(schema_name, table_prefixo, table_name, columns)
        setattr(self, f"{self.table_prefixo}_dh_expiracao", None)
        setattr(self, f"{self.table_prefixo}_st_deletado", None)
