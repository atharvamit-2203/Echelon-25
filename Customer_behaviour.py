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

def analyze_customer_satisfaction(text):
    sentiment_score = TextBlob(text).sentiment.polarity

    if sentiment_score > 0.2:
        return "Loyal"
    elif -0.2 <= sentiment_score <= 0.2:
        return "Saturated"
    else:
        return "At Risk"

# Example usage
audio_path = "WhatsApp Audio 2025-03-08 at 15.29.28_9e022865.dat (online-audio-converter.com).mp3"  # Change this to your file path
transcribed_text = convert_audio_to_text(audio_path)

if transcribed_text not in ["Could not understand the audio", "API request failed"]:
    customer_category = analyze_customer_satisfaction(transcribed_text)
    print("Transcribed Text:", transcribed_text)
    print("Customer Category:", customer_category)
else:
    print("Error:", transcribed_text)
