import speech_recognition as sr
import pyttsx3


class Voice:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.engine = pyttsx3.init()

    def speech_to_text(self):

        with sr.Microphone() as source:

            print("Listening...")

            audio = self.recognizer.listen(source)

        try:

            return self.recognizer.recognize_google(audio)

        except Exception:

            return ""

    def text_to_speech(self, text):

        self.engine.say(text)

        self.engine.runAndWait()


voice = Voice()