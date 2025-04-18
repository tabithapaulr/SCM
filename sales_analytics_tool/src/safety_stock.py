# safety_stock.py

import pandas as pd
import matplotlib.pyplot as plt
import io



def safety_stock_function(results_df, safety_stock_percentage=0.1):

    # Extract predicted and actual quantities for each year
    predicted_2024 = results_df['Predicted 2024']
    predicted_2025 = results_df['Predicted 2025']
    actual_2021 = results_df['Actual 2021']
    actual_2022 = results_df['Actual 2022']
    actual_2023 = results_df['Actual 2023']
    
    # Calculate forecasted demand for each combination of predicted and actual quantities
    forecasted_demand_2024_2021 = predicted_2024 - actual_2021
    forecasted_demand_2024_2022 = predicted_2024 - actual_2022
    forecasted_demand_2024_2023 = predicted_2024 - actual_2023
    forecasted_demand_2025_2021 = predicted_2025 - actual_2021
    forecasted_demand_2025_2022 = predicted_2025 - actual_2022
    forecasted_demand_2025_2023 = predicted_2025 - actual_2023
    
    # Combine forecasted demand for both years
    forecasted_demand = pd.DataFrame({
        '2024_2021': forecasted_demand_2024_2021,
        '2024_2022': forecasted_demand_2024_2022,
        '2024_2023': forecasted_demand_2024_2023,
        '2025_2021': forecasted_demand_2025_2021,
        '2025_2022': forecasted_demand_2025_2022,
        '2025_2023': forecasted_demand_2025_2023
    })
    
    # Calculate safety stock by adding 10% to the forecasted demand
    safety_stock = (forecasted_demand * (1 + safety_stock_percentage)).round(decimals=0)
    

    # Plot the safety stock
    plt.figure(figsize=(14, 8))  # Increase the figure size
    ax = safety_stock.plot(kind='bar', ax=plt.gca(), width=0.8)  # Adjust the width of the bars
    plt.title('Safety Stock for Each Product and Each Year')
    plt.xlabel('Product')
    plt.ylabel('Safety Stock')
    plt.xticks(rotation=45, ha='right')
    
    # Add safety stock values on top of each bar
    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height(), str(round(i.get_height(), 2)), ha='center', va='bottom')
    
    plt.tight_layout()
    

    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Close the plot
    plt.close()
    
    return img_buffer.getvalue()

