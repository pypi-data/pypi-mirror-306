import shutil
import math
from enum import IntFlag
from .type_maps import TRUNCATED
from .type_defs import ForeignKey, Check

class W(IntFlag):
    TOP_HEADER = 0
    BOTTOM_HEADER = 1
    BOTTOM_MARGIN = 2

class Printer:
    __col_width:int = 12
    row_limit:int = 20
    start_row:int = 0
    max_columns:int = 0

    @property
    def col_width(self) -> int:
        return self.__col_width
    @col_width.setter
    def col_width(self, input):
        if input < 7:
            self.__col_width = 7
        else:
            self.__col_width = input

    def print_database(self):
        pass

    def print_table(self, table_records:list[dict], col_name_list:list[str], col_num_count:int):
        PRINT_TABLE = ""
        terminal_x, terminmal_y = self.__get_terminal_size()
        if self.col_width > terminal_x - 9:
            self.col_width = terminal_x - 10
        self.max_columns = math.floor(((terminal_x - 9) / (self.col_width + 1)))
        col_count, col_names, concat_col_pos  = self.__get_concat_position(col_num_count, col_name_list)

        PRINT_TABLE += self.__write_margin(W.TOP_HEADER, self.col_width, col_count, concat_col_pos)
        PRINT_TABLE += f"\n│     │"
        for col in col_names:
            PRINT_TABLE += self.__write_cell(self.col_width, col)
        PRINT_TABLE += self.__write_margin(W.BOTTOM_HEADER, self.col_width, col_count, concat_col_pos)

        for pos, row in enumerate(table_records[self.start_row:]):
            PRINT_TABLE += "│" + str(pos + self.start_row).center(5) + "│"
            for col in col_names:
                if not col == "...":
                    PRINT_TABLE += self.__write_cell(self.col_width, str(row[col]))
                else:
                    PRINT_TABLE += self.__write_cell(self.col_width, col)
            PRINT_TABLE += "\n"
            if pos >= self.row_limit:
                break
        
        PRINT_TABLE += self.__write_margin(W.BOTTOM_MARGIN, self.col_width, col_count, concat_col_pos)
        
        print(PRINT_TABLE)

    def get_schema_header(self):
        PRINT_HEADER = "┌───┐" + "────────────────┐" + "────────────────┐" + "────────────────────────────────────────────────────────────" + "┐"
        PRINT_HEADER += "\n│   │"
        PRINT_HEADER += "col_name".center(16) + "│"
        PRINT_HEADER += "datatype".center(16) + "│"
        PRINT_HEADER += "constraints".center(60) + "│"
        PRINT_HEADER += "\n│───┼" + "────────────────┼" + "────────────────┼" + "────────────────────────────────────────────────────────────" "│\n"

        return PRINT_HEADER
    
    def get_schema_footer(self):
        return "└───┘" + "────────────────┘" + "────────────────┘" + "────────────────────────────────────────────────────────────" "┘\n"

    def print_column(self, position:int, name:str, data_type, primary_key:bool, foreign_key:ForeignKey, 
                     nullable:bool, unique:bool, default, check_constraint:Check):
        
        PRINT_COLUMN = ""
        constraints = ""

        PRINT_COLUMN += "│" + str(position).center(3) + "│"
        if primary_key:
            PRINT_COLUMN += self.__write_cell(16, f"[PK] {name}")
            constraints += "unique, not-null, "
        else:
            PRINT_COLUMN += self.__write_cell(16, f"{name}")
            if unique:
                constraints += "unique, "
            if not nullable:
                constraints += "not-null, "

        PRINT_COLUMN += self.__write_cell(16, f"{TRUNCATED[data_type]}")
        if foreign_key:
            constraints += f"[FK] {foreign_key.ref_table}({foreign_key.ref_col}), "
        if check_constraint:
            constraints += f"check constraint, "
        if default:
            constraints += f"default={default}, "

        constraints = constraints[:-2]
        PRINT_COLUMN += self.__write_cell(60, f"{constraints.ljust(58)}")

        return PRINT_COLUMN

    def __get_terminal_size(self):
        size = shutil.get_terminal_size(fallback=(80, 20))
        return size.columns, size.lines
    
    def __write_margin(self, option:W, col_width:int, col_count:int, concat_col_index:int):
        text = ""
        match option:
            case W.TOP_HEADER:
                leftmost = "┌─────┐"
                rightmost = "┐"
            case W.BOTTOM_HEADER:
                leftmost = "\n│─────┼"
                rightmost = "┼"
            case W.BOTTOM_MARGIN:
                leftmost = "└─────┘"
                rightmost = "┘"

        text += leftmost
        for i in range(col_count):
            dashs = ""
            if i == concat_col_index:
                dashs = "───"
            else:
                for k in range(col_width):
                    dashs += "─"
            text += dashs + rightmost

        if option == W.BOTTOM_HEADER:
            text = text[:-1] + "│\n"

        return text
    
    def __write_cell(self, col_width:int, value:str):
        text = ""
        if value == "...":
            text += value.center(3) + "│"
        else:
            if len(value) > col_width:
                value = value[:col_width-4] + "..."
                text += value.center(col_width) + "│"
            else:
                text += value.center(col_width) + "│"
        return text
    
    def __get_concat_position(self, col_count:int, col_names:tuple[str]) -> tuple[int, tuple[str], int]:
        if self.max_columns == 1:
            concat_col = -1
        elif col_count > self.max_columns:
            size = math.floor(self.max_columns / 2)
            front = col_names[:size]
            back = col_names[(0-size):]
            col_names = front + ("...", ) + back
            col_count = len(col_names)
            concat_col = col_names.index("...")
        else:
            concat_col = -1
        
        return col_count, col_names, concat_col