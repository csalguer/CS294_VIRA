# -*- coding: utf-8 -*-
"""Config

Stores configuration constants for various operating systems.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""


class Windows(object):
    """Configuration variables for Windows 10"""
    APP_DATA_DIR = r'D:\SteamLibrary\steamapps\common'
    APP_EXTENSION = ".exe"


class Mac(object):
    """Configuration variables for macOS 10.12"""
    APP_DATA_DIR = r'/Users/mchenja/Library/Application Support/Steam/steamapps/common'
    APP_EXTENSION = ".app"
