#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()


class SpeechRecognition:
    def __init__(self):
        pass

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            lowercase_string = r.recognize_google(audio).lower()
            no_space_string = lowercase_string.replace(" ", "")
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            print(no_space_string)
            return no_space_string
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))