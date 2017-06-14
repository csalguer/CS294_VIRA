VIRA
====
A virtual assistant for games

Installation
============
```
    ### Mac OS X only 
    # Requires homebrew - https://brew.sh
    brew install portaudio
    pip install pyobjc
    pip install appscript
    ####

    ### (Windows Subsystem for) Linux only
    sudo apt-get install gcc portaudio19-dev python-all-dev
    ####

    git clone https://github.com/vira-assistant/vira.git
    cd vira
    pip install -r requirements.txt

    # put on your (optional VR headset with) microphone + headphones
    python demo.py
```

Usage
=====
VIRA requires at least one Steam game be installed to function properly.
We recommend [panGEMic](http://store.steampowered.com/app/547540/panGEMic/) be used when testing VIRA because it is lightweight and loads quickly.

VIRA works best with a high-speed internet connection.

VIRA won't work if headphones and a microphone are not being used.

Example commands:
- "VIRA, what's the weather like outside?"
- "VIRA, please set an alarm to go off in three minutes."
- "VIRA, tell me a joke."
- "VIRA, what time is it?"
- "VIRA, search Mario."

Warnings
========
If working with a slow internet connection, there may be a lag between when you say "VIRA" and
when you hear the audible confirmation that VIRA is listening for a command. Wait for the confirmation
noise before speaking your command!

VIRA does not currently work on Windows or Linux due to [this issue](https://github.com/TaylorSMarks/playsound/issues/1#issuecomment-304482654). The fix has not yet been installed, and the workaround is hacky, so we are waiting for the fix to be installed before continuing cross-platform development.

Contributing to VIRA
====================
Anyone can submit a [pull request](https://github.com/vira-assistant/vira/pulls) to customize this baseline implementation of VIRA. Please ensure that your code confirms to PEP8 before submission; run
both Pylint and flake8 on it. (These tools are stricter than is necessary to confirm to PEP8, which
is why you will notice they report issues with the pre-existing code even though they have been
continually used during development.)

Notes
=====
Designed to run with Python 2, version 2.7.11 or later
