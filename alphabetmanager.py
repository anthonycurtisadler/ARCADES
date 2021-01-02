###Class for managing alphabets

from alphabets import Alphabet
from display import Display

abbreviations = {'gr':'greek'}
def deb (x):
    """To unabbreviate the language names"""
    
    if x in abbreviations:
        return abbreviations[x]
    return x

def all_indexes (text,phrase):

    """Returns a list of all index positions for phrase in text"""
    
    returnlist = []
    starting_from = 0

    while text and phrase in text:
        position = text.index(phrase)
        returnlist.append(starting_from+position)
        text = text[position+len(phrase):]
        starting_from += position+len(phrase)
    return returnlist

def all_positive(entrylist):

    """True iff all values in the list are positive"""

    for x in entrylist:
        if x<0:
            return False
    return True

        
class AlphabetManager:


    def __init__ (self):

        self.alphabets = {}
        self.display = Display()
        self.load()
        self.load('de')
        self.load('xl')
        self.load('heb')

    def load (self,language='gr'):

        """Attempts to load in a new alphabet to the dictionary"""

        try:
            self.alphabets[language] = Alphabet(language)
            self.display.noteprint(('ATTENTION',
                                    deb(language) + ' successfully loaded'))
            
            return True 
        except:
            self.display.noteprint(('ATTENTION',
                                    'Cannot load '+deb(language)))
            return False

    
        
    def interpret (self,text):

        """Recursive function for de-transcribing foreign language.
        Recursion is used so that it can handle multiple alphabet.

        Phrases to be interprets in foreign language should be encompassed in [*LAN] [LAN*]
        
        """
        
        if '[*' not in text:
            return text

        if '[*' in text and '*]' in text.split('[*')[1]:
            right_identifier = ''
            left_identifier = ''
            if ']' in text.split('[*')[1].split('[')[0]:
                language_id = text.split('[*')[1].split(']')[0]
                left_identifier = '[*'+language_id+']'
                right_identifier = '['+language_id+'*]'
            if not (language_id in self.alphabets or self.load(language_id)):
                return self.interpret(text.replace(left_identifier,'').replace(right_identifier,''))
            
            

            

            if not (left_identifier
                and right_identifier
                and text.count(left_identifier)==text.count(right_identifier)):
                return self.interpret(text.replace(left_identifier,'').replace(right_identifier,''))
            

            left_indexes = all_indexes(text,left_identifier)
            right_indexes = all_indexes(text,right_identifier)
            index_pairs = []
            for x in range(len(left_indexes)):
                index_pairs.append((left_indexes[x],right_indexes[x]))
            differences = [x[1]-x[0] for x in index_pairs]
            if not all_positive(differences):
                return self.interpret(text.replace(left_identifier,'').replace(right_identifier,''))

            last_position = 0
            returntext = ''
            for x in index_pairs:

                left_pos = x[0]
                right_pos = x[1]

                if left_pos > last_position:
                    returntext += text[last_position:left_pos]

                returntext += self.alphabets[language_id].transcribe(text[left_pos+len(left_identifier):
                                                                          right_pos])

                last_position = right_pos+len(right_identifier)
            if last_position < len(text):
                returntext += text[last_position:]
            return self.interpret(returntext)
        return text

    def console (self):

        while True:
            self.display.noteprint(('ALPHABETS = '+','.join([x for x in self.alphabets.keys()]),
                                   """
(H)elp for script
(V)iew all characters
(S)ome characters
(Q)uit"""))

            command = input('?')
            if command:
                command = command[0].lower()
                if command == 'h':
                    language = input('For language?')
                    if language  in self.alphabets:
                        self.display.noteprint(('',self.alphabets[language].help()))
                elif command == 'v':
                    language = input('For language?')
                    if language  in self.alphabets:
                        self.display.noteprint(('',self.alphabets[language].characters()))
                elif command == 's':
                    language = input('For language?')
                    if language  in self.alphabets:
                        chars = input('Which characters do you want to see?')
                        self.display.noteprint(('',self.alphabets[language].characters(chars)))                       
                elif command == 'q':
                    break
                        
                                                                     
                    
if __name__ == '__main__':

    alph_man = AlphabetManager()

    print(alph_man.interpret("This [*de]Wa$er ist gu:te[de*] is a test [*gr]hexis[gr*]Oh yes[*heb]ADAM[heb*] it is[*gr]filo'sofia[gr*]NOW"))
    print(alph_man.interpret("This is a test [*xl]he: a: o: xis  o.p*[xl*]Oh yes[*heb]adonai[heb*] it is[*gr]filo'sofia[gr*]NOW"))
    alph_man.console()
                    

                
            
                
        
            
            
    
