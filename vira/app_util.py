#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""ApplicationUtility

System-related methods for manipulating games (and, in future
implementations, other applications) that have already been installed
on the system.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import os
import subprocess


class AppUtility(object):
    """A class for manipulating installed games."""

    def __init__(self, apps_dir_path):
        self.apps_dir_path = apps_dir_path
        self.app_name = None
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
                    self.app_name = filename.split('.')[0]
                    return os.path.join(dirpath, filename)

            # reach here if no files ended with the desired extension
            for dirname in dirnames:
                if dirname.endswith(extension):
                    self.app_name = dirname.split('.')[0]
                    return os.path.join(dirpath, dirname)

            return None

    def spawn_app(self, app, extension):
        exec_path = self.get_app_executable_path(app, extension)
        try:
            # is this Windows specific? need to ask Chris
            self.app_process = subprocess.Popen(['exec', exec_path])
        except OSError:
            # macOS / Linux specific
            self.app_process = subprocess.Popen(["/usr/bin/open", exec_path])

    def kill_app(self):
        assert self.app_process
        try:
            # windows specific
            subprocess.call(['taskkill', '/F', '/T', '/PID',
                             str(self.app_process.pid)])
        except OSError:
            # this seems to be macOS / Linux specific
            # TODO: non-Pangemic apps are not named "main"
            app_name = self.app_name
            if app_name == "pangemic":
                app_name = "main"
            with open(os.devnull, 'wb') as devnull:
                subprocess.Popen(['/usr/bin/killall', app_name],
                                 stdout=devnull,
                                 stderr=subprocess.STDOUT)


def main():
    import config
    CNFG = config.get_config()
    steam_util = AppUtility(CNFG.APP_DATA_DIR)
    apps = steam_util.get_all_apps()
    print "Available Steam applications:"
    for num, elem in enumerate(apps, start=1):
        print "    {}. {}".format(num, elem)
    steam_util.spawn_app(apps[0], CNFG.APP_EXTENSION)
    print "Waiting for enter to kill process: [PRESS ENTER]"
    print "================================================"
    raw_input()
    steam_util.kill_app()


if __name__ == "__main__":
    main()
