from typing import Literal, TypedDict
from .type_maps import POSTGIS_TYPES
from .type_defs import ForeignKey, Check
from .printer import Printer

TYPES = POSTGIS_TYPES

class SQLColumn:
    __slots__ = ('name', 'data_type', 'position', 'nullable', 'primary_key', 
                 'foreign_key', 'unique', 'check_constraint', 'default', 'printer', 'print')
    def __init__(self, name:str, data_type:TYPES, position:int=1, primary_key:bool=False, 
                 nullable=True, unique:bool=False, default=None, check_constraint:Check=None, 
                 foreign_key:ForeignKey=None):
        
        self.printer = Printer()
        self.print = self.printer.print_column
        
        self.position:int = position
        self.name:str = name
        self.data_type:TYPES = data_type

        self.primary_key:bool = primary_key
        self.foreign_key:ForeignKey = foreign_key
        self.nullable:bool = nullable
        self.unique:bool = unique
        self.default = default
        self.check_constraint:Check = check_constraint

    def __repr__(self) -> str:
        return self.print(self.position, self.name, self.data_type, self.primary_key, self.foreign_key, 
                          self.nullable, self.unique, self.default, self.check_constraint)
    
    @property
    def to_dict(self) -> dict:
        return {"position": self.position, "name": self.name, "data_type": self.data_type, "primary_key": self.primary_key,
                "foreign_key": self.foreign_key, "nullable": self.nullable, "unique": self.unique, "default": self.default,
                "check_constraint": self.check_constraint}

class SQLSchema:
    def __init__(self, sql_cols:list[SQLColumn]):
        self.printer = Printer()
        self.__schema:dict[str, SQLColumn] = {row.name : row for row in sql_cols}
        self.order_columns()

    @property
    def schema_map(self) -> dict[str, SQLColumn]:
        return self.__schema
    @schema_map.setter
    def schema_map(self, input):
        self.__schema = input
    
    @property
    def col_name_list(self) -> tuple[str]:
        return tuple(col.name for col in self.schema_map.values())
    @property
    def positions_list(self) -> tuple[int]:
        return tuple(col.position for col in self.schema_map.values())
    @property
    def col_positions(self) -> dict[str, int]:
        return {key:col.position for key, col in self.schema_map.items()}
    @property
    def col_count(self) -> int:
        return len(self.__schema)
    
    def order_by_location(self):
        for pos, col_name in enumerate(self.schema_map.keys()):
            self.schema_map[col_name].position = pos + 1

    def order_by_position_id(self):
        temp_schema = {}
        sort_pos = sorted(self.col_positions.items(), key=lambda x: x[1])
        for col in sort_pos:
            temp_schema[col[0]] = self.schema_map[col[0]]
        
        self.schema_map = temp_schema
        
    def add_column(self, col:SQLColumn):
        self.schema_map[col.name] = col
        self.order_columns()

    def drop_column(self, col_name):
        del self.schema_map[col_name]
        self.order_columns()

    def order_columns(self):
        pos_list = sorted(self.positions_list)
        if pos_list == tuple(range(min(pos_list), max(pos_list)+1)) and pos_list[0] == 1:
            self.order_by_position_id()
        else:
            self.order_by_location()

    def filter_columns(self, col_name_list:list):
        extract_map = {}
        for col_name in col_name_list:
            extract_map[col_name] = self.schema_map[col_name]
        self.schema_map = extract_map
        self.order_by_location()
    
    def __repr__(self) -> str:
        text = ""
        text += self.printer.get_schema_header()
        for sql_col in self.schema_map.values():
            text += f"{sql_col}\n"
        text += self.printer.get_schema_footer()
        return text

    @property
    def to_dict(self) -> list[dict]:
        return [col.to_dict for col in self.schema_map.values()]

