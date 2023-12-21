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

        create_database_button = customtkinter.CTkButton(menu_options_frame, text="Создать базу данных")
        create_database_button.pack(pady=5, padx=5)

        delete_database_button = customtkinter.CTkButton(menu_options_frame, text="Удалить базу данных...", command=self.delete_database_window)
        delete_database_button.pack(padx=5)

        move_to_database_button = customtkinter.CTkButton(menu_options_frame, text="Перейти к базе данных...", command=self.choice_database_window)
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

    def delete_database_window(self):
        ctrl = controller.Controller(self, self._model)
        list_db = ctrl.get_list_db()

        self.delete_database_window = customtkinter.CTkToplevel(self)
        self.delete_database_window.title('Удаление базы данных')
        self.delete_database_window.wm_attributes("-top", True)
        self.delete_database_window.after(250, lambda: self.delete_database_window.iconbitmap(self.iconpath))
        width = 400
        height = 150
        x, y = self.coord_to_center(width, height)
        self.delete_database_window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        if (len(list_db) == 0):
            error_message(self.delete_database_window, 'Доступных для удаления баз данных нет.')
        else:
            info_for_user = customtkinter.CTkLabel(master=self.delete_database_window, text='Выберите базу данных, которую хотите удалить:', font=customtkinter.CTkFont(family="Helvetica", size=14))
            info_for_user.pack(side='top', pady=5, padx=20, expand=False)
            db_list_option = customtkinter.CTkOptionMenu(self.delete_database_window, values=list_db)
            db_list_option.pack(pady=5, padx=5)
            database = db_list_option.get()

            confirm = customtkinter.CTkButton(self.delete_database_window, text='удалить', fg_color='#FF3636', hover_color='#BA0000', command=lambda: ctrl.delete_database_window_event(database))
            confirm.pack(pady=5, padx=5)

    def choice_database_window(self):
        ctrl = controller.Controller(self, self._model)
        list_db = ctrl.get_list_db()

        self.choice_database_window = customtkinter.CTkToplevel(self)
        self.choice_database_window.title('Выбор базы данных')
        self.choice_database_window.wm_attributes("-top", True)
        self.choice_database_window.after(250, lambda: self.choice_database_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 150
        x, y = self.coord_to_center(app_width, app_height)
        self.choice_database_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        if (len(list_db) == 0):
            error_message(self.choice_database_window, 'Доступных для просмотра баз данных нет.')
        else:
            info_for_user = customtkinter.CTkLabel(master=self.choice_database_window,
                                                   text='Выберите базу данных для просмотра:',
                                                   font=customtkinter.CTkFont(family="Helvetica", size=14))
            info_for_user.pack(side='top', pady=5, padx=20, expand=False)

            db_list_option = customtkinter.CTkOptionMenu(self.choice_database_window, values=list_db)
            db_list_option.pack(pady=5, padx=5)
            database = db_list_option.get()

            confirm = customtkinter.CTkButton(self.choice_database_window, text='посмотреть', command=lambda: self.interaction_database_window(database))
            confirm.pack(pady=5, padx=5)

    def interaction_database_window(self, database):
        self.choice_database_window.destroy()
        self.choice_database_window.update()

        self.interaction_database_window = customtkinter.CTkToplevel(self)
        self.interaction_database_window.title(f'{database}')
        self.interaction_database_window.wm_attributes("-top", True)
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

            add_data_button = customtkinter.CTkButton(menu_frame, text='добавить данные', command=lambda: self.add_data_window(database))
            add_data_button.pack(padx=5)

            delete_data_button = customtkinter.CTkButton(menu_frame, text='удалить данные')
            delete_data_button.pack(pady=5, padx=5)

            delete_table_button = customtkinter.CTkButton(menu_frame, text='удалить таблицу')
            delete_table_button.pack(padx=5)

            create_table_button = customtkinter.CTkButton(menu_frame, text='создать таблицу')
            create_table_button.pack(pady=10, padx=10)

    def view_tables(self, database):
        def update_table(table):
            df = pd.DataFrame(self._model.get_table(database, table))
            pt.model.df = df
            pt.redraw()
        view_tables_window = customtkinter.CTkToplevel(self.interaction_database_window)
        view_tables_window.title(f'{database}')
        view_tables_window.wm_attributes("-top", True)
        view_tables_window.after(250, lambda: view_tables_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 400
        x, y = self.coord_to_center(app_width, app_height)
        view_tables_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        list_tables = self._model.get_list_tables(database)

        if (len(list_tables) == 0):
            error_message(view_tables_window, 'Доступных для просмотра таблиц нет.')
        else:
            tables_button_default = customtkinter.StringVar(value=list_tables[0])
            tables_button = customtkinter.CTkSegmentedButton(view_tables_window, values=list_tables,
                                                             variable=tables_button_default, command=lambda table: update_table(table))
            tables_button.pack(side='top', anchor='center')
            table_frame = customtkinter.CTkFrame(view_tables_window)
            table_frame.pack(side='bottom', expand=True, fill='both')

            df = pd.DataFrame(self._model.get_table(database, tables_button.get()))
            pt = Table(table_frame, dataframe=df)
            pt.show()

    def add_data_window(self, database):
        add_data_window = customtkinter.CTkToplevel(self.interaction_database_window)
        add_data_window.title(f'{database}')
        add_data_window.wm_attributes("-topmost", True)
        add_data_window.after(250, lambda: add_data_window.iconbitmap(self.iconpath))
        app_width = 400
        app_height = 400
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






'''
        data_management_label = customtkinter.CTkLabel(menu_options_frame, text="Управление данными", font=my_font)
        data_management_label.pack(pady=5, padx=20)

        display_table_content_button = customtkinter.CTkButton(menu_options_frame, text="Показать содержимое таблицы")
        display_table_content_button.pack(padx=5)

        add_new_data_button = customtkinter.CTkButton(menu_options_frame, text="Добавить новые данные")
        add_new_data_button.pack(pady=10, padx=5)

        #new_window = customtkinter.CTkToplevel(self)
        #new_window.title("новое окно")
        #new_window.geometry("100x100")
'''