import tkinter as tk
import customtkinter
from PIL import Image
from gui import controller
from pandastable import Table
import pandas as pd
def error_message(master, error_info):
    info_for_user = customtkinter.CTkLabel(master=master,
                                           text=error_info, text_color='white',
                                           fg_color='#FF3636',
                                           font=customtkinter.CTkFont(family="Helvetica", size=16),
                                           corner_radius=15)
    info_for_user.pack(side='top', pady=20, padx=20)

class View(customtkinter.CTk):

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.title("Управление базой данных автошколы")
        app_width = 800
        app_height = 600
        x,y = self.coord_to_center(app_width, app_height)
        self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.my_font = customtkinter.CTkFont(family="Helvetica", size=16, weight="bold")
        self.iconpath = 'gui/icon.ico'
        self.iconbitmap(self.iconpath)


        customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        logo_frame = customtkinter.CTkFrame(self, width=400, height=400, corner_radius=0)
        logo_frame.pack(side='left', expand=True, fill='both')
        bg_image = customtkinter.CTkImage(light_image=Image.open("gui/bg_image.png"), size=(400, 300))
        bg_image_label = customtkinter.CTkLabel(master=logo_frame, image=bg_image, text='')
        bg_image_label.place(relx=0.5, rely=0.5, anchor='center')

        menu_frame = customtkinter.CTkFrame(self, width=400, height=400, corner_radius=0)
        menu_frame.pack(side='right', expand=True, fill='both')
        menu_options_frame = customtkinter.CTkFrame(menu_frame, width=400, height=400,  corner_radius=10)
        menu_options_frame.place(relx=0.5, rely=0.5, anchor='center')

        operations_label = customtkinter.CTkLabel(master=menu_options_frame, text='Операции с базами данных', font=self.my_font)
        operations_label.pack(pady=5, padx=20)

        create_database_button = customtkinter.CTkButton(menu_options_frame, text="Создать базу данных", command=self.create_database)
        create_database_button.pack(pady=5, padx=5)

        delete_database_button = customtkinter.CTkButton(menu_options_frame, text="Удалить базу данных...", command=self.delete_database)
        delete_database_button.pack(padx=5)

        move_to_database_button = customtkinter.CTkButton(menu_options_frame, text="Перейти к базе данных...", command=self.choose_database)
        move_to_database_button.pack(pady=10, padx=5)

    # calculate center position for window
    def coord_to_center(self, app_width, app_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        return x, y

    def Run(self):
        self.mainloop()

    def create_database(self):
        create_database_window = customtkinter.CTkToplevel(self)
        create_database_window.title('Создание базы данных')
        create_database_window.wm_attributes("-topmost", True)
        create_database_window.after(250, lambda: create_database_window.iconbitmap(self.iconpath))
        width = 400
        height = 150
        x, y = self.coord_to_center(width, height)
        create_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        info_for_user = customtkinter.CTkLabel(master=create_database_window,
                                               text='Введите название для базы данных:',
                                               font=customtkinter.CTkFont(family="Helvetica", size=14))
        info_for_user.pack(side='top', pady=5, padx=20, expand=False)
        db_entry = customtkinter.CTkEntry(create_database_window)
        db_entry.pack(pady=5, padx=5)
        database = db_entry.get()

        ctrl = controller.Controller(self, self._model)

        confirm = customtkinter.CTkButton(create_database_window, text='добавить',
                                          command=lambda: ctrl.create_database(database, create_database_window))
        confirm.pack(pady=5, padx=5)

    def delete_database(self):
        ctrl = controller.Controller(self, self._model)
        list_db = ctrl.get_list_db()

        delete_database_window = customtkinter.CTkToplevel(self)
        delete_database_window.title('Удаление базы данных')
        delete_database_window.wm_attributes("-topmost", True)
        delete_database_window.after(250, lambda: delete_database_window.iconbitmap(self.iconpath))
        width = 400
        height = 150
        x, y = self.coord_to_center(width, height)
        delete_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        if (len(list_db) == 0):
            error_message(delete_database_window, 'Доступных для удаления баз данных нет.')
        else:
            info_for_user = customtkinter.CTkLabel(master=delete_database_window, text='Выберите базу данных, которую хотите удалить:', font=customtkinter.CTkFont(family="Helvetica", size=14))
            info_for_user.pack(side='top', pady=5, padx=20, expand=False)
            db_list_option = customtkinter.CTkOptionMenu(delete_database_window, values=list_db)
            db_list_option.pack(pady=5, padx=5)
            database = db_list_option.get()

            confirm = customtkinter.CTkButton(delete_database_window, text='удалить', fg_color='#FF3636', hover_color='#BA0000', command=lambda: ctrl.delete_database(database, delete_database_window))
            confirm.pack(pady=5, padx=5)

    def choose_database(self):
        ctrl = controller.Controller(self, self._model)
        list_db = ctrl.get_list_db()

        choice_database_window = customtkinter.CTkToplevel(self)
        choice_database_window.title('Выбор базы данных')
        choice_database_window.wm_attributes("-topmost", True)
        choice_database_window.after(250, lambda: choice_database_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 150
        x, y = self.coord_to_center(app_width, app_height)
        choice_database_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        if (len(list_db) == 0):
            error_message(choice_database_window, 'Доступных для просмотра баз данных нет.')
        else:
            info_for_user = customtkinter.CTkLabel(master=choice_database_window,
                                                   text='Выберите базу данных для просмотра:',
                                                   font=customtkinter.CTkFont(family="Helvetica", size=14))
            info_for_user.pack(side='top', pady=5, padx=20, expand=False)

            db_list_option = customtkinter.CTkOptionMenu(choice_database_window, values=list_db)
            db_list_option.pack(pady=5, padx=5)

            confirm = customtkinter.CTkButton(choice_database_window, text='посмотреть', command=lambda: self.interaction_database(db_list_option.get(), choice_database_window))
            confirm.pack(pady=5, padx=5)

    def interaction_database(self, database, choice_database_window):
        choice_database_window.destroy()
        choice_database_window.update()

        self.interaction_database_window = customtkinter.CTkToplevel(self)
        self.interaction_database_window.title(f'{database}')
        self.interaction_database_window.wm_attributes("-topmost", True)
        self.interaction_database_window.after(250, lambda: self.interaction_database_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 400
        x, y = self.coord_to_center(app_width, app_height)
        self.interaction_database_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        ctrl = controller.Controller(self, self._model)
        list_tables = ctrl.get_list_tables(database)

        if(len(list_tables) == 0):
            error_message(self.interaction_database_window, 'В данной базе нет доступных таблиц для просмотра.')
        else:

            menu_frame = customtkinter.CTkFrame(self.interaction_database_window, width=300, height=300)
            menu_frame.place(relx=0.5,rely=0.5,anchor='center')

            view_tables_button = customtkinter.CTkButton(menu_frame, text='посмотреть таблицы', command=lambda: self.view_tables(database))
            view_tables_button.pack(pady=10, padx=5)

            view_students_to_city = customtkinter.CTkButton(menu_frame, text='поиск и удаление студентов по городу', command=lambda: self.view_students_to_city(database))
            view_students_to_city.pack(padx=5)

            add_data_button = customtkinter.CTkButton(menu_frame, text='добавить данные', command=lambda: self.add_data(database))
            add_data_button.pack(padx=5, pady=10)

            change_data_button = customtkinter.CTkButton(menu_frame, text='изменить данные',
                                                      command=lambda: self.change_data(database))
            change_data_button.pack(padx=5)

            delete_data_button = customtkinter.CTkButton(menu_frame, text='удалить запись', command=lambda: self.delete_row(database))
            delete_data_button.pack(pady=10, padx=5)

            clear_table_button = customtkinter.CTkButton(menu_frame, text='очистить таблицу', command=lambda: self.clear_table(database))
            clear_table_button.pack(padx=5)

            clear_tables_button = customtkinter.CTkButton(menu_frame, text='очистить все таблицы', fg_color='#FF3636', hover_color='#BA0000',
                                                          command=lambda: ctrl._model.clear_all_tables(database))
            clear_tables_button.pack(padx=10, pady=10)

    def view_tables(self, database):
        def update_table(table):
            df = pd.DataFrame(self._model.get_table(database, table))
            pt.model.df = df
            pt.redraw()
        view_tables_window = customtkinter.CTkToplevel(self.interaction_database_window)
        view_tables_window.title(f'{database}')
        view_tables_window.wm_attributes("-topmost", True)
        view_tables_window.after(250, lambda: view_tables_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 400
        x, y = self.coord_to_center(app_width, app_height)
        view_tables_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        list_tables = self._model.get_list_tables(database)

        tables_button_default = customtkinter.StringVar(value=list_tables[0])
        tables_button = customtkinter.CTkSegmentedButton(view_tables_window, values=list_tables,
                                                         variable=tables_button_default, command=lambda table: update_table(table))
        tables_button.pack(side='top', anchor='center')
        table_frame = customtkinter.CTkFrame(view_tables_window)
        table_frame.pack(side='bottom', expand=True, fill='both')

        df = pd.DataFrame(self._model.get_table(database, tables_button.get()))
        pt = Table(table_frame, dataframe=df)
        pt.show()

    def add_data(self, database):
        add_data_window = customtkinter.CTkToplevel(self.interaction_database_window)
        add_data_window.title(f'{database}')
        add_data_window.wm_attributes("-topmost", True)
        add_data_window.after(250, lambda: add_data_window.iconbitmap(self.iconpath))
        app_width = 800
        app_height = 600
        x, y = self.coord_to_center(app_width, app_height)
        add_data_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        ctrl = controller.Controller(self, self._model)
        list_tables = ctrl.get_list_tables(database)

        if (len(list_tables) == 0):
            error_message(add_data_window, 'Доступных для добавления данных таблиц нет.')
        else:
            table_choose_frame = customtkinter.CTkFrame(add_data_window)
            table_choose_frame.pack(side='left', fill='y')

            add_data_frame = customtkinter.CTkFrame(add_data_window)
            add_data_frame.pack(side='right', fill='both', expand=True)

            table_label = customtkinter.CTkLabel(table_choose_frame, text="Выберите таблицу:")
            table_label.pack()

            def update_data_entries(table):
                for widget in add_data_frame.winfo_children():
                    widget.destroy()
                columns = ctrl.get_columns(database, table)
                data_entries = []
                for column in columns:
                    data_label = customtkinter.CTkLabel(add_data_frame, text=f"Введите данные для столбца {column}:")
                    data_label.pack()
                    data_entry = customtkinter.CTkEntry(add_data_frame)
                    data_entries.append(data_entry)
                    data_entry.pack(pady=5)
                add_button = customtkinter.CTkButton(add_data_frame, text='добавить',
                                                     command=lambda: ctrl.add_data_to_table(database, table,
                                                                                            data_entries, info_label))
                add_button.pack()
                info_label = customtkinter.CTkLabel(add_data_frame, text='')
                info_label.pack()

            table_option = customtkinter.CTkOptionMenu(table_choose_frame, values=list_tables, command=lambda table: update_data_entries(table))
            table_option.pack(pady=10, padx=10)

            table = table_option.get()
            columns = ctrl.get_columns(database, table)
            data_entries = []
            for column in columns:
                data_label = customtkinter.CTkLabel(add_data_frame, text=f"Введите данные для столбца {column}:")
                data_label.pack()
                data_entry = customtkinter.CTkEntry(add_data_frame)
                data_entries.append(data_entry)
                data_entry.pack(pady=5)
            add_button = customtkinter.CTkButton(add_data_frame, text='добавить', command=lambda: ctrl.add_data_to_table(database, table, data_entries, info_label))
            add_button.pack()
            info_label = customtkinter.CTkLabel(add_data_frame, text='')
            info_label.pack()

    def delete_row(self, database):
        delete_row_window = customtkinter.CTkToplevel(self.interaction_database_window)
        delete_row_window.title(f'{database}')
        delete_row_window.wm_attributes("-topmost", True)
        delete_row_window.after(250, lambda: delete_row_window.iconbitmap(self.iconpath))
        app_width = 800
        app_height = 500
        x, y = self.coord_to_center(app_width, app_height)
        delete_row_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        ctrl = controller.Controller(self, self._model)
        list_tables = ctrl.get_list_tables(database)

        if (len(list_tables) == 0):
            error_message(delete_row_window, 'Доступных для удаления данных таблиц нет.')
        else:
            table_choose_frame = customtkinter.CTkFrame(delete_row_window)
            table_choose_frame.pack(side='left', fill='y')

            table_label = customtkinter.CTkLabel(table_choose_frame, text="Выберите таблицу:")
            table_label.pack()

            def update_table(table):
                df = pd.DataFrame(self._model.get_table(database, table))
                pt.model.df = df
                pt.redraw()

            tables_option_default = customtkinter.StringVar(value=list_tables[0])
            tables_option = customtkinter.CTkOptionMenu(table_choose_frame, values=list_tables,
                                                             variable=tables_option_default,
                                                             command=lambda table: update_table(table))
            tables_option.pack(side='top', anchor='center')

            table_frame = customtkinter.CTkFrame(delete_row_window)
            table_frame.pack(side='right', fill='both', expand=True)

            df = pd.DataFrame(self._model.get_table(database, tables_option.get()))
            pt = Table(table_frame, dataframe=df)
            pt.show()

            delete_label = customtkinter.CTkLabel(table_choose_frame, text="Выберите строку, которую хотите удалить")
            delete_label.pack()
            delete_button = customtkinter.CTkButton(table_choose_frame, text='удалить строку', fg_color='#FF3636', hover_color='#BA0000')
            delete_button.pack()

            info_label = customtkinter.CTkLabel(table_choose_frame, text='')
            info_label.pack()

            def handle_click_delete(event):
                rowclicked = pt.get_row_clicked(event)
                pt.setSelectedRow(rowclicked)
                colclicked = pt.get_col_clicked(event)
                pt.setSelectedCol(colclicked)
                info_label.configure(text='')
                delete_button.configure(text=f'удалить {rowclicked + 1} строку', command=lambda: ctrl.delete_row(database, tables_option.get(), pt.model.getValueAt(rowclicked, 0), info_label))
                pt.redraw()

            pt.bind("<ButtonRelease-1>", handle_click_delete)

    def clear_table(self, database):
        ctrl = controller.Controller(self, self._model)
        list_tb = ctrl.get_list_tables(database)

        clear_table_window = customtkinter.CTkToplevel(self.interaction_database_window)
        clear_table_window.title(f'{database}')
        clear_table_window.wm_attributes("-topmost", True)
        clear_table_window.after(250, lambda: clear_table_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 150
        x, y = self.coord_to_center(app_width, app_height)
        clear_table_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        info_for_user = customtkinter.CTkLabel(master=clear_table_window, text='Выберите таблицу, которую хотите очистить:', font=customtkinter.CTkFont(family="Helvetica", size=14))
        info_for_user.pack(side='top', pady=5, padx=20, expand=False)
        tb_list_option = customtkinter.CTkOptionMenu(clear_table_window, values=list_tb)
        tb_list_option.pack(pady=5, padx=5)
        table = tb_list_option.get()

        confirm = customtkinter.CTkButton(clear_table_window, text='очистить', fg_color='#FF3636', hover_color='#BA0000', command=lambda: ctrl.clear_table(database, table, clear_table_window))
        confirm.pack(pady=5, padx=5)

    def change_data(self, database):
        change_data_window = customtkinter.CTkToplevel(self.interaction_database_window)
        change_data_window.title(f'{database}')
        change_data_window.wm_attributes("-topmost", True)
        change_data_window.after(250, lambda: change_data_window.iconbitmap(self.iconpath))
        app_width = 800
        app_height = 500
        x, y = self.coord_to_center(app_width, app_height)
        change_data_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        ctrl = controller.Controller(self, self._model)
        list_tables = ctrl.get_list_tables(database)

        table_choose_frame = customtkinter.CTkFrame(change_data_window)
        table_choose_frame.pack(side='left', fill='y')

        table_label = customtkinter.CTkLabel(table_choose_frame, text="Выберите таблицу:")
        table_label.pack()

        def update_table(table):
            df = pd.DataFrame(self._model.get_table(database, table))
            pt.model.df = df
            pt.redraw()

        tables_option_default = customtkinter.StringVar(value=list_tables[0])
        tables_option = customtkinter.CTkOptionMenu(table_choose_frame, values=list_tables,
                                                    variable=tables_option_default,
                                                    command=lambda table: update_table(table))
        tables_option.pack(side='top', anchor='center', pady=15)

        table_frame = customtkinter.CTkFrame(change_data_window)
        table_frame.pack(side='right', fill='both', expand=True)

        df = pd.DataFrame(self._model.get_table(database, tables_option.get()))
        pt = Table(table_frame, dataframe=df)
        pt.show()

        form_frame = customtkinter.CTkFrame(table_choose_frame)
        form_frame.pack(fill='both')

        change_label = customtkinter.CTkLabel(table_choose_frame, text="Выберите ячейку, которую хотите изменить")
        change_label.pack(pady=10, padx=10)

        info_label = customtkinter.CTkLabel(table_choose_frame, text='')
        info_label.pack()

        def handle_click_change(event):
            for widget in form_frame.winfo_children():
                widget.destroy()
            input_label = customtkinter.CTkLabel(form_frame, text='Введите новое значение для ячейки:')
            input_label.pack()
            data_entry = customtkinter.CTkEntry(form_frame)
            data_entry.pack()
            save_button = customtkinter.CTkButton(form_frame, text='сохранить новое значение')
            save_button.pack(pady=15)
            rowclicked = pt.get_row_clicked(event)
            pt.setSelectedRow(rowclicked)
            colclicked = pt.get_col_clicked(event)
            pt.setSelectedCol(colclicked)
            info_label.configure(text='')
            save_button.configure(command=lambda: ctrl.change_row(database, tables_option.get(),
                                                                    pt.model.getValueAt(rowclicked, 0), colclicked,  data_entry.get(), pt, info_label, form_frame, rowclicked))
            pt.redraw()

        pt.bind("<ButtonRelease-1>", handle_click_change)

    def view_students_to_city(self, database):
        def view_students(city, info_label):
            df = pd.DataFrame(ctrl.find_students_to_city(database, city, info_label))
            pt.model.df = df
            pt.redraw()
        view_students_to_city_window = customtkinter.CTkToplevel(self.interaction_database_window)
        view_students_to_city_window.title(f'{database}')
        view_students_to_city_window.wm_attributes("-topmost", True)
        view_students_to_city_window.after(250, lambda: view_students_to_city_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 400
        x, y = self.coord_to_center(app_width, app_height)
        view_students_to_city_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        left_frame = customtkinter.CTkFrame(view_students_to_city_window)
        left_frame.pack(side='left', fill='y')

        find_label = customtkinter.CTkLabel(left_frame, text='Введите город, по которому\n хотите найти студентов:')
        find_label.pack(pady=10, padx=50)

        city_entry = customtkinter.CTkEntry(left_frame)
        city_entry.pack(pady=10)

        find_button = customtkinter.CTkButton(left_frame,text='показать студентов', command=lambda: view_students(city_entry.get(), info_label))
        find_button.pack(pady=10)

        ctrl = controller.Controller(self, self._model)

        delete_label = customtkinter.CTkLabel(left_frame, text='Введите город, по которому\n хотите удалить студентов:')
        delete_label.pack(pady=10, padx=50)

        city_entry2 = customtkinter.CTkEntry(left_frame)
        city_entry2.pack(pady=10)

        delete_button = customtkinter.CTkButton(left_frame, text='удалить студентов', fg_color='#FF3636', hover_color='#BA0000',
                                              command=lambda: ctrl.delete_students_to_city(database, city_entry2.get(), info_label))
        delete_button.pack(pady=10)

        info_label = customtkinter.CTkLabel(left_frame, text='')
        info_label.pack(pady=10, padx=10)

        table_frame = customtkinter.CTkFrame(view_students_to_city_window)
        table_frame.pack(side='right', expand=True, fill='both')

        pt = Table(table_frame)
        pt.show()

