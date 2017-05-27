VIRA
====
A virtual assistant for VR-enabled operating systems.

Installation
============
```
    git clone https://github.com/csalguer/CS294_VIRA.git
    cd CS294_VIRA

    # only if on mac (requires homebrew installation)
    brew install portaudio
    pip install pyobjc
    pip install pyaudio

    # only if on linux (or linux on windows)
    sudo apt-get install python-pyaudio

    # for mac, windows, and linux
    pip install -r requirements.txt

    # put on your VR headset with microphones + headphones
    python demo.py
```

Notes
=====
Designed to run with Python 2, version 2.7.11 or later
