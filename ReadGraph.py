import codecs
import io
import time
import sys

def askQuestion():
    print()
    print("If you would like to exit, type -1")
    print("Type in two words seperated by a : to find the WCF between the two words, i.e. red : blue")
    print("Type in one word followed by space, : , and a space and then a number (default 3) and you will be given the closest words ranked by WCF of the given word i.e ground : 5")
    print()
    response = input()
    return response.split(" : ")


def findIndexOf(word, WCF):
    index = 0
    for row in WCF:
        if row[0] == word:
            return index
        index += 1
    return -1

def findClosest(currRow, ignoreThese):
    max = -5
    maxIndex = -1
    for i in range(len(currRow)):
        if i in ignoreThese:
            continue
        elif float(currRow[i]) >= max:
            max = float(currRow[i])
            maxIndex = i
    return maxIndex

def findClosestThree(currRow):
    topThree = []
    topThree.append(findClosest(currRow, topThree))
    topThree.append(findClosest(currRow, topThree))
    topThree.append(findClosest(currRow, topThree))
    return topThree

print("loading ... ")

WCF = []
graph = open("graph.txt", "r")
for line in graph:
    WCF.append(line.split())

print("loaded")

response = ""
while response != '-1':
    responses = askQuestion()
    response = responses[0]
    print("Your input:", responses)
    if response == '-1':
        break
    elif len(responses) == 2:
        wordA = responses[0].lower()
        wordB = responses[1].lower()

        indexOfA = findIndexOf(wordA, WCF)
        print("index of " + wordA + " is " + str(indexOfA))
        indexOfB = findIndexOf(wordB, WCF)
        print("index of " + wordB + " is " + str(indexOfB))

        if indexOfA == -1:
            print(wordA + " was not found in the database")
        elif indexOfB == -1:
            print(wordB + " was not found in the database")
        else:
            print("WCF between " + wordA + " and " + wordB + " is " + str(WCF[indexOfA][indexOfB + 1]))
    elif len(responses) == 1:
        word = responses[0].lower()
        index = findIndexOf(word, WCF)
        if index == -1:
            print("sorry, " + word + " was not found, thus no suggestions can be made")
        else:
            CurrRow = WCF[index][1:]
            topThree = findClosestThree(CurrRow)
            for i in topThree:
                print(WCF[i][0])


print("closing ..")
graph.close()
print("closed")
