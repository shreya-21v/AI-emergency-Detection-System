import speech_recognition as sr
from textblob import TextBlob
from collections import deque
voice_buffer = deque(maxlen=5)

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=2)

distress_keywords = [
    "help", "stop", "danger", "save me",
    "emergency", "call police",
    "scared", "afraid", "hurt", "unsafe"
]

def get_voice_distress_score():
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)

        text = recognizer.recognize_google(audio)
        print("Voice:", text)

        match_count = 0
        for word in distress_keywords:
            if word in text.lower():
                match_count += 1

        keyword_score = match_count * 20

        analysis = TextBlob(text)
        sentiment = analysis.sentiment.polarity

        if sentiment < -0.3:
            sentiment_score = 20
        elif sentiment < -0.05:
            sentiment_score = 10
        else:
            sentiment_score = 0

        voice_buffer.append(keyword_score + sentiment_score)
        return sum(voice_buffer) / len(voice_buffer)

    except:
        if len(voice_buffer) > 0:
            return sum(voice_buffer) / len(voice_buffer)
        return 0
