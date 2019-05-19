"""Module containing the class which stores and applies key definitions
pylint rated 10.0/10
"""

import nformat
from displaylist import DisplayList
from globalconstants import COLON, COMMA, UNDERLINE, TILDA
from globalconstants import YESTERMS, ADDTERMS, DELETETERMS, CLEARTERMS, \
     LEFTNOTE, RIGHTNOTE, LEFTCURLY, RIGHTCURLY, EOL, BLANK, COLON, QUESTIONMARK, UNDERLINE,\
     EMPTYCHAR, SHOWTERMS, QUITTERMS, EQUAL

class KeyDefinitions:


    """ Holds and applies key definitions, which are
    used to automatically assign keys to notes
    according the words found in them.
    """

    def __init__(self, displayobject, headings=None, terms=None):

        self.key_definitions = {}
        self.definition_keys = {}
        self.displayobject = displayobject
        if not headings:
            from plainenglish import DefaultConsoles
            self.headings = DefaultConsoles()
        else:
            self.headings = headings
        if not terms:
            from plainenglish import ADDTERMS,DELETETERMS,\
                 SHOWTERMS,QUITTERMS,CLEARTERMS
            self.ADDTERMS = ADDTERMS
            self.DELETETERMS = DELETETERMS
            self.SHOWTERMS = SHOWTERMS
            self.QUITTERMS = QUITTERMS
            self.CLEARTERMS = CLEARTERMS
        else:
            self.ADDTERMS = terms[0]
            self.DELETETERMS = terms[1]
            self.SHOWTERMS = terms[2]
            self.QUITTERMS = terms[3]
            self.CLEARTERMS = terms[4]

    def change_language(self,headings=None,terms=None):

        if not headings:
            from plainenglish import DefaultConsoles
            self.headings = DefaultConsoles()
        else:
            self.headings = headings
        self.ADDTERMS = terms[0]
        self.DELETETERMS = terms[1]
        self.SHOWTERMS = terms[2]
        self.QUITTERMS = terms[3]
        self.CLEARTERMS = terms[4]

    def add(self, keyword, definitions):

        """add keyword and definition"""

        if keyword in self.key_definitions:
            self.key_definitions[keyword].update({x_temp.strip() for x_temp in definitions})
        else:
            self.key_definitions[keyword] = {x_temp.strip() for x_temp in definitions}

        for d_temp in {x_temp.strip() for x_temp in definitions}:
            if d_temp in self.definition_keys:
                self.definition_keys[d_temp].add(keyword)
            else:
                self.definition_keys[d_temp] = {keyword}

    def delete(self, keyword, definitions):

        """delete keyword and definitions
        For reasons I don't fully understand, I have to make a copy of the definitions.
        Otherwise definitions is empty before the second half of the routine.
        """

        definitionscopy = list(definitions) 
        if keyword in self.key_definitions:
            for d_temp in list(definitions):
                self.key_definitions[keyword].discard(d_temp)
                if not self.key_definitions[keyword]:
                    del self.key_definitions[keyword]


        for d_temp in definitionscopy:

            if d_temp in self.definition_keys:
                self.definition_keys[d_temp].discard(keyword)

                if not self.definition_keys[d_temp]:
                    del self.definition_keys[d_temp]


    def get_definition(self, keyword):

        """get definitions for a given keyword"""

        if keyword in self.key_definitions:
            return self.key_definitions[keyword]
        return {}

    def get_key(self, definition):

        """get keywords for a given definition"""

        if definition in self.definition_keys:
            return self.definition_keys[definition]
        return {}

    def return_keys(self, words):

        """return all keys"""

        returnkeys = set()
        for word in {a_temp.lower() for a_temp in words}.union({a_temp for a_temp in words}):
            returnkeys.update(self.get_key(word))
        return returnkeys

    def show_kd(self,returntext=False):

        """ show keys with definitions"""

        show_keys = DisplayList(displayobject=self.displayobject)

        if not returntext:
            show_keys = DisplayList(displayobject=self.displayobject)
        else:
            show_keys = []

        spacer = ' '*(not returntext)
        

        for counter, k_temp in enumerate(sorted(list(self.key_definitions.keys()),
                             key=lambda x_temp: x_temp.lower())):

            if not returntext:
                countermark = str(counter+1)
            else:
                countermark = EMPTYCHAR
            key_temp = nformat.format_keys(self.get_definition(k_temp))
            if returntext:
                key_temp = key_temp.replace(COMMA+BLANK,COMMA).replace(BLANK,UNDERLINE)
            show_keys.append(countermark+spacer+k_temp+COLON+spacer+key_temp)
        if returntext:
            return EOL.join(show_keys)
        
        show_keys.show(header='KEYWORDS : DEFINITIONS', centered=True)


    def show_dk(self):

        """show definitions with keys

        For reasons that I do not understand,
        I need to add this blank space to
        keep the formatting normal when
        displaying the note...
        """

        show_definitions = DisplayList(displayobject=self.displayobject)

        for counter, d_temp in enumerate(sorted(list(self.definition_keys.keys()),
                             key=lambda x_temp: x_temp.lower())):
 
                
            show_definitions.append(str(counter+1)+BLANK+d_temp+COLON+BLANK
                                    +nformat.format_keys(self.get_key(d_temp))+BLANK*3)
        show_definitions.show(header=self.headings.KEY_DEF, centered=True)



    def load(self, entrylist):

        """ load in a list of keyword defintions.
        Take note that the load function is shared by Key_Definitions
        and Abbreviate, which allows instantiations
        of both classes to be passed into the defauly_from_notes class,
        which is used to store default values as notes!"""


        for l_temp in entrylist:

            l_temp = l_temp.lstrip(UNDERLINE)
            l_temp = l_temp.strip()

            deleting = False
            if l_temp[0] == TILDA:
                l_temp = l_temp[1:]
                deleting = True
            key, definitions = l_temp.split(COLON)[0], {x_temp.replace(UNDERLINE,BLANK) for x_temp in l_temp.split(COLON)[1].split(COMMA)}
            if not deleting:
                self.add(key, definitions)
            else:
                self.delete(key, definitions)

        self.show_kd()
        self.show_dk()

    def console(self):

        """ opens up console for adding and deleting """

        go_on = True
        while go_on:
            console = DisplayList([self.headings.ADD_MENU,
                                   self.headings.DELETE_MENU,
                                   self.headings.SHOW_MENU,
                                   self.headings.CLEAR_MENU,
                                   self.headings.QUIT_MENU],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.ADDTERMS:

                self.add(input(self.headings.KEYS), [x_temp.strip() for x_temp in input(self.headings.DEFINITIONS).split(',')])
            if i in self.DELETETERMS:

                while True:
                    self.show_kd()
                    to_delete = input (self.headings.DELETE)
                    if to_delete == EMPTYCHAR:
                        break
                    if to_delete.isnumeric() and int(to_delete) > 0 and int(to_delete) < len(self.key_definitions)+1:
                        from_temp = sorted(list(self.key_definitions.keys()),
                                           key=lambda x_temp: x_temp.lower())[int(to_delete)-1]
                        to_temp = self.key_definitions[from_temp]
                        print('A',from_temp,to_temp)
                        self.delete(from_temp,to_temp)
            if i in self.SHOWTERMS:
                self.show_kd()
                self.show_dk()
            if i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                    self.key_definitions = {}
                    self.definition_keys = {}                 
            if i in self.QUITTERMS:
                go_on = False

