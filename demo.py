# -*- coding: utf-8 -*-
"""Demo

A demo of VIRA.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""


import os
import sys
import time

import vira


def speak_and_print(voice_util, phrase):
    if voice_util:
        voice_util.utter_phrase(phrase)
    print phrase

def main():
    print "VIRA is loading...", '\r',
    sys.stdout.flush()
    CNFG = vira.config.get_config()

    # load controller(s)
    alarm_util = vira.alarm_util.AlarmUtility(CNFG.VLC_PATH, CNFG.ALARM_PATH)
    apps_dir_path = CNFG.APP_DATA_DIR
    app_util = vira.app_util.AppUtility(apps_dir_path)
    apps = app_util.get_all_apps()
    spell_util = vira.spell_util.SpellUtility(apps)
    volume_util = vira.volume_util.VolumeUtility()

    # load view(s)
    voice_util = vira.voice_util.VoiceUtility(CNFG.VOICE_PATH, CNFG.ALERT_PATH, CNFG.CONFIRM_PATH)

    # load models
    joke_util = vira.joke_util.JokeUtility()
    names = ["Vira", "Ikechi", "Matt", "Chris", "Giovanni", "Monica", "Violet", "Kaneshiro"]
    speech_util = vira.speech_util.SpeechUtility(voice_util, CNFG.GOOGLE_CREDENTIALS, apps + names)
    time_util = vira.time_util.TimeUtility()
    weather_util = vira.weather_util.WeatherUtility()
    search_util = vira.search_util.SearchUtility(config_file=CNFG.SEARCH_CREDENTIAL_PATH)

    # begin demo
    sys.stdout.write("\033[K")  # clear "loading..." line
    sys.stdout.flush()
    speech_util.get_name()
    speech_util.print_hello()

    phrase = "{}, the following games are available:".format(speech_util.first_name)
    speak_and_print(voice_util, phrase)
    while True:
        for app in apps:
            voice_util.utter_phrase(app)
            print "    - {}".format(app)
        print

        app = speech_util.get_app(spell_util)
        if app in apps:
            phrase = "Sounds good, {}. Opening {}...".format(speech_util.first_name, app)
            speak_and_print(voice_util, phrase)
            app_util.spawn_app(app, CNFG.APP_EXTENSION)
            break
        else:
            speak_and_print(voice_util, "Unfortunately, I don't think we have that app.")
            speak_and_print(voice_util, "Sorry, {}!".format(speech_util.first_name))
            phrase = "As a reminder, {}, the following games are available:".format(speech_util.first_name)
            speak_and_print(voice_util, phrase)

    while True:
        speech_util.listen_for_prompt()
        voice_util.play_alert()
        volume_util.minimize_volume()
        command = speech_util.listen_for_command()
        voice_util.play_confirm()
        volume_util.restore_volume()

        # sentiment analysis... sort of. This will get put in a module eventually.
        # As a future improvement, a more complex classifier should be implemented.
        # This unigram-based one is too simple and naive to be put in its own module.
        # Ideally, something like DIPRE needs to be implemented for relationship extraction.
        # These commands only demonstrate a bit of VIRA's functionality.
        if "weather" in command or "temperature" in command:
            weather_report = weather_util.get_weather()
            speak_and_print(voice_util, "{}, ".format(speech_util.first_name) + weather_report)

        elif "alarm" in command or "timer" in command:
            command_list = command.split()
            if "minutes" in command_list:
                minutes_index = command_list.index("minutes")
            elif "minute" in command_list:
                minutes_index = command_list.index("minute")
            else:
                speak_and_print(voice_util, "{}, I'm afraid I didn't understand.".format(speech_util.first_name))
                speak_and_print(voice_util, "Try a command like, 'Set an alarm for five minutes from now.'".format(speech_util.first_name))
                continue

            try:
                num_minutes = int(command_list[minutes_index - 1])  # the word before minutes
                unit = "minute"
                if num_minutes > 1:
                    unit = "minutes"
                elif num_minutes < 1:
                    raise ValueError
                alarm_util.start_alarm(num_minutes)
                speak_and_print(voice_util, "Okay, {}, I set an alarm for {} {} from now.".format(speech_util.first_name, num_minutes, unit))
            except ValueError:
                speak_and_print(voice_util, "{}, I'm afraid I didn't understand.".format(speech_util.first_name))
                speak_and_print(voice_util, "Try a command like, 'Set a timer to go off five minutes from now.'".format(speech_util.first_name))
                continue

        elif "joke" in command or "jokes" in command or "funny" in command:
            speak_and_print(voice_util, "Here's a joke, {}:".format(speech_util.first_name))
            joke = joke_util.get_joke()
            speak_and_print(voice_util, joke)
            speak_and_print(voice_util, "hahaha!")

        elif "time" in command:
            time = time_util.get_time()
            speak_and_print(voice_util, "The curent time is {}, {}.".format(time, speech_util.first_name))

        elif ("search" in command or "look up" in command):
            query = command.replace("look up", "")
            query = query.replace("search", "")
            res_data = search_util.get_data_from_search(query)
            links = res_data["link"]
            bestURL = links[0]
            totalMentions = search_util.get_relevant_snippets(res_data, [0])
            page_responses = totalMentions[0]
            if len(page_responses) > 0:
                for i in xrange(min(len(page_responses), 3)):
                    speak_and_print(voice_util, page_responses[i])
            else:
                speak_and_print(voice_util, "I couldn't find a best hint, but here's a link to the most relevant result: ")
                print(bestURL)

        elif "quit" in command or "close" in command:
            speak_and_print(voice_util, "Alright, {}. I'll shut down.".format(speech_util.first_name))
            app_util.kill_app()
            return

        else:
            speak_and_print(voice_util, "I'm sorry, {}. Could you try another command?".format(speech_util.first_name))



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
