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

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.name = None
        self.first_name = None

    def get_app(self, spell_corr):
        with sr.Microphone() as mike:
            print "Which app would you like to open, {}?".format(self.first_name)

            while True:
                try:
                    print "Listening for audio...", '\r',
                    sys.stdout.flush()
                    audio = self.recognizer.listen(mike)
                    print "Analyzing your speech...", '\r',
                    sys.stdout.flush()
                    # TODO: get API key for Google Speech Recognition
                    app_guess = self.recognizer.recognize_google(audio)

                except sr.UnknownValueError:
                    sys.stdout.write("\033[K")  # clear line
                    sys.stdout.write("\033[F")  # back to previous line
                    sys.stdout.write("\033[K")  # clear line
                    print "Sorry, I didn't hear your properly.",
                    print "Which app would you like to open, {}?".format(self.first_name)
                    sys.stdout.flush()
                    continue

                except sr.RequestError:
                    print "RequestError: The requested transmission failed."
                    raise

                break

        sys.stdout.write("\033[K")  # clear line
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        sys.stdout.flush()
        app = spell_corr.get_closest_name(app_guess.lower())
        return app

    def get_name(self):
        with sr.Microphone() as mike:
            print "What is your name?"

            while True:
                try:
                    print "Listening for audio...", '\r',
                    sys.stdout.flush()
                    audio = self.recognizer.listen(mike)
                    print "Analyzing your speech...", '\r',
                    sys.stdout.flush()
                    # TODO: get API key for Google Speech Recognition
                    name = self.recognizer.recognize_google(audio).title()

                except sr.UnknownValueError:
                    sys.stdout.write("\033[K")  # clear line
                    sys.stdout.write("\033[F")  # back to previous line
                    sys.stdout.write("\033[K")  # clear line
                    print "Sorry, I didn't hear your properly. What is your name?"
                    sys.stdout.flush()
                    continue

                except sr.RequestError:
                    print "RequestError: The requested transmission failed."
                    raise

                break

        sys.stdout.write("\033[K")  # clear line
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        sys.stdout.flush()
        self.name = name
        self.first_name = self.name.split()[0]

    def print_hello(self):
        if not self.name:
            self.get_name()
        print "Hi, {}!".format(self.first_name)


def main():
    speech_util = SpeechUtility()
    speech_util.print_hello()


if __name__ == "__main__":
    main()
