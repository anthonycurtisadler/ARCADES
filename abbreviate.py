"""Module for keeping track of abbreviations that are applied to notes
pylint rated 9.63/10
"""


from displaylist import DisplayList
from globalconstants import YESTERMS, ADDTERMS, DELETETERMS, CLEARTERMS, \
     LEFTNOTE, RIGHTNOTE, LEFTCURLY, RIGHTCURLY, BLANK, COLON, QUESTIONMARK, UNDERLINE,\
     EMPTYCHAR, SHOWTERMS, QUITTERMS, EQUAL,EOL, TILDA

import presets

from display import Display
import sqlite3

class Abbreviate:


    """ Holds and applies preset transformations
    Do applies a transformation, undo undoes it.
    This is needed in order to allow arrow brackets
    and curly brackets in the note text...
    These should be preceded with a single underscore
    """

    def __init__(self,
                 newdefaults=None,
                 use_presets=False,
                 displayobject=None,
                 headings=None,
                 terms=None,
                 presets=None,
                 using_database=False,
                 objectname=None):


        self.default_debreviations = {}
        self.default_abbreviations = {}
        self.create_objects()
        #displayobject must be passed in
        if objectname is None:
            objectname = 'macros.db'
        self.objectname = objectname 
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
        
        if newdefaults is None:
            newdefaults = {}
        if presets is None:
            presets = {}
        

            


        self.load_presets(presets)
        self.load_defaults(newdefaults)

        


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

 
    def load_defaults (self,newdefaults):
        if 'o' in self.db_flag:

            self.default_debreviations.update(newdefaults)
            self.default_abbreviations = {value:key for  key,
                                          value in self.default_debreviations.items()}
        if 'd' in self.db_flag:

            for x in newdefaults:

                self.query(term1='db',term2=x,term3=newdefaults[x],action='set')
                self.query(term1='ab',term2=newdefaults[x],term3=x,action='set')



    def create_objects (self):

        self.dict_object_dict= {'ab':self.default_abbreviations,
                       'db':self.default_debreviations}

        self.get_script_two_dict = {'ab':"SELECT definition FROM abbreviations WHERE notebook=? AND key=?",
                      'db':"SELECT key FROM debreviations WHERE notebook=? AND definition=?"}

        self.get_script_one_dict = {'ab':"SELECT key FROM abbreviations WHERE notebook=?",
                         'db':"SELECT definition FROM debreviations WHERE notebook=?"}

        self.get_script_items_dict = {'ab':"SELECT key, definition FROM abbreviations WHERE notebook=?",
                         'db':"SELECT definition, key FROM debreviations WHERE notebook=?"}

        self.set_script_dict = {'ab':"INSERT OR REPLACE INTO abbreviations (notebook, key, definition) VALUES (?,?,?);",
                      'db':"INSERT OR REPLACE INTO debreviations (notebook, definition, key) VALUES (?,?,?);"}

        self.delete_script_two_dict = {'ab':"DELETE FROM abbreviations WHERE notebook=? AND key=? AND definition=?",
                             'db':"DELETE FROM debreviations WHERE notebook=? AND definition=? AND key=?"}

        self.delete_script_one_dict = {'ab':"DELETE FROM abbreviations WHERE notebook=? AND key=?",
                             'db':"DELETE FROM debreviations WHERE notebook=? AND definition=?"}

        self.delete_script_none_dict = {'ab':"DELETE FROM abbreviations WHERE notebook=?",
                             'db':"DELETE FROM debreviations WHERE notebook=?"}



    def load_presets (self,presets):


        if 'o' in self.db_flag:

            self.default_debreviations.update(presets)
            self.default_abbreviations = {value:key for  key,
                                          value in self.default_debreviations.items()}
        if 'd' in self.db_flag:

            self.db_cursor.execute("SELECT * FROM debreviations")
            if len(self.db_cursor.fetchall()) < 10:
                self.displayobject.noteprint(('ATTENTION!','LOADING PRESETS'))

                for x in presets:

                        self.query(term1='db',term2=x,term3=presets[x],action='set')
                        self.query(term1='ab',term2=presets[x],term3=x,action='set')
            else:
                self.displayobject.noteprint(('ATTENTION!','PRESETS ALREADY LOADED'))
                    
                
    def create_database (self):

        self.db_cursor.executescript("""

            CREATE TABLE IF NOT EXISTS notebooks (
            
                    notebook TEXT NOT NULL UNIQUE);

              
            CREATE TABLE IF NOT EXISTS abbreviations (
              
                    notebook TEXT NOT NULL,
                    key TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    
                    PRIMARY KEY (notebook, key)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    
              );

            CREATE TABLE IF NOT EXISTS debreviations (
              
                    notebook TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    key TEXT NOT NULL,
                    
                    PRIMARY KEY (notebook, definition)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    
              );
              """)

    def open_connection (self):

        self.db_connection = sqlite3.connect('notebooks'+'/'+self.objectname)
        self.db_cursor = self.db_connection.cursor()                                         

    def purge_connection (self):

        self.db_connection = None
        self.db_cursor = None
       
    def expose (self):

        print(self.default_abbreviations)
        print(self.default_debreviations)

        if self.using_database:
            self.db_cursor.execute("SELECT * FROM abbreviations")
            print(self.db_cursor.fetchall())
            self.db_cursor.execute("SELECT * FROM debreviations")
            print(self.db_cursor.fetchall())
        

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
        

        #TERM 1 "ab" or "db" for ABBREVIATE or DEBREVIATE 

        dict_object = self.dict_object_dict[term1]

        get_script_two = self.get_script_two_dict[term1]

        get_script_one = self.get_script_one_dict[term1]

        set_script = self.set_script_dict[term1]

        delete_script_two = self.delete_script_two_dict[term1]

        delete_script_one = self.delete_script_one_dict[term1]

        delete_script_none = self.delete_script_none_dict[term1]

        get_script_items = self.get_script_items_dict[term1]

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

        if action == 'getitems':

            dict_result, data_result = None, None

            if 'o' in self.db_flag:

                dict_result = dict_object.items()

            if 'd' in self.db_flag:

                self.db_cursor.execute(get_script_items,value_tuple[0:1])
                data_result = self.db_cursor.fetchall()
                data_result = [(x[0],x[1]) for x in data_result]


            if 'd' in self.db_flag:
                return data_result
            else:
                return dict_result

                
                

                
            
        
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
                    
                else:
                    self.db_cursor.execute(delete_script_none,value_tuple[0:1])
                self.db_connection.commit()
                    

        
        
           
    def do(self,
           text,
           lchar=UNDERLINE,
           rchar=EMPTYCHAR):

        """ to apply 'debreviations'=shorter to longer.
        These must be preceded with _.
        This is mainly done in order to circumvent
        reserved characters <>{} in entering text.
        """

        keys = reversed(sorted(self.query(term1='db',action='get')))
        for key in keys:
            value = self.query(term1='db',term2=key,action='get')[0]
            text = text.replace(lchar+key+rchar, value)

        return text

    def undo(self,
             text,
             lchar=EMPTYCHAR,
             rchar=EMPTYCHAR):

        """apply 'abbreviations' ---
        The reverse of debreviations.
        """

        for key, value in self.query(term1='ab',action='getitems'):
            text = text.replace(lchar+key+rchar, value)

        return text

    def add(self,
            from_this,
            to_this,
            no_query=False):

        """add a conversion formula
        to the abbreviation/debreviation dictionary
        """

        if (not self.query(term1='db',term2=from_this,action='in')
                and  not self.query(term1='ab',term2=to_this,action='in')
                and (no_query or input(self.headings.ADD
                                       +from_this
                                       +BLANK+COLON+BLANK
                                       +to_this+QUESTIONMARK) in YESTERMS+[EMPTYCHAR])):
            self.query(term1='db',term2=from_this,term3=to_this,action='set')
            self.query(term1='ab',term2=to_this,term3=from_this,action='set')
            
    def delete(self,
               from_this,
               to_this):

        """delete a conversion formulat from the
        abbreviation/debreviation dictionary"""

        if (from_this in self.default_debreviations
                and to_this in self.default_abbreviations
                and from_this not in [LEFTCURLY, RIGHTCURLY, LEFTNOTE, RIGHTNOTE] and
                input('Delete|'+from_this+BLANK+COLON+BLANK+to_this) in YESTERMS):

            self.displayobject.noteprint((self.headings.DELETING, EMPTYCHAR))
            self.query(term1='db',term2=from_this,action='delete')
            self.query(term1='ab',term2=to_this,action='delete')

    def show(self,returntext=False):

        """show all the stored debreviations"""
        if not returntext:
            show_debreviations = DisplayList(displayobject=self.displayobject)
            spacer = BLANK
        else:
            show_debreviations = []
            spacer = EMPTYCHAR
        for counter, key in enumerate(sorted(self.query(term1='db',action='get'))):
            if not returntext:
                countermark = str(counter+1)
            else:
                countermark = EMPTYCHAR
            deb_temp = self.query(term1='db',term2=key,action='get')
            for x in deb_temp:
                if returntext:
                    x = x.replace(BLANK,TILDA)                                        
                show_debreviations.append(countermark+spacer+key+EQUAL+x)
        if returntext:
            return EOL.join(show_debreviations)
        show_debreviations.present()

    def load(self,
             entrylist):

        """load a list in... LOAD is standard method name for analogous classes... """

        for l_temp in entrylist:
            from_to = l_temp.split(EQUAL)
            from_this = from_to[0].replace(UNDERLINE, EMPTYCHAR)
            to_this = from_to[1].replace(UNDERLINE,BLANK).replace(TILDA,BLANK)
            self.add(from_this.strip(), to_this.strip(), no_query=True)
        self.show()

    def export_string(self):

        """Exports string for database archiving"""

        return str(self.default_debreviations) + '!@#BREAK!@#' + str(self.default_abbreviations)

    def import_string(self,text):

        """Imports string from archive"""

        text1,text2 = text.split('!@#BREAK!@#')
        self.default_debreviations = eval(text1)
        self.default_abbreviations = eval(text2)
        
        

    def console(self):

        """ opens up console for adding and deleting """

        go_on = True
        while go_on:
            console = DisplayList([self.headings.ADD_MENU,
                                   self.headings.DELETE_MENU,
                                   self.headings.SHOW_MENU,
                                   self.headings.CLEAR_MENU,
                                   self.headings.QUIT_MENU,
                                   'N)otebook'*self.using_database],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.ADDTERMS:

                self.add(input(self.headings.FROM_THIS), input(self.headings.TO_THIS))
            elif i in self.DELETETERMS:

                while True:
                    self.show()
                    to_delete = input (self.headings.DELETE)
                    if to_delete == EMPTYCHAR:
                        break
                    if to_delete.isnumeric() and int(to_delete) > 0 and int(to_delete) < len(self.query(term1='db',action='get'))+1:
                        from_temp = sorted(self.query(term1='db',action='get'))[int(to_delete)-1]
                        to_temp = self.query(term1='db',term2=from_temp,action='delete')
                        self.delete(from_temp,to_temp)
            elif i in self.SHOWTERMS:
                self.show()

            elif i in ['n','N'] and self.using_database:
                self.db_cursor.execute('SELECT notebook FROM notebooks')
                notebooks = [x[0] for x in self.db_cursor.fetchall()]
                self.displayobject.noteprint(('NOTEBOOKS','\n'.join(notebooks)))
                action = input('NAME OF EXISTING OR NEW NOTEBOOK?').strip()
                if action in notebooks:
                    self.notebookname = action

            elif i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                    if input(self.headings.ARE_YOU_SURE) in YESTERMS:
                        self.query(term1='ab',action='delete')
                        self.query(term1='db',action='delete')
            elif i in self.QUITTERMS:
                go_on = False

if __name__ == "__main__":

        temp_object = Abbreviate()
        temp_object.console()
