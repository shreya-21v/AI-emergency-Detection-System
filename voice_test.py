import speech_recognition as sr

recognizer = sr.Recognizer()

# Use microphone array (index may vary slightly)
mic = sr.Microphone(device_index=2)

print("Adjusting for noise...")

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("Speak now...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError:
    print("Speech service unavailable")
