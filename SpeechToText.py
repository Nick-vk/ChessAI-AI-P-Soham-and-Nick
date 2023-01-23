# PyAudio is required to run this file
import speech_recognition as sr

# obtain audio from the microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()


class SpeechRecognition:
    # def __init__(self):
        # pass

    def speech_to_text(self, listening_time):
        elapsed_time = 0
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Set minimum energy threshold to {}".format(recognizer.energy_threshold))
            while True:
                print("Speak now")
                with microphone as source: audio = recognizer.listen(source)
                # recognize speech using Google Speech Recognition
                try:
                    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                    # instead of `r.recognize_google(audio)`
                    output = recognizer.recognize_google(audio)

                    reformatted_input = output.lower().replace(" ", "")
                    # print("Google Speech Recognition thinks you said " + output)
                    # print(reformatted_input)print("You said {}".format(value))
                    return reformatted_input

                except sr.UnknownValueError:
                    print("Audio not recognized")
                    # print("Let's try that again")
                    # self.speech_to_text()
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except KeyboardInterrupt:
            pass
