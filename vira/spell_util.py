# -*- coding: utf-8 -*-
"""SpellUtility

Spelling corrector based on Levenshtein distance
and a system-specific language model.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

import collections


class SpellUtility(object):
    """Spelling corrector."""

    def __init__(self, app_names):
        self.app_names = dict()
        for name in app_names:
            self.app_names[name.lower()] = name
        self.distances = collections.defaultdict(lambda: 10)

    def levenshtein(self, string_1, string_2):
        if not string_2:
            return len(string_1)

        # ensure len(string_1) >= len(string_2)
        if len(string_1) < len(string_2):
            return self.levenshtein(string_2, string_1)

        previous_row = range(len(string_2) + 1)
        for i, char1 in enumerate(string_1):
            current_row = [i + 1]
            for j, char2 in enumerate(string_2):
                # use j+1 instead of j since previous_row and current_row
                # are one character longer than string_2
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (char1 != char2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def get_distances(self, word):
        for name in self.app_names:
            self.distances[name] = self.levenshtein(word, name)

    def get_closest_name(self, word):
        self.get_distances(word)
        name = min(self.distances, key=self.distances.get)
        return self.app_names[name] if self.distances[name] < 10 else ""


def main():
    app_names = ["FEZ", "Super Meat Boy"]
    spell_util = SpellUtility(app_names)
    input_string = raw_input('Enter a word: ')
    print spell_util.get_closest_name(input_string.lower())


if __name__ == "__main__":
    main()
