# -*- coding: utf-8 -*-
"""WeatherUtility

An API for checking the weather through VIRA

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import pyowm

import config


class WeatherUtility(object):
    """docstring for WeatherUtility"""

    def __init__(self):
        _config = config.get_config()
        self.owm = pyowm.OWM(_config.OWM_API_KEY)


def main():
    weather_util = WeatherUtility()
    obs = weather_util.owm.weather_at_place('Stanford, CA')
    w = obs.get_weather()
    print w
    print w.get_wind()
    print w.get_humidity()
    print w.get_temperature('fahrenheit')

if __name__ == '__main__':
    main()
