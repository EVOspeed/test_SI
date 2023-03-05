# Импорт необходимых библиотек
import requests
import pandas as pd
from datetime import datetime, timedelta
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
    df['lag_price'] = df.priceUsd.shift(1)
    df['rate_of_increase_%'] = round((df.priceUsd / df.lag_price - 1) * 100, 3)

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
min_date = st.sidebar.date_input('С', min_value=df.date.min(),
                                 max_value=df.date.max(), value=df.date.min())
max_date = st.sidebar.date_input('По', min_value=df.date.min(), max_value=df.date.max(),
                                 value=df.date.max())
if show_timerange == True:
    df = df[(df.date >= datetime.strftime(min_date, '%Y-%m-%d')) & (df.date <= datetime.strftime(max_date, '%Y-%m-%d'))]

#Вывод графика и датафрейма
st.line_chart(data=df.sort_values(by='date'), x='date', y='priceUsd')
increase = round((df.priceUsd[df.date == df.date.max()].values[0] /
                  df.priceUsd[df.date == df.date.min()].values[0]) * 100 - 100, 2)
change = df.priceUsd[df.date == df.date.max()].values[0] - df.priceUsd[df.date == df.date.min()].values[0]
if increase > 0:
    st.markdown(f'За анализируемый период курс криптовалюты вырос в абсолютном значении на \
                {round(change, 2)}USD, прирост составил {increase}%.')
else:
    st.markdown(f' За анализируемый период курс криптовалюты снизился в абсолютном значении на \
                {round(change, 2)}USD, падение составило {increase}%.')
st.markdown('Ежедневные показатели темпов прироста отражены на диаграмме.')
st.bar_chart(data=df.sort_values(by='date'), x='date', y='rate_of_increase_%')
df.date = df.date.apply(lambda x: datetime.strftime(x, '%d-%m-%Y'))
st.dataframe(df.drop(columns='lag_price'))

# Чтобы воспользоваться скриптом необходимо в терминале ввести команду 'streamlit run test_python.py'