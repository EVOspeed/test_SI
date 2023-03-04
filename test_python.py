# Импорт необходимых библиотек
import requests
import pandas as pd
from datetime import datetime
import streamlit as st

def get_assets_list(url='https://api.coincap.io/v2/assets'):
    #получение всех возможных криптовалют, информацию о которых
    #предоставляет сервис по api и запись их в список

    response = requests.get(url)
    data = response.json()
    assets_list = []
    for i in data['data']:
        assets_list.append(i['id'])

    return assets_list

def get_df(select_assets):
    #формирование и преобразование датафрейма по необходимой валюте

    response = requests.get(f'https://api.coincap.io/v2/assets/{select_assets}/history?interval=d1')
    data = response.json()
    df = pd.DataFrame(data['data'])
    df.priceUsd = df.priceUsd.apply(lambda x: int(x.split('.')[0]) + float('0' + '.' + x.split('.')[1][0:2]))
    df.date = pd.to_datetime(df.date)
    df.drop(columns='time', inplace=True)

    return df

assets_list = get_assets_list()

# объявление структуры окна (заголовок, сайдбар и прочие элименты)
st.sidebar.title('Параметры')
st.sidebar.info('''Выберите интересующую криптовалюту, а я Вам покажу динамику изменения курса на графике''')
select_assets = st.sidebar.selectbox('Select asset', assets_list)
st.title(f'Динамика изменения курса {select_assets}.')

df = get_df(select_assets)

# Реализация сортировки по датам
show_timerange = st.sidebar.checkbox("Отсортировать по дате")
min_date = st.sidebar.date_input('Сортировать по дате - С')
max_date = st.sidebar.date_input('По')
if show_timerange == True:
    df = df[(df.date >= datetime.strftime(min_date, '%Y-%m-%d')) & (df.date <= datetime.strftime(max_date, '%Y-%m-%d'))]

#Вывод графика и датафрейма
st.line_chart(data=df.sort_values(by='date'), x='date', y='priceUsd')
st.dataframe(df)

# Чтобы воспользоваться скриптом необходимо в терминале ввести команду 'streamlit run test_python.py'