import datetime
import pandas as pd

# filename = 'test.csv' # название файла
filename = 'test_status.csv' # название файла
df = pd.read_csv(filename, delimiter=';', encoding='cp1251') # датафрейм файла
font = ('Times New Roman', 14) # шрифт
filename_otk = datetime.date.today().strftime('%d.%m.%Y') + '_otk' + '.csv' # название файла с заказами на ОТК

day_list = [day for day in range(1, 32)]
month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
year_list = [year for year in range(2023, 2037)]

set_num = list(set(df['Номер заказа'])) # список уникальных номеров сопроводительных

# перевод str в float
for num in range(len(set_num)):
    set_num[num] = set_num[num].replace(',', '.')
set_num = [str(i) for i in sorted(set_num, key=lambda x: float(x))]

closet_num = list()

# добавление в список закрытых заказов
for num in set_num:
    if '.' in num:
        num = num.replace('.', ',')
        new_df = df[df['Номер заказа'] == num]

        if 'Заказ закрыт' in new_df['Вид работы'].values:
            closet_num.append(num)
            continue
    else:
        new_df = df[df['Номер заказа'] == num]
        if 'Заказ закрыт' in new_df['Вид работы'].values:
            closet_num.append(num)
            continue


new_df = df.loc[df['Номер заказа'].isin(closet_num)] # датафрейм с закрытыми заказами
name_column = df.columns.tolist()  # список заголовков столбцов
