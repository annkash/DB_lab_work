from tkinter import ttk
from gui import view
import customtkinter
import tkinter as tk
from gui import model
from pandastable import Table
import pandas as pd

class Controller:

    def __init__(self, view, model):
        self._view = view
        self._model = model
        self.open_table = False

    def get_list_db(self):
        return self._model.get_list_db()

    def delete_database_window_event(self, database):
        self._model.delete_database(database)
        self._view.delete_database_window.destroy()
        self._view.delete_database_window.update()

    def get_list_tables(self, database):
        return self._model.get_list_tables(database)

    def get_columns(self, database, table):
        return self._model.get_columns(database, table)


    def add_data_to_table(self,database, table, data_entries, info_label):
        data_list = []
        for i in range(0, len(data_entries)):
            data_list.append(data_entries[i].get())
        if '' in data_list:
            info_label.configure(text='Некоторые поля не заполнены', text_color='red')
            pass
        else:
            self._model.add_data_to_table(database, table, data_list)
            info_label.configure(text='Данные добавлены', text_color='green')

