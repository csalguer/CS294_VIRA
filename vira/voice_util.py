# -*- coding: utf-8 -*-
"""VoiceUtility

System-related methods for manipulating Steam games
that have already been installed on the system.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
Cstring_294W, Spring 2016-2017.
© Stanford University.
"""

import gtts
import playsound


class VoiceUtility(object):
    """docstring for VoiceUtility"""

    def __init__(self, output_path='voice_files/output.mp3'):
        super(VoiceUtility, self).__init__()
        self.chunk_size = 1024
        self.rel_path = output_path

    def utter_phrase(self, text):
        if not text:
            return False

        try:
            self._create_spoken_file(text)
        except:
            print "[Error]: Couldn't find file location for temp utterance"
            return False

        self._playback_utterance()
        return True

    def _create_spoken_file(self, text):
        try:
            gtts.gTTS(text, lang='en', slow=False).save(self.rel_path)
        except Exception as e:
            print "Error in voice_synth creation"
            raise

    def _playback_utterance(self):
        playsound.playsound(self.rel_path)


def main():
    voice_box = VoiceUtility()
    voice_box.utter_phrase("Choices are, One: Mobius Final Fantasy, Two: Tilt brush, Three: Bioshock, and finally Four: Faerie")


if __name__ == '__main__':
    main()
