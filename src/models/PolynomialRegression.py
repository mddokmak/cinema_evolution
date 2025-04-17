import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def polynomial_regression(train, degree=2, n_forecast=20):
    x_train = np.arange(len(train)).reshape(-1, 1)
    y_train = train.values
    
    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(x_train)
    
    model = LinearRegression()
    model.fit(x_poly, y_train)
    
    x_future = np.arange(len(train), len(train) + n_forecast).reshape(-1, 1)
    x_future_poly = poly_features.transform(x_future)
    prediction = model.predict(x_future_poly)

    start_date = train.index[-1]  
    prediction_index = pd.date_range(start=start_date, periods=n_forecast + 1, freq='D')[1:]
    prediction_timeseries = pd.Series(prediction, index=prediction_index)
    
    return prediction_timeseries