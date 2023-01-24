# PyAudio is required to run this file
import speech_recognition as sr

# obtain audio from the microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()


class SpeechRecognition:
    def speech_to_text(self):
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Set minimum energy threshold to {}".format(recognizer.energy_threshold))
            while True:
                print("Speak now")
                with microphone as source:
                    audio = recognizer.listen(source)
                # recognize speech using Google Speech Recognition
                try:
                    output = recognizer.recognize_google(audio)

                    # breakpoint
                    if output == "stop":
                        print("Engine shutting down")
                        quit()

                    reformatted_input = output.lower().replace(" ", "")
                    return reformatted_input

                except sr.UnknownValueError:
                    print("Audio not recognized")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except KeyboardInterrupt:
            pass
