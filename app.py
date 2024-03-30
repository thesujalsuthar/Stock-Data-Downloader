import pandas as pd
import streamlit as st
import yfinance as yf
import datetime
import plotly.graph_objs as go
from io import BytesIO

st.title('Stock Data Downloader')

stock = st.text_input('Name of Stock (Enter Ticker)','SBIN')

def set_default_start(stock_history):
    if not stock_history.empty:
        stock_start_date = stock_history.index[0].date()
        start_date = st.date_input(f'Start Date (Default: {stock_start_date})', value=stock_start_date)
    
        return start_date    

stock_info = yf.Ticker(stock)
stock_history = stock_info.history(period="max")
    
default_start = set_default_start(stock_history)

end_date = st.date_input('Enter End Date (Default: Today)',value=datetime.date.today())

stock_data = yf.download(stock, start=default_start, end=end_date)

# Displaying data
if not stock_data.empty:
    df = stock_data.reset_index()
    df['Date'] = df['Date'].dt.date
    df.set_index('Date', inplace=True)

    st.subheader('Stock Data')
    st.write(df)

    # Displaying line chart of stock closing prices
    st.subheader('Closing Prices')
    st.line_chart(stock_data['Close'])

    #Disply Candlestick Chart
    st.subheader('Candlestick Chart')
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error('Data not found. Please specify the exchange if the stock is Indian')
    exchange = st.selectbox('Select Exchange (Default: NSE)', ['NSE', 'BSE'])
    if exchange == 'NSE':
        stock = f"{stock}.NS"
    elif exchange == 'BSE':
        stock = f"{stock}.BO"

    stock_info = yf.Ticker(stock)
    stock_history = stock_info.history(period="max")    
        
    default_start = set_default_start(stock_history)

    stock_data = yf.download(stock, start=default_start, end=end_date)
    if not stock_data.empty:

        df = stock_data.reset_index()
        df['Date'] = df['Date'].dt.date
        df.set_index('Date', inplace=True)

        st.subheader('Stock Data')
        st.write(df)

        # Displaying line chart of stock closing prices
        st.subheader('Closing Prices')
        st.line_chart(stock_data['Close'])

        #Displaying Candlestick chart
        st.subheader('Candlestick Chart')
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write(f"No data found for stock symbol {stock}")

csv_bytes = df.to_csv().encode('utf-8')

csv_buffer = BytesIO(csv_bytes)
st.download_button(label='Download Data', data=csv_buffer, file_name=f'{stock}_data.csv', mime='text/csv')

st.markdown('<center>Made with ❤️ by Sujal Suthar</center>', unsafe_allow_html=True)