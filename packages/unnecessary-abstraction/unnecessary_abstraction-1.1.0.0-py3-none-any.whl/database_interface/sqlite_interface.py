from .database import Database
import sqlite3
from uuid import UUID
from datetime import datetime
import re

from .utils.schema_objects import SQLColumn, SQLSchema
from .utils.type_maps import SQLITE_TYPE_MAP
from .utils.type_defs import Check, ForeignKey
from .utils.errors import DatabaseInterfaceError, Error

class SQLite(Database):
    def __init__(self, sqlite_path:str=":memory:", foreign_keys_on=False):
        super().__init__(self)
        parse_path = sqlite_path.split(".")

        if sqlite_path == ":memory:":
            self.__db_conn = sqlite3.Connection(sqlite_path)        
        elif len(parse_path) == 1:
            sqlite_path = sqlite_path + ".db"
            self.__db_conn = sqlite3.Connection(sqlite_path)
        elif len(parse_path) >= 2 and parse_path[-1] in ["sqlite", "db"]:
                self.__db_conn = sqlite3.Connection(sqlite_path)
        else:
            raise DatabaseInterfaceError(Error.INVALID_SQLITE_NAME)
        
        self.__name = sqlite_path
        self.__binding_char = "?"
        self.__type_map = SQLITE_TYPE_MAP
        if foreign_keys_on:
            cur = self.db_conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            resp = cur.execute("PRAGMA foreign_keys")
            print(f"Foreign Keys being enforced for {sqlite_path}:", bool(resp.fetchall()[0][0]))

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def db_conn(self) -> sqlite3.Connection:
        return self.__db_conn
    @property
    def type_map(self) -> dict:
        return self.__type_map
    @property
    def binding_char(self) -> str:
        return self.__binding_char

    @property
    def table_list(self) -> tuple[str]:
        res = self.execute_query("SELECT name FROM sqlite_master")
        return tuple(table[0] for table in res)

    @property
    def table_ptr(self) -> str:
        return self.__table
    @property
    def table_name(self) -> str:
        return self.__table
    @table_name.setter
    def table_name(self, input):
        self.__table = input

    def get_schema(self, table_name:str) -> SQLSchema | None:
        self.table_name = table_name
        cur = self.db_conn.cursor()
        res = cur.execute(f"PRAGMA table_info({self.table_ptr})").fetchall()
        if not res:
            return None
        
        uniq_inx = tuple(name[1] for name in cur.execute(f"PRAGMA index_list({self.table_ptr})").fetchall())
        if uniq_inx:
            unique_cols = []
            for idx in uniq_inx:
                unique_cols.append(cur.execute(f"PRAGMA index_info({idx})").fetchall())
            unique_cols = tuple(cols[0][2] for cols in unique_cols)
        else:
            unique_cols = tuple()

        checks:str = cur.execute(f"SELECT sql FROM sqlite_master WHERE type = 'table' AND name = '{self.table_ptr}'").fetchall()[0][0]
        checks:tuple[int] = tuple(pos for pos, col in enumerate(checks.split(", ")) if re.search(r"check", col, flags=re.IGNORECASE))

        for_key_list = cur.execute(f"PRAGMA foreign_key_list('{self.table_ptr}');").fetchall()
        for_key_map = {}
        for row in for_key_list:
            for_key_map[row[3]] = ForeignKey(row[2], row[4])
        
        col_list = []
        for col in res:
            if col[3] == 0:
                nullable = True
            else:
                nullable = False
            if col[1] in unique_cols:
                unique = True
            else:
                unique = False
            if col[0] in checks:
                check_con = Check(col[1])
            else:
                check_con = None
            if col[1] in for_key_map:
                for_key = for_key_map[col[1]]
            else:
                for_key = None

            col_list.append(SQLColumn(col[1], col[2], col[0] + 1, bool(col[5]), nullable, unique, col[4], check_con, for_key))
    
        return SQLSchema(col_list)
    
    def infer_type(self, val) -> str:
        if type(val) == int:
            return "integer"
        elif type(val) == float:
            return "real"
        elif type(val) == bool:
            return "text"
        elif type(val) == UUID:
            return "uuid"
        elif type(val) == datetime:
            return "text"
        elif type(val) == dict or type(val) == list or type(val) == tuple:
            raise Exception(Error.SQLITE_JSON_SUPPORT)
        else:
            val:str
            split = val.split(".")
            if len(split) == 2 and split[0].isnumeric() and split[1].isnumeric():
                return "real"
            elif val.isnumeric():
                if val == "0":
                    return "numeric"
                else:
                    return "integer"
            else:
                return "text"