import tkinter as tk
from tkinter import ttk, messagebox
from data import font, df, filename_otk, name_column


del name_column[1]  # удаляем ненужный стобец


def create_tab1(parent):
    def number_order_info():
        selected_column = column_var.get()
        value = entry_number.get()  # из поля ввода сохраняется в переменную
        filtered_df = df[df[selected_column] == str(value)]  # вывод информации

        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_df.iterrows():
            tree.insert('', 'end', values=row.tolist())

    lbl_column = tk.Label(parent, text='Выбери столбец для фильтрации', font=font)  # заголовок
    lbl_column.pack()

    column_var = tk.StringVar(parent)  # создание выпадающего списка
    column_var.set('Выбери операцию')  # заголовок выпадающего списка
    column_menu = tk.OptionMenu(parent, column_var,
                                *name_column)  # добавление в выпадающий список наименований столбцов
    column_menu.config(font=font)
    column_menu.pack()

    menu = column_menu.nametowidget(column_menu.menuname)
    menu.config(font=font)

    label_number = tk.Label(parent, text='Значение', font=font)
    label_number.pack()

    entry_number = tk.Entry(parent, font=font)
    entry_number.pack()

    filter_button = tk.Button(parent, text='Поиск', command=number_order_info, font=font)
    filter_button.pack()

    tree = ttk.Treeview(parent, columns=df.columns, show='headings')  # создание дерева
    tree.heading('#1', text='Дата')  # заголовки столбцов в таблице в дереве
    tree.heading('#2', text='Время')
    tree.heading('#3', text='Номер СЛ')
    tree.heading('#4', text='Операция')
    tree.heading('#5', text='Оператор')
    tree.heading('#6', text='Статус')

    style = ttk.Style()
    style.configure('Treeview.Heading', font=font)

    tree.pack()

    def on_otk():
        otk = df[df['Вид работы'] == 'ОТК']  # все заказы, которые были/есть на отк
        close_num = df.loc[df['Вид работы'] == 'Заказ закрыт', ['Номер заказа']]  # номера заказов, которые закрыты
        new_df = otk.merge(close_num, on='Номер заказа', how='left',
                           indicator=True)  # слияние таблицы с заказами на ОТК с номерами закрытых заказов
        filtered_df = new_df[new_df['_merge'] == 'left_only']
        filtered_df = filtered_df.drop('_merge', axis=1)  # удаление лишних столбов
        filtered_df = filtered_df.reset_index(drop=True)

        for item in tree.get_children():
            tree.delete(item)

        for index, row in filtered_df.iterrows():
            tree.insert('', 'end', values=row.tolist())

        filtered_df.to_csv(filename_otk, index=False, sep=';', encoding='cp1251')  # запись заказов на ОТК в файл
        messagebox.showinfo(f'На ОТК {len(filtered_df)} заказов', f'Данные записаны в {filename_otk}')

    otk_btn = tk.Button(parent, text='Заказы на ОТК', command=on_otk, font=font, width=20, height=2)
    otk_btn.pack()
