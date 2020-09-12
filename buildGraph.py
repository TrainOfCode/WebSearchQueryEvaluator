import codecs
import io
import sys
import time

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


class WCFFinder:
    def __init__(self, stemGroups):
        self.groups = stemGroups
    def findWCF(self, wordI, wordJ, stemGroupI, stemGroupJ):

        runningSum = 0
        for i in range(len(stemGroupI.members)):
            for j in range(len(stemGroupJ.members)):
                runningSum += 1/(self.distBetween(stemGroupI.membersPos[i], stemGroupJ.membersPos[j]) + 1)
        denom = (len(stemGroupI.members) * len(stemGroupJ.members))
        WCF = -1.1
        if denom != 0:
            WCF = runningSum / (denom)
        return WCF

    def distBetween(self, ar1, ar2):
        i = 0
        j = 0
        diff = sys.maxsize
        while (i < len(ar1) and j < len(ar2)):
            posDiff = abs(int(ar1[i]) - int(ar2[j]))
            if (posDiff < diff):
                diff = posDiff
            if (int(ar1[i]) < int(ar2[j])):
                i += 1
            else:
                j += 1

        return diff


class stemGroup:
    def __init__(self, stem):
        self.stem = stem
        self.members = []
        self.membersPos = []

    def add(self, newMember, newMemberPosString):
        self.members.append(newMember)
        positions = newMemberPosString.split(" ")
        self.membersPos.append(positions)

    def size(self):
        return len(self.members)

    def getStem(self):
        return self.stem

    def toPrint(self):
        line = self.stem + " : "
        for word in self.members:
            line += word + " "
        line += "\n"
        return line

dictionaryWiki = open("dictionary.txt", "r")
ps = PorterStemmer()

stemGroups = []

listOfAllWords = []
listOfAllWordsStem = []
startTime = time.time()
n = 1
i = 0
numLines = file_len("dictionary.txt")

stemWordsSeen = set()
alreadySeen = False

for line in dictionaryWiki:
    words = line.split(" : ")
    listOfAllWords.append(words[0])
    groupToAdd = -1
    if words[2] in stemWordsSeen:
        alreadySeen = True
    if alreadySeen:
        for i in range(len(stemGroups)):
            if stemGroups[i].getStem() == words[2]:
                groupToAdd = i
                break
    if groupToAdd == -1:
        newStemGroup = stemGroup(ps.stem(words[0]))
        newStemGroup.add(words[0], words[1])
        stemGroups.append(newStemGroup)
        listOfAllWordsStem.append(newStemGroup)
    else:
        stemGroups[groupToAdd].add(words[0], words[1])
        listOfAllWordsStem.append(newStemGroup)
    i += 1
    alreadySeen = False
    if time.time() - startTime > (600 * n):
        n += 1
        print('{:3.5f} minutes since starting'.format((time.time() - startTime)/60))
        print('{:3.5f} % percent finished'.format((i/numLines * 100)))
        print(str(i) + " out of " + str(numLines))
        print()

WCF = WCFFinder(stemGroups)

print("Finding WCFS")
output_file = codecs.open("graph.txt", 'w', 'utf-8')
output = io.StringIO()
n = 1

WCFG = [[-1 for x in range(len(listOfAllWords))] for y in range(len(listOfAllWords))]

for i in range(len(listOfAllWords)):
    output.write(listOfAllWords[i])
    for j in range(len(listOfAllWords)):
        if time.time() - startTime > (600 * n):
            n += 1
            print('{:3.5f} minutes since starting'.format((time.time() - startTime)/60))
            print('{:3.5f} % percent finished'.format((i/len(listOfAllWords) * 100)))
            print(str(i) + " out of " + str(len(listOfAllWords)))
            print()

        if i == j:
            WCFG[i][j] = -2
        elif WCFG[j][i] == -1:
            WCFG[i][j] = WCF.findWCF(listOfAllWords[i], listOfAllWords[j], listOfAllWordsStem[i], listOfAllWordsStem[j])
        else:
            WCFG[i][j] = WCFG[j][i]

        output.write(" " + str(WCFG[i][j]))

    output.write('\n')
    output_file.write(output.getvalue())
    output = io.StringIO()
output_file.close()
