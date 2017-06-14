#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""JokeUtility

An API that allows VIRA to tell jokes.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import random


class JokeUtility(object):
    """A class for telling jokes.
       Compiled with material from OneLineFun (onelinefun.com)."""
    _jokes = [("Today a man knocked on my door and asked for a small"
               " donation towards the local swimming pool. I gave him"
               " a glass of water."),
              ("Team work is important; it"
               " helps to put the blame on someone else."),
              ("All pro athletes are bilingual."
               " They speak English and profanity."),
              ("Relationships are a lot like algebra."
               " Have you ever looked at your X and wondered Y?"),
              "I used to think I was indecisive, but now I'm not too sure."]

    def __init__(self):
        random.seed()
        self.jokes = list(JokeUtility._jokes)

    def get_joke(self):
        """Returns a single, randomly chosen joke.
           Will repeat jokes upon running out."""
        if not self.jokes:
            self.__init__()
        index = random.randint(0, len(self.jokes) - 1)
        joke = self.jokes.pop(index)
        return joke


def main():
    """Demonstrates how to use the joke_util module."""
    joke_util = JokeUtility()
    for i in xrange(7):
        print "{}. ".format(i + 1) + joke_util.get_joke()


if __name__ == '__main__':
    main()
