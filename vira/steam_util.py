# -*- coding: utf-8 -*-
"""SteamUtility

System-related methods for manipulating Steam games
that have already been installed on the system.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
Cstring_294W, Spring 2016-2017.
© Stanford University.
"""

import os
import subprocess


class SteamUtility(object):
    """Class for manipulating Steam games"""

    def __init__(self, apps_dir_path):
        self.apps_dir_path = apps_dir_path

    def get_all_apps(self):
        for _, dirnames, _ in os.walk(self.apps_dir_path):
            return dirnames

    def get_app_executable_path(self, app_dir, extension, app_path=None):
        if app_path is None:
            app_path = os.path.join(self.apps_dir_path, app_dir)

        for (dirpath, dirnames, filenames) in os.walk(app_path):
            for filename in filenames:
                if filename.endswith(extension):
                    return os.path.join(dirpath, filename)

            for dirname in dirnames:
                if dirname.endswith(extension):
                    return os.path.join(dirpath, dirname)

            return None

    def spawn_app(self, app, extension):
        exec_path = self.get_app_executable_path(app, extension)
        try:
            subprocess.call([exec_path])
        except OSError as err:
            try:
                subprocess.call(["/usr/bin/open", exec_path])
            except:
                print "Original error:\n{}".format(err)
                print "==============================="
                print "There is another error:"
                raise


def main():
    import config
    apps_dir_path = config.Mac.APP_DATA_DIR
    steam_util = SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()
    print "Available Steam applications:"
    for num, elem in enumerate(apps, start=1):
        print "    {}. {}".format(num, elem)


if __name__ == "__main__":
    main()
