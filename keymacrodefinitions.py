"""Module containing the class which stores and applies key definitions
pylint rated 10.0/10
"""

import nformat
from displaylist import DisplayList
from globalconstants import UNDERLINE, TILDA, COLON, COMMA, YESTERMS, EQUAL, EMPTYCHAR,\
     ADDTERMS, DELETETERMS, SHOWTERMS, QUITTERMS, CLEARTERMS, EMPTYCHAR, BLANK

from keydefinitions import KeyDefinitions
from display import Display
import sqlite3

class KeyMacroDefinitions(KeyDefinitions):


    """ Holds and applies key definitions, which are
    used to automatically assign keys to notes
    according the words found in them.

    """
    
    def __init__(self, displayobject=None, headings=None, terms=None, using_database=True,presets=None):


        self.key_definitions = {}
        self.definition_keys = None 
        if not displayobject:
            displayobject = Display()
        self.displayobject = displayobject
        self.using_database = using_database
        if self.using_database:
            self.notebookname = 'GENERAL'
            self.open_connection()
            self.create_database()
            self.db_cursor.execute("INSERT OR REPLACE INTO macro_notebooks (notebook) VALUES (?);",(self.notebookname,))
            self.db_connection.commit()
            self.db_flag = 'd'
        else:
            self.db_flag = 'o'
            self.notebookname = None
        
        if presets:

            self.load_presets(presets=presets)       

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

    def create_database (self):


        self.db_cursor.executescript("""

            CREATE TABLE IF NOT EXISTS macro_notebooks (
            
                    notebook TEXT NOT NULL UNIQUE);

              
            CREATE TABLE IF NOT EXISTS key_macro_definitions (
              
                    notebook TEXT NOT NULL,
                    key TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    
                    PRIMARY KEY (notebook, key)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    
              );
              """)

        self.dict_object_dict= {'kd':self.key_definitions,
                       'dk':self.definition_keys}

        self.get_script_two_dict = {'kd':"SELECT definition FROM key_macro_definitions WHERE notebook=? AND key=?",
                                    'dk':""}

        self.get_script_one_dict = {'kd':"SELECT key FROM key_macro_definitions WHERE notebook=?",
                                    'dk':""}

        self.set_script_dict = {'kd':"INSERT OR REPLACE INTO key_macro_definitions (notebook, key, definition) VALUES (?,?,?);",
                                'dk':""}

        self.delete_script_two_dict = {'kd':"DELETE FROM key_macro_definitions WHERE notebook=? AND key=? AND definition=?",
                                       'dk':""}

        self.delete_script_one_dict = {'kd':"DELETE FROM key_macro_definitions WHERE notebook=? AND key=?",
                                       'dk':""}

        self.delete_script_none_dict = {'kd':"DELETE FROM key_macro_definitions WHERE notebook=?",
                                        'dk':""}

    def expose (self):

        print(self.key_definitions)

        if self.using_database:
            self.db_cursor.execute("SELECT * FROM key_macro_definitions")
            print(self.db_cursor.fetchall())


    def add(self, keyword, definitions):

        """add keyword and definition"""
        for x_temp in definitions:
            self.query(term1='kd',term2=keyword,term3=x_temp.strip(),action='set')
            
    def delete(self, keyword, definitions):

        """delete keyword and definitions
        """
        print(keyword,definitions)
        if self.query(term1='kd',term2=keyword,action='in'):
            self.query('kd',term2=keyword,term3=definitions,action='delete')


    def load_presets(self,presets):

        if 'd' in self.db_flag:

            self.key_definitions = presets

        if 'o' in self.db_flag:

            for x in presets:

                self.query(term1='kd',term2=x,term3=presets[x])
            

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
                                   self.headings.QUIT_MENU,
                                   '(N)otebook'*self.using_database],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.ADDTERMS:

                self.add(input(self.headings.KEYMACRO), [x_temp.strip() for x_temp in input(self.headings.KEYS).split(',')])
            elif i in self.DELETETERMS:

                while True:
                    self.show_kd()
                    to_delete = input (self.headings.DELETE)
                    if to_delete == EMPTYCHAR:
                        break
                    if to_delete.isnumeric() and int(to_delete) > 0 and int(to_delete) < len(self.query(term1='kd',action='get'))+1:
                        from_temp = sorted(list(self.query(term1='kd',action='get')),
                                           key=lambda x_temp: x_temp.lower())[int(to_delete)-1]
                        to_temp = self.query(term1='kd',term2=from_temp,action='get')
                        
                        self.delete(from_temp,to_temp[0])


            elif i in self.SHOWTERMS:
                self.show_kd()
            elif i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                    self.query(term1='kd',action='delete')
            elif i in ['n','N'] and self.using_database:
                self.db_cursor.execute('SELECT notebook FROM notebooks')
                notebooks = [x[0] for x in self.db_cursor.fetchall()]
                self.displayobject.noteprint(('NOTEBOOKS','\n'.join(notebooks)))
                action = input('NAME OF EXISTING OR NEW NOTEBOOK?').strip()
                if action in notebooks:
                    self.notebookname = action
                else:
                    if input('Do you want to creat a new notebook titled '+action) in YESTERMS:
                        self.notebookname = action
                        self.db_cursor.execute("INSERT OR REPLACE INTO notebooks (notebook) VALUES (?);",(self.notebookname,))
                        
                 
            elif i in self.QUITTERMS:
                go_on = False

if __name__ == "__main__":

        temp_object = KeyMacroDefinitions()
        temp_object.console()
    

