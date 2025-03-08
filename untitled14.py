# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1raLogKsQyBlH53JPjlpCwRID9O--IHtW
"""

!pip install opencv-python pytesseract numpy transformers torch flask

!apt-get install -y tesseract-ocr
!pip install pytesseract

from transformers import pipeline

# Sentiment analysis model load karo
sentiment_analyzer = pipeline("sentiment-analysis")

# Example text ka test run
text = "This service is amazing!"
result = sentiment_analyzer(text)

print("Sentiment Result:", result)

import cv2
import pytesseract
import numpy as np
from google.colab import files
from PIL import Image

# Manually upload image
uploaded = files.upload()

# Read image
for filename in uploaded.keys():
    image = Image.open(filename)
    open_cv_image = np.array(image)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # OCR se text extract karo
    extracted_text = pytesseract.image_to_string(gray)

    print("Extracted Text:", extracted_text)

# Sentiment Analysis kare extracted text pe
sentiment_result = sentiment_analyzer(extracted_text)

print("Final Sentiment Analysis:", sentiment_result)

import pandas as pd

# 📝 Example: Sentiment Analysis Output (From Extracted Text)
sentiment_result = sentiment_analyzer(extracted_text)  # ✅ AI se analyze ho chuka hai

# 🔢 Categorization Logic
def categorize_customer(sentiment_result):
    positive, negative, neutral = 0, 0, 0

    for result in sentiment_result:
        if result['label'] == 'POSITIVE':
            positive += 1
        elif result['label'] == 'NEGATIVE':
            negative += 1
        else:
            neutral += 1

    # 🔢 Loyalty Score Calculation
    total = positive + negative + neutral
    loyalty_score = (positive - negative) / total if total > 0 else 0

    # 🏷️ Customer Category Based on Score
    if loyalty_score > 0.5:
        category = "Loyal ✅"
    elif loyalty_score < -0.2:
        category = "At-Risk ⚠️"
    else:
        category = "Saturated ❌"

    return {"Score": round(loyalty_score, 2), "Category": category}

# 🚀 Run Categorization
customer_category = categorize_customer(sentiment_result)

# 📌 Print Result
print("Final Customer Categorization:", customer_category)

pip install openai

!pip install openai





def ai_generate_recommendations(customer_feedback, customer_category):
    prompt = f"""
    Based on the following customer feedback, analyze the issues and suggest improvements:

    Customer Feedback: {customer_feedback}

    Customer Category: {customer_category}

    Provide clear, specific, and actionable business improvement strategies to enhance customer satisfaction.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a business expert providing recommendations to improve customer satisfaction."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]

!pip install transformers

from transformers import pipeline

# Initialize GPT-2 text-generation pipeline with pad_token_id for GPT-2
generator = pipeline(
    "text-generation",
    model="gpt2",
    pad_token_id=50256  # Prevents truncation error
)

def generate_recommendations_hf(extracted_text, category):
    prompt = (
        f"Based on the following customer conversation data and the customer category, "
        f"analyze the issues and provide specific, actionable business recommendations "
        f"to improve customer satisfaction. Provide your suggestions as a numbered list.\n\n"
        f"Customer Conversation Data: {extracted_text}\n"
        f"Customer Category: {customer_category}\n"
        f"Recommendations:"
    )

    # Generate text with max_length
    result = generator(
        prompt,
        max_length=300,
        num_return_sequences=1
    )

    # Return the generated text
    return result[0]["generated_text"]

# Example usage
extracted_text = "The delivery was delayed and customer service did not respond promptly."
category = "At-Risk ⚠️"

recommendations_hf = generate_recommendations_hf(extracted_text, customer_category)
print("Business Improvement Recommendations (Hugging Face):")
print(recommendations_hf)

!pip install transformers sentencepiece

from transformers import pipeline

# Load an instruction-tuned model (FLAN-T5) for text-to-text generation.
model_name = "google/flan-t5-base"  # You can try a larger version if available.
generator = pipeline("text2text-generation", model=model_name)

def generate_recommendations_flant5(extracted_text, customer_category):
    prompt = (
        "You are a seasoned business consultant with deep expertise in customer engagement. "
        "Analyze the following customer conversation data and the given customer category. "
        "Regardless of the category, provide at least three actionable business recommendations "
        "to further improve customer satisfaction. If the customer is loyal, suggest strategies to "
        "enhance their engagement and turn their loyalty into increased revenue. Please provide your answer "
        "as a numbered list with clear, specific, and detailed recommendations.\n\n"
        f"Customer Conversation Data:\n{extracted_text}\n\n"
        f"Customer Category: {customer_category}\n\n"
        "Recommendations:"
    )

    # Debug: Print the prompt to verify it looks as expected.
    print("Generated Prompt:\n", prompt)

    result = generator(
        prompt,
        max_new_tokens=200,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )
    return result[0]["generated_text"]



recommendations = generate_recommendations_flant5(extracted_text, customer_category)
print("\nBusiness Improvement Recommendations (FLAN-T5):")
print(recommendations)