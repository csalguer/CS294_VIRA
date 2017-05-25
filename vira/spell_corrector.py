import collections

class SpellCorrector(object):
    
    def __init__(self, appNames):
        self.appNames = dict()
        for name in appNames:
            self.appNames[name.lower()] = name
        self.distances = collections.defaultdict(lambda: 10)


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
            #print name, self.distances[name]

    def getClosestName(self, word):
        self.getDistances(word)
        name = min(self.distances, key=self.distances.get)
        #print
        return self.appNames[name] if self.distances[name] < 10 else ""

def main():
    appNames = ["FEZ", "Super Meat Boy"]
    sp = SpellCorrector(appNames)
    s = raw_input('Enter a word: ')
    name = sp.getClosestName(s.lower())
    print name

if __name__ == "__main__":
    main()


