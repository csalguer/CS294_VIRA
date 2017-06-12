# -*- coding: utf-8 -*-
"""AlarmUtility

An alarm clock / timer / stopwatch.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import datetime
import sys
import threading
import subprocess
import multiprocessing


class AlarmUtility(object):
    """A basic alarm clock"""

    def __init__(self):
        self.alarm_time = None
        self._alarm_thread = None
        self.update_interval = 1
        self.event = threading.Event()

    def run(self):
        while True:
            self.event.wait(self.update_interval)
            if self.event.isSet():
                break
            now = datetime.datetime.now()
            if self._alarm_thread and self._alarm_thread.is_alive():
                alarm_symbol = '+'
            else:
                alarm_symbol = ' '
            # sys.stdout.write("\r%02d:%02d:%02d %s" 
            #     % (now.hour, now.minute, now.second, alarm_symbol))
            sys.stdout.flush()

    def ring(self):
        self.event.set()
        path = '/Applications/VLC.app/Contents/MacOS/VLC'
        mp3 = '/Users/Ikechi/Developer/cs294w/CS294_VIRA/vira/alarm.mp3'
        subprocess.call([path, mp3])


    def set_alarm(self, hour, minute):
        now = datetime.datetime.now()
        alarm = now.replace(hour=int(hour), minute=int(minute), second = 0)
        delta = int((alarm - now).total_seconds())
        if delta <= 0:
            alarm = alarm.replace(day=alarm.day + 1)
            delta = int((alarm - now).total_seconds())
        if self._alarm_thread:
            self._alarm_thread.cancel()
        self._alarm_thread = threading.Timer(delta, self.ring)
        self._alarm_thread.daemon = True
        self._alarm_thread.start()


def process_func(hour, minute):
    alarm = AlarmUtility()
    alarm.set_alarm(hour, minute)
    alarm.run()

def start_alarm():
    call_time = datetime.datetime.now()
    alarm_time = call_time.replace(minute=(call_time.minute+3)%60)
    p = multiprocessing.Process(target=process_func, args=(alarm_time.hour, alarm_time.minute))
    p.start()

if __name__ == "__main__":
    start_alarm()
    
