import bz2
import codecs
import io
import time


num_lines = 1000000

print('type y if you want to only read a certain number of num_lines')
resp = input()
if resp == 'y':
    print('how many lines')
    num_lines = int(input())
    print('reading ', num_lines, 'lines')
else:
    num_lines = -1

print('what is the name of the file that you would like to output to?')
toOutputFile = input()

class Reader():

    def __init__( self , time, filename):
        self.output = io.StringIO()
        self.output_file = codecs.open(filename + ".txt", 'w+', 'utf-8')
        self.inPage = False
        self.shouldWriteToFile = False
        self.numPages = 0
        self.hadText = False
        self.initialTime = time
        self.prevTime = time


    def read(self, label ):
        if(self.checkShouldRead(label)):
            self.output.write(self.format(label))
            self.output.write('\n')
            if self.shouldWriteToFile:
                self.writeToFile()


    def format(self, label):
        label = label.replace('\'\'\'', '')
        label = label.replace('\'\'', '')
        label = label.replace('&quot;', '')
        label = label.replace('&lt;!--', '')
        label = label.replace('&lt;', '')
        label = label.replace('&lt;', '')
        label = label.replace('&gt;', '')
        label = label.replace('--&gt;', '')
        label = label.replace('#', '')
        label = label.replace('small&gt;', '')
        label = label.replace('!', '')

        #indexOfFile = label.find('File')


        # while indexOfFile != -1:
        #     if label[indexOfFile - 1] == '[':
        #         indexOfEndBrak = label.find(']]', indexOfFile) + 2
        #         label = label.replace(label[(indexOfFile - 2):indexOfEndBrak], '')
        #     indexOfFile = label.find('File', indexOfFile + 1)


        indexOfCurl = label.find('{{')
        while indexOfCurl != -1:
            indexOfCurlEnd = label.find('}}')
            label = label.replace(label[indexOfCurl:indexOfCurlEnd + 2], '')
            indexOfCurl = label.find('{{', indexOfCurl + 1)

        label = label.replace('[[', '')
        label = label.replace(']]', '')
        label = label.replace('|}', '')
        label = label.replace('|', ' ')

        label = label.replace('=', '')


        return label


    def checkShouldRead(self, label):
        if not self.inPage:
            if label.startswith('<page>'):
                self.inPage = True
            return False

        if self.inPage:
            if label.startswith('</page>'):
                self.inPage = False
                self.shouldWriteToFile = True
            if label.startswith('<') or label.startswith('{') or label.startswith('*') or label.startswith(';') or label.startswith('}'):
                return False
            self.hadText = True
            return True




    def writeToFile(self):
        self.output_file.write(self.output.getvalue())
        self.output.close()
        self.output = io.StringIO()
        self.shouldWriteToFile = False
        self.printTime()


    def printTime(self):
        self.numPages += 1
        if(time.time() - self.prevTime > 30):
            print('%s numPages in 30 seconds' %self.numPages)
            self.numPages = 0
            t2 = time.time() - self.initialTime
            print('{:3.5f} seconds since starting'.format(t2))
            self.prevTime = time.time()

    def closeFile(self):
        self.output_file.close()


    def printNumPages(self):
        self.numPages += 1
        print('So far %s pages' %(self.numPages))




with bz2.open("enwiki-20200401-pages-articles-multistream.xml.bz2", "rt") as bz_file:
    reader = Reader(time.time(), toOutputFile)
    count = 0
    for line in bz_file:
        label = line.rstrip('\n').lstrip()
        reader.read(label)
        count += 1
        if count > num_lines and num_lines != -1:
            break

reader.closeFile()
