import pandas as pd
import matplotlib.pyplot as plt
import io

def product_performance_function(df):

    # Convert 'MONTH' and 'YEAR' columns to datetime
    df['DATE'] = pd.to_datetime(df['MONTH'] + ' ' + df['YEAR'].astype(str), format='%B %Y')

    # Group the data by product and month/year, and calculate total sales revenue
    grouped_df = df.groupby(['PRODUCT', 'DATE']).agg({'SALES_REVENUE': 'sum'}).reset_index()

    # Plotting
    plt.figure(figsize=(12, 8))

    for product in grouped_df['PRODUCT'].unique():
        product_data = grouped_df[grouped_df['PRODUCT'] == product]
        plt.plot(product_data['DATE'], product_data['SALES_REVENUE'], label=product)

    plt.xlabel('Date')
    plt.ylabel('Sales Revenue')
    plt.title('Product Performance Monitoring')
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()
