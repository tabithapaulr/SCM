import pandas as pd
import matplotlib.pyplot as plt
import io 
def demand_planning_function(df):
    # Group the data by both 'REGION' and 'PRODUCT'
    grouped = df.groupby(['REGION', 'PRODUCT'])

    # Create a figure and axis object for plotting
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the demand trend for each group
    for i, (name, group) in enumerate(grouped):
        # Convert 'MONTH' column from month names to numerical values
        month_to_num = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        group['MONTH'] = group['MONTH'].map(month_to_num)

        # Calculate the demand trend (e.g., using mean HISQTY for simplicity)
        demand_trend = group.groupby(['YEAR', 'MONTH'])['HISQTY'].mean().reset_index()
        
        # Combine 'YEAR' and 'MONTH' columns to create a numerical representation of date
        demand_trend['Year_Month'] = demand_trend['YEAR'] + (demand_trend['MONTH'] - 1) / 12.0
        
        # Extract region and product from the name tuple
        region, product = name
        
        # Spread the plots apart for better visibility
        x_offset = i * 0.1
        
        # Plot the demand trend for the current group with x offset
        ax.plot(demand_trend['Year_Month'] + x_offset, demand_trend['HISQTY'], label=f'{product} - {region}')

    # Set labels and title
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Demand')
    ax.set_title('Demand Trend by Region and Product')
    ax.legend()
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

    # Show the plot
    plt.tight_layout()
        # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()

