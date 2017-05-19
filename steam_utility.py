from __future__ import print_function
import sys
import os
import subprocess



class SteamUtility(object):
    """docstring for SteamUtility"""
    def __init__(self, appsPathname):
        super(SteamUtility, self).__init__()
        self.appsPathname = appsPathname
        self.appNames = []
        

    def spawnApp(self, gameDir):
        execPath = gameDir + self.getGameExecutablePath(gameDir)
        subprocess.run(["start", appsPathname+gameDir])


    def getAllAppPaths(self):
        # dirs = [d for d in os.listdir(self.appsPathname) if os.path.isdir(os.path.join(self.appsPathname, d))]
        # return dirs
        d = []
        for (dirpath, dirnames, filenames) in os.walk(self.appsPathname):
            d.extend(dirnames)
            break
        dPaths = [os.path.join(dirpath, dirName) for dirName in d ]
        return dPaths

    def getAllApps(self):
        a = []
        for (dirpath, dirnames, filenames) in os.walk(self.appsPathname):
            a.extend(dirnames)
            break
        return a

    def getAppExecutablePath(self, appDir, appPath=None):
        # dirItems = os.listdir(self.appsPathname)
        # for file in dirItems:
        #     if file.split(".")[1] == 'exe'
        #         return self.appsPathname + "\\" + gameDir + "\\" + file
        # return None
        f = []
        if appPath is None:
            appPath =  os.path.join(self.appsPathname, appDir)
        for (dirpath, dirnames, filenames) in os.walk(appPath):
            f.extend(filenames)
            break
        for file in f:
            if file.endswith('.exe'):
                return os.path.join(dirpath, file)
        return None



def main():
    appDataDir = 'C:\Program Files (x86)\Steam\steamapps\common'
    stmUtil = SteamUtility(appDataDir)
    appPaths = stmUtil.getAllAppPaths()
    apps = stmUtil.getAllApps()


    print(appPaths)
    print(apps)
    for app in apps:
        print(stmUtil.getAppExecutablePath(app))
if __name__ == "__main__":
    main()