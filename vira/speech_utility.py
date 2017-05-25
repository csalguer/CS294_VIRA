# -*- coding: utf-8 -*-
"""SpeechUtility

CS294W, Spring 2016-2017.
"""

import sys
import speech_recognition as sr


class SpeechUtility(object):
    """Encapsulates Automatic Speech Recognition functionality"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.name = self.get_name()

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
            return name

    def print_hello(self):
        print "Hi, {}".format(self.name)


def main():
    speech_util = SpeechUtility()
    speech_util.print_hello()


if __name__ == "__main__":
    main()
