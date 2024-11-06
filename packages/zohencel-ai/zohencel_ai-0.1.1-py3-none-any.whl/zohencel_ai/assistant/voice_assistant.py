# zohencel_ai/assistant/main.py
import speech_recognition as sr
import pyttsx3
from .Grog_streaming import get_qadrix
import assemblyai as aai

# Set your API key as an environment variable instead of hardcoding for security
aai.settings.api_key = "your_assemblyai_api_key"
recognizer = sr.Recognizer()
transcriber = aai.Transcriber()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        transcript = transcriber.transcribe(audio)
        print("Recognized text from speech recognition:", text)
        print("\n\n\nText from new API", transcript.text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return None

def run_voice_assistant():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful voice assistant. Make your sound funny and informative, and keep the response short and engaging."
        }
    ]

    while True:
        text = listen()
        if text:
            if len(messages) > 5:
                messages = messages[:1] + messages[-4:]
            messages.append({"role": "user", "content": text})
            response = get_qadrix(messages)
            speak(response)
            messages.append({"role": "assistant", "content": response})

