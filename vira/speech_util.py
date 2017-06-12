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

    def __init__(self, voice_util=None, preferred_phrases=[]):
        self.recognizer = sr.Recognizer()
        self.name = None
        self.first_name = None
        self.voice_util = voice_util
        self.google_credentials = r"""{
                                       "type": "service_account",
                                       "project_id": "pac2text",
                                       "private_key_id": "43a5e4cfc4f61e777910d053ccb249c47e928198",
                                       "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDD4OAxtLagWeQ+\nhQ7NgOt+Xdd2kBPv41QrIR8Uq4pWmq4xzrIRiQc4f59A8QirJ86B4/LKxcVLJoDf\nV7cWdfA9iwkPxeQeOulh5BbM8Wwksej3matdpd9ZZgvtU4D7LuZmwgnIrFjRSwPR\nyQDZYK1Wq1wgjUusJmfLQ2OMxYQS7z0gHLKuDIag2SC5eOVwZ8y+Duzv3CLFMhhc\njOTCoNTmXvAbrZCmIrYRPqxuhV92t+k3lcl9GxOA/kEaw+sjxPo03MFm7FtGUyaM\n02xcAj16Z18CeFEN3hTWLWvsjmtC96vy6TQn3Sza2S1mILzCrqOm7gk8lwHvHo+U\nMm15Fge1AgMBAAECggEAB1l5sAPC0nNs//eIHafXri8hNX6kcNzLvK6KdwEUuLkn\nDhFeVxAYKEOJmyswExP0SKVf58HR7EbukPK+mOYl9HkyBth6/bNiLF0dieUJFLtk\nLV4jsujVX4pXqjj23vXciUCAk3n7/yZcZ1OuZ3mcJ2NYmpQSocvzGwpVQuPqV7d3\nbAoVpix2rUYuq+OZO4IeAB2YbpPAnLoGVLywYlS/8IS7B9T21MqT1xzKpgJ/elR1\nFFgvjyQN+7ECuMt8ZMQHaWE+5UDZ2xEjxjeJHUQPm0LrYrQzhdkbcb5+wC+NIYVQ\nNYi/oTYahabR0HhjR2g8JJ6ZdLyqTQu1GU89TXVU5QKBgQDzPE1Yo9vXXtGifg25\n26ivywFVMgaTnY5vepIDzQ1yxAa7ZBxBmrdFY+NFgWv84MwjJYSjRPhTCYX+GHLx\n4YzuIyrioVxznFF5Fc4ATveQ5jdoWtZgRjKt1VEW7L66tyzp4Ko2Jw4265LhRYpQ\neFMcNtFeYWx3C6awfnlNYnbSXwKBgQDOKF0tqcZoE2dhswKHmc+3oPRXfUS55KHH\nnoQvCaeNT4+9+eJxh5PEnrdajt3jl7KTfro6zGzCXfbQMumt9n0n7WWii7RvbbqW\nu33W/WhHqk62QGauCsDRaqPatNKSWPD+XYUkvDq9U2PrYaI2l6fi9qU/lyvkWMve\n+p648w4mawKBgBbr994CkxUYumi1uFVrfdoTJ2z/6d6/WkznIBt7l2jZUEkYhhEo\no1zGrQQ/zg1modYuEvHP7hblLttjMnHY748BgWkaC7xZXtQqWd9tkab2CwKqjMlF\n1EDNeXbPmKm/2Vuw8FlqFMzYJl9UTlSHAk4GXHSoebA+SNcZFBVW0hvBAoGAUyZC\nlsVQKfARlX0++vRVrEm144e57YRCoCHWTKaHNt6tKkGcTJATUI13hIX1BvPLaeQG\nNur2vtppTwYJ7Elrp2v/vzS73OmUBXGvysPAiI8vWiDViUL7DDwHxJGEENTgtqd/\nqRZmVrBIr8pcQ8qdQ1SZx/EwGdSavd+1nwEhZusCgYEA1SlFw2uZGNvNnV07rWgD\naievVSrW3UBEEYiyOEq1JIEaOFRdxJjbfrU5GeOJiTo57SYVFm51K8n/g1n2xPY0\ngSO51FxYlcG5db9AaBiA+SPgzitbuEXj4CBxHC0kvC2LoKA+/tEkfIqcuj8T9Try\na8C5ijEftpuQR8cBS4AnsKQ=\n-----END PRIVATE KEY-----\n",
                                       "client_email": "matt-415@pac2text.iam.gserviceaccount.com",
                                       "client_id": "108600580804135879328",
                                       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                       "token_uri": "https://accounts.google.com/o/oauth2/token",
                                       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                       "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/matt-415%40pac2text.iam.gserviceaccount.com"
                                      }
                                   """
        self.preferred_phrases = preferred_phrases

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
        if self.voice_util:
            self.voice_util.utter_phrase(phrase)
        print phrase

    def print_hello(self):
        if not self.name:
            self.get_name()
        print "Hi, {}!".format(self.first_name)

    def listen_for_command(self):
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
    speech_util = SpeechUtility()
    speech_util.print_hello()


if __name__ == "__main__":
    main()
