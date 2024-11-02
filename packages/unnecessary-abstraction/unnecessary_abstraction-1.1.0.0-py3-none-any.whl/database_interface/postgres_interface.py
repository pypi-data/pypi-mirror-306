from .database import Database
import psycopg2
import json
from uuid import UUID
from datetime import datetime

from .utils.schema_objects import SQLColumn, SQLSchema
from .utils.type_maps import POSTGRES_TYPE_MAP, POSTGRES_TYPES
from .utils.type_defs import ForeignKey, Check
from .utils.errors import DatabaseInterfaceError, Error


class PostgreSQL(Database):
    def __init__(self, db_name:str, username:str, password:str, namespace:str, host="localhost", port=5432):
        self.__name = db_name
        self.__db_conn = psycopg2.connect(database=db_name, user=username, password=password, host=host, port=port)
        self.__binding_char = "%s"
        self.__type_map = POSTGRES_TYPE_MAP
        self.__namespace = namespace
        self.__table = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def db_conn(self):
        return self.__db_conn
    
    @property
    def type_map(self) -> dict:
        return self.__type_map
    
    @property
    def binding_char(self) -> str:
        return self.__binding_char
    
    @property
    def table_list(self) -> tuple[str]:
        cur = self.execute_query(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.__namespace}'")
        res = cur.fetchall()
        return tuple(table[0] for table in res)
    
    @property
    def table_ptr(self) -> str:
        return f"{self.__namespace}.{self.__table}"
    @property
    def table_name(self):
        return self.__table
    @table_name.setter
    def table_name(self, input):
        self.__table = input

    @property
    def current_namespace(self):
        return self.__namespace
    @current_namespace.setter
    def current_namespace(self, input:str):
        self.__namespace = input

    def change_col_dtype(self, table_name:str, col_name:str, to_data_type:POSTGRES_TYPES) -> None:
        self.table_name = table_name
        cur = self.db_conn.cursor()
        sql_statement = f"ALTER TABLE {self.table_ptr} ALTER COLUMN {col_name} {self.type_map[to_data_type]}"
        cur.execute(sql_statement)
        self.db_conn.commit()

    def get_schema(self, table_name:str) -> SQLSchema | None:
        self.table_name = table_name
        GET_COL_SCHEMA = f"""
        SELECT column_name, data_type, ordinal_position, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_schema='{self.__namespace}' AND table_name='{table_name}'
        """
        GET_CONSTRAINTS = f"""
        SELECT conname, contype, pg_get_constraintdef(oid) AS constraint_definition
        FROM pg_constraint
        WHERE conrelid = '{self.table_ptr}'::regclass AND contype IN ('p', 'f', 'c', 'u')
        """
        cur = self.db_conn.cursor()
        cur.execute(GET_COL_SCHEMA)
        res = cur.fetchall()
        if not res:
            return None

        cur.execute(GET_CONSTRAINTS)
        res2 = cur.fetchall()
        con_map = {'p': {}, 'u': {}, 'c': {}, 'f': {}}
        for con in res2:
            con:tuple[str]
            match con[1]:
                case 'p':
                    split = con[2].split(" ")
                    con_map['p'][split[2][1:-1]] = "pk"
                case 'u':
                    split = con[2].split(" ")
                    con_map['u'][split[1][1:-1]] = "unique"
                case 'c':
                    split = con[2].split(" ")
                    con_map['c'][split[1][2:]] = "Check"
                case 'f':
                    split = con[2].split(" ")
                    split2 = split[4].split("(")
                    con_map['f'][split[2][1:-1]] = ForeignKey(split2[0], split2[1][:-1])
        
        col_list = []
        for col in res:
            if col[0] in con_map["p"]:
                primary_key = True
            else:
                primary_key = False
            if col[3] == 'YES':
                nullable = True
            else:
                nullable = False
            if col[0] in con_map["u"]:
                unique = True
            else:
                unique = False
            if col[0] in con_map["c"]:
                check_con = Check(col[1])
            else:
                check_con = None
            if col[0] in con_map["f"]:
                for_key = con_map["f"][col[0]]
            else:
                for_key = None
            if col[4]:
                default = col[4].split("::")[0]
            else:
                default = None

            col_list.append(SQLColumn(col[0], col[1], col[2], primary_key, nullable, unique, default, check_con, for_key))

            schema = SQLSchema(col_list)
            return schema
        
    def create_namespace(self, name:str):
        statement = "CREATE SCHEMA " + name + ";"
        cur = self.db_conn.cursor()
        cur.execute(statement)
        self.db_conn.commit()

    def create_database(self, db_name:str, owner:str="", clone_from:str=""):
        statement = "CREATE DATABASE " + db_name
        if owner or clone_from:
            statement += " WITH"
            if clone_from:
                statement += " TEMPLATE " + clone_from
            if owner:
                statement += " OWNER " + owner
        
        statement += ";"
        cur = self.db_conn.cursor()
        cur.execute(statement)
        self.db_conn.commit()

    def infer_type(self, val) -> str:
        def is_datetime(x) -> bool:
            try:
                datetime.fromisoformat(x)
                return True
            except ValueError:
                return False
            
        def string_jsonable(x) -> bool:
            try:
                json.loads(x)
                return True
            except (TypeError, OverflowError, json.decoder.JSONDecodeError):
                return False
        def dict_jsonable(x) -> bool:
            try:
                json.dumps(x)
                return True
            except (TypeError, OverflowError, json.decoder.JSONDecodeError):
                return False

        if type(val) == int:
            return "integer"
        elif type(val) == float:
            return "decimal"
        elif type(val) == bool:
            return "text"
        elif type(val) == UUID:
            return "uuid"
        elif type(val) == datetime:
            return "timestamp"
        elif type(val) == str:
            val:str
            split = val.split(".")
            if len(split) == 2 and split[0].isnumeric() and split[1].isnumeric():
                if len(split[1]) > 8:
                    return "double precision"
                else:
                    return "real"
            elif val.isnumeric():
                if val == "0":
                    return "numeric"
                else:
                    return "integer"
            elif is_datetime(val):
                if datetime.fromisoformat(val).tzinfo:
                    return "timestamp with time zone"
                else:
                    return "timestamp"
            elif string_jsonable(val):
                return "json"
            else:
                return "text"
        elif type(val) == dict or type(val) == list or type(val) == tuple:
            if dict_jsonable(val):
                return "json"
            else:
                raise DatabaseInterfaceError(Error.INVALID_JSON)

