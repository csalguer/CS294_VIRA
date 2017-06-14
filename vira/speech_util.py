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

    def __init__(self, voice_util=None, google_credentials=None,
                 preferred_phrases=None):
        self.recognizer = sr.Recognizer()
        self.name = None
        self.first_name = None
        self.voice_util = voice_util
        self.google_credentials = google_credentials
        self.preferred_phrases = preferred_phrases

    def get_app(self, spell_corr):
        """Listens for an application name, then uses the spelling
           corrector to fix any transcription errors."""
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
                    app_guess = self.recognizer.recognize_google_cloud(audio, credentials_json=self.google_credentials, preferred_phrases=self.preferred_phrases)
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
        """Asks the user for her name, and saves it."""
        self.speak_and_print("What is your name?")

        with sr.Microphone() as mike:
            while True:
                try:
                    print "Listening for audio...", '\r',
                    sys.stdout.flush()
                    audio = self.recognizer.listen(mike)
                    print "Analyzing your speech...", '\r',
                    sys.stdout.flush()
                    name = self.recognizer.recognize_google_cloud(audio, credentials_json=self.google_credentials, preferred_phrases=self.preferred_phrases).title()
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
        """If possible to speak the phrase, then speaks the phrase.
           At minimum, will print the phrase to standard out."""
        if self.voice_util:
            self.voice_util.utter_phrase(phrase)
        print phrase

    def print_hello(self):
        """Says hello using the saved name."""
        if not self.name:
            self.get_name()
        print "Hi, {}!".format(self.first_name)

    def listen_for_command(self):
        """Listens for anything; upon hearing it, returns what was heard."""
        with sr.Microphone() as mike:
            while True:
                try:
                    audio = self.recognizer.listen(mike)
                    command = self.recognizer.recognize_google_cloud(audio, credentials_json=self.google_credentials, preferred_phrases=self.preferred_phrases)
                    break
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print "RequestError: The requested transmission failed."
                    raise

        return command


def main():
    import config
    CNFG = config.get_config()
    speech_util = SpeechUtility(CNFG.GOOGLE_CREDENTIALS)
    speech_util.print_hello()


if __name__ == "__main__":
    main()
