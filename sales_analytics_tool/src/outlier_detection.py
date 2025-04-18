import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

def outlier_detection_function(df):

    
    # Specify the column names for analysis
    column_name = 'HISQTY'
    group_by_column = 'PRODUCT'
    
    # Define the range for outliers
    lower_bound = 80
    upper_bound = 100

    # Detect outliers
    outliers = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]

    # Replace outliers with median
    median_value = df[column_name].median()
    df.loc[outliers.index, column_name] = median_value

    # Plot HISQTY distribution before and after outlier correction
    products = df[group_by_column].unique()
    num_products = len(products)
    fig, axes = plt.subplots(1, num_products, figsize=(15, 5))

    for i, product in enumerate(products):
        product_data = df[df[group_by_column] == product][column_name]
        axes[i].plot(product_data, label='Before Correction', linestyle='--', marker='o', color='skyblue')
        
        # Plot outliers
        outliers_data = outliers[outliers[group_by_column] == product][column_name]
        axes[i].plot(outliers_data.index, outliers_data, 'ro', label='Outliers')
        
        # Plot after correction
        corrected_data = df[df[group_by_column] == product][column_name]
        axes[i].plot(corrected_data, label='After Correction', linestyle='-', marker='x', color='green')
        
        axes[i].set_title(f'{product} - HISQTY Distribution')
        axes[i].set_xlabel('Index')
        axes[i].set_ylabel('HISQTY')
        axes[i].legend()

    # Show the plot
    plt.tight_layout()
        # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()

 