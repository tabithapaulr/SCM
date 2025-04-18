import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

def inventory_turnover_function(df):

    # Group the data by product and region, and calculate total sales quantity
    sales_qty_df = df.groupby(['PRODUCT', 'REGION'])['HISQTY'].sum().reset_index()

    # Group the data by product and region, and calculate average inventory level
    inventory_df = df.groupby(['PRODUCT', 'REGION'])['HISQTY'].mean().reset_index()

    # Merge the two dataframes on 'PRODUCT' and 'REGION' columns
    merged_df = pd.merge(sales_qty_df, inventory_df, on=['PRODUCT', 'REGION'], suffixes=('_sales', '_inventory'))

    # Choose a demo product (let's take the first product in the dataset)
    demo_product = merged_df['PRODUCT'].iloc[0]
    product_data = merged_df[merged_df['PRODUCT'] == demo_product]
    product_data['Inventory_Turnover_Rate'] = product_data['HISQTY_sales'] / product_data['HISQTY_inventory']

    # Generate some dummy x-values for demonstration
    x = np.arange(len(product_data))

    # Generate some dummy y-values for demonstration (inventory turnover rate)
    y = product_data['Inventory_Turnover_Rate']

    # Plotting
    plt.figure(figsize=(10, 6))

    # Step plot with 'pre' parameter (default)
    plt.step(x, y, label='pre (default)', where='pre')

    # Overlay the step plot with marker points for better visualization
    plt.plot(x, y, 'o--', color='grey', alpha=0.3)

    # Step plot with 'mid' parameter
    plt.step(x, y + 1, label='mid', where='mid')
    plt.plot(x, y + 1, 'o--', color='grey', alpha=0.3)

    # Step plot with 'post' parameter
    plt.step(x, y + 2, label='post', where='post')
    plt.plot(x, y + 2, 'o--', color='grey', alpha=0.3)

    plt.grid(axis='x', color='0.95')
    plt.legend(title='Parameter where:', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(f'Inventory Turnover Rate for {demo_product}')
    plt.xlabel('Region')
    plt.ylabel('Inventory Turnover Rate')
    # Show the plot
    plt.tight_layout()
        # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()
