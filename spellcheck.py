"""Spellchecker module
Tyler Barrus PYSPELLCHECKER is an external dependency
pylint rated 8.83/10
"""

import string

from spellchecker import SpellChecker
from globalconstants import EMPTYCHAR, BLANK, EOL, COLON, COMMABLANK, DASH, SLASH, YESTERMS
from display import Display
import sqlite3




class SpellCheck:


    """Class for applying Tyler Barrus PYSPELLCHECKER
    to text default language is English, but German, French,
    and Spanish are also available added words for each
    language are kept in separate keys of added_words"""

    def __init__(self, displayobject=None,added_words=None,headings=None,using_database=False,notebookname=None):

        if not headings:
            from plainenglish import Spelling
            self.headings = Spelling()
        else:
            self.headings = headings

        if not notebookname:
            notebookname = 'GENERAL'
        self.notebookname = notebookname


        self.language = 'en'
        self.spell = SpellChecker(language=self.language)
        if not added_words:
            self.added_words = {'es':set(),
                                'en':set(),
                                'fr':set(),
                                'de':set()}
        else:
            self.added_words = added_words
            for language in self.added_words:
                self.language = language
                for word in self.added_words:
                    self.spell.word_frequency.load_words(word)

        if not displayobject:
            self.displayobject = Display()

        else:
            self.displayobject = displayobject
        self.open_connection()
        self.create_database()
        self.update_notebook()
        self.update_language()
        self.load_words_from_DB()
        

        

    def create_database (self):

        self.db_cursor.executescript("""

            CREATE TABLE IF NOT EXISTS notebooks (
            
                    notebook TEXT NOT NULL UNIQUE);

              
            CREATE TABLE IF NOT EXISTS languages (
              
                    notebook TEXT NOT NULL,
                    language TEXT NOT NULL,
                                        
                    PRIMARY KEY (notebook, language)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    
              );

            CREATE TABLE IF NOT EXISTS words (
              
                    notebook TEXT NOT NULL,
                    language TEXT NOT NULL,
                    word TEXT NOT NULL,
                    
                    PRIMARY KEY (notebook, language, word)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    FOREIGN KEY (language) REFERENCES languages (language) ON DELETE CASCADE
                    
              );
              """)

    def update_notebook (self):

        self.db_cursor.execute("INSERT OR REPLACE "+
                               " INTO notebooks "+
                               "(notebook) VALUES (?);",(self.notebookname,))
        self.db_connection.commit()

    def update_language (self,language=None):
        if language is None:
            language=self.language
        value_tuple = (self.notebookname,self.language,)
        self.db_cursor.execute("INSERT OR REPLACE INTO languages "+
                               " (notebook, language) VALUES (?,?);",
                               value_tuple)
        self.db_connection.commit()

    def open_connection (self):

        self.db_connection = sqlite3.connect('notebooks'+'/'+'spelling.db')
        self.db_cursor = self.db_connection.cursor()                                         

    def purge_connection (self):

        self.db_connection = None
        self.db_cursor = None

    def load_words_from_DB (self):

        for language in self.added_words:
            value_tuple = (self.notebookname, language,)
            self.db_cursor.execute("SELECT word FROM words WHERE notebook=? and language=?",value_tuple)
            words = self.db_cursor.fetchall()
            self.added_words[language].update([word[0] for word in words])
            
    def add_word (self,word,language=None):

        """Adds words both to dictionary and to database"""

        if language is None:
            language = self.language

        self.added_words[self.language].add(word)
        value_tuple = (self.notebookname, language, word)
        self.update_language()
        self.db_cursor.execute("INSERT OR REPLACE "+
                               " INTO words "+
                               "(notebook, language, word)"+
                               "  VALUES (?,?,?);",
                               value_tuple)
        self.db_connection.commit()
        value_tuple = (self.notebookname, self.language, word)
        

    def discard_word (self,word,language=None):
        
        if language is None:
            language = self.language
        self.added_words[self.language].discard(word)
        self.update_language()
        value_tuple = (self.notebookname, language, word)
        self.db_cursor.execute("DELETE FROM words "+
                              "WHERE notebook=? AND "+
                              "language=? AND word=?;",value_tuple)
        self.db_connection.commit()
       
               

    def set_language(self,
                     entry='en'):
        """sets language. Options are 'en' 'de' 'fr' es'"""

        if entry in ['en',
                     'de',
                     'fr',
                     'es']:
            self.language = entry
        self.spell = SpellChecker(language=self.language)

    def checktext(self,
                  text):

        """applies spellchecker to text"""

        def upper_lower(word,
                        boolean):

            """ applies capitalization only if boolean is true"""

            if boolean:
                return word.capitalize()
            else:
                return word

        for a_temp in string.punctuation:
            text = text.replace(a_temp, BLANK+a_temp+BLANK)
        wordlist_lower = [a_temp.strip() for a_temp in text.split(BLANK)
                          if len(a_temp) > 0 and a_temp[0].islower()]
        wordlist_upper = [a_temp.strip().lower() for a_temp in text.split(BLANK)
                          if len(a_temp) > 0 and a_temp[0].isupper()]
        misspelled_lower = [a_temp for a_temp in self.spell.unknown(wordlist_lower)
                            if len(a_temp) > 2 and a_temp not in self.added_words[self.language]]
        misspelled_upper = [a_temp.upper() for a_temp in self.spell.unknown(wordlist_upper)
                            if len(a_temp) > 2 and a_temp not in self.added_words[self.language]]
        english = len(misspelled_lower+misspelled_upper)

        if english > 10:
            lang_temp = self.language
            self.set_language('de')
            misspelled_lower_german = [a_temp for a_temp
                                       in self.spell.unknown(wordlist_lower)
                                       if len(a_temp) > 2 and a_temp not in self.added_words[self.language]]
            misspelled_upper_german = [a_temp for a_temp
                                       in self.spell.unknown(wordlist_upper)
                                       if len(a_temp) > 2 and a_temp not in self.added_words[self.language]]
            german = len(misspelled_lower_german+misspelled_upper_german)
            if german < english:
                misspelled_lower = misspelled_lower_german
                misspelled_upper = misspelled_upper_german
            self.set_language(lang_temp)
            print(self.language)
        

        misspelled = []
        allwords = EMPTYCHAR

        for a_temp in misspelled_lower+misspelled_upper:
            misspelled.append((a_temp[0].isupper(), a_temp))
            allwords += a_temp+COMMABLANK
        self.displayobject.noteprint((self.headings.THERE_ARE
                                      +str(len(misspelled))
                                      +self.headings.MISSPELLED,
                                      allwords[:-2]))

        if misspelled and input(self.headings.SKIP_CORRECTIONS) != BLANK:

            for word in misspelled:



                 
                is_upper = word[0]
                word = word[1]
                print(EOL+BLANK+BLANK+word,self.headings.IS_MISPELLED+EOL)
                if len(word) < 10 and DASH not in word:
                    candidatelist = list(self.spell.candidates(word))
                    for a_temp, b_temp in enumerate(candidatelist):
                        print(a_temp, COLON, b_temp)
                    print()
                    inp = input(self.headings.INPUT_MENU)
                    if inp == EMPTYCHAR:
                        pass
                    elif inp == BLANK:
                        self.load(upper_lower(word,is_upper),language=self.language)
                        self.add_word(upper_lower(word,is_upper))
                        self.spell.word_frequency.load_words(upper_lower(word,is_upper))
                        self.displayobject.noteprint(('/C/ ATTENTION!',upper_lower(word,is_upper)
                                                      +' added to dictionary for '
                                                      +{'en':'English',
                                                        'es':'Spanish',
                                                        'de':'German',
                                                        'fr':'French'}[self.language]))
                        
                        
                    elif inp == BLANK + BLANK:
                        break
                    elif inp.isnumeric():
                        print(upper_lower(word, is_upper),
                              upper_lower(candidatelist[int(inp)], is_upper))
                        text = text.replace(upper_lower(word, is_upper),
                                            upper_lower(candidatelist[int(inp)],
                                                        is_upper))
                    else:
                        if inp[0] == BLANK:
                            self.add_word(word)
                            self.spell.word_frequency.load_words([word])
                            text = text.replace(upper_lower(word, is_upper),
                                                upper_lower(inp, is_upper))
                        text = text.replace(upper_lower(word, is_upper),
                                            upper_lower(inp, is_upper))
                else:
                    inp = input(self.headings.SMALL_INPUT_MENU)
                    if inp == EMPTYCHAR:
                        pass
                    elif inp == BLANK:
                        self.add_word(word)
                        self.spell.word_frequency.load_words(word)
                    elif inp == SLASH:
                        break
                    else:
                        if inp[0] == BLANK:
                            self.add_word(word)
                            self.spell.word_frequency.load_words([word])
                            text = text.replace(upper_lower(word, is_upper),
                                                upper_lower(inp, is_upper))

                        text = text.replace(upper_lower(word, is_upper),
                                                upper_lower(inp, is_upper))
        for a_temp in string.punctuation:
            text = text.replace(BLANK+a_temp+BLANK, a_temp)
        self.set_language('en')
        return text, self.added_words

    def load(self,entryset=None,language='en'):
        if isinstance(entryset,str):
            for x_temp in string.punctuation.replace('-',''):
                entryset = entryset.replace(x_temp,' ')
            entryset = set(entryset.split(' '))
        oldlanguage = self.language
        if not entryset:
            entryset = set()
        self.set_language(language)
        entryset = [a_temp for a_temp
                    in self.spell.unknown(list(entryset))
                    if len(a_temp) > 2
                    and a_temp not in self.added_words[self.language]]
        self.spell.word_frequency.load_words(list(entryset))
        for word in entryset:
            self.add_word(word)
        self.displayobject.noteprint(('/C/ ATTENTION!',', '.join(list(entryset))
                              +' added to dictionary for '
                              +{'en':'English',
                                'es':'Spanish',
                                'de':'German',
                                'fr':'French'}[self.language]))
        self.set_language(oldlanguage)

    def console(self):
        go_on = True 
        while go_on:

            self.displayobject.noteprint((self.headings.SPELLING_DICTIONARY+' '+self.notebookname,
                                          self.headings.WORDS_TO_DELETE))
            command = input('?')
            if not command:
                go_on = False
            else:
                command = command[0].upper()
                if command == 'A':
                    word = input(self.headings.WORD_TO_ADD)
                    self.load(word,language=self.language)
                if command == 'D':
                    word = {x_temp.strip() for x_temp in input(self.headings.WORD_TO_DELETE).split(',')}
                    for w_temp in word:
                        self.discard_word(w_temp)
                if command == 'S':
                    self.show_added(self.language)
                if command == 'C':
                    newlanguage = input(self.headings.LANGUAGE_SELECT)
                    if newlanguage in ['es','fr','en','de']:
                        self.set_language(newlanguage)
                if command == 'L':
                    text = input(self.headings.TEXT_TO_ADD)
                    self.load(text,language=self.language)
                if command == 'E':
                    if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                        self.added_words[self.language] = set()
                if command == "X":
                    self.db_cursor.execute("SELECT * FROM notebooks")
                    nb_list = [x[0] for x in self.db_cursor.fetchall()]
                    self.displayobject.noteprint(('NOTEBOOKS',', '.join(nb_list)))
                    new_nb = input('NAME of notebook to switch to?')
                    query = True
                    if new_nb not in nb_list:
                        query = input('Are you sure you want to create '+new_nb) in YESTERMS
                    if query:
                        self.notebookname = new_nb
                        self.update_notebook()
                        self.added_words = {'es':set(),
                                'en':set(),
                                'fr':set(),
                                'de':set()}
                        self.load_words_from_DB()
                        
                        
                if command == 'Q':
                    go_on = False
 

    def show_added(self,language='en'):

        """shows all the words that have
        been added to the dictionary
        """
        if language not in ['en','de','fr','es']:
            language = 'en'
        self.set_language(language)

        self.displayobject.noteprint(('/C/'+{'en':'ENGLISH',
                                             'de':'GERMAN',
                                             'fr':'FRENCH',
                                             'es':'SPANISH'}[self.language],
                                      ', '.join(list(sorted(self.added_words[self.language],key=lambda x:x.lower())))))

if __name__ == "__main__":

    spellchecker = SpellCheck()
    spellchecker.console()
    

