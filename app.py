from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Serve the resource optimization frontend
@app.route('/')
def index():
    return render_template('resource_optimization.html')  # Serves the correct HTML file

# Endpoint to handle CSV file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Process the uploaded CSV file
        df = pd.read_csv(file)

        # Handle missing values
        df.fillna(method='ffill', inplace=True)
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df.fillna({'TotalCharges': df['TotalCharges'].median()}, inplace=True)

        # Encode categorical variables
        label_encoders = {}
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le

        # Churn Analysis - Identifying Key Factors
        churn_corr = df.corr()['Churn'].sort_values(ascending=False)

        # Generate insights
        insights = """
        1. Reduce High Churn Services - Customers with high monthly charges churn more. Consider loyalty discounts.
        2. Contract Optimization - Long-term contract holders churn less. Offer discounts on yearly subscriptions.
        3. Customer Segmentation - High tenure customers are less likely to leave. Focus on new customer retention.
        4. Upselling Strategy - Services like 'OnlineSecurity' and 'TechSupport' reduce churn. Promote these services.
        """

        # Prepare and return the response
        return jsonify({
            'churn_correlation': churn_corr.to_dict(),
            'insights': insights
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True) 