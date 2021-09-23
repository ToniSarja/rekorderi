import speech_recognition as sr
import pyaudio

import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    try:
        audio = r.listen(source)
        text = r.recognize_google(audio, language="ru")
        print(text)
        if text == 'Привет':
            print('vittu')
    except:
        pass
