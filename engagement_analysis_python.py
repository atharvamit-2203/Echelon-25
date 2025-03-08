import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
input_file = "t.csv"  # Change this to your input CSV file
output_file = "categorized_customers.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Check if 'tenure' and 'Churn' columns exist
if "tenure" not in df.columns or "Churn" not in df.columns:
    raise ValueError("CSV file must contain 'tenure' and 'Churn' columns")

# Categorize customers
def categorize_customer(row):
    if row["Churn"].strip().lower() == "yes":
        return "High Engagement"
    elif row["tenure"] > 24:
        return "Moderate Engagement"
    else:
        return "Low Engagement"

df["Category"] = df.apply(categorize_customer, axis=1)

# Save categorized data to a new CSV file
df.to_csv(output_file, index=False)
print(f"Categorized customer data saved to {output_file}")

# Count the categories
category_counts = df["Category"].value_counts()

# Plot pie chart
plt.figure(figsize=(6,6))
plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", colors=["#28a745", "#ffc107", "#dc3545"])
plt.title("Customer Segmentation: High vs Moderate vs Low Engagement")
plt.show()

print("\nCategorized Customers (Stored in 'categorized_customers.csv'):\n")
categorized_df = pd.read_csv(output_file)
print(categorized_df)