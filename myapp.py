import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io

st.write("""
# График котировок Apple за выбранное время
         
""")

# Загрузка данных о котировках Apple
apple = yf.Ticker("AAPL")

# Выбор периода времени в боковой панели
period = st.sidebar.selectbox(
    "Выберите период времени",
    ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"),
    key="period"
)

# Получение истории котировок за последний год
history = apple.history(period=period)

# Отображение графика котировок
st.line_chart(history)

# Отображение информации о компании
st.write(f"Название компании: {apple.info['longName']}")
st.write(f"Сектор: {apple.info['sector']}")
st.write(f"Индустрия: {apple.info['industry']}")

# Отображение текущей цены акции
st.write(f"Текущая цена акции: {history['Close'].iloc[-1]}")

# Добавление виджетов в боковую панель
with st.sidebar:
    # Текстовое поле ввода
    user_name = st.text_input('Введите ваше имя: ')
    st.write(f"Привет, {user_name}!")

    # Кнопка
    if st.button('Нажмите меня'):
        st.write('Вы нажали кнопку!')

    # Радио-кнопки
    shipping_method = st.radio(
        "Выберите способ доставки",
        ("Стандарт (5-15 дней)", "Экспресс (2-5 дней)")
    )
    st.write(f"Выбран способ доставки: {shipping_method}")

    # Выпадающий список
    contact_method = st.selectbox(
        "Как вам бы хотелось связаться?",
        ("Email", "Домашний телефон", "Мобильный телефон")
    )
    st.write(f"Выбран способ связи: {contact_method}")

# Загрузка CSV файла
uploaded_file = st.file_uploader("Загрузите CSV файл", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    st.line_chart(df)


# Функция для скачивания графика
def download_graph():
    fig = plt.figure(figsize=(10, 6))
    plt.plot(history.index, history['Close'])
    plt.title('График котировок Apple')
    plt.xlabel('Дата')
    plt.ylabel('Цена закрытия')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Кнопка скачивания графика
if st.button("Скачать график котировок Apple"):
    graph_bytes = download_graph().read()
    b64 = base64.b64encode(graph_bytes).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="Apple_Closing_Prices.png">Скачать график</a>'
    st.markdown(href, unsafe_allow_html=True)