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
import signal


class SteamUtility(object):
    """Class for manipulating Steam games"""

    def __init__(self, apps_dir_path):
        self.apps_dir_path = apps_dir_path
        self.app_process = None

    def get_all_apps(self):
        for _, dirnames, _ in os.walk(self.apps_dir_path):
            return dirnames

    def get_app_executable_path(self, app_dir, extension, app_path=None):
        if app_path is None:
            app_path = os.path.join(self.apps_dir_path, app_dir)

        for (dirpath, dirnames, filenames) in os.walk(app_path):
            for filename in filenames:
                if filename.endswith(extension):
                    self.APPNAME = filename.split('.')[0]
                    return os.path.join(dirpath, filename)

            for dirname in dirnames:
                if dirname.endswith(extension):
                    self.APPNAME = dirname.split('.')[0]
                    return os.path.join(dirpath, dirname)

            return None

    def spawn_app(self, app, extension):
        exec_path = self.get_app_executable_path(app, extension)
        try:
            self.app_process = subprocess.Popen(['exec', exec_path])
            print self.app_process
        except OSError as err:
            try:
                self.app_process = subprocess.Popen(["/usr/bin/open", exec_path])
                print "[Popen OBJ]: ", self.app_process
                print "[PID]: ", self.app_process.pid
            except:
                print "Original error:\n{}".format(err)
                print "==============================="
                print "There is another error:"
                raise

    def kill_app(self):
        assert self.app_process is not None
        try:
            # WINDOWS specific implementation for killing
            print("<WINDOWS> Closing {}".format(self.APPNAME))
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.app_process.pid)])
        except OSError as err:
            # MAC Specific implementation for killing app
            print "<WINDOWS FAILED> Kill command not recognized"
            print "\tSwitching to different OS kill cmd..."
            print "<MAC> Closing {}".format(self.APPNAME)
            subprocess.Popen(['killall', self.APPNAME])
            


def main():
    import config
    apps_dir_path = config.get_config().APP_DATA_DIR
    steam_util = SteamUtility(apps_dir_path)
    apps = steam_util.get_all_apps()
    print "Available Steam applications:"
    for num, elem in enumerate(apps, start=1):
        print "    {}. {}".format(num, elem)
    #     steam_util.spawn_app(elem, config.Mac.APP_EXTENSION)
    # print "Waiting for enter to kill process: [PRESS ENTER]"
    # print "================================================"
    # raw_input()
    # steam_util.kill_app()



if __name__ == "__main__":
    main()
