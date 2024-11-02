from typing import Protocol, Literal
import psycopg2
import csv, json, pathlib, sqlite3, copy
from collections import defaultdict

import psycopg2._psycopg
from .utils.schema_objects import SQLSchema, SQLColumn
from .utils.type_maps import SQLITE_TYPES, POSTGRES_TYPES, POSTGIS_TYPES, RECORD_INVERT_OPTIONS
from .utils.type_defs import Check, Where, Join
from .utils.errors import DatabaseInterfaceError, Error
from .utils.printer import Printer

class Database(Protocol):

    printer:Printer = Printer()

    @property
    def name(self) -> str:
        ...

    @property
    def db_conn(self) -> psycopg2.extensions.connection | sqlite3.Connection:
        ...
    @property
    def type_map(self) -> dict:
        ...
    @property
    def binding_char(self) -> str:
        ...

    @property
    def table_list(self):
        ...

    @property
    def table_ptr(self):
        ...
    @property
    def table_name(self):
        ...
    @table_name.setter
    def table_name(self, input):
        ...

    def infer_type(self, val:str) -> str:
        ...

    def get_schema(self, table_name:str) -> SQLSchema:
        ...
    
    def print_table(self, table_name:str):
        recs, schema = self.table_to_records(table_name, return_schema=True)
        self.printer.print_table(recs, schema.col_name_list, schema.col_count)

    def records_to_table(self, table_name:str, table_records:list[dict], 
                         if_exists:Literal["append", "replace", "fail"], 
                         col_overrides:list[SQLColumn]=[], deep_evaluation:bool=False) -> None:
        schema = self.get_schema(table_name)

        if schema and if_exists == "append":
            schema.filter_columns(list(table_records[0].keys()))

        elif if_exists == "replace" or not schema:
            self.drop_table(table_name)
            if deep_evaluation:
                schema = self.deep_schema_evaluation(table_records, col_overrides)
            else:
                schema = self.evaluate_schema(table_records, col_overrides)
            self.create_blank_table(table_name, schema)

        elif if_exists == "fail":
            self.table_name = table_name
            raise DatabaseInterfaceError(Error.TABLE_EXISTS, db_name=self.name, table_name=self.table_ptr)
        else:
            raise DatabaseInterfaceError(Error.INVALID_REC_TO_TABLE_OP)
            
        insert_statement = self.insert_into_table_statement(table_name, schema)
        table_records_sql = [tuple(val for val in row.values()) for row in table_records]
        cur = self.db_conn.cursor()
        cur.executemany(insert_statement, table_records_sql)
        self.db_conn.commit()

    
    def table_to_records(self, table_name:str, columns:str="*", where_clause:Where=None, return_schema:bool=False) -> list[dict] | tuple[list[dict], SQLSchema]:
        self.table_name = table_name
        schema:SQLSchema = self.get_schema(table_name)
        table_data = self.get_table(table_name, columns, where_clause)

        if columns != "*":
            schema.filter_columns(columns.split(", "))
            
        records = []
        for row in table_data:
            record_row = {}
            for col_name, sql_col in schema.schema_map.items():
                record_row[col_name] = row[sql_col.position - 1]
            records.append(record_row)

        if return_schema:
            return records, schema
        else:
            return records



    ### DATABASE TASKS ###

    def execute_query(self, sql_statement:str) -> sqlite3.Cursor | psycopg2._psycopg.cursor:
        cur = self.db_conn.cursor()
        cur.execute(sql_statement)
        self.db_conn.commit()
        return cur

    def create_blank_table(self, table_name:str, schema:SQLSchema) -> None:
        sql = self.create_table_statement(table_name, schema)
        self.execute_query(sql)

    def drop_table(self, table_name) -> None:
        self.execute_query(f"DROP TABLE IF EXISTS {table_name}")
    
    def get_table(self, table_name:str, columns:str="*", where_clause:Where=None) -> list[tuple]:
        select_statement = self.select_table_statement(table_name, columns, where_clause)
        cur = self.db_conn.cursor()
        try:
            cur.execute(select_statement)
        except:
            raise DatabaseInterfaceError(Error.TABLE_NOT_EXIST, db_name=self.name, table_name=self.table_ptr)
        return cur.fetchall()
    
    def migrate_table_to(self, table_name:str, target_db) -> None:
        target_db:Database
        table_data, table_schema = self.table_to_records(table_name, return_schema=True)
        ## Currently cannot support check constraint migration
        ## This just empties it out until a future update
        for col in table_schema.schema_map.values():
            col.check_constraint = None

        target_db.create_blank_table(table_name, table_schema)
        if table_data:
            target_db.records_to_table(table_name, table_data, "append")

    def join(self, base_table:str, joins:list[Join], return_cols:list[str]):
        joins = copy.deepcopy(joins)
        for join in joins:
            self.table_name = join.join_table
            join.join_table = self.table_ptr

            self.table_name = join.join_on_table
            join.join_on_table = self.table_ptr

        for pos, col in enumerate(return_cols):
            self.table_name = col
            return_cols[pos] = self.table_ptr

        query = f"SELECT {', '.join(return_cols)}\nFROM {base_table}\n"
        for join in joins:
            query += join.query + "\n"
        
        return self.execute_query(query).fetchall()


    ### DATABASE TASKS ###


    ### TABLE ALTERATIONS ###

    def update_with_unique_records(self, table_name:str, records:list[dict], unique_key_col:str) -> None:
        cur = self.db_conn.cursor()
        for row in records:
            update_statement = self.create_update_statement(table_name, row, f"WHERE {unique_key_col}='{row[unique_key_col]}'")
            cur.execute(update_statement)
        self.db_conn.commit()

    def delete_rows(self, table_name:str, where_clause:Where) -> None:
        delete_statement = self.create_delete_statement(table_name, where_clause)
        self.execute_query(delete_statement)

    def delete_all_records(self, table_name:str) -> None:
        self.table_name = table_name
        self.execute_query(f"DELETE FROM {self.table_ptr};")

    def add_column(self, table_name:str, col_name:str, data_type:SQLITE_TYPES | POSTGRES_TYPES | POSTGIS_TYPES) -> None:
        self.table_name = table_name
        self.execute_query(f"ALTER TABLE {self.table_ptr} ADD {col_name} {self.type_map[data_type]};")
    
    def drop_column(self, table_name:str, col_name:str) -> None:
        self.table_name = table_name
        self.execute_query(f"ALTER TABLE {self.table_ptr} DROP COLUMN {col_name}")
    
    def rename_column(self, table_name:str, col_name:str, new_col_name:str) -> None:
        self.table_name = table_name
        self.execute_query(f"ALTER TABLE {self.table_ptr} RENAME COLUMN {col_name} TO {new_col_name}")

    def rename_table(self, table_name:str, new_table_name:str) -> None:
        self.table_name = table_name
        self.execute_query(f"ALTER TABLE {self.table_ptr} RENAME TO {new_table_name}")
        
    ### TABLE ALTERATIONS ###


    ### STATEMENT BUILDERS ###

    def create_table_statement(self, table_name:str, schema:SQLSchema) -> str:
        statement = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for col_name, sql_col in schema.schema_map.items():
            statement += f"{col_name} {self.type_map[sql_col.data_type]}"
            if sql_col.primary_key:
                statement = statement + f" PRIMARY KEY"
            if sql_col.unique and not sql_col.primary_key:
                statement = statement + f" UNIQUE"
            if not sql_col.nullable and not sql_col.primary_key:
                statement = statement + f" NOT NULL"
            if sql_col.default:
                statement = statement + f" DEFAULT {sql_col.default}"
            if sql_col.check_constraint:
                statement = statement + f" {sql_col.check_constraint}"
            if sql_col.foreign_key:
                statement = statement + f" REFERENCES {sql_col.foreign_key.ref_table} ({sql_col.foreign_key.ref_col})"
            statement = statement + ", "
        statement = statement[:-2] + f");"
        return statement

    def select_table_statement(self, table_name:str, columns:str="*", where_clause:Where=None) -> str:
        self.table_name = table_name
        statement = f"SELECT {columns} FROM {self.table_ptr}"
        if where_clause:
            statement += " " + where_clause.query
        statement += ";"
        return statement
    
    def create_update_statement(self, table_name:str, record_row:dict, where_clause:Where) -> str:
        self.table_name = table_name
        statement = f"UPDATE {self.table_ptr} SET "
        for col_name, value in record_row.items():
            statement += f"{col_name}='{value}', "
        statement = statement[:-2] + " " + where_clause.query + ";"
        return statement

    def create_delete_statement(self, table_name:str, where_clause:Where=None) -> str:
        self.table_name = table_name
        statement = f"DELETE FROM {self.table_ptr}"
        if where_clause:
            statement += " " + where_clause.query
        statement += ";"
        return statement

    def insert_into_table_statement(self, table_name:str, schema:SQLSchema) -> str:
        self.table_name = table_name
        statement = f"INSERT INTO {self.table_ptr} ("
        bindings = ""
        for col_name, sql_col in schema.schema_map.items():
            statement += f"{col_name}, "
            bindings += f"{self.binding_char}, "
        statement = statement[:-2] + f") VALUES (" + bindings[:-2] + ");"
        return statement

    ### STATEMENT BUILDERS ###

    #### CSV Functions #####

    def rename_duplicate_columns(self, fieldname_list:list[str]) -> list[str]:
        d = defaultdict(list)
        [d[name].append(seq) for seq, name in enumerate(fieldname_list)]
        for col, count in d.items():
            if len(count) > 1:
                for seq, index in enumerate(count[1:]):
                    fieldname_list[index] = f"{fieldname_list[index]}_{seq+2}"
        return fieldname_list
    
    def csv_to_records(self, csv_path:str) -> list[dict]:
        csv_path:pathlib.Path = pathlib.Path(csv_path)
        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                reader.fieldnames = self.rename_duplicate_columns(reader.fieldnames)
            records = [row for row in reader]
        
        for row in records:
            for key, val in row.items():
                if val == '':
                    row[key] = None
        return records

    def csv_to_table(self, csv_path:str, if_exists:Literal["append", "replace", "fail"], col_overrides:list[SQLColumn]=[]) -> None:
        csv_name = pathlib.Path(csv_path).stem
        records = self.csv_to_records(csv_path)
        self.records_to_table(csv_name, records, if_exists, col_overrides)

    def records_to_csv(self, csv_name:str, table_records:list[dict], csv_path:str=".") -> None:
        headers = table_records[0].keys()
        print(table_records[0])
        with open(f"{csv_path}\\{csv_name}.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(table_records)

    def schema_to_csv(self, table_name:str, save_path:str="."):
        schema = self.get_schema(table_name).to_dict
        self.records_to_csv(f"{table_name}_schema", schema, save_path)

    def table_to_csv(self, table_name:str, file_name:str="", save_path:str=".", columns:str="*", where_clause:Where=None) -> None:
        table_records= self.table_to_records(table_name, columns, where_clause)
        if not file_name:
            file_name = table_name
        self.records_to_csv(file_name, table_records, save_path)
    
    def csv_to_json(self, csv_path:str, json_save_path:str=".") -> None:
        table_name = pathlib.Path(csv_path).stem
        records = self.csv_to_records(csv_path)
        self.records_to_json(table_name, records, json_save_path)

    ### CSV Functions #####

    ### JSON Functions ####

    def json_to_records(self, json_path:str) -> list[dict]:
        json_path:pathlib.Path = pathlib.Path(json_path)
        with open(json_path, "r") as f:
            data = json.load(f)
        
        if type(data) == list or type(data) == tuple:
            invalid = tuple(False for row in data if type(row) != dict)
            if invalid:
                raise Exception(DatabaseInterfaceError(Error.INVALID_RECORD_FORMAT_UNK_LIST))
        elif type(data) == dict:
            invalid = tuple(False for col in data.values() if not type(col) == list or type(col) == tuple)
            if invalid:
                raise Exception(DatabaseInterfaceError(Error.INVALID_RECORD_FORMAT_UNK_DICT))
            data = self.invert_records(data)
            
        return data

    def json_to_table(self, json_path:str, if_exists:Literal["append", "replace", "fail"], col_overrides:list[SQLColumn]=[]) -> None:
        table_name = pathlib.Path(json_path).stem
        records = self.json_to_records(json_path)
        self.records_to_table(table_name, records, if_exists, col_overrides, True)

    def records_to_json(self, json_name:str, table_records:list[dict], json_path:str=".") -> None:
        with open(f"{json_path}\\{json_name}.json", "w") as f:
            json.dump(table_records, f, indent=2)

    def schema_to_json(self, table_name:str, save_path:str=".") -> None:
        schema = self.get_schema(table_name).to_dict
        self.records_to_json(f"{table_name}_schema", schema, save_path)

    def table_to_json(self, table_name:str, file_name:str="", save_path:str=".", columns:str="*", where_clause:Where=None) -> None:
        table_data = self.table_to_records(table_name, columns, where_clause)
        if not file_name:
            file_name = table_name
        self.records_to_json(file_name, table_data, save_path)
    
    def json_to_csv(self, json_path:str, csv_save_path:str=".") -> None:
        table_name = pathlib.Path(json_path).stem
        records = self.json_to_records(json_path)
        self.records_to_csv(table_name, records, csv_save_path)


    ### JSON Functions ####

    ### Record/Schema inspection functions ####
    def invert_records(self, records:list[dict] | dict[list], use_tuple:bool=False) -> list[dict] | dict[list]:
        if type(records) == list:
            if use_tuple:
                new_data = {col: tuple(row[col] for row in records) for col in records[0]}
            else:
                new_data = {col: [row[col] for row in records] for col in records[0]}
            return new_data
        elif type(records) == dict:
            if use_tuple:
                new_data = tuple(dict(zip(records.keys(), row)) for row in zip(*records.values()))
            else:
                new_data = [dict(zip(records.keys(), row)) for row in zip(*records.values())]
            return new_data

    def deep_schema_evaluation(self, records:list[dict] | dict[list], col_overrides:list[SQLColumn]=[]) -> SQLSchema:
        records:dict[list] = self.invert_records(records)

        schema = []
        overide_col_list = tuple(col.name for col in col_overrides)
        
        for pos, (col_name, col_data) in enumerate(records.items(), 1):
            if col_name in overide_col_list:
                col:SQLColumn = col_overrides[overide_col_list.index(col_name)]
                schema.append(SQLColumn(name=col.name, 
                                        data_type=self.type_map[col.data_type], 
                                        position=pos, 
                                        is_primary_key=col.primary_key, 
                                        foreign_key=col.foreign_key, 
                                        is_unique=col.unique, 
                                        check_constraint=col.check_constraint,
                                        not_null=col.nullable, 
                                        default=col.default))
            else:
                col_type = tuple(self.infer_type(x)for x in col_data if x != None)
                if len(set(col_type)) > 1:
                    raise DatabaseInterfaceError(Error.MIXED_COL_TYPES, col_name)
                schema.append(SQLColumn(name=col_name, data_type=col_type[0], position=pos))

        return SQLSchema(schema)

    def evaluate_schema(self, records:list[dict], col_overrides:list[SQLColumn]=[]) -> SQLSchema:

        def find_non_null_record(records:list[dict], col_name:str):
            for row in records:
                if row[col_name]:
                    return row[col_name]
            return "empty_col_default_to_string"

        schema = []
        try:
            top_row:dict = records[0]
        except:
            Exception(DatabaseInterfaceError(Error.INVALID_RECORD_FORMAT, type_err=type(records)))
        overide_col_list = tuple(col.name for col in col_overrides)

        for pos, (col_name, col_val) in enumerate(top_row.items()):
            if col_name in overide_col_list:
                col:SQLColumn = col_overrides[overide_col_list.index(col_name)]
                schema.append(SQLColumn(name=col.name, 
                                        data_type=self.type_map[col.data_type], 
                                        position=pos, 
                                        is_primary_key=col.primary_key, 
                                        foreign_key=col.foreign_key, 
                                        is_unique=col.unique, 
                                        check_constraint=col.check_constraint,
                                        not_null=col.nullable, 
                                        default=col.default))
            else:
                if col_val:
                    d_type = self.infer_type(col_val)
                else:
                    d_type = self.infer_type(find_non_null_record(records, col_name))
                schema.append(SQLColumn(name=col_name, data_type=d_type, position=pos))

        return SQLSchema(schema)