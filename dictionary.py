import codecs
import io
import time

from nltk.stem import PorterStemmer

stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def parseLine(line):
    words = line.split()
    for i in range(len(words)):
        words[i] = words[i].replace('(','')
        words[i] = words[i].replace(')','')
        words[i] = words[i].replace('[','')
        words[i] = words[i].replace(']','')
        words[i] = words[i].replace('/','')
        words[i] = words[i].replace(',','')
        words[i] = words[i].replace(':','')
        words[i] = words[i].replace(';','')
        if words[i].find('http') != -1:
            words[i] = ''
        if words[i].find('.') != -1:
            words[i] = ''
        if words[i].find('}') != -1:
            words[i] = ''
        if words[i].lower() in stop_words:
            words[i] = ''
    return words

print("name of file that you would like to build a dictionary from")
filename = input()
wikipediaText = open(filename, "r")
startTime = time.time()
wikipediaDictionary = {}
index = -1
print("loading")
numLines = file_len(filename)
print("loaded")
n = 0
i = -1
for line in wikipediaText:
    i += 1
    if time.time() - startTime > (600 * n):
        n += 1
        print('{:3.5f} minutes since starting'.format((time.time() - startTime)/60))
        print('{:3.5f} % percent finished'.format(((i/numLines) * 100)))
        print(str(i) + " out of " + str(numLines))
        print()

    for word in parseLine(line):
        index += 1
        if word == '':
            word += " "
        elif word.lower() not in wikipediaDictionary:
            wikipediaDictionary[word.lower()] = str(index)
        else:
            prevPos = wikipediaDictionary[word.lower()]
            wikipediaDictionary[word.lower()] = prevPos + " " + str(index)


ps = PorterStemmer()

output_file = codecs.open("dictionary.txt", 'w+', 'utf-8')
output = io.StringIO()
for word in wikipediaDictionary:
    output.write(word)
    output.write(" : ")
    output.write(wikipediaDictionary[word])
    output.write(" : ")
    output.write(ps.stem(word))
    output.write(" : ")
    output.write('\n')

output_file.write(output.getvalue())

output.close()
wikipediaText.close()
output_file.close()
