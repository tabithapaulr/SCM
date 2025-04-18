
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import io

from flask import send_file

def production_planning_function_with_vis(df):

    
    # Load the dataset
    data = df # Replace "your_dataset.csv" with the actual filename
    
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

    # Perform linear regression for each product
    for product, group in grouped:
        X = group['Year_Month'].values.reshape(-1, 1)
        y = group['HISQTY'].values
        model = LinearRegression()
        model.fit(X, y)

        # Make predictions for 2024 and 2025
        predictions = model.predict([[2024 + (1 - 1) / 12.0], [2025 + (1 - 1) / 12.0]])

        # Store actual and predicted values
        results[product] = {
            'Actual 2021': group.loc[group['YEAR'] == 2021, 'HISQTY'].values[0],
            'Actual 2022': group.loc[group['YEAR'] == 2022, 'HISQTY'].values[0],
            'Actual 2023': group.loc[group['YEAR'] == 2023, 'HISQTY'].values[0],
            'Predicted 2024': predictions[0],
            'Predicted 2025': predictions[1]
        }

    # Convert results to DataFrame
    results_df = pd.DataFrame(results).T

    # Plot the results
    plt.figure(figsize=(12, 8))

    bar_width = 0.15
    for i, (product, values) in enumerate(results.items()):
        plt.bar(i - 2.5*bar_width, values['Actual 2021'], color='lightblue', label='Actual 2021', width=bar_width)
        plt.bar(i - 1.5*bar_width, values['Actual 2022'], color='lightgreen', label='Actual 2022', width=bar_width)
        plt.bar(i - 0.5*bar_width, values['Actual 2023'], color='lightcoral', label='Actual 2023', width=bar_width)
        plt.bar(i + 0.5*bar_width, values['Predicted 2024'], color='khaki', label='Predicted 2024', width=bar_width)
        plt.bar(i + 1.5*bar_width, values['Predicted 2025'], color='thistle', label='Predicted 2025', width=bar_width)

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
    
def production_planning_function(df):

    
    # Load the dataset
    data = df # Replace "your_dataset.csv" with the actual filename
    
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

    # Perform linear regression for each product
    for product, group in grouped:
        X = group['Year_Month'].values.reshape(-1, 1)
        y = group['HISQTY'].values
        model = LinearRegression()
        model.fit(X, y)

        # Make predictions for 2024 and 2025
        predictions = model.predict([[2024 + (1 - 1) / 12.0], [2025 + (1 - 1) / 12.0]])

        # Store actual and predicted values
        results[product] = {
            'Actual 2021': group.loc[group['YEAR'] == 2021, 'HISQTY'].values[0],
            'Actual 2022': group.loc[group['YEAR'] == 2022, 'HISQTY'].values[0],
            'Actual 2023': group.loc[group['YEAR'] == 2023, 'HISQTY'].values[0],
            'Predicted 2024': predictions[0],
            'Predicted 2025': predictions[1]
        }

    # Convert results to DataFrame
    results_df = pd.DataFrame(results).T
    return results_df

