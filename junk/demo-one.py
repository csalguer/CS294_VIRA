#!/usr/bin/env python2

import os
import speech_recognition as sr
import subprocess
import sys

class SteamUtility(object):
    """docstring for SteamUtility"""
    def __init__(self, appsPathname):
        super(SteamUtility, self).__init__()
        self.appsPathname = appsPathname
        self.appNames = []
        

    def spawnApp(self, gameDir):
        execPath = self.getAppExecutablePath(gameDir)
        print(execPath)
        subprocess.call([execPath])


    def getAllAppPaths(self):
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
    # Used for voice recognition
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What is your name?")
        print("Listening for audio...", end='\r')
        audio = r.listen(source)
        print("Analyzing your speech...", end='\r')
        name = r.recognize_google(audio).title()

    print("                            ", end='\r')
    print("Hi, {}".format(name))
    
    ###

    # print("{}, would you like to change the volume?".format(name))
    # print("Indicate ")



    # appDataDir = 'D:\SteamLibrary\steamapps\common'
    # stmUtil = SteamUtility(appDataDir)
    # appPaths = stmUtil.getAllAppPaths()
    # apps = stmUtil.getAllApps()


    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        result = r.recognize_google(audio)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said {}".format(result))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # if result == "tilt brush":
    #     stmUtil.spawnApp("Tilt Brush")  
    # print(appPaths)
    # print(apps)
    # stmUtil.spawnApp("Tilt Brush")
if __name__ == "__main__":
    main()