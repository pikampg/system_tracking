import csv
import tkinter as tk
from tkinter import messagebox
import datetime
import os
import pandas as pd
import sqlite3 as sl


filename = 'test_status.csv' # Название файла, откуда берутся данные

font = ('Times New Roman', 25) # стиль и размер шрифта
operators = 'operations.csv' # фамилии операторов и вид их работ. Заголовок столбца = вид работ
df = pd.read_csv(operators, delimiter=';', encoding='cp1251')
con = sl.connect('my-test.db') # название бд и подключение к ней


def write_file(value):
    num_order = entry_order.get() # из поля ввода сохраняется в переменную номер заказа
    surname = surname_str.get() # из выпадающего списка сохраняется в переменную фамилия исполнителя
    today = datetime.date.today().strftime('%d.%m.%Y') # сегодняшняя дату
    current_time = datetime.datetime.now().time().strftime('%H:%M:%S') # время записи в таблицу
    work_status = work_complete.get()
    my_list = [today, current_time, num_order, value, surname, work_status] # список данных, которые записываются в таблицу

    if num_order == '' or ' ' in num_order or surname == 'Фамилия оператора' or work_status == 'В работе/Завершено': # проверка на заполнение полей
        messagebox.showerror('Ошибка', 'Поля обязательны к заполнению')
    else:

        # если файл записи отсутствует, то он создается и в него записывается "шапка" таблицы
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(['Дата', 'Время', 'Номер заказа', 'Вид работы', 'Оператор', 'Статус']) # шапка таблицы
                # ошибка показывается только если нет файла для записи. Если попробовать еще раз, вся информация уcпешно запишется
                messagebox.showerror('ОШИБКА', 'Информация не записана\nНажмите ОК еще раз')

        else:

            with open(filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerow(my_list) # запсь данных из списка
                messagebox.showinfo('OK', 'Информация записана')
        # запись информации в БД
        sql = 'INSERT INTO USER (date, time, number, operation, operator, status) values(?, ?, ?, ?, ?, ?)'
        data = [
            (today, current_time, num_order, value, surname, work_status)
        ]
        with con:
            con.executemany(sql, data)


root = tk.Tk()
root.geometry('500x500')

options = ['Очистка', 'ХимН', 'Покрытие', 'Отжиг', 'ОТК', 'Заказ закрыт'] # перечень операций


def on_column_select(*args):
    selected_column = selected_options.get()

    values = set(df[selected_column])
    non_nan = sorted([v for v in values if pd.notna(v)])

    surname_str.set('Фамилия оператора')
    values_menu['menu'].delete(0, 'end')
    for value in non_nan:
        values_menu['menu'].add_command(label=value, font=font, command=tk._setit(surname_str, value))


selected_options = tk.StringVar(root)
selected_options.set('Выберите операцию') # заголовок где идет выбор операций
option_menu = tk.OptionMenu(root, selected_options, *options, command=on_column_select)
option_menu.config(font=font)
option_menu.pack()

menu = option_menu.nametowidget(option_menu.menuname)
menu.config(font=font)

label_num_order = tk.Label(root, text='Введите номер\nсопроводительного листа', font=font)
label_num_order.pack()
entry_order = tk.Entry(root, font=font)
entry_order.pack()


surname_str = tk.StringVar()
surname_str.set('Фамилия оператора')
values_menu = tk.OptionMenu(root, surname_str, '')
values_menu.config(font=font)
values_menu.pack()

work_complete = tk.StringVar()
work_complete.set('В работе/Завершено')
work_complete_menu = tk.OptionMenu(root, work_complete, *['В работе', 'Завершено'])
work_complete_menu.config(font=font)
work_complete_menu.pack()

btn = tk.Button(root, text='   OK   ', command=lambda: write_file(selected_options.get()), font=font)
btn.pack()

root.mainloop()
