import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

def set_working_directory(path):
    os.chdir(path)
    print(f"Changed working directory to: {os.getcwd()}")

def load_data(file_path):
    df = pd.read_csv("Nat_Gas (2).csv", parse_dates=['Dates'])
    return df['Dates'].values, df['Prices'].values

def generate_months(start_date, end_date):
    months = []
    current_date = start_date
    while current_date <= end_date:
        months.append(current_date)
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)
    return months

def simple_regression(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean
    return slope, intercept

def bilinear_regression(y, sin_t, cos_t):
    slope1 = np.sum(y * sin_t) / np.sum(sin_t ** 2)
    slope2 = np.sum(y * cos_t) / np.sum(cos_t ** 2)
    return slope1, slope2

def interpolate(date, start_date, days_from_start, prices, amplitude, shift, slope, intercept):
    days = (date - pd.Timestamp(start_date)).days
    if days in days_from_start:
        return prices[days_from_start.index(days)]
    else:
        return amplitude * np.sin(days * 2 * np.pi / 365 + shift) + days * slope + intercept

def analyze_gas_prices(file_path, start_date, end_date):
    dates, prices = load_data(file_path)
  
    months = generate_months(start_date, end_date)
    days_from_start = [(month - start_date).days for month in months]
   
    time = np.array(days_from_start)
    slope, intercept = simple_regression(time, prices)
    
    detrended_prices = prices - (time * slope + intercept)

    sin_time = np.sin(time * 2 * np.pi / 365)
    cos_time = np.cos(time * 2 * np.pi / 365)

    slope1, slope2 = bilinear_regression(detrended_prices, sin_time, cos_time)
    
    amplitude = np.sqrt(slope1 ** 2 + slope2 ** 2)
    shift = np.arctan2(slope2, slope1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, 'o', label='Natural Gas Prices')
    plt.plot(dates, time * slope + intercept, label='Linear Trend')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Natural Gas Prices with Linear Trend')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(time, detrended_prices, 'o', label='Detrended Prices')
    plt.plot(time, amplitude * np.sin(time * 2 * np.pi / 365 + shift), label='Seasonal Model')
    plt.xlabel('Days from Start Date')
    plt.ylabel('Price (After Removing Trend)')
    plt.title('Seasonal Variation in Gas Prices')
    plt.legend()
    plt.show()
    
    continuous_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    smoothed_estimates = [interpolate(date, pd.Timestamp(start_date), days_from_start, prices, amplitude, shift, slope, intercept) for date in continuous_dates]
    
    plt.figure(figsize=(10, 6))
    plt.plot(continuous_dates, smoothed_estimates, label='Smoothed Estimate')
    plt.plot(dates, prices, 'o', label='Original Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Natural Gas Prices (Smoothed Estimate)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

start_date = date(2020, 10, 31)
end_date = date(2024, 9, 30)
analyze_gas_prices('NatGas (2).csv', start_date, end_date)