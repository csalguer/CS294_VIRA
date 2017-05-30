VIRA
====
A virtual assistant for VR-enabled operating systems.

Installation
============
```
    ############ Mac OS X only ############
    # Requires homebrew - https://brew.sh
    brew install portaudio
    pip install pyobjc
    ##########################################

    ########### (Windows Subsystem for) Linux only ###########
    sudo apt-get install gcc portaudio19-dev python-all-dev
    ##########################################################

    git clone https://github.com/csalguer/CS294_VIRA.git
    cd CS294_VIRA
    pip install -r requirements.txt

    # put on your VR headset with microphones + headphones
    python demo.py
```

Notes
=====
Designed to run with Python 2, version 2.7.11 or later
