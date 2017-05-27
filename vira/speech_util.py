# -*- coding: utf-8 -*-
"""SpeechUtility

ASR system based on Google Speech Recognition.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import sys
import speech_recognition as sr


class SpeechUtility(object):
    """Encapsulates Automatic Speech Recognition functionality"""

    def __init__(self, voice_util=None):
        self.recognizer = sr.Recognizer()
        self.name = None
        self.first_name = None
        self.voice_util = voice_util

    def get_app(self, spell_corr):
        phrase = "Which app would you like to open, {}?".format(self.first_name)
        self.speak_and_print(phrase)

        with sr.Microphone() as mike:
            while True:
                try:
                    print "Listening for audio...", '\r',
                    sys.stdout.flush()
                    audio = self.recognizer.listen(mike)
                    print "Analyzing your speech...", '\r',
                    sys.stdout.flush()
                    # TODO: get API key for Google Speech Recognition
                    app_guess = self.recognizer.recognize_google(audio)
                    break

                except sr.UnknownValueError:
                    sys.stdout.write("\033[K")  # clear line
                    sys.stdout.write("\033[F")  # back to previous line
                    sys.stdout.write("\033[K")  # clear line
                    phrase = ("Sorry, I didn't hear you properly. "
                              "Which app would you like to open, {}?".format(self.first_name))
                    self.speak_and_print(phrase)
                    sys.stdout.flush()
                    continue

                except sr.RequestError:
                    print "RequestError: The requested transmission failed."
                    raise

        sys.stdout.write("\033[K")  # clear line
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        sys.stdout.flush()
        app = spell_corr.get_closest_name(app_guess.lower())
        return app

    def get_name(self):
        self.speak_and_print("What is your name?")

        with sr.Microphone() as mike:
            while True:
                try:
                    print "Listening for audio...", '\r',
                    sys.stdout.flush()
                    audio = self.recognizer.listen(mike)
                    print "Analyzing your speech...", '\r',
                    sys.stdout.flush()
                    # TODO: get API key for Google Speech Recognition
                    name = self.recognizer.recognize_google(audio).title()
                    if name.lower() == "ekg":
                        name = "Ikechi"
                    break

                except sr.UnknownValueError:
                    sys.stdout.write("\033[K")  # clear line
                    sys.stdout.write("\033[F")  # back to previous line
                    sys.stdout.write("\033[K")  # clear line
                    self.speak_and_print("Sorry, I didn't hear you properly. What is your name?")
                    sys.stdout.flush()
                    continue

                except sr.RequestError:
                    print "RequestError: The requested transmission failed."
                    raise


        sys.stdout.write("\033[K")  # clear line
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        sys.stdout.flush()
        self.name = name
        self.first_name = self.name.split()[0]

    def speak_and_print(self, phrase):
        if self.voice_util:
            self.voice_util.utter_phrase(phrase)
        print phrase

    def print_hello(self):
        if not self.name:
            self.get_name()
        print "Hi, {}!".format(self.first_name)


def main():
    speech_util = SpeechUtility()
    speech_util.print_hello()


if __name__ == "__main__":
    main()
