import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

# Loading  the CSV file with company names and stock symbols  downloaded from yahoo finance
list_of_company = pd.read_csv('C:/Users/bsmaw/Desktop/STOCK PREDICTION/company list.csv')

 
# The  CSV has columns 'Company Name' and 'Stock Symbol'
# Extracting  the company names and symbols for the dropdown menu
name_of_company = list_of_company['Company Name'].tolist()
symbol_of_company = list_of_company['Stock Symbol'].tolist()

# Loading model that we have trained on stocks dataset downloaded from yfinance
model = tf.keras.models.load_model('C:/Users/bsmaw/Desktop/STOCK PREDICTION/Stock Predictions Model.keras')

st.header('Stock Market Predictor')

# User can search the stock by its symbol in search bar with a specific time range, default is the last 10 years
company_entered = st.selectbox('Select Company', name_of_company)  # Dropdown for company name

# Find the corresponding stock symbol based on the selected company
symbol_of_stock = symbol_of_company[name_of_company.index(company_entered)]

# User can define the start and end date for the stock data
start = st.date_input('Start Date', pd.to_datetime('2014-01-01'))
end = st.date_input('End Date', pd.to_datetime('today'))

# Downloading the stock data from Yahoo Finance for the user-selected stock and date range
data = yf.download(symbol_of_stock, start=start, end=end)

st.subheader('Stock Data')
st.write(data)

# Split the data into training and test sets
model_training = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
model_testing = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

# Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaler.fit(model_training)  # Fit scaler on training data only

data_train_scaled = scaler.transform(model_training)
data_test_scaled = scaler.transform(model_testing)

# Prepare test data with the past 100 days of the stock price from the data downloaded from Yahoo Finance 
past_100_days = model_training.tail(100)
data_test_scaled = np.concatenate([scaler.transform(past_100_days), data_test_scaled], axis=0)

# Create sequences
x, y = [], []
for i in range(100, data_test_scaled.shape[0]):
    x.append(data_test_scaled[i-100:i])
    y.append(data_test_scaled[i, 0])

x, y = np.array(x), np.array(y)

# Reshape x for model
x = x.reshape(x.shape[0], x.shape[1], 1)

# Make predictions
predict = model.predict(x)

# Rescale predictions
predict = scaler.inverse_transform(predict)
y = scaler.inverse_transform(y.reshape(-1, 1))



# Plotting Results
st.subheader('Price vs MA50')
ma_50_days = data.Close.rolling(50).mean()
fig1 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r-', linewidth=2, label='MA50 (50-day Moving Average)')  # Red solid line
plt.plot(data.Close, 'g-', linewidth=1.3, label='Close Price')  # Green solid line
plt.xlabel('Time(Years)')
plt.ylabel('Closing Price')
plt.legend()  # Adding  legend to code show what each coloured line represents in the plotted graph
st.pyplot(fig1)

st.subheader('Price vs MA50 vs MA100')
ma_100_days = data.Close.rolling(100).mean()
fig2 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r-', linewidth=2, label='MA50 (50-day Moving Average)')  # Red solid line
plt.plot(ma_100_days, 'b-', linewidth=2, label='MA100 (100-day Moving Average)')  # Blue solid line
plt.plot(data.Close, 'g-', linewidth=1.3, label='Close Price')  # Green solid line
plt.legend()
plt.xlabel('Time(Years)')
plt.ylabel('Closing Price')
st.pyplot(fig2)

st.subheader('Price vs MA100 vs MA200')
ma_200_days = data.Close.rolling(200).mean()
fig3 = plt.figure(figsize=(8,6))
plt.plot(ma_100_days, 'b-', linewidth=2, label='MA100 (100-day Moving Average)')  # Blue solid line
plt.plot(ma_200_days, 'r-', linewidth=2, label='MA200 (200-day Moving Average)')  # Red solid line
plt.plot(data.Close, 'g-', linewidth=1.3, label='Close Price')  # Green solid line
plt.legend()
plt.xlabel('Time(Years)')
plt.ylabel('Closing Price')
st.pyplot(fig3)

st.subheader('Original Price vs Predicted Price')
fig4 = plt.figure(figsize=(8,6))
plt.plot(predict, 'r-', linewidth=2, label='Predicted Price')  # Red solid line
plt.plot(y, 'g-', linewidth=2, label='Original Price')  # Green solid line
plt.xlabel('Time(DAYS)')
plt.ylabel('Closing Price')
plt.legend()
st.pyplot(fig4)


# Calculate and display accuracy metrics
# MAPE (Mean Absolute Percentage Error) measures the average percentage difference between the predicted and actual stock prices
mape = mean_absolute_percentage_error(y, predict)
predict = predict * scaler.scale_ #converting into scaler values again to calculate mse for the model and doing same for y
y = y * scaler.scale_
mse = mean_squared_error(y, predict)

# Calculate accuracy of the model
accuracy = 100 - mape * 100  # Accuracy in percentage of model

st.subheader('Model Accuracy')
st.write(f'Mean Absolute Percentage Error (MAPE): {mape:.2f}')
st.write(f'Mean Squared Error (MSE): {mse:.2f}')
st.write(f'Prediction Accuracy: {accuracy:.2f}%')  # Display the accuracy as a percentage


# Download stock data
st.download_button('Download Stock Data', data.to_csv().encode(), file_name='stock_data.csv', mime='text/csv')
