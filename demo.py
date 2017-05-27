# -*- coding: utf-8 -*-
"""Demo

A demo of VIRA.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
Cstring_294W, Spring 2016-2017.
© Stanford University.
"""

import sys

import vira


def speak_and_print(voice_util, phrase):
    if voice_util:
        voice_util.utter_phrase(phrase)
    print phrase


def main():
    print "VIRA is loading...", '\r',
    sys.stdout.flush()

    apps_dir_path = vira.config.Mac.APP_DATA_DIR
    steam_util = vira.steam_util.SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()
    spell_util = vira.spell_util.SpellUtility(apps)
    voice_util = vira.voice_util.VoiceUtility('vira/voice_files/output.mp3')
    sys.stdout.write("\033[K")  # clear "loading..." line

    speech_util = vira.speech_util.SpeechUtility(voice_util)
    speech_util.get_name()
    speech_util.print_hello()
    print

    phrase = "{}, the following games are available:".format(speech_util.first_name)
    speak_and_print(voice_util, phrase)
    for app in apps:
        voice_util.utter_phrase(app)
        print "    - {}".format(app)
    print

    app = speech_util.get_app(spell_util)
    if app in apps:
        phrase = "Sounds good, {}. Opening {}...".format(speech_util.first_name, app)
        speak_and_print(voice_util, phrase)
        steam_util.spawn_app(app, vira.config.Mac.APP_EXTENSION)
    else:
        speak_and_print(voice_util, "Unfortunately, I don't think we have that app.")
        speak_and_print(voice_util, "Sorry, {}!".format(speech_util.first_name))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
