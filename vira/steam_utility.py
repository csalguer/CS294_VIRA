# -*- coding: utf-8 -*-
"""SteamUtility

CS294W, Spring 2016-2017.
"""

import os
import subprocess


class SteamUtility(object):
    """Class for manipulating Steam games"""

    def __init__(self, apps_dir_path):
        self.apps_dir_path = apps_dir_path

    def get_all_apps(self):
        for dirpath, dirnames, filenames in os.walk(self.apps_dir_path):
            return dirnames


def main():
    import config
    apps_dir_path = config.Mac.app_data_dir
    steam_util = SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()
    print "Available Steam applications:"
    for num, elem in enumerate(apps, start=1):
        print "    {}. {}".format(num, elem)


if __name__ == "__main__":
    main()
