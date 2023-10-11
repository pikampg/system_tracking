from tkinter import ttk
import pandas as pd
from data import df

closet_num = list()


def create_tab2(parent):
    set_num = list(set(df['Номер заказа']))
    for num in range(len(set_num)):
        set_num[num] = set_num[num].replace(',', '.')
    set_num = [str(i) for i in sorted(set_num, key=lambda x: float(x))]

    tree = ttk.Treeview(parent)  # создание дерева
    tree.pack(fill='both', expand=True)

    tree.column('#0', stretch=True)

    for num in set_num:

        if '.' in num:
            num = num.replace('.', ',')
            new_df = df[df['Номер заказа'] == num]

            if 'Заказ закрыт' in new_df['Вид работы'].values:
                closet_num.append(num)

                continue
            else:
                p = tree.insert('', 'end', text=num)
                for i in range(len(new_df)):
                    my_str = new_df.iloc[i]
                    df_n = pd.DataFrame([my_str])
                    df_n.pop('Номер заказа')
                    tree.insert(p, 'end', text=df_n.to_string(index=False, header=False))
        else:
            new_df = df[df['Номер заказа'] == num]

            if 'Заказ закрыт' in new_df['Вид работы'].values:
                closet_num.append(num)
                continue
            else:
                p = tree.insert('', 'end', text=num)
                for i in range(len(new_df)):
                    my_str = new_df.iloc[i]
                    df_n = pd.DataFrame([my_str])
                    df_n.pop('Номер заказа')
                    tree.insert(p, 'end', text=df_n.to_string(index=False, header=False))

    tree.insert('', 'end', text='Закрытые заказы')

    for num in closet_num:
        new_df = df[df['Номер заказа'] == num]
        p = tree.insert('', 'end', text=num)
        for i in range(len(new_df)):
            my_str = new_df.iloc[i]
            df_n = pd.DataFrame([my_str])
            df_n.pop('Номер заказа')
            tree.insert(p, 'end', text=df_n.to_string(index=False, header=False))
