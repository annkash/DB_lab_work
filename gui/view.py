import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://superuser@localhost:5432/driving_school')
con = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
# session.close()

class View(customtkinter.CTk):
    width = 800
    height = 600

    def add_data_to_table(self, chosen_table):
        window_1 = tk.Toplevel(self)
        window_1.title("Добавление новых данных")
        window_1.geometry("600x600")
        window_1.iconbitmap('gui/icon.ico')

        result = con.execute(text(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{chosen_table}'"))
        columns = [row[0] for row in result]
        data_entry_list = []
        for column in columns:
            data_label = tk.Label(window_1, text=f"Введите данные для столбца {column}:")
            data_label.pack()
            data_entry = tk.Entry(window_1)
            data_entry_list.append(data_entry.get())
            data_entry.pack()
        add_button = tk.Button(window_1, text="Добавить")
        add_button.pack()

    def add_data_window(self):
        window = tk.Toplevel(self)
        window.title("Добавление новых данных")
        window.geometry("600x600")
        window.iconbitmap('gui/icon.ico')

        table_label = tk.Label(window, text="Выберите таблицу:")
        table_label.pack()

        table_options = ["students", "instructors", "cars", "exams", "study_cost"]
        chosen_table = tk.StringVar()
        table_combobox = ttk.Combobox(window, textvariable=chosen_table, values=table_options, state="readonly")
        table_combobox.pack()

        submit_button = tk.Button(window, text="Выбрать",
                               command=lambda: self.add_data_to_table(chosen_table.get()))
        submit_button.pack()

    def __init__(self):
        super().__init__()
        self.title("Управление базой данных автошколы")

        self.geometry("800x600")

        customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.iconbitmap('gui/icon.ico')

        logo_frame = customtkinter.CTkFrame(self, width=400, height=400, corner_radius=0)
        logo_frame.pack(side='left', expand=True, fill='both')

        bg_image = customtkinter.CTkImage(light_image=Image.open("gui/bg_image.png"), size=(400, 300))
        bg_image_label = customtkinter.CTkLabel(master=logo_frame, image=bg_image, text='')
        bg_image_label.place(relx=0.5, rely=0.5, anchor='center')

        menu_frame = customtkinter.CTkFrame(self, width=400, height=400, corner_radius=0)
        menu_frame.pack(side='right', expand=True, fill='both')

        menu_options_frame = customtkinter.CTkFrame(menu_frame, width=400, height=400,  corner_radius=10)
        menu_options_frame.place(relx=0.5, rely=0.5, anchor='center')

        my_font = customtkinter.CTkFont(family="Helvetica", size=16, weight="bold")
        operations_label = customtkinter.CTkLabel(master=menu_options_frame, text='Операции с базой данных', font=my_font)
        operations_label.pack(pady=5, padx=20)

        create_database_button = customtkinter.CTkButton(menu_options_frame, text="Создать базу данных")
        create_database_button.pack(pady=5, padx=5)

        delete_database_button = customtkinter.CTkButton(menu_options_frame, text="Удалить базу данных")
        delete_database_button.pack(pady=5, padx=5)

        data_management_label = customtkinter.CTkLabel(menu_options_frame, text="Управление данными", font=my_font)
        data_management_label.pack(pady=5, padx=20)

        display_table_content_button = customtkinter.CTkButton(menu_options_frame, text="Показать содержимое таблицы")
        display_table_content_button.pack(padx=5)

        add_new_data_button = customtkinter.CTkButton(menu_options_frame, text="Добавить новые данные",
                                                      command=self.add_data_window)
        add_new_data_button.pack(pady=10, padx=5)