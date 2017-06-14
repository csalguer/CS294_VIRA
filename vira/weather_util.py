# -*- coding: utf-8 -*-
"""WeatherUtility

An API for checking the weather through VIRA.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import pyowm

import config


class WeatherUtility(object):
    """Allows us to check the weather."""

    def __init__(self):
        _config = config.get_config()
        self.owm = pyowm.OWM(_config.OWM_API_KEY)

    def get_weather(self, location='Stanford, CA'):
        """Returns the weather at the desired location."""
        obs = self.owm.weather_at_place(location)
        weather = obs.get_weather()
        w_status = weather.get_detailed_status()
        w_temp = weather.get_temperature('fahrenheit')
        w_temp_h = int(w_temp["temp_max"])
        w_temp_l = int(w_temp["temp_min"])
        w_humid = weather.get_humidity()
        w_wind = int(weather.get_wind()["speed"])
        result = ("the weather today is best characterized as {}.\n"
                  "The humidity is {}%, and the wind speed is {};\n"
                  "the high is {}, and the low is {}.\n"
                  "It's a great day for gaming.\n"
                 )
        return result.format(w_status, w_humid, w_wind, w_temp_h, w_temp_l)


def main():
    """Tests the weather utility."""
    weather_util = WeatherUtility()
    weather_msg = weather_util.get_weather()
    print weather_msg


if __name__ == '__main__':
    main()
