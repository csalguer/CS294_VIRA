# -*- coding: utf-8 -*-
"""AlarmUtility

ASR system based on Google Speech Recognition.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import os
import sys
import time

class AlarmUtility(object):
    """A basic alarm clock"""

# A simple python alarm clock
# example: python alarm.py [time in 24h with :] [music file]
# example: python alarm.py "6:30" "Trollenn.mp3" 
import time, os, sys

ctime = time.strftime("%H:%M")
print(ctime)

while ctime != sys.argv[1]:
 ctime = time.strftime("%H,%M")

os.system("mpv " + sys.argv[2])