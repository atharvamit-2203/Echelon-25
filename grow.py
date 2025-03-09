from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Serve the customer segmentation frontend
@app.route('/')
def index():
    return render_template('customer-segmentation.html')

# Utility function to handle encoding transformations
def encode_categorical_columns(df):
    label_encoders = {}
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    return df, label_encoders

# Define a function to transform data with flexible columns
def transform_data(df):
    # Create a copy to avoid modifying the original dataframe
    df = df.copy()
    
    # Handle missing values by forward filling
    df.fillna(method='ffill', inplace=True)
    
    # If 'TotalCharges' exists, ensure it's numeric
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df.fillna({'TotalCharges': df['TotalCharges'].median()}, inplace=True)
    
    # Apply encoding to categorical columns
    df, label_encoders = encode_categorical_columns(df)
    
    return df, label_encoders

# Customer Segmentation Logic with flexible columns
def segment_customer(row, columns_available):
    # Default segment
    segment = 'General'
    
    # Check which columns are available and apply rules accordingly
    if 'MonthlyCharges' in columns_available and 'Churn' in columns_available:
        monthly_charges = row['MonthlyCharges']
        # Convert Churn to int if it exists to ensure proper comparison
        churn = int(row['Churn']) if 'Churn' in columns_available else 0
        
        if monthly_charges > 100 and churn == 1:
            segment = 'At Risk'
        elif monthly_charges < 50 and churn == 0:
            segment = 'Loyal'
    
    if segment == 'General' and 'Tenure' in columns_available:
        tenure = row['Tenure']
        if tenure < 12:
            segment = 'Potential'
        elif segment == 'General':  # Only change if not already categorized
            segment = 'Saturated'
            
    return segment

# Endpoint to handle CSV file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is part of the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Process the uploaded CSV file
        df = pd.read_csv(file)
        
        # Generate ID column if not present
        if 'CustomerID' not in df.columns:
            df['CustomerID'] = ['C' + str(i) for i in range(1, len(df) + 1)]
        
        # Transform the data (cleaning, encoding)
        df, label_encoders = transform_data(df)
        
        # Get available columns for segmentation
        columns_available = df.columns.tolist()
        
        # Segment customers using the flexible segment_customer function
        df['Segment'] = df.apply(lambda row: segment_customer(row, columns_available), axis=1)
        
        # Count of customers in each segment
        segment_counts = df['Segment'].value_counts().to_dict()
        
        # Generate insights directly as dictionary (no string manipulation)
        insights = {
            "Loyal": "These customers have a low monthly charge and are less likely to churn.",
            "At Risk": "These customers have high monthly charges and are more likely to churn.",
            "Potential": "These customers have a short tenure and may need additional engagement.",
            "Saturated": "These customers have been with the company for a while, but their retention needs to be encouraged.",
            "General": "These customers couldn't be segmented due to insufficient data."
        }
        
        # Only include insights for segments that exist in the data
        present_segments = segment_counts.keys()
        filtered_insights = {}
        for segment in present_segments:
            if segment in insights:
                filtered_insights[segment] = insights[segment]
        
        # Prepare the result to return
        result = {
            'customer_segments': df[['CustomerID', 'Segment']].to_dict(orient='records'),
            'segment_counts': segment_counts,
            'insights': filtered_insights,
            'columns_used': columns_available
        }
        
        return jsonify(result)
    
    except Exception as e:
        # Print detailed error information for debugging
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

# Run the Flask app on a specific port
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)