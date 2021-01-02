###Class for entering in words from foreign alphabets

class Alphabet:

    def __init__ (self,language='gr'):

        from ALLALPHABETS import all_alphabets
        
        self.letters = all_alphabets[language]['alphabet']
        self.mod_word = all_alphabets[language]['function']
        self.help_script = all_alphabets[language]['helpscript']
        self.orientation = all_alphabets[language]['orientation']
        self.add_regular_latin = all_alphabets[language]['latin']

        self.definitions = {}

        #Creates a dictionary for interpreting Roman transcription into the target alphabet
        #KEYS are the plain characters in the Roman alphabet
        #VALUE consists in a list of all the characters in the target alphabet, including diacritics = head,
        #together with the marks that interpret the given diacritics = determinant 
        #{char1:[head1a#determinant1a,head1b#determinant1b]}
        self.det_chars = set()
        found_heads = set()
        for line in self.letters.split('\n'):
            if line:
                head,body = line.split('|')[0],line.split('|')[1]
                char,determinant = body.split('#')[0],body.split('#')[1]
                self.det_chars.update(set(determinant))

                if self.add_regular_latin and char not in found_heads:
                    if char in self.definitions:
                        if (char,'') not in self.definitions[char]:
                            self.definitions[char].append((char,''))
                    else:
                        self.definitions[char] = [(char,'')]
                    found_heads.add(char)
                
                        

                if char not in self.definitions:
                    self.definitions[char] = [(head,determinant.replace(' ',''))]
                else:
                    for x in self.definitions:
                        if (head,determinant.replace(' ','')) in self.definitions[x]:
                            print('ALREADY FOUND',x,(head,determinant.replace(' ','')))
                    self.definitions[char].append((head,determinant.replace(' ','')))
                    
                   
        #String containing all the chars in the Roman alphabet appearing as keys in the dictionary
        self.all_chars = ''.join(list(set(self.definitions.keys())))

    def get_segments (self,phrase):

        """Returns a list of tuples containing
        the Roman character and the determinants for the diacritics
        """
        
        starting_at = 0
        returned_segments = []
        header = ''
        other_parts = ''
        for counter, x in enumerate(phrase):

            if x in self.all_chars:

                if header:
                    returned_segments.append((header,phrase[starting_at:counter]))
                header = x
                starting_at = counter + 1
            elif x not in self.det_chars:
                if header:
                    returned_segments.append((header,phrase[starting_at:counter]))
                    header = ''
                returned_segments.append((x,''))
                starting_at = counter + 1

        
                
                
                
        returned_segments.append((header,phrase[starting_at:]))
                
        return returned_segments

    def get_values (self,compare_from,defs):

        """Returns a list of tuples with values describing
        the "match" of a given determinant and the
        characters from the target alphabet, based
        on the list of definitions taken from the

        100=perfect match
        5 = empty determinant
        +10 for every matching element of the determinant,
            with a decreasing fraction reflecting
            order of appearance
        """


        segments = []
        for temp_def in defs:
            value = 0
            x = temp_def[1]
            char = temp_def[0]
            if x == compare_from:
                value = 100
            elif x:
                for counter,y in enumerate(compare_from):
                    for xx in x:
                        if xx == y:
                            value+=10+5/(counter+1)
            else:
                value = 5
            segments.append((char,value))
        return segments


    def get_best (self,segments):

        """Returns the best-matched character for the target alphabet
        by sorting through the list of tuples
        """

        ordered = sorted(segments,key=lambda x:x[1],reverse=True)

        return ordered[0][0]
               

    def interpret (self,segments):

        """Transcribes a single word into the target alphabet"""

        returnphrase = ''

        for counter, x in enumerate(segments):

            
            head = x[0]
            determinants = x[1]

            if head in self.definitions:
                all_determinants = self.definitions[head]
                vals = self.get_values(determinants,all_determinants)
                returnphrase += self.get_best(vals)
            else:
                returnphrase += head
            
        return returnphrase
            
    def transcribe(self,phrase):

        """Transcribes an entire phrase"""
        
        output = []
        for word in phrase.split(' '):
            word = self.mod_word(word)
            
            segments = self.get_segments(word)

            output.append(self.interpret(segments))
        if self.orientation:
            result = ' '.join(output)
        else:
            result = ' '.join(reversed(output))
 
            
        return result

    def help (self):

        """Returns help script"""

        return self.help_script

    def characters (self,chars=None):

        returnlist = []
        if chars:
            domain = set(self.definitions.keys()).intersection(set(chars))
        else:
            domain = self.definitions.keys()
        for char in domain:
            phrase = ''
            phrase += char + ' = '
            segs = []
            for seg in self.definitions[char]:
                segs.append(seg[0]+'['+seg[1]+']')
            phrase += ', '.join(segs)
            returnlist.append(phrase)
        return '\n\n'.join(returnlist)
    
    
            

if __name__ == "__main__":

    greek_keyboard = Alphabet('heb')
    while True:
        print(greek_keyboard.transcribe(input('?')))
        print(greek_keyboard.help())  

        

        

    
    


    

    
