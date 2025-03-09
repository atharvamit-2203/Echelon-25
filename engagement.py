import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the dataset
file_path = "t.csv"  # Change this if needed
try:
    print("📌 Loading dataset...")
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("❌ Error: File not found! Please check the file path.")
    exit()

# Drop customer ID
df.drop(columns=['customerID'], inplace=True, errors='ignore')

# Convert 'TotalCharges' to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
df.fillna(method='ffill', inplace=True)

# Encode categorical variables
categorical_columns = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                       'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                       'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
                       'PaymentMethod', 'Churn']

for col in categorical_columns:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

# Standardize numerical columns
num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Define engagement categories
def engagement_level(row):
    if row.get('tenure', 0) > 0.5 and row.get('OnlineSecurity', 0) == 1 and row.get('TechSupport', 0) == 1:
        return "Highly Engaged"
    elif row.get('tenure', 0) > 0.3 and row.get('StreamingTV', 0) == 1:
        return "Moderately Engaged"
    else:
        return "Low Engagement"

df['Engagement_Level'] = df.apply(engagement_level, axis=1)

# Display engagement distribution
engagement_counts = df['Engagement_Level'].value_counts()
print("\n📊 Engagement Level Distribution:\n", engagement_counts)

# Engagement Distribution Plot
sns.countplot(x="Engagement_Level", data=df, palette="coolwarm")
plt.title("Customer Engagement Levels")
plt.xlabel("Engagement Category")
plt.ylabel("Customer Count")
plt.show()

# Correlation Analysis
corr_df = df.drop(columns=['Engagement_Level'], errors='ignore')
plt.figure(figsize=(12, 7))
sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm")
plt.title("Customer Engagement Correlation Analysis")
plt.show()

# Save results
output_file = "customer_engagement_analysis.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ Engagement analysis saved successfully as '{output_file}'!")

# Optional: AI-based Insights using GPT-2

from transformers import pipeline

print("🤖 Generating AI insights...")

# Load GPT-2 Model
'''
generator = pipeline("text-generation", model="gpt2-medium")

def generate_local_ai_insights(data):
    prompt = f\"\"\"The following is an analysis of customer engagement levels:

    - Highly Engaged Customers: {data.get("Highly Engaged", 0)}
    - Moderately Engaged Customers: {data.get("Moderately Engaged", 0)}
    - Low Engagement Customers: {data.get("Low Engagement", 0)}

    Suggest **3 key strategies** to improve engagement and prevent customer churn.
    \"\"\"

    response = generator(prompt, max_length=150, num_return_sequences=1)
    generated_text = response[0]['generated_text']
    insights = "\\n".join(["✅ " + line for line in generated_text.split(". ") if line.strip()])
    return insights

# Generate insights
ai_suggestions = generate_local_ai_insights(engagement_counts)
print("\n🤖 **Locally Generated AI Insights:**")
print(ai_suggestions)
'''

print("\n🚀 Analysis Completed Successfully!")
