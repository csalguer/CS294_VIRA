#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""Config

Stores configuration constants for various operating systems.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import os
import sys

_cwd = os.path.dirname(os.path.realpath(__file__))

class _Config(object):
    """Configuration variables that are not OS-specific"""
    ALARM_PATH = os.path.join(_cwd, "audio_files", "alarm.mp3")
    ALARM_WAV_PATH = os.path.join(_cwd, "audio_files", "alarm.wav")
    ALERT_PATH = os.path.join(_cwd, "audio_files", "alert.wav")
    APP_DATA_DIR = None
    APP_EXTENSION = None
    CONFIRM_PATH = os.path.join(_cwd, "audio_files", "confirm.wav")
    GOOGLE_CREDENTIALS = r"""{
                              "type": "service_account",
                              "project_id": "pac2text",
                              "private_key_id": "43a5e4cfc4f61e777910d053ccb249c47e928198",
                              "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDD4OAxtLagWeQ+\nhQ7NgOt+Xdd2kBPv41QrIR8Uq4pWmq4xzrIRiQc4f59A8QirJ86B4/LKxcVLJoDf\nV7cWdfA9iwkPxeQeOulh5BbM8Wwksej3matdpd9ZZgvtU4D7LuZmwgnIrFjRSwPR\nyQDZYK1Wq1wgjUusJmfLQ2OMxYQS7z0gHLKuDIag2SC5eOVwZ8y+Duzv3CLFMhhc\njOTCoNTmXvAbrZCmIrYRPqxuhV92t+k3lcl9GxOA/kEaw+sjxPo03MFm7FtGUyaM\n02xcAj16Z18CeFEN3hTWLWvsjmtC96vy6TQn3Sza2S1mILzCrqOm7gk8lwHvHo+U\nMm15Fge1AgMBAAECggEAB1l5sAPC0nNs//eIHafXri8hNX6kcNzLvK6KdwEUuLkn\nDhFeVxAYKEOJmyswExP0SKVf58HR7EbukPK+mOYl9HkyBth6/bNiLF0dieUJFLtk\nLV4jsujVX4pXqjj23vXciUCAk3n7/yZcZ1OuZ3mcJ2NYmpQSocvzGwpVQuPqV7d3\nbAoVpix2rUYuq+OZO4IeAB2YbpPAnLoGVLywYlS/8IS7B9T21MqT1xzKpgJ/elR1\nFFgvjyQN+7ECuMt8ZMQHaWE+5UDZ2xEjxjeJHUQPm0LrYrQzhdkbcb5+wC+NIYVQ\nNYi/oTYahabR0HhjR2g8JJ6ZdLyqTQu1GU89TXVU5QKBgQDzPE1Yo9vXXtGifg25\n26ivywFVMgaTnY5vepIDzQ1yxAa7ZBxBmrdFY+NFgWv84MwjJYSjRPhTCYX+GHLx\n4YzuIyrioVxznFF5Fc4ATveQ5jdoWtZgRjKt1VEW7L66tyzp4Ko2Jw4265LhRYpQ\neFMcNtFeYWx3C6awfnlNYnbSXwKBgQDOKF0tqcZoE2dhswKHmc+3oPRXfUS55KHH\nnoQvCaeNT4+9+eJxh5PEnrdajt3jl7KTfro6zGzCXfbQMumt9n0n7WWii7RvbbqW\nu33W/WhHqk62QGauCsDRaqPatNKSWPD+XYUkvDq9U2PrYaI2l6fi9qU/lyvkWMve\n+p648w4mawKBgBbr994CkxUYumi1uFVrfdoTJ2z/6d6/WkznIBt7l2jZUEkYhhEo\no1zGrQQ/zg1modYuEvHP7hblLttjMnHY748BgWkaC7xZXtQqWd9tkab2CwKqjMlF\n1EDNeXbPmKm/2Vuw8FlqFMzYJl9UTlSHAk4GXHSoebA+SNcZFBVW0hvBAoGAUyZC\nlsVQKfARlX0++vRVrEm144e57YRCoCHWTKaHNt6tKkGcTJATUI13hIX1BvPLaeQG\nNur2vtppTwYJ7Elrp2v/vzS73OmUBXGvysPAiI8vWiDViUL7DDwHxJGEENTgtqd/\nqRZmVrBIr8pcQ8qdQ1SZx/EwGdSavd+1nwEhZusCgYEA1SlFw2uZGNvNnV07rWgD\naievVSrW3UBEEYiyOEq1JIEaOFRdxJjbfrU5GeOJiTo57SYVFm51K8n/g1n2xPY0\ngSO51FxYlcG5db9AaBiA+SPgzitbuEXj4CBxHC0kvC2LoKA+/tEkfIqcuj8T9Try\na8C5ijEftpuQR8cBS4AnsKQ=\n-----END PRIVATE KEY-----\n",
                              "client_email": "matt-415@pac2text.iam.gserviceaccount.com",
                              "client_id": "108600580804135879328",
                              "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                              "token_uri": "https://accounts.google.com/o/oauth2/token",
                              "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                              "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/matt-415%40pac2text.iam.gserviceaccount.com"
                              }
                           """
    OWM_API_KEY = '572e5d5ca97f536750ce07827fc53fa6'
    SEARCH_CREDENTIAL_PATH = os.path.join(_cwd, "config_files", "search.json")
    VLC_PATH = None
    VOICE_PATH = os.path.join(_cwd, "audio_files", "output.mp3")


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
