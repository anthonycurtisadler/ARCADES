"""Module containing the class which stores and applies key definitions
pylint rated 10.0/10
"""

import nformat
from displaylist import DisplayList
from globalconstants import COLON, COMMA, UNDERLINE, TILDA
from globalconstants import YESTERMS, ADDTERMS, DELETETERMS, CLEARTERMS, \
     LEFTNOTE, RIGHTNOTE, LEFTCURLY, RIGHTCURLY, EOL, BLANK, COLON, QUESTIONMARK, UNDERLINE,\
     EMPTYCHAR, SHOWTERMS, QUITTERMS, EQUAL

from display import Display
import sqlite3

class KeyDefinitions:


    """ Holds and applies key definitions, which are
    used to automatically assign keys to notes
    according the words found in them.
    """

    def __init__(self, displayobject=None, headings=None, terms=None, using_database=True):

        self.key_definitions = {}
        self.definition_keys = {}
        if not displayobject:
            displayobject = Display()
        self.displayobject = displayobject
        self.using_database = using_database
        if self.using_database:
            self.notebookname = 'GENERAL'
            self.open_connection()
            self.create_database()
            self.db_cursor.execute("INSERT OR REPLACE INTO notebooks (notebook) VALUES (?);",(self.notebookname,))
            self.db_connection.commit()
            self.db_flag = 'd'
        else:
            self.db_flag = 'o'
            self.notebookname = None
        
        

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

        self.dict_object_dict= {'kd':self.key_definitions,
                       'dk':self.definition_keys}

        self.get_script_two_dict = {'kd':"SELECT definition FROM key_definitions WHERE notebook=? AND key=?",
                      'dk':"SELECT key FROM definition_keys WHERE notebook=? AND definition=?"}

        self.get_script_one_dict = {'kd':"SELECT key FROM key_definitions WHERE notebook=?",
                         'dk':"SELECT definition FROM definition_keys WHERE notebook=?"}

        self.set_script_dict = {'kd':"INSERT OR REPLACE INTO key_definitions (notebook, key, definition) VALUES (?,?,?);",
                      'dk':"INSERT OR REPLACE INTO definition_keys (notebook, definition, key) VALUES (?,?,?);"}

        self.delete_script_two_dict = {'kd':"DELETE FROM key_definitions WHERE notebook=? AND key=? AND definition=?",
                             'dk':"DELETE FROM definition_keys WHERE notebook=? AND definition=? AND key=?"}

        self.delete_script_one_dict = {'kd':"DELETE FROM key_definitions WHERE notebook=? AND key=?",
                             'dk':"DELETE FROM definition_keys WHERE notebook=? AND definition=?"}

        self.delete_script_none_dict = {'kd':"DELETE FROM key_definitions WHERE notebook=?",
                             'dk':"DELETE FROM definition_keys WHERE notebook=?"}

    def create_database (self):

        self.db_cursor.executescript("""

            CREATE TABLE IF NOT EXISTS notebooks (
            
                    notebook TEXT NOT NULL UNIQUE);

              
            CREATE TABLE IF NOT EXISTS key_definitions (
              
                    notebook TEXT NOT NULL,
                    key TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    
                    PRIMARY KEY (notebook, key)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    
              );

            CREATE TABLE IF NOT EXISTS definition_keys (
              
                    notebook TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    key TEXT NOT NULL,
                    
                    PRIMARY KEY (notebook, definition)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    
              );
              """)
    def expose (self):

        print(self.key_definitions)
        print(self.definition_keys)

        if self.using_database:
            self.db_cursor.execute("SELECT * FROM key_definitions")
            print(self.db_cursor.fetchall())
            self.db_cursor.execute("SELECT * FROM definition_keys")
            print(self.db_cursor.fetchall())
        

    def open_connection (self):

        self.db_connection = sqlite3.connect('notebooks'+'/'+'macros.db')
        self.db_cursor = self.db_connection.cursor()                                         

    def purge_connection (self):

        self.db_connection = None
        self.db_cursor = None
       

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

    def query (self,term1=None,term2=None,term3=None,action=None):

        dict_object = self.dict_object_dict[term1]

        get_script_two = self.get_script_two_dict[term1]

        get_script_one = self.get_script_one_dict[term1]

        set_script = self.set_script_dict[term1]

        delete_script_two = self.delete_script_two_dict[term1]

        delete_script_one = self.delete_script_one_dict[term1]

        delete_script_none = self.delete_script_none_dict[term1]

        value_tuple = (self.notebookname,term2,term3,)

        if action == 'set':

            if 'o' in self.db_flag:

                if term2 in dict_object:
                    dict_object[term2].add(term3)
                else:
                    dict_object[term2] = {term3}

            if 'd' in self.db_flag:
                self.db_cursor.execute(set_script,value_tuple)
                self.db_connection.commit()

        if action == 'get':

            dict_result, data_result = None, None

            if 'o' in self.db_flag:

                if not term2:

                    dict_result = dict_object.keys()
                else:
                    if term2 in dict_object:
                        dict_result = dict_object[term2]
                    else:
                        dict_result = {}

                

            if 'd' in self.db_flag:

                if not term2:
                    self.db_cursor.execute(get_script_one,value_tuple[0:1])
                else:
                    self.db_cursor.execute(get_script_two,value_tuple[0:2])
                data_result = self.db_cursor.fetchall()
                data_result = [x[0] for x in data_result]

            if 'd' in self.db_flag:
                return data_result
            else:
                return dict_result

        if action == 'in':

            dict_result, data_result = None, None

            if 'o' in self.db_flag:

                if not term3:

                    dict_result = dict_object.keys()
                    in_term = term2
                    
                else:
                    if term2 in dict_object:
                        dict_result = dict_object[term2]
                    else:
                        dict_result = {}
                    in_term = term3

                

            if 'd' in self.db_flag:

                if not term3:
                    self.db_cursor.execute(get_script_one,value_tuple[0:1])
                    in_term = term2 
                else:
                    self.db_cursor.execute(get_script_two,value_tuple[0:2])
                    in_term = term3
                data_result = self.db_cursor.fetchall()
                data_result = [x[0] for x in data_result]

            if 'd' in self.db_flag:
                return in_term in data_result
            else:
                return in_term in dict_result

            


        if action == 'delete':

            if 'o' in self.db_flag:

                if not term3 and term2:

                    if term2 in dict_object:
                        del dict_object[term2]

                elif term3 and term2:
                    if term2 in dict_object:
                        x =  dict_object[term2]
                        x.discard(term3)
                        
                        dict_object[term2] = x
                        
                        if not dict_object[term2]:
                            del dict_object[term2]
                elif not term3 and not term2:
                    for x in list(dict_object):
                        del dict_object[x]
                        

            if 'd' in self.db_flag:


                if not term3 and term2:

                    self.db_cursor.execute(delete_script_one,value_tuple[0:2])
                elif term2:
                    self.db_cursor.execute(delete_script_two,value_tuple)
                    self.db_connection.commit()
                else:
                    self.db_cursor.execute(delete_script_none,value_tuple[0:1])
                    

        

    def add(self, keyword, definitions):

        """add keyword and definition"""
        for x_temp in definitions:
            self.query(term1='kd',term2=keyword,term3=x_temp.strip(),action='set')
            
        for d_temp in definitions:
            self.query(term1='dk',term2=d_temp.strip(),term3=keyword,action='set')
            
    def delete(self, keyword, definitions):

        """delete keyword and definitions
        """

        definitionscopy = list(definitions) 
        if self.query(term1='kd',term2=keyword,action='in'):
            for d_temp in list(definitions):
                self.query('kd',term2=keyword,term3=d_temp,action='delete')



        
        for d_temp in definitionscopy:

            if self.query(term1='dk',term2=d_temp,action='in'):
                self.query(term1='dk',term2=d_temp,term3=keyword,action='delete')


    def get_definition(self, keyword):

        """get definitions for a given keyword"""

        if self.query(term1='kd',term2=keyword,action='in'):
            return self.query(term1='kd',term2=keyword,action='get')
        return {}

    def get_key(self, definition):

        """get keywords for a given definition"""

        if self.query(term1='dk',term2=definition,action='in'):
            return self.query(term1='dk',term2=definition,action='get')
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
        

        for counter, k_temp in enumerate(sorted(list(self.query(term1='kd',action='get')),
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

    def export_string (self):

        """Outputs string for archiving in database"""

        return str(self.key_definitions)+'!@#BREAK!@#'+str(self.definition_keys)

    def import_string (self,text):

        """Reconstritutes dictionaries from archived string"""


        text1,text2 = text.split('!@#BREAK!@#')

        self.key_definitions = eval(text1)
        self.definition_keys = eval(text2)
   
    def show_dk(self):

        """show definitions with keys

        For reasons that I do not understand,
        I need to add this blank space to
        keep the formatting normal when
        displaying the note...
        """

        show_definitions = DisplayList(displayobject=self.displayobject)

        for counter, d_temp in enumerate(sorted(list(self.query(term1='dk',action='get')),
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
                                   self.headings.QUIT_MENU,
                                   '(N)otebook'*self.using_database],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.ADDTERMS:

                self.add(input(self.headings.KEYS), [x_temp.strip() for x_temp in input(self.headings.DEFINITIONS).split(',')])
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
                        
                        self.delete(from_temp,to_temp)

            elif i in self.SHOWTERMS:
                self.show_kd()
                self.show_dk()
            elif i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                    self.query(term1='dk',action='delete')
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

        temp_object = KeyDefinitions()
        temp_object.console()
    

