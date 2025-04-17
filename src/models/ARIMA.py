import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def arima(train, order=(2, 1, 2), n_forecast=20):
    
    model = ARIMA(train, order=order)
    fitted_model = model.fit()
    prediction = fitted_model.forecast(steps=n_forecast)

    start_date = train.index[-1]  
    prediction_index = pd.date_range(start=start_date, periods=n_forecast + 1, freq='D')[1:]
    prediction_timeseries = pd.Series(prediction, index=prediction_index)
    
    return prediction_timeseries