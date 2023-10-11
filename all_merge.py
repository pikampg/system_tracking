import tkinter as tk
from tkinter import ttk
from tab1 import create_tab1
from tab2 import create_tab2
from tab3 import create_tab3


root = tk.Tk()
root.title('APP')
root.geometry('1200x570')

notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

create_tab1(tab1)
create_tab2(tab2)
create_tab3(tab3)

notebook.add(tab1, text='Поиск')
notebook.add(tab2, text='Номера сопроводительных')
notebook.add(tab3, text='Закрытые заказы')

notebook.pack(fill='both', expand=True)
root.mainloop()
