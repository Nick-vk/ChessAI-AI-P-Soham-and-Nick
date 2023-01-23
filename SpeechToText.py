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
            print("Speak now")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            output = r.recognize_google(audio)
            reformatted_input = output.lower().replace(" ", "")
            # print("Google Speech Recognition thinks you said " + output)
            # print(reformatted_input)
            return reformatted_input
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            # print("Let's try that again")
            # self.speech_to_text()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
