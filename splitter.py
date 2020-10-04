import string, os

def get_text_file(filename,folder=os.altsep+'textfiles',suffix='.txt'):


    """opens a text file a returns the text"""

    directoryname = os.getcwd()+folder
    if os.altsep+'notebooks'+os.altsep+'textfiles' in directoryname:
        print(directoryname)
        directoryname = directoryname.replace(os.altsep + 'notebooks'
                                              + os.altsep+'textfiles',
                                              os.altsep+'textfiles')
        print(directoryname)
    if  os.altsep+'notebooks'+'/'+'textfiles' in directoryname:
        print(directoryname)
        directoryname = directoryname.replace(os.altsep + 'notebooks'
                                              + '/' + 'textfiles',
                                              os.altsep+'textfiles')
        print(directoryname)
        
    
    with open(directoryname+os.altsep+filename+suffix,'r',
                    encoding='utf-8') as textfile:
        returntext = textfile.read().replace('\ufeff',
                                         '')
    return returntext



class wordlist:

    def __init__(self,text=''):

        self.all_words = {}
        self.text = text

    def load (self,filename):
        self.text = get_text_file (filename)
        

    def purge (self,text='',topurge=''):

        for char in topurge:
            text = text.replace(char,' ')
        return text

    def reduce (self):

        self.text = self.purge(self.text,string.punctuation + ','+'.'+'[](){}<>' + '»«'+'”'+'—“')
        self.text = self.purge(self.text,string.whitespace)
        self.text = self.purge(self.text,'01234567890')
        
    def split (self):

        all_words = self.text.split(' ')
        all_words = list(set(all_words))
        return all_words

if __name__ == "__main__":

    while True:
        x = input('?')
        if x == '':
            break
        splitter = wordlist(x)
        splitter.load(x)
        splitter.reduce()
        
        words = sorted(splitter.split())
        words = [x.lower() for x in words]
        
##        for counter, word in enumerate(words):
##            print(str(counter)+' : '+word)
        print('TOTAL NUMBER OF WORDS = ',len(words))
        print(', '.join(words))
        
    
