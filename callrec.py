import speech_recognition as sr
import librosa
import soundfile as sf
from textblob import TextBlob

def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    # Load audio using librosa
    audio_data, sample_rate = librosa.load(audio_file, sr=None)
    
    # Save as WAV using soundfile
    wav_file = "converted_audio.wav"
    sf.write(wav_file, audio_data, sample_rate)
    
    # Read the WAV file using speech_recognition
    with sr.AudioFile(wav_file) as source:
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError:
            return "API request failed"

def analyze_behavior(text):
    sentiment = TextBlob(text).sentiment.polarity
    
    # Define keywords for categorization
    loyalty_keywords = ["happy", "satisfied", "love", "recommend", "great", "excellent"]
    at_risk_keywords = ["unhappy", "disappointed", "hate", "bad", "worst", "cancel"]
    saturated_keywords = ["okay", "fine", "neutral", "average", "nothing special"]
    
    # Count keyword occurrences
    text_lower = text.lower()
    loyalty_count = sum(word in text_lower for word in loyalty_keywords)
    at_risk_count = sum(word in text_lower for word in at_risk_keywords)
    saturated_count = sum(word in text_lower for word in saturated_keywords)
    
    # Determine category
    if sentiment > 0.2 or loyalty_count > at_risk_count and loyalty_count > saturated_count:
        return "Loyal"
    elif sentiment < -0.2 or at_risk_count > loyalty_count and at_risk_count > saturated_count:
        return "At Risk"
    else:
        return "Saturated"

# Example usage
audio_path = "vidhi_audio (online-audio-converter.com).mp3"  # Change to your file path
transcribed_text = convert_audio_to_text(audio_path)
if transcribed_text not in ["Could not understand the audio", "API request failed"]:
    category = analyze_behavior(transcribed_text)
    print("Transcribed Text:", transcribed_text)
    print("User Category:", category)
else:
    print(transcribed_text)
