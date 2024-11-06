from typing import Literal
from enum import IntEnum

class Error(IntEnum):
    TABLE_EXISTS = 1
    TABLE_NOT_EXIST = 2
    MIXED_COL_TYPES = 3
    INVALID_JSON = 4
    SQLITE_JSON_SUPPORT = 5
    INVALID_SQLITE_NAME = 6
    INVALID_REC_TO_TABLE_OP = 7
    INVALID_RECORD_FORMAT = 8
    INVALID_RECORD_FORMAT_UNK_LIST = 9
    INVALID_RECORD_FORMAT_UNK_DICT = 10


PY_DICT_ERROR = """
Your data contains a python dictionary that cannot be formed into a JSON.
Check the values of your dictionary to find what is causing json.dumps()
to error out and convert as necessary. PostgreSQL doesn't have any type
to support this data structure.
"""

INVALID_TABLE_TO_RECORD_ERROR_MSG = """
You either mispelled or didnt select a valid if_exists option. Set it to
either 'append', 'replace', or 'fail' in the situation that the table you 
are trying to send records to already exists in the database.
"""

SQLITE_JSON_SUPPORT_ERROR = """
You are attempting to pass a Python Dict, List or Tuple which does not have an
equivalent type in SQLite. Try converting your values by calling the __str__() method
or using json.dumps() function. SQLite can then maniplulate these data structures
as if they were JSON formatted strings.
"""


class DatabaseInterfaceError(Exception):
    def __init__(self, error:Error, db_name:str="", table_name:str="", col_name:str="", type_err:type=None) -> None:
        match error:
            case Error.TABLE_EXISTS:
                self.message:str = f"Table '{table_name}' is already a table in '{db_name}'."
            case Error.TABLE_NOT_EXIST:
                self.message:str = f"Table '{table_name}' does not exist in '{db_name}'"
            case Error.MIXED_COL_TYPES:
                self.message:str = f"{col_name} has mixed datatypes contained in its column"
            case Error.INVALID_JSON:
                self.message:str = PY_DICT_ERROR
            case Error.SQLITE_JSON_SUPPORT:
                self.message:str = SQLITE_JSON_SUPPORT_ERROR
            case Error.INVALID_SQLITE_NAME:
                self.message:str = "Your SQLite file name must end the extension with .db or .sqlite"
            case Error.INVALID_REC_TO_TABLE_OP:
                self.message:str = INVALID_TABLE_TO_RECORD_ERROR_MSG
            case Error.INVALID_RECORD_FORMAT:
                self.message:str = f"'{type_err}' is not a valid format that can be parsed as a 'table record'"
            case Error.INVALID_RECORD_FORMAT_UNK_LIST:
                self.message:str = "Within your list of table records contains a data structure that isn't a valid dictionary"
            case Error.INVALID_RECORD_FORMAT_UNK_DICT:
                self.message:str = "Within your dictionary of table columns contains a data structure that isn't a valid list of row values"

        super().__init__(self.message)



