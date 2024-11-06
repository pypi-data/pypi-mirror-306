from typing import NamedTuple, Literal


class ForeignKey(NamedTuple):
    ref_table:str
    ref_col:str

class Join:
    def __init__(self, table:str, column:str, type:Literal["INNER", "LEFT", "RIGHT", "FULL OUTER"]="INNER") -> None:
        self.__join_table:str = table
        self.__join_column:str = column
        self.__join_on_table:str = ""
        self.__join_on_column:str = ""
        self.__query:str = f"{type} JOIN"

    @property
    def query(self):
        return f"{self.__query} {self.__join_table} ON {self.__join_on_table}.{self.__join_on_column} = {self.__join_table}.{self.__join_column}"

    @property
    def join_table(self) -> str:
        return self.__join_table
    @join_table.setter
    def join_table(self, input):
        self.__join_table:str = input

    @property
    def join_on_table(self) -> str:
        return self.__join_on_table
    @join_on_table.setter
    def join_on_table(self, input):
        self.__join_on_table:str = input

    def on(self, table, col):
        self.__join_on_table:str = table
        self.__join_on_column:str = col
        return self


class Where:
    def __init__(self, value):
        self.__query:str = f"WHERE {value}"

    @property
    def query(self):
        return self.__query

    def and_(self, value):
        self.__query += f" AND {value}"
        return self

    def is_(self, operator:Literal[">", "<", ">=", "<=", "==", "!="], value):
        match operator:
            case "<":
                self.__query += f" < {value}"
            case ">":
                self.__query += f" > {value}"
            case "<=":
                self.__query += f" <= {value}"
            case ">=":
                self.__query += f" >= {value}"
            case "==":
                self.__query += f" == {value}"
            case "!=":
                self.__query += f" != {value}"
        return self

    def between(self, value1, value2):
        self.__query += f" BETWEEN {value1} AND {value2}"
        return self

    def __str__(self):
        return self.__query

class Check:
    def __init__(self, col_name):
        self.__query:str = f"CHECK ({col_name}"

    @property
    def query(self):
        return self.__query

    def and_(self, value):
        self.__query += f" AND {value}"
        return self

    def is_(self, operator:Literal[">", "<", ">=", "<=", "==", "!="], value):
        match operator:
            case "<":
                self.__query += f" < {value}"
            case ">":
                self.__query += f" > {value}"
            case "<=":
                self.__query += f" <= {value}"
            case ">=":
                self.__query += f" >= {value}"
            case "==":
                self.__query += f" == {value}"
            case "!=":
                self.__query += f" != {value}"
        return self

    def between(self, value1, value2):
        self.__query += f" BETWEEN {value1} AND {value2}"
        return self

    def __str__(self):
        return self.__query + ")"
