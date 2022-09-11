import speech_recognition as sr
import pyaudio

class Recog:
    def __init__(self):
        self.tunnista()

    def tunnista(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio, language="ru")
                print(text)
                if text == 'Привет':
                    print('Как дела')
            except:
                pass

if __name__=='__main__':
    Recog()
