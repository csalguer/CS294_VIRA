import vira
import sys


def main():
    print "VIRA is loading...", '\r',
    sys.stdout.flush()

    apps_dir_path = vira.config.Mac.app_data_dir
    steam_util = vira.steam_utility.SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()

    spell_corr = vira.spell_corrector.SpellCorrector(apps)
    sys.stdout.write("\033[K")  # clear line

    speech_util = vira.speech_utility.SpeechUtility()
    speech_util.get_name()
    speech_util.print_hello()
    print

    print "{}, the following applications are available:".format(speech_util.first_name)
    for app in apps:
        print "    - {}".format(app)
    print

    app = speech_util.get_app(spell_corr)
    print "Sounds good, {}. Opening {}...".format(speech_util.first_name, app)
    steam_util.spawn_app(app, vira.config.Mac.extension)





    # print "Available Steam applications:"
    # for num, elem in enumerate(apps, start=1):
    #     print "    {}. {}".format(num, elem)

    # def main():
    # appNames = ["FEZ", "Super Meat Boy"]
    # sp = SpellCorrector(appNames)
    # s = raw_input('Enter a word: ')
    # name = sp.getClosestName(s.lower())
    # print name

    

    # vira.steam_utility.main()
    # vira.speech_utility.main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
