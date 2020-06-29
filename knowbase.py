"""Module containing knowledgebase
pylint rated 8.62/10
Pylint seems to think variables should be constants,
and objects to definitions outside outer scope of class
"""

import sqlite3

from globalconstants import KNOWLEDGEITERATIONS,\
     QUESTIONMARK, SLASH, TILDA, UNDERLINE, EQUAL, EOL, BLANK, EMPTYCHAR, \
     SHOWTERMS, QUITTERMS, CLEARTERMS, LEARNTERMS, UNLEARNTERMS
from displaylist import DisplayList
from display import Display


class KnowledgeBase():

    """ A very simple knowledgebase designed to store and
    draw inferences from species-genus relations
    """

    def __init__(self,
                 displayobject=None,
                 headings=None,
                 terms=None,
                 notebook=None,
                 using_dict=True,
                 using_database=True):

        self.knowledge_dict = {}
        if not displayobject:
            displayobject = Display()
        self.displayobject = displayobject
        self.notebookname = notebook
        self.using_database = using_database
        self.db_flag = 'd' * using_database + 'o' * using_dict
        
        self.open_connection()

        if not self.notebookname:
            self.notebookname = "GENERALKNOWLEDGE"
        
        if not headings:
            from plainenglish import DefaultConsoles
            self.headings = DefaultConsoles()
        else:
            self.headings = headings
        from plainenglish import ADDTERMS,DELETETERMS,\
                 SHOWTERMS,QUITTERMS,CLEARTERMS, LEARNTERMS, UNLEARNTERMS,\
                 YESTERMS, NOTERMS
        if not terms:
            
            self.ADDTERMS = ADDTERMS
            self.DELETETERMS = DELETETERMS
            self.SHOWTERMS = SHOWTERMS
            self.QUITTERMS = QUITTERMS
            self.CLEARTERMS = CLEARTERMS
            self.LEARNTERMS = LEARNTERMS
            self.UNLEARNTERMS = UNLEARNTERMS
            self.YESTERMS = YESTERMS
            self.NOTERMS = NOTERMS
        else:
            if len(terms)<8: terms = (ADDTERMS,
                                      DELETETERMS,
                                      SHOWTERMS,
                                      QUITTERMS,
                                      CLEARTERMS,
                                      LEARNTERMS,
                                      UNLEARNTERMS,
                                      YESTERMS,
                                      NOTERMS)
            self.ADDTERMS = terms[0]
            self.DELETETERMS = terms[1]
            self.SHOWTERMS = terms[2]
            self.QUITTERMS = terms[3]
            self.CLEARTERMS = terms[4]
            self.LEARNTERMS = terms[5]
            self.UNLEARNTERMS = terms[6]
            self.YESTERMS = terms[7]
            self.NOTERMS = terms[8]

        if self.using_database:
            self.create_database()
            

            
            

    def create_database (self):

        self.db_cursor.executescript("""

            CREATE TABLE IF NOT EXISTS notebooks (
            
                    notebook TEXT NOT NULL UNIQUE);

            CREATE TABLE IF NOT EXISTS things (

                    notebook TEXT NOT NULL,
                    thing TEXT NOT NULL,
                    PRIMARY KEY (notebook, thing)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    );
              
            CREATE TABLE IF NOT EXISTS ontologies (
              
                    notebook TEXT NOT NULL,
                    genus TEXT NOT NULL,
                    species TEXT NOT NULL,
                    PRIMARY KEY (notebook, genus)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    FOREIGN KEY (genus) REFERENCES things (thing) ON DELETE CASCADE
                    FOREIGN KEY (species) REFERENCES things (thing) ON DELETE CASCADE
                    
              );""")


    def open_connection (self):

        self.db_connection = sqlite3.connect('notebooks'+'/'+'ontologies.db')
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
        self.LEARNTERMS = terms[5]
        self.UNLEARNTERMS = terms[6]

    def query (self,term1=None,term2=None,action=None,from_things=False):

        db_result = None
        dict_result = None 
        

        if action == 'get':

            if not term1:
                if 'd' in self.db_flag:
                        value_tuple = (self.notebookname,)
                        self.db_cursor.execute("SELECT genus FROM ontologies"+
                                           " WHERE notebook=?;",value_tuple)
                        temp_results1 = self.db_cursor.fetchall()

            
                        self.db_cursor.execute("SELECT thing FROM things"+
                                           " WHERE notebook=?;",value_tuple)
                        temp_results2 = self.db_cursor.fetchall()
                        temp_results = temp_results1+temp_results2


                        db_result = {x[0] for x in temp_results}
                        

                if 'o' in self.db_flag:

                    dict_result = self.knowledge_dict.keys()
                    

                if 'd' in self.db_flag:
                    return db_result
                else:
                    return dict_result
                
                    

            if 'd' in self.db_flag:

                value_tuple = (self.notebookname,term1)

                self.db_cursor.execute("SELECT species FROM ontologies"+
                                       " WHERE notebook=? AND genus=?;",
                                       value_tuple)                                                   
                temp_results = self.db_cursor.fetchall()

                db_result = {x[0] for x in temp_results}
                

            if 'o' in self.db_flag:
                dict_result = {}
                if term1 in self.knowledge_dict:

                    dict_result = self.knowledge_dict[term1]

            if 'd' in self.db_flag:
                return db_result
            else:
                return dict_result
            
                
        elif action == 'set':

            if not term1 and not term2:
                return False

            if not term2:

                if 'd' in self.db_flag:

                    value_tuple = (self.notebookname, term1,)

                    self.db_cursor.execute("INSERT OR REPLACE"+
                                           " INTO things"+
                                           "(notebook, thing) VALUES (?,?);",
                                           value_tuple)

                    

                    

            if 'd' in self.db_flag and term1 and term2:

                value_tuple = (self.notebookname, term2, )

                self.db_cursor.execute("INSERT OR REPLACE"+
                                       " INTO things"+
                                       "(notebook, thing) VALUES (?,?);",
                                       value_tuple)

                value_tuple = (self.notebookname, term1, term2)
                

                self.db_cursor.execute("INSERT OR REPLACE"+
                                       " INTO ontologies"+
                                       "(notebook, genus, species) VALUES (?,?,?);",
                                       value_tuple)
                
                self.db_connection.commit()

            if 'o' in self.db_flag and term1 and term2:

                if term1 in self.knowledge_dict:
                    temp = self.knowledge_dict[term1]
                    temp.add(term2)
                    self.knowledge_dict[term1] = temp

                else:
                    self.knowledge_dict[term1] = {term2}

                if term2 not in self.knowledge_dict:
                    self.knowledge_dict[term2] = set()

        elif action == 'in':

            if not term1 and not term2:
                return False

            if 'd' in self.db_flag:

                if not from_things:


                    value_tuple = (self.notebookname,term1,)
                    self.db_cursor.execute("SELECT species FROM ontologies"+
                                           " WHERE notebook=? AND genus=?",
                                           value_tuple)                                                   
                    temp_results = self.db_cursor.fetchall()

                    db_result = {x[0] for x in temp_results}
                    if not term2:
                        db_result = (not db_result is None)

                        
                    else:
                        db_result = term2 in db_result


                else:
                    value_tuple = (self.notebookname,)
                    self.db_cursor.execute("SELECT thing FROM things"+
                                       " WHERE notebook=?",
                                       value_tuple)                                                   
                    temp_results = self.db_cursor.fetchall()
                    db_result = {x[0] for x in temp_results}
                    db_result = term1 in db_result
            

            if 'o' in self.db_flag:
                
                dict_result = {}

                if not term2:
                    if not from_things:
                        dict_result = (term1 in self.knowledge_dict and (self.knowledge_dict[term1] != set()))

                    else:
                        dict_result = ((term1 in self.knowledge_dict) and (self.knowledge_dict[term1] == set()))

                        
                elif term1 in self.knowledge_dict:

                    dict_result = (term2 in self.knowledge_dict[term1])

                else:
                    dict_result = (False)



                
            if 'd' in self.db_flag:
                return db_result
            else:
                return dict_result
            
            

        elif action == 'delete':

            if not term1 and not term2:
                if 'd' in self.db_flag:
                    print('DELETING')

                    self.db_cursor.execute("DELETE FROM ontologies "+
                      " WHERE notebook=?;",(self.notebookname,))

                    self.db_connection.commit()
                    

                if 'o' in self.db_flag:
                    self.knowledge_dict = {}
                    

            if 'd' in self.db_flag:

            
                value_tuple = (self.notebookname,term1,term2) 
                self.db_cursor.execute("DELETE FROM ontologies "+
                                      " WHERE notebook=? and genus=? and species=?;",
                                      value_tuple)

                self.db_connection.commit()

            if 'o' in self.db_flag:

                if term1 in self.knowledge_dict:
                    temp = self.knowledge_dict[term1]
                    temp.discard(term2)
                    self.knowledge_dict[term1] = temp

    def expose(self):

        if 'd' in self.db_flag:
            self.db_cursor.execute("SELECT * FROM things")
            print(self.db_cursor.fetchall())
            self.db_cursor.execute("SELECT * FROM ontologies")
            print(self.db_cursor.fetchall())
        if 'o' in self.db_flag:

            print(self.knowledge_dict)
            
    
    def learn(self, species, genus):

        """Teaches knowledge base that species is genus"""

        self.query(term1=genus,term2=species,action='set')


    def learned(self, item):

        """Tests knowledge of knowledge base"""

        return self.query(term1=item,action='in')

    def species(self, item):

        """Tests to see whether item is a species,
        i.e. at lower leve.
        """


        if not self.query(term1=item,action='in',from_things=True):
            return False
        if not len(self.query(term1=item,action='get'))>0:
            return True
        return False

    def genus(self, item):

        """Tests to see if an item is a genus,
        i.e. not at lower level
        """


        if len(self.query(term1=item,action='get'))>0:
            return True
        if not self.query(term1=item,action='in',from_things=True):
            return False
        return True

    def unlearn(self, species, genus):

        """unlearns that species is genus"""

        self.query(term1=genus,term2=species,action='delete')

    def load(self, entrylist):

        """Loads in a list of facts into the knowledgebase"""

        obj = self.learn
        for line in entrylist:
            line = line.lstrip(UNDERLINE).replace(UNDERLINE,BLANK)
            if line[0] == TILDA:
                obj = self.unlearn
            if SLASH in line:
                tag, definitions = line.split(SLASH)[0], line.split(SLASH)[1]
                if EQUAL in definitions:
                    definitions = [tag]+definitions.split(EQUAL)
                else:
                    definitions = [tag]+[definitions]

            else:
                definitions = line.split(EQUAL)


            if len(definitions) > 1:
                for r_temp in range(0,
                                    len(definitions)-1):
                    obj(definitions[r_temp],
                        definitions[r_temp+1])


    def reveal(self, genus):

        """Reveals knowledge"""
        if not self.query(term1=genus,action='in'):
            return set()
        found_higher = {genus}
        found_lowest = set()

        not_done = True
        counter = 0
        while not_done and counter <= KNOWLEDGEITERATIONS:

            # Second condition to prevent infinite loops

            counter += 1
            for g_temp in set(found_higher): #to freeze set for iteration
                found_higher.discard(g_temp)

                if self.query(term1=g_temp,action='in'):
                    found_higher.update(self.query(term1=g_temp,action='get'))  
                    found_lowest.update(self.query(term1=g_temp,action='get'))
                else:
                    found_lowest.add(g_temp)

            if not found_higher:
                not_done = False
        return found_lowest


    def bore(self, listobject=None):

        """recite all knowledge"""
        listobject = DisplayList(displayobject=self.displayobject)

        if listobject is None:
            listobject = []

        for  k in self.query(action='get'):
            l_temp = self.query(term1=k,action='get')
            if l_temp == set():
                listobject.append(self.headings.I_KNOW
                                  +k+self.headings.IS_WHAT_IT_IS)
            else:
                for m_temp in l_temp:
                    listobject.append(self.headings.I_KNOW
                                      +m_temp+self.headings.IS_AN+k)
        if isinstance(listobject,list):
            print(listobject)
        else:
            listobject.show()

    def record(self):

        listobject = []

        for k in  self.query(action='get'):
            l_temp = self.query(term1=k,action='get')
            if l_temp == set():
                pass
            else:
                for m_temp in l_temp:
                    listobject.append((m_temp+EQUAL+k).replace(BLANK,UNDERLINE))
                    
        return EOL.join(listobject)

    def console(self):

        """ opens up console for adding and deleting """

        go_on = True
        while go_on:
            console = DisplayList([self.headings.LEARN_MENU,
                                   self.headings.UNLEARN_MENU,
                                   self.headings.SHOW_MENU,
                                   self.headings.CLEAR_MENU,
                                   self.headings.QUIT_MENU,
                                   'N)otebook'*self.using_database],
                                   displayobject=self.displayobject)
            i = input()
            if i in self.LEARNTERMS:

                self.learn(input(self.headings.LEARN_THAT_THIS), input(self.headings.IS_WHAT))
            elif i in self.UNLEARNTERMS:

                self.unlearn(input(self.headings.UNLEARN_THAT_THIS), input(self.headings.IS_WHAT))
            elif i in self.SHOWTERMS:
                self.bore()
            elif i in ['n','N'] and self.using_database:
                self.db_cursor.execute('SELECT notebook FROM notebooks')
                notebooks = [x[0] for x in self.db_cursor.fetchall()]
                self.displayobject.noteprint(('NOTEBOOKS','\n'.join(notebooks)))
                action = input('NAME OF EXISTING OR NEW NOTEBOOK?').strip()
                if action in notebooks:
                    self.notebookname = action

            elif i in self.CLEARTERMS:
                if input(self.headings.ARE_YOU_SURE) in self.YESTERMS:
                    self.query(action='delete')
                    self.db_cursor.execute("DELETE FROM things WHERE notebook=?;",(self.notebookname,))
                    self.db_connection.commit()
                    
                                   
            elif i in self.QUITTERMS:
                go_on = False

    def export_string(self):

        """ Exports string of dictionary for database"""

        return str(self.knowledge_dict)

    def import_string(self,string):

        """ Imports string from database"""

        self.knowledge_dict = eval(string)



