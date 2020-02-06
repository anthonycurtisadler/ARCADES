"""Module containing the class which stores and applies key definitions
pylint rated 10.0/10
"""

import nformat
from displaylist import DisplayList
from globalconstants import UNDERLINE, TILDA, COLON, COMMA, YESTERMS, EQUAL, EMPTYCHAR,\
     ADDTERMS, DELETETERMS, SHOWTERMS, QUITTERMS, CLEARTERMS, EMPTYCHAR, BLANK


class KeyMacroDefinitions:


    """ Holds and applies key definitions, which are
    used to automatically assign keys to notes
    according the words found in them.
    """

    def __init__(self,displayobject,headings=None,terms=None,presets=None):

        if presets is None:
            self.key_definitions = {}
        else:
            self.key_definitions = presets
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
            self.key_definitions[keyword].update(set(definitions))
        else:
            self.key_definitions[keyword] = set(definitions)

    def delete(self, keyword):

        """delete keyword"""
        
        if keyword in self.key_definitions:
            del self.key_definitions[keyword]


    def get_definition(self, keyword):

        """get definitions for a given keyword"""

        if keyword in self.key_definitions:
            return self.key_definitions[keyword]
        return {}

    def return_keys(self, words):

        """return all keys"""

        returnkeys = set()
        for word in [a_temp.lower() for a_temp in words]:
            returnkeys.update(self.get_key(word))
        return returnkeys

    def show_kd(self,returntext=False):

        """ show keys with definitions"""

        if not returntext:
            show_keys = DisplayList(displayobject=self.displayobject)
        else:
            show_keys = []
        spacer = ' '*(not returntext)
    

        for counter, k_temp in enumerate(sorted(self.key_definitions.keys(),
                             key=lambda x_temp: x_temp.lower())):
            if not returntext:
                countermark = str(counter+1)
            else:
                countermark = EMPTYCHAR
            key_temp = nformat.format_keys(self.get_definition(k_temp))
            if returntext:
                key_temp = key_temp.replace(COMMA+BLANK,COMMA).replace(BLANK,UNDERLINE)

            show_keys.append(countermark+spacer+k_temp+COLON+spacer+key_temp)
        if not returntext:
            show_keys.show(header=self.headings.KEY_DEF, centered=True)
        else:
            return '\n'.join(show_keys)

    def export_string (self):

        """returns the dictionary as a string"""

        
        return str(self.key_definitions)

    def import_string (self,text):

        self.key_definitions = eval(text)

    


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
            key, definitions = l_temp.split(COLON)[0], {x_temp.strip().replace(UNDERLINE,BLANK).replace(TILDA,BLANK) for x_temp in l_temp.split(COLON)[1].split(COMMA)}
            if not deleting:
                self.add(key, definitions)
            else:
                self.delete(key, definitions)

        self.show_kd()

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

                self.add(input(self.headings.KEYMACRO), [x_temp.strip() for x_temp in input(self.headings.KEYS).split(',')])
            if i in self.DELETETERMS:

                while True:
                    self.show_kd()
                    to_delete = input (self.headings.DELETE)
                    if to_delete == EMPTYCHAR:
                        break
                    if to_delete.isnumeric() and int(to_delete) > 0 and int(to_delete) < len(self.key_definitions)+1:
                        from_temp = sorted(list(self.key_definitions.keys()),
                                           key=lambda x_temp: x_temp.lower())[int(to_delete)-1]
                        
                        self.delete(from_temp)
            if i in self.SHOWTERMS:
                self.show_kd()
            if i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                    self.key_definitions = {}
                 
            if i in self.QUITTERMS:
                go_on = False
