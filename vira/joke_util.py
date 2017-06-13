# -*- coding: utf-8 -*-
"""JokeUtility

An API for getting jokes from VIRA

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""


class JokeUtility(object):
    """docstring for JokeUtility"""

    def get_joke(self):
        return "All pro athletes are  bilingual. They speak English and profanity."

def main():
    print JokeUtility().get_joke()

if __name__ == '__main__':
    main()
