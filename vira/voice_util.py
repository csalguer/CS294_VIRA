# -*- coding: utf-8 -*-
"""VoiceUtility

A module that allows VIRA to speak.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import os

import gtts
import playsound
import urllib3

urllib3.disable_warnings()


class VoiceUtility(object):
    """The VoiceUtility module is a wrapper around
       Google's text to speech API."""

    def __init__(self, output_path='voice_files/output.mp3'):
        super(VoiceUtility, self).__init__()
        self.chunk_size = 1024
        self.rel_path = output_path

    def utter_phrase(self, text):
        """Says the given phrase in VIRA's voice."""
        if not text:
            return False

        num_failures = 0
        while True:
            if num_failures > 2:
                return False

            try:
                gtts.gTTS(text, lang='en', slow=False).save(self.rel_path)
                break

            except IOError:
                num_failures += 1
                dir_ = os.path.dirname(self.rel_path)
                if not os.path.exists(dir_):
                    os.makedirs(dir_)
                open(self.rel_path, 'w').close()

            except Exception as exception:
                print exception
                return False

        self._playback_utterance()
        return True

    def _playback_utterance(self):
        playsound.playsound(self.rel_path)


def main():
    """Tests the voice utility."""
    voice_box = VoiceUtility()
    voice_box.utter_phrase("Choices are, One: Mobius Final Fantasy, Two: Tilt brush, Three: Bioshock, and finally Four: Faerie")


if __name__ == '__main__':
    main()
