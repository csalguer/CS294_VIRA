#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""AlarmUtility

An alarm clock / timer / stopwatch.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import datetime
import multiprocessing
import os
import subprocess
import threading

import config
import voice_util

class AlarmUtility(object):
    """A class representing a basic alarm clock."""

    def __init__(self, vlc_path=None, mp3_path=None):
        self.alarm_time = None
        self._alarm_thread = None
        self.update_interval = 1
        self.event = threading.Event()
        self.vlc_path = vlc_path
        self.mp3_path = mp3_path

        CNFG = config.get_config()
        self.voice_util = voice_util.VoiceUtility(CNFG.VOICE_PATH, CNFG.ALERT_PATH, CNFG.CONFIRM_PATH)
        self.alarm_path = CNFG.ALARM_WAV_PATH

    def run(self):
        while True:
            self.event.wait(self.update_interval)
            if self.event.isSet():
                break

    def vlc_ring(self):
        if not (self.vlc_path and self.mp3_path):
            print "Your alarm is ringing!"
        else:
            with open(os.devnull, 'wb') as devnull:
                subprocess.check_call([self.vlc_path, self.mp3_path],
                                      stdout=devnull,
                                      stderr=devnull)
        self.event.set()

    def ring(self):
        try:
            self.voice_util.play_noise(self.alarm_path)
        except Exception as err:
            self.vlc_ring()
        self.event.set()

    def set_alarm(self, hour, minute):
        now = datetime.datetime.now()
        alarm = now.replace(hour=int(hour), minute=int(minute), second=0)
        delta = int((alarm - now).total_seconds())
        if delta <= 0:
            alarm = alarm.replace(day=alarm.day + 1)
            delta = int((alarm - now).total_seconds())
        if self._alarm_thread:
            self._alarm_thread.cancel()
        self._alarm_thread = threading.Timer(delta, self.ring)
        self._alarm_thread.daemon = True
        self._alarm_thread.start()

    def process_func(self, hour, minute):
        self.set_alarm(hour, minute)
        self.run()

    def start_alarm(self, minutes_from_now=1):
        call_time = datetime.datetime.now()
        alarm_time = call_time.replace(minute=(call_time.minute + minutes_from_now) % 60)
        process = multiprocessing.Process(target=self.process_func,
                                          args=(alarm_time.hour,
                                                alarm_time.minute))
        process.start()


if __name__ == "__main__":
    CNFG = config.get_config()
    ALARM_UTIL = AlarmUtility(CNFG.VLC_PATH, CNFG.ALARM_PATH)
    ALARM_UTIL.start_alarm()