if __name__ == "__main__":

    knower = KnowledgeBase()
    keep_going = True
    while keep_going:

        knower.expose()
        knower.console()

##        say_what = input('Teach me!')
##        if (say_what.startswith('=')
##                or say_what.startswith('=')):
##            genus = say_what.split('=')[1].strip().replace(QUESTIONMARK, EMPTYCHAR)
##            print('Maybe I know this!')
##            answers = knower.reveal(genus)
##            if not answers:
##                print("I'm stumped!")
##            else:
##                for species in answers:
##                    print(species, ' is a '+genus)
##
##
##        elif '|' in say_what:
##            species = say_what.split('|')[0].strip()
##            genus = say_what.split('|')[1].strip()
##
##
##            knower.learn(species,genus)
##            print('I learned that '
##                  +species+' is a '+genus)
##            
####            print(knower.query(term1=genus,action='in'))
####            print(knower.query(term1=genus,action='in',from_things=True))
####            print(knower.query(term1=genus,term2=species,action='in'))
####            print(knower.query(term1=genus,action='get'))
####            print(knower.query(term1=genus,term2=species,action='get'))
####            print(knower.query(term1=genus,action='get',from_things=True))
##            
##
##        elif say_what in ['bored now',
##                          'stop',
##                          'had enought',
##                          'quit']:
##
##            keep_going = False
##
##            print('See you later!')
##            print('But first let me bore you with everything I know!')
##            knower.bore()
