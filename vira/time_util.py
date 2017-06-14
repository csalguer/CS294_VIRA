# -*- coding: utf-8 -*-
"""TimeUtility

A clock.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import datetime


class TimeUtility(object):
    """Basic class to tell the time"""

    def get_time(self):
        """Returns the time, already formatted."""
        now = datetime.datetime.now()
        hour = 12 if now.hour % 12 == 0 else now.hour % 12
        meridiem = "AM" if now.hour < 12 else "PM"
        return "%d:%02d %s" % (hour, now.minute, meridiem)


def main():
    """Prints the time."""
    time_util = TimeUtility()
    print "The time is " + time_util.get_time() + "."


if __name__ == "__main__":
    main()
