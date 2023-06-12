import pandas as pd
import numpy as np
import pickle
from statsmodels.tsa.arima.model import ARIMA

def train_model(df):
    # Fit ARIMA model
    arima_model = ARIMA(df['Net Cashflow from Operations'], order=(30,1,30))  # change order according to your data
    arima_model_fit = arima_model.fit()

    # Save the model for future use
    with open('model.pkl', 'wb') as f:
        pickle.dump(arima_model_fit, f)
        
    return arima_model_fit

def load_model():
    # Load the model if it exists
    try:
        with open('model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def predict(df, train_new_model):
    if train_new_model:
        model = train_model(df)
    else:
        model = load_model()
        if model is None:
            print('No existing model found. Training a new one...')
            model = train_model(df)

    # Forecast the next 70 periods using ARIMA for the mean
    num_forecast_steps = 70
    arima_forecasts = model.get_forecast(steps=num_forecast_steps).predicted_mean

    # Generate dates for forecasts
    last_date = df.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=num_forecast_steps+1, freq='D')[1:]  # assuming daily frequency
    arima_forecasts.index = forecast_dates

    return arima_forecasts
