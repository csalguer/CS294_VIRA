import collections

class SpellCorrector(object):
    
    def __init__(self, appNames):
        self.appNames = [name.lower() for name in appNames]
        self.distances = collections.defaultdict(lambda: 0)


    def levenshtein(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

    def getDistances(self, word):
        for name in self.appNames:
            self.distances[name] = self.levenshtein(word, name)
            print name, self.distances[name]

    def getClosestName(self, word):
        self.getDistances(word)
        name = min(self.distances, key=self.distances.get)
        print
        print name
        return name

def main():
    print "Woop"
    appNames = ["paint", "steam", "tilt brush"]
    sp = SpellCorrector(appNames)
    name = sp.getClosestName("eight")

if __name__ == "__main__":
    main()


