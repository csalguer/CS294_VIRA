# -*- coding: utf-8 -*-
"""Config

Stores configuration constants for various operating systems.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import os
import sys


class _Config(object):
    """Configuration variables that are not OS-specific"""
    ALARM_PATH = os.path.join('audio_files', 'alarm.mp3')
    APP_DATA_DIR = None
    APP_EXTENSION = None
    OWM_API_KEY = '572e5d5ca97f536750ce07827fc53fa6'
    VLC_PATH = None


class _Mac(_Config):
    """Configuration variables for macOS 10.12"""
    APP_DATA_DIR = os.path.expanduser(r'~/Library/Application Support/Steam/steamapps/common')
    APP_EXTENSION = ".app"
    VLC_PATH = '/Applications/VLC.app/Contents/MacOS/VLC'


class _Windows(_Config):
    """Configuration variables for Windows 10"""
    APP_DATA_DIR = r'D:\SteamLibrary\steamapps\common'
    APP_EXTENSION = ".exe"


class _Linux(_Config):
    """Configuration variables for Linux (i.e., Linux on Windows)"""
    APP_DATA_DIR = r'/mnt/d/SteamLibrary/steamapps/common'
    APP_EXTENSION = ".exe"


def get_config():
    """Returns a configuration variable for the given system"""
    platform = sys.platform
    if platform == 'darwin':
        return _Mac()
    if platform == 'win32':
        return _Windows()
    if platform == 'linux2':
        return _Linux()
    return _Config()
