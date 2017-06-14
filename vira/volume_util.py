# -*- coding: utf-8 -*-
"""VolumeUtility

Allows the user to change the volume.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import osax

class VolumeUtility(object):
    """Changes the volume.
       Currently only tested on OS X.
    """

    def __init__(self):
        self.sa = osax.OSAX()
        self.original_volume = list(self.sa.get_volume_settings().iteritems())[2][1]

    def minimize_volume(self, low_setting=0.05):
        self.sa.set_volume(low_setting)

    def restore_volume(self, coefficient=14.3):
        self.sa.set_volume(self.original_volume / coefficient)


def main():
    """Changes the volume. Run this with music in the background."""
    import time
    vol_util = VolumeUtility()
    vol_util.minimize_volume()
    time.sleep(2)
    vol_util.restore_volume()


if __name__ == "__main__":
    main()
