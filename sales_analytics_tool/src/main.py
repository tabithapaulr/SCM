# main.py

#flask related imports
from flask import Flask, render_template
import os
import matplotlib.pyplot as plt

#import for analytics functions
from production_planning import production_planning_function_with_vis,production_planning_function
from safety_stock import safety_stock_function
from model_comparison import model_comparison_function
from demand_planning import demand_planning_function
from outlier_detection import outlier_detection_function
from price_analysis import price_analysis_function
from product_performance import product_performance_function
from inventory_turnover_rate import inventory_turnover_function

import pandas as pd

import base64  

# Get the path to the templates folder
templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

app = Flask(__name__, template_folder=templates_dir)







#route for landing page
@app.route('/')
def index():
    return render_template('index.html')



#route for Production Planning
@app.route('/predict_production_planning')
def predict_production_planning():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_graph = production_planning_function_with_vis(df)
    # Encode the image data using base64
    image_data_base64 = base64.b64encode(result_graph).decode('utf-8')
    # Render the other_page.html template and pass the base64-encoded image data
    return render_template('production_planning_result.html', result_graph=image_data_base64)

#route for Safety Stock
@app.route('/predict_safety_stock')
def predict_safety_stock():
    df = pd.read_csv("Samsung-SalesData.csv")
    results = production_planning_function(df)
    result_img = safety_stock_function(results)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('safety_stock_result.html', result_img=image_data_base64)

#route for Model Comparison 
@app.route('/model_comparison')
def model_comparison():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_img = model_comparison_function(df)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('model_comparison_result.html', result_img=image_data_base64)


#route for Demand Planning 
@app.route('/demand_planning')
def predict_demand_planning():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_img = demand_planning_function(df)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('demand_planning_result.html', result_img=image_data_base64)


#route for Price Analysis 
@app.route('/price_analysis')
def price_analysis():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_img = price_analysis_function(df)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('price_analysis_result.html', result_img=image_data_base64)


#route for Outlier Detection 
@app.route('/outlier_detection')
def outlier_detection():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_img = outlier_detection_function(df)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('outlier_detection_result.html', result_img=image_data_base64)
    

#route for Inventory Turnover Rate 
@app.route('/inventory_turnover_rate')
def predict_inventory_turnover_rate():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_img = inventory_turnover_function(df)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('inventory_turnover_result.html', result_img=image_data_base64)


#route for Product Performance
@app.route('/product_performance')
def product_performance():
    df = pd.read_csv("Samsung-SalesData.csv")
    result_img = product_performance_function(df)
    image_data_base64 = base64.b64encode(result_img).decode('utf-8')
    return render_template('product_performance_result.html', result_img=image_data_base64)
    

if __name__ == '__main__':
    app.run(debug=True)
