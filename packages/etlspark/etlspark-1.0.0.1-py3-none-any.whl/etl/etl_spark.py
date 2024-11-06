from typing import List
from datatable.tables import DataTableBronze, DataTableSilver


class Bronze_to_silver:
    def __init__(
        self,
        spark,
        datatable_bronze: DataTableBronze,
        datatable_silver: DataTableSilver,
    ):
        self.spark = spark
        self.datatable_bronze = datatable_bronze
        self.datatable_silver = datatable_silver

    def create_database_if_not_exists(self):
        self.spark.sql(
            f"CREATE DATABASE IF NOT EXISTS {self.datatable_silver.table_name}"
        )

    def create_table_silver_if_not_exists(self, manager_type="iceberg"):
        columns_sql = ", ".join(
            [str(column) for column in self.datatable_silver.columns]
        )
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.datatable_silver.schema_name}.{self.datatable_silver.table_name} (
                {columns_sql}
            )
            USING {manager_type}
        """
        self.spark.sql(sql)

    # todo
    def build_comparison_query(self):
        return NotImplementedError(
            "TODO:No futuro essa classe fará o build da query de compraração"
        )

    def merge_data(self, comparison_query):
        sql = f"""
            MERGE INTO {self.datatable_silver.schema_name}.{self.datatable_silver.table_name} AS t
            USING ({comparison_query}) AS s
            ON t.{self.datatable_silver.getPk().name} = s.{self.datatable_bronze.getPk().name}
            WHEN MATCHED THEN
                UPDATE SET t.{self.datatable_silver.table_prefixo}_dh_carga = s.{self.datatable_silver.table_prefixo}_dh_carga
            WHEN NOT MATCHED THEN
                INSERT *
        """
        self.spark.sql(sql)

    def create_or_replace(self, comparison_query):
        self.create_database_if_not_exists()
        self.create_table_silver_if_not_exists()
        self.merge_data(comparison_query)
