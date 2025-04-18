import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
import io

def model_comparison_function(df):
    # Load the dataset
    data = df  # Replace "your_dataset.csv" with the actual filename
    
    # Convert month names to numerical values
    month_to_num = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    data['MONTH'] = data['MONTH'].map(month_to_num)

    # Combine YEAR and MONTH columns to create a numerical representation of the date
    data['Year_Month'] = data['YEAR'] + (data['MONTH'] - 1) / 12.0

    # Drop rows with missing values
    data.dropna(subset=['Year_Month', 'HISQTY'], inplace=True)

    # Group data by PRODUCT
    grouped = data.groupby('PRODUCT')

    # Dictionary to store actual and predicted values for each product
    results = {}

    # Perform forecasting for each product
    for product, group in grouped:
        # Extract time series data
        time_series = group['HISQTY'].values
        
        # Simple Moving Average (SMA)
        sma_predictions = np.mean(time_series[-3:])
        
        # Simple Exponential Smoothing (SES)
        ses_model = SimpleExpSmoothing(time_series)
        ses_fit = ses_model.fit()
        ses_predictions = ses_fit.forecast(2)[-1]
        
        # ARIMA
        arima_model = ARIMA(time_series, order=(1, 1, 1))  # Example order, adjust as needed
        arima_fit = arima_model.fit()
        arima_predictions = arima_fit.forecast(steps=2)  # Get forecasted values for 2024 and 2025

        # Store actual and predicted values
        results[product] = {
            'Actual 2021': group.loc[group['YEAR'] == 2021, 'HISQTY'].values[0],
            'Actual 2022': group.loc[group['YEAR'] == 2022, 'HISQTY'].values[0],
            'Actual 2023': group.loc[group['YEAR'] == 2023, 'HISQTY'].values[0],
            'SMA Predicted 2024': sma_predictions,
            'SES Predicted 2024': ses_predictions,
            'ARIMA Predicted 2024': arima_predictions[0],  # Access the forecast for 2024
            'SMA Predicted 2025': sma_predictions,
            'SES Predicted 2025': ses_predictions,
            'ARIMA Predicted 2025': arima_predictions[1]   # Access the forecast for 2025
        }

    # Convert results to DataFrame
    results_df = pd.DataFrame(results).T
    
    # Plot the results
    plt.figure(figsize=(12, 8))
    bar_width = 0.2
    for i, (product, values) in enumerate(results.items()):
        plt.bar(i - 1.5*bar_width, values['Actual 2021'], color='lightblue', label='Actual 2021', width=bar_width)
        plt.bar(i - 0.5*bar_width, values['Actual 2022'], color='lightgreen', label='Actual 2022', width=bar_width)
        plt.bar(i + 0.5*bar_width, values['Actual 2023'], color='lightcoral', label='Actual 2023', width=bar_width)
        plt.bar(i + 1.5*bar_width, values['SMA Predicted 2024'], color='khaki', label='SMA Predicted 2024', width=bar_width)
        plt.bar(i + 2.5*bar_width, values['SES Predicted 2024'], color='thistle', label='SES Predicted 2024', width=bar_width)
        plt.bar(i + 3.5*bar_width, values['ARIMA Predicted 2024'], color='lightpink', label='ARIMA Predicted 2024', width=bar_width)
        plt.bar(i + 4.5*bar_width, values['SMA Predicted 2025'], color='lightyellow', label='SMA Predicted 2025', width=bar_width)
        plt.bar(i + 5.5*bar_width, values['SES Predicted 2025'], color='lightgray', label='SES Predicted 2025', width=bar_width)
        plt.bar(i + 6.5*bar_width, values['ARIMA Predicted 2025'], color='lightcyan', label='ARIMA Predicted 2025', width=bar_width)

    plt.xticks(np.arange(len(results)), list(results.keys()), rotation=45, ha='right')
    plt.ylabel('Quantity')
    plt.title('Actual and Predicted Quantity for Each Product')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.tight_layout()
    
    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()
