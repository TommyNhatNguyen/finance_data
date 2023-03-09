import streamlit as st 
import pandas as pd
import numpy as np 
import plotly.express as px
import plotly.figure_factory as ff
from vnstock import * 
import datetime
from collections import Counter
import plotly.graph_objects as go

st.title('Stock Dashboard :chart_with_upwards_trend:')
ticker = st.sidebar.text_input('Ticker', value='DRC')
start_date = st.sidebar.date_input('Start Date', min_value=datetime.date(1996,11,28), value=datetime.date(2000,10,14)).strftime("%Y-%m-%d")
end_date = st.sidebar.date_input('End Date').strftime("%Y-%m-%d")

data = stock_historical_data(
    symbol=ticker, 
    start_date=start_date,
    end_date=end_date
).set_index('TradingDate')

# data['Close_t-1']= data['Close'].shift(1)
# data['Close_t-30']= data['Close'].shift(30)
# data['Close_t-90']= data['Close'].shift(90)
# data['Close_t-256']= data['Close'].shift(256)

# data['daily_return'] = data['Close']/data['Close_t-1'] - 1 
# data['monthly_return'] = data['Close']/data['Close_t-30'] - 1 
# data['quarterly_return'] = data['Close']/data['Close_t-90'] - 1 
# data['yearly_return'] = data['Close']/data['Close_t-256'] - 1 

data
st.download_button('Tải em đi', data.to_csv().encode('utf-8'), mime='text/csv', file_name='{}.csv'.format(ticker))

fig = px.line(data, x=data.index, y=data['Close'], title=ticker)
st.plotly_chart(fig)
# -----------------------------

st.title('Financial Report Dashboard :money_mouth_face:')

source, timeline = st.columns(2)

with source:
    source=st.radio(
        "Choose Financial Report Source",
        options=["SSI", "TCBS"],
    )

with timeline:
    timeline=st.radio(
        "Select financial report timeline",
        options=["Quarterly", "Yearly"],
    )

if source=='TCBS':
    data_income_statement = financial_flow(symbol=ticker, report_type='incomestatement', report_range=timeline.lower())
    data_balance_sheet = financial_flow(symbol=ticker, report_type='balancesheet', report_range=timeline.lower())
    data_cash_flow = financial_flow(symbol=ticker, report_type='cashflow', report_range=timeline.lower())
else:
    data_income_statement = financial_report(symbol=ticker, report_type='IncomeStatement', frequency=timeline)
    data_balance_sheet = financial_report(symbol=ticker, report_type='BalanceSheet', frequency=timeline)
    data_cash_flow = financial_report(symbol=ticker, report_type='CashFlow', frequency=timeline)

data_income_statement
st.download_button('Tải em đi:', data_income_statement.to_csv().encode('utf-8'), mime='text/csv', file_name='IncomeStatement_{}.csv'.format(ticker))

data_balance_sheet
st.download_button('Tải em đi:', data_balance_sheet.to_csv().encode('utf-8'), mime='text/csv', file_name='BalanceSheet_{}.csv'.format(ticker))

data_cash_flow
st.download_button('Tải em đi:', data_cash_flow.to_csv().encode('utf-8'), mime='text/csv', file_name='CashFlow_{}.csv'.format(ticker))

# fig3 = go.Figure(data=[go.Candlestick(x=data.index,
#                 open=data['Open'],
#                 high=data['High'],
#                 low=data['Low'],
#                 close=data['Close'])])
# st.plotly_chart(fig3)


# stock_return = st.select_slider(
#     'Select return timeline',
#     options=['daily_return', 'monthly_return', 'quarterly_return', 'yearly_return'])
# st.write('Return: ', stock_return)

# fig2 = px.histogram(data, x=stock_return)
# fig2.add_vline(x=data[stock_return].mean(), line_dash='dash', line_color='red', annotation_text='Mean', annotation_position="top", annotation={'font_color':'red'})

# fig2.add_vline(x=data[stock_return].median(), line_dash='dash', line_color='green', annotation_text='Median', annotation_position="top",annotation={'font_color':'green'})

# fig2.add_vrect(x0=data[stock_return].mean() + data[stock_return].std(), 
#                x1=data[stock_return].mean() - data[stock_return].std(), 
#                line_width=0, 
#                fillcolor="gray", 
#                opacity=0.5)

# st.plotly_chart(fig2)

