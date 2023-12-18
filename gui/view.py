import tkinter as tk
import customtkinter
from PIL import Image

class View(customtkinter.CTk):
    width = 800
    height = 600
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

        add_new_data_button = customtkinter.CTkButton(menu_options_frame, text="Добавить новые данные")
        add_new_data_button.pack(pady=10, padx=5)