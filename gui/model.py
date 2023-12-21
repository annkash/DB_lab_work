import psycopg2
import pandas as pd

class Model:
    def get_list_db(self):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname='driving_school')
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM get_databases_names();")
        result = cursor.fetchall()
        result_list = [row[0] for row in result]
        databases = result_list[0].split(",")
        cursor.close()
        connect.close()
        return databases

    def create_database(self, database):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname='driving_school')
        cursor = connect.cursor()
        cursor.execute(f"SELECT create_db('{database}');")
        connect.commit()
        cursor.close()
        connect.close()
        connect2 = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor2 = connect2.cursor()
        sql_file = open('gui/template.sql', 'r')
        cursor2.execute(sql_file.read())
        connect2.commit()
        cursor2.close()
        connect2.close()

    def delete_database(self, database):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname='driving_school')
        cursor = connect.cursor()
        cursor.execute(f"SELECT drop_db('{database}');")
        connect.commit()
        cursor.close()
        connect.close()

    def get_list_tables(self, database):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM get_table_names();")
        result = cursor.fetchall()
        result_list = [row[0] for row in result]
        tables = result_list[0].split(",")
        cursor.close()
        connect.close()
        return tables

    def get_table(self, database, table):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM {table};")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        cursor.close()
        connect.close()
        return df

    def get_columns(self, database, table):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM get_table_columns('{table}','{database}');")
        result = cursor.fetchall()
        result_list = [row[0] for row in result]
        columns = result_list[0].split(",")
        cursor.close()
        connect.close()
        return columns

    def add_data_to_table(self, database, table, data_entry_list):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM get_table_columns_type('{table}','{database}');")
        result = cursor.fetchall()
        cursor.close()
        result_list = [row[0] for row in result]
        columns_type = result_list[0].split(",")
        for i in range(len(data_entry_list)):
            if (columns_type[i] != 'integer' and columns_type[i] != 'numeric'):
                data_entry_list[i] = f"''{data_entry_list[i]}''"
        data_entry = ', '.join(data_entry_list)
        cursor_2 = connect.cursor()
        cursor_2.execute(f"SELECT * FROM insert_data('{table}','{data_entry}');")
        connect.commit()
        connect.close()
        cursor_2.close()

    def clear_table(self, database, table):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT one_table_cleaning('{table}');")
        connect.commit()
        cursor.close()
        connect.close()

    def clear_all_tables(self, database):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT full_database_cleaning('{database}');")
        connect.commit()
        cursor.close()
        connect.close()

    def delete_row(self, database, table, row):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM get_table_columns('{table}','{database}');")
        result = cursor.fetchall()
        result_list = [row[0] for row in result]
        columns = result_list[0].split(",")
        cursor.close()
        cursor_2 = connect.cursor()
        try:
            row + 0
            cursor_2.execute(f"SELECT delete_record_by_primary_key('{table}','{columns[0]}',{row});")
        except TypeError:
            cursor_2.execute(f"SELECT delete_record_by_primary_key('{table}','{columns[0]}','{row}');")
        connect.commit()
        connect.close()
        cursor_2.close()

    def change_row(self, database, table, id, num_col, value):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM get_table_columns('{table}','{database}');")
        result = cursor.fetchall()
        result_list = [row[0] for row in result]
        columns = result_list[0].split(",")
        cursor.close()
        cursor_2 = connect.cursor()
        if (id.isdigit() and value.isdigit()):
            cursor_2.execute(f"SELECT update_tuple('{table}','{columns[num_col]}','{columns[0]}',{id},{value});")
        if (id.isdigit() and not value.isdigit()):
            cursor_2.execute(f"SELECT update_tuple('{table}','{columns[num_col]}','{columns[0]}',{id},'{value}');")
        if (not id.isdigit() and value.isdigit()):
            cursor_2.execute(f"SELECT update_tuple('{table}','{columns[num_col]}','{columns[0]}','{id}',{value});")
        if (not id.isdigit() and not value.isdigit()):
            cursor_2.execute(f"SELECT update_tuple('{table}','{columns[num_col]}','{columns[0]}','{id}','{value}');")
        connect.commit()
        connect.close()
        cursor_2.close()

    def find_students_to_city(self, database, city):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT * FROM search_by_address('{city}');")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        connect.commit()
        cursor.close()
        connect.close()
        return df

    def delete_students_to_city(self, database, city):
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname=database)
        cursor = connect.cursor()
        cursor.execute(f"SELECT delete_by_address('{city}');")
        connect.commit()
        cursor.close()
        connect.close()
