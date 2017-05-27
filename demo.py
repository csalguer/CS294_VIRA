# -*- coding: utf-8 -*-
"""Demo

A demo of VIRA.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
Cstring_294W, Spring 2016-2017.
© Stanford University.
"""

import sys

import vira


def main():
    print "VIRA is loading...", '\r',
    sys.stdout.flush()

    apps_dir_path = vira.config.Mac.APP_DATA_DIR
    steam_util = vira.steam_util.SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()

    spell_corr = vira.spell_util.SpellUtility(apps)
    sys.stdout.write("\033[K")  # clear line

    speech_util = vira.speech_util.SpeechUtility()
    speech_util.get_name()
    speech_util.print_hello()
    print

    print "{}, the following applications are available:".format(speech_util.first_name)
    for app in apps:
        print "    - {}".format(app)
    print

    app = speech_util.get_app(spell_corr)
    if app in apps:
        print "Sounds good, {}. Opening {}...".format(speech_util.first_name, app)
        steam_util.spawn_app(app, vira.config.Mac.APP_EXTENSION)
    else:
        print "Unfortunately, I don't think we have that app."
        print "Sorry, {}!".format(speech_util.first_name)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
