class TableColumnBronze:
    def __init__(
        self,
        name: str,
        alias: str,
        data_type: str,
        nullable: bool,
        column_type: str = "",
    ):
        self.name = name
        self.alias = alias
        self.data_type = data_type
        self.nullable = nullable
        self.column_type = column_type

    def __str__(self):
        nullable_str = "NOT NULL" if not self.nullable else ""
        return f"{self.name} {self.data_type} {nullable_str}".strip()


class TableColumnSilver:
    def __init__(
        self, name: str, data_type: str, nullable: bool, column_type: str = ""
    ):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.column_type = column_type

    def __str__(self):
        nullable_str = "NOT NULL" if not self.nullable else ""
        return f"{self.name} {self.data_type} {nullable_str}".strip()
