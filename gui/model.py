import psycopg2
import pandas as pd
class Model:
    def __init__(self):
        # примеры аттрибутов, принадлежащих бд
        self._list_db = ["dr_school", "dr_school2"]
        self._list_tb = ['cars', 'instructors']
        self._list_cols = ['model', 'id']
        self._list_cols2 = ['id']

    def get_list_db(self):
        return self._list_db

    def delete_database(self, database):
        self._list_db.remove(database)

    def get_list_tables(self, database):
        return self._list_tb

    def get_table(self, database, table):
        # пример для показа таблицы в гуи
        connect = psycopg2.connect(port='5432', host='localhost', user='superuser', password='1',
                                   dbname='driving_school_full')
        cursor = connect.cursor()
        if table == 'cars':
            cursor.execute("SELECT * FROM cars")
        elif table == 'instructors':
            cursor.execute("SELECT * FROM instructors")
        result = cursor.fetchall()
        df = pd.DataFrame(result)
        cursor.close()
        connect.close()
        return df

    def get_columns(self, database, table):
        # пример для теста кнопки
        if (table == 'cars'):
            return self._list_cols
        return self._list_cols2

    def add_data_to_table(self, database, table, data_entry_list):
        pass

    def delete_row(self, database, table, row):
        pass

    def delete_table(self, database, table):
        pass