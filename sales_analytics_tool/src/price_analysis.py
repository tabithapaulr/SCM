import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

def price_analysis_function(df):


    # Group the data by product and region, and calculate average price, total sales revenue, and total demand
    grouped_df = df.groupby(['PRODUCT', 'REGION']).agg({
        'PRICE': 'mean',
        'SALES_REVENUE': 'sum',
        'HISQTY': 'sum'
    }).reset_index()

    # Pivot the dataframe for heatmap
    pivot_df = grouped_df.pivot(index='PRODUCT', columns='REGION', values=['PRICE', 'SALES_REVENUE', 'HISQTY'])

    # Plotting heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap: Price, Sales Revenue, and Demand')
    plt.xlabel('Metrics')
    plt.ylabel('Metrics')
    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()
