import codecs
import io

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

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
    return words

wikipediaText = open("smallerOutput.txt", "r")
count = 0
wikipediaDictionary = set()
for line in wikipediaText:
    for word in parseLine(line):
        count += 1
        wikipediaDictionary.add(word.lower())

print(count)


ps = PorterStemmer()

output_file = codecs.open("dictionary.txt", 'w+', 'utf-8')
output = io.StringIO()
for word in wikipediaDictionary:
    output.write(word)
    output.write(" : ")
    output.write(ps.stem(word))
    output.write('\n')

output_file.write(output.getvalue())

output.close()
wikipediaText.close()
output_file.close()
