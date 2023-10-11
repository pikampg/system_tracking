import tkinter as tk
from tkinter import ttk
from data import font, day_list, month_list, year_list, df


def create_tab3(parent):
    day_var = tk.StringVar(parent)  # создание выпадающего списка
    day_var.set('Выбери день')  # заголовок выпадающего списка
    day_menu = tk.OptionMenu(parent, day_var, *day_list)  # добавление в выпадающий список наименований столбцов
    day_menu.config(font=font)
    day_menu.pack()

    month_var = tk.StringVar(parent)  # создание выпадающего списка
    month_var.set('Выбери месяц')  # заголовок выпадающего списка
    month_menu = tk.OptionMenu(parent, month_var, *month_list)  # добавление в выпадающий список наименований столбцов
    month_menu.config(font=font)
    month_menu.pack()

    year_var = tk.StringVar(parent)  # создание выпадающего списка
    year_var.set('Выбери год')  # заголовок выпадающего списка
    year_menu = tk.OptionMenu(parent, year_var, *year_list)  # добавление в выпадающий список наименований столбцов
    year_menu.config(font=font)
    year_menu.pack()

    def need():
        need_day = day_var.get() # значение дня
        need_month = month_var.get() # значение месяца
        for month in range(1, len(month_list) + 1):
            if need_month == month_list[month - 1]:
                need_month = str(month) # перевод буквенного обозначения месяца в цифровое

        need_year = year_var.get() # значение года
        if len(need_day) == 1:
            need_day = '0' + need_day
        if len(need_month) == 1:
            need_month = '0' + need_month
        date = need_day + '.' + need_month + '.' + need_year # дата, по которой необходимо фильтровать

        # filtered_df = new_df.loc[new_df['Дата'].isin([date])]
        filtered_df = df.loc[
            (df['Вид работы'] == 'Заказ закрыт') & (df['Статус'] == 'Завершено') & (df['Дата'] == date)]

        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_df.iterrows():
            tree.insert('', 'end', values=row.tolist())

    btn = tk.Button(parent, text='   OK   ', command=need, font=font)
    btn.pack()

    tree = ttk.Treeview(parent, columns=df.columns, show='headings')
    tree.heading('#1', text='Дата')
    tree.heading('#2', text='Время')
    tree.heading('#3', text='Номер СЛ')
    tree.heading('#4', text='Операция')
    tree.heading('#5', text='Оператор')
    tree.heading('#6', text='Статус')
    tree.pack()
