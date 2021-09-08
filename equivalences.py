## Keeps track of equivalent terms ##

import sqlite3
import random
from display import Display
from displaylist import DisplayList

class Equivalences:

    def __init__ (self,directoryname=None,filename=None,testing=False):

        if filename:
               self.notebookname = filename
        else:
               self.notebookname = 'GENERALKNOWLEDGE'

        self.open_connection()
        self.create_database()
        self.display = Display()
        self.active = True
        self.testing = testing 
        
        

    def open_connection (self):

          self.db_connection = sqlite3.connect('notebooks'+'/'+'equivalences.db')
          self.db_cursor = self.db_connection.cursor()

    def purge_connection (self):

          self.db_connection = None
          self.db_cursor = None

    def close (self):

          if self.using_database:

               self.db_connection.close()

    def create_database (self):

          

          self.db_cursor.executescript("""
          CREATE TABLE IF NOT EXISTS notebooks (
          notebook TEXT NOT NULL UNIQUE);

          

          CREATE TABLE IF NOT EXISTS classes (
          
               notebook TEXT NOT NULL,
               class INTEGER NOT NULL,
               UNIQUE (notebook, class)
               PRIMARY KEY (notebook, class)
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
          );
          
          
          CREATE TABLE IF NOT EXISTS terms (
          
               notebook TEXT NOT NULL,
               term TEXT NOT NULL,
               class INTEGER NOT NULL,
               UNIQUE (notebook, term)
               PRIMARY KEY (notebook, term)
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
               FOREIGN KEY (notebook, class) REFERENCES classes (notebook, class) ON DELETE CASCADE
          );
          CREATE TABLE IF NOT EXISTS terms_for_classes (
          
               notebook TEXT NOT NULL,
               class INTEGER NOT NULL,
               term TEXT NOT NULL,
               UNIQUE (notebook, class, term)
               PRIMARY KEY (notebook, class, term)
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
               FOREIGN KEY (notebook, class) REFERENCES classes (notebook, class) ON DELETE CASCADE
               FOREIGN KEY (notebook, term) REFERENCES terms (notebook, term) ON DELETE CASCADE
          );
          
          
          """)

    ## INTERNAL METHODS
          

    def get_notebooks (self):

        self.db_cursor.execute ("SELECT notebook FROM notebooks")
        temp_results = self.db_cursor.fetchall()
        return {x[0] for x in temp_results}

    def add_notebook (self,
                      notebook):

        value_tuple = (notebook,)

        self.db_cursor.execute("INSERT OR REPLACE INTO notebooks"+
                             "(notebook) VALUES (?);",
                                                     value_tuple)

    def get_terms (self,
                   notebook):

        value_tuple = (notebook,)
        self.db_cursor.execute ("SELECT term FROM terms WHERE notebook=?;",value_tuple)
        temp_results = self.db_cursor.fetchall()
        return {x[0] for x in temp_results}

    def get_classes (self,
                     notebook):

        value_tuple = (notebook,)
        self.db_cursor.execute ("SELECT class FROM classes WHERE notebook=?;",value_tuple)
        temp_results = self.db_cursor.fetchall()
        if temp_results:
            return {int(x[0]) for x in temp_results}
        return {}
        
    def exists_term (self,
                     notebook,
                     term):

        return term in self.get_terms (notebook)

    def exists_class (self,
                      notebook,
                      class_value):
        return class_value in self.get_classes (notebook)

    def add_class (self,
                   notebook,
                   class_value):

        value_tuple = (notebook,str(class_value))

        self.db_cursor.execute("INSERT OR REPLACE INTO classes"+
                             "(notebook, class) VALUES (?,?);",
                                                     value_tuple)

    def add_term (self,
                  notebook,
                  term,
                  class_value):
        if not self.exists_class(notebook,class_value):
            self.add_class(notebook,
                           class_value)


        value_tuple = (notebook,term,str(class_value))

        
        
        self.db_cursor.execute("INSERT OR REPLACE INTO terms"+
                             "(notebook, term, class) VALUES (?,?,?);",
                                                     value_tuple)
        
        
    def get_class_for_term (self,
                            notebook,
                            term):

        value_tuple = (notebook,term)
        self.db_cursor.execute ("SELECT class FROM terms WHERE notebook=? and term=?;",value_tuple)
        temp_results = self.db_cursor.fetchall()
        if temp_results:
            return [int(x[0]) for x in temp_results][0]
        else:
            return None 

    def add_term_for_class  (self,
                              notebook,
                              class_value,
                              term):

         value_tuple = (notebook,str(class_value),term)
         self.db_cursor.execute("INSERT OR REPLACE INTO terms_for_classes"+
                             "(notebook, class, term) VALUES (?,?,?);",
                                                     value_tuple)

    def add_new_equivalence (self,
                  notebook,
                  term,
                  equivalent):

        if term == equivalent:

            if not self.exists_term(notebook,term):

                

                new_class = self.get_classes(notebook)
                
                if not new_class:
                    new_class = 0
                elif len(new_class)==max(new_class)+1:
                    new_class = max(new_class)+1
                else:
                    count = 0
                    while count in new_class:
                        count += 1
                    new_class = count
                        

                self.add_term (notebook,
                               term,
                               new_class)

                self.add_term_for_class (notebook,
                                         new_class,
                                         term)

        else:

            if not self.exists_term(notebook,
                                    term):

                self.add_new_equivalence(notebook,
                                         term,
                                         term)
            if self.exists_term(notebook,
                                equivalent):
                pass
            else:

                existing_class = self.get_class_for_term (notebook,
                                                          term)

                self.add_term (notebook,
                               equivalent,
                               existing_class)

                self.add_term_for_class (notebook,
                                         existing_class,
                                         equivalent)


    def get_all_terms_for_class (self,
                                 notebook,
                                 class_value):
    
        value_tuple = (notebook,str(class_value))
        self.db_cursor.execute ("SELECT term FROM terms_for_classes WHERE notebook=? and class=?;",value_tuple)
        temp_results = self.db_cursor.fetchall()
        return {x[0] for x in temp_results}
        
    def get_class_pairs (self,
                       notebook):

        value_tuple = (notebook,)
        self.db_cursor.execute ("SELECT class, term FROM terms_for_classes WHERE notebook=?;",value_tuple)
        
        temp_results = self.db_cursor.fetchall()
        return {(x[0],x[1]) for x in temp_results}

    def get_term_pairs (self,
                       notebook):

        value_tuple = (notebook,)
        self.db_cursor.execute ("SELECT term, class FROM terms WHERE notebook=?;",value_tuple)
        
        temp_results = self.db_cursor.fetchall()
        return {(x[0],x[1]) for x in temp_results}
        

    def delete_terms_for_class (self,
                                    notebook,
                                    class_value):

        value_tuple = (notebook,str(class_value))
        
        self.db_cursor.execute("DELETE FROM terms_for_classes WHERE notebook=? and class=?;",
                               value_tuple)

    def delete_term (self,
                notebook,
                term):


        value_tuple = (notebook,term)
        
        self.db_cursor.execute("DELETE FROM terms WHERE notebook=? and term=?;",
                               value_tuple)
       
    def delete_single_term (self,
                            notebook,
                            term):
        class_value = self.get_class_for_term(notebook,term)
        self.delete_term(notebook,term)
        value_tuple = (notebook,term)
        self.db_cursor.execute("DELETE FROM terms_for_classes WHERE notebook=? and term=?;",
                               value_tuple)
        self.cascade_term (notebook,class_value)
        self.db_connection.commit()
        

    def delete_class (self,
                      notebook,
                      class_value):

        value_tuple = (notebook,str(class_value))
        
        self.db_cursor.execute("DELETE FROM classes WHERE notebook=? and class=?;",
                               value_tuple)

    def cascade_term (self,
                      notebook,
                      class_value):
        value_tuple = (notebook,
                       str(class_value))
        self.db_cursor.execute("SELECT term FROM terms_for_classes where notebook=? and class=?",value_tuple)
        temp_results = self.db_cursor.fetchall()
        if not(temp_results):

            self.delete_class(notebook,class_value)

    
        

    def delete_all_equivalences (self,
                             notebook,
                             term):

        class_value = self.get_class_for_term (notebook,
                                               term)
        all_terms = self.get_all_terms_for_class(notebook,
                                                 class_value)
        self.delete_terms_for_class (notebook,
                                     class_value)
        for term in all_terms:
            self.delete_term (notebook,
                              term)
        self.delete_class(notebook,
                          class_value)
        self.db_connection.commit()

    def join_terms_in_equivalence_class (self,
                      notebook,
                      term_list):

        if not len(term_list)>1:
            return False
        first_term = term_list[0]
        for second_term in term_list[1:]:
            self.add_new_equivalence(self.notebookname,first_term,second_term)
        self.db_connection.commit()
            

    def merge_equivalence_classes (self,
                                   notebook,
                                   term1,
                                   term2):

        if not (self.exists_term(notebook,
                                term1) and
                self.exists_term(notebook,
                                 term2)):
            return False

        first_class = self.get_class_for_term (notebook,
                                               term1)
        second_class = self.get_class_for_term (notebook,
                                                term2)

        if first_class == second_class:
            return False

        first_terms = self.get_all_terms_for_class(notebook,
                                            first_class)

        second_terms = self.get_all_terms_for_class(notebook,
                                            second_class)


        self.delete_all_equivalences (notebook,
                                      term1)
        self.delete_all_equivalences (notebook,
                                      term2)

        self.join_terms_in_equivalence_class(notebook,
                                             list(first_terms)+list(second_terms))

        self.db_connection.commit()

    def is_valid (self,notebook):

        # TESTS to see if the database is in regular form

        splice = lambda x,y:{z[y] for z in x}
        leftsplice = lambda x:splice(x,0)
        rightsplice = lambda x:splice(x,1)
        def apply (entered_set, x):
            returnset = set()
            for a in entered_set:
                if a[0] == x:
                    returnset.add(a[1])
            return returnset
        

        
        classes = self.get_classes(notebook)
        term_pairs = self.get_term_pairs(notebook)
        class_pairs = self.get_class_pairs(notebook)
        if classes:
        
            terms_tp, classes_tp = leftsplice(term_pairs),rightsplice(term_pairs)
            classes_cp, terms_cp = leftsplice(class_pairs),rightsplice(class_pairs)

            if terms_cp.difference(terms_tp):
                print('1')
                return False
            if classes_cp.difference(classes_tp):
                print('2')
                return False
            if classes.difference(classes_tp):
                print('3')
                return False
            if classes.difference(classes_cp):
                print('4')
                return False
            for x in term_pairs:

                if str(x[0]) not in apply(class_pairs,x[1]):
                    print('5')
                    print(str(x[0]))
                    print(apply(class_pairs,x[1]))
                    return False
        return True 

            
        

    ## THE PRIMARY INTERFACE 
        

    def is_equal (self,
                  x,
                  y):
        notebook = self.notebookname

        if not (self.exists_term(notebook,
                                x) and
                self.exists_term(notebook,
                                 y)):
            return False

        return self.get_class_frpm_term(notebook,
                                        x)==self.get_class_from_term(notebook,y)

    def merge (self,x,y):

        self.merge_equivalence_classes (self.notebookname,
                                        x,
                                        y)
    def new_class (self,entrylist):

        self.join_terms_in_equivalence_class(notebook=self.notebookname,
                                             term_list=entrylist)
        self.display.noteprint(('NEW EQUIVALENCE CLASS',', '.join(entrylist)))
    def del_class (self,x):

        self.delete_all_equivalences(self.notebookname,x)

    def del_term (self,x):
        self.delete_single_term(self.notebookname,
                                x)

    def exists (self,x):
        return self.exists_term(self.notebookname,
                         x)
        
    def fetch (self,x,override=False):

        if self.active or override:
            found_class = self.get_class_for_term(self.notebookname,
                                                              x)

            
            results = {x.lstrip("'") for x in self.get_all_terms_for_class(self.notebookname,
                                                               found_class) if '(' not in x}
            
            if not results:
                results = {x}
            return results
        return {x}

    def fetch_bracketed (self,x,override=False):

        if self.active or override:
            found_class = self.get_class_for_term(self.notebookname, x)
            
            results = {x for x in self.get_all_terms_for_class(self.notebookname,
                                                               found_class) if x[0]=='(' and '~' not in x}
            if not results:
                return False
            if len(results)>1:
                return '('+'|'.join(results)+')'
            return list(results)[0]

    def fetch_all (self,x):

        if self.active or override:
            found_class = self.get_class_for_term(self.notebookname,
                                                              x)
            results = {x for x in self.get_all_terms_for_class(self.notebookname,
                                                               found_class)}
            if not results:
                results = {x}
            return results
        return {x}

        
            
            
    def fetch_reverse_bracketed (self,matching_phrase,override=False):

        

        get_terms = lambda x:{y for y in x.replace('(',' ').replace(')',' ').replace('&',' ').replace('|',' ').split(' ') if y}
        if isinstance (matching_phrase,str):
            matching_phrase = get_terms(matching_phrase)
        if isinstance (matching_phrase,list):
            matching_phrase = set(matching_phrase)
            
        
        return_dict = {}
        if self.active or override:
            return_dict = {}

            terms = self.get_terms(self.notebookname)
            bracketed = [x for x in terms if x.startswith('(') and x.endswith(')')]

            for bt in bracketed:
                if get_terms(bt).intersection(matching_phrase):
                    terms2 = self.fetch_all(bt)
                    
                    return_dict[bt]=terms2
        return return_dict
       

    def toggle (self):

        self.active = not self.active
        self.display.noteprint(('YIELDING EQUIVALENCES',
                                str(self.active)))
        

    def show (self,to_display=True):

        returntextlist = []
        
        value_tuple = (self.notebookname,)
        
        self.db_cursor.execute ("SELECT * FROM classes WHERE notebook=?;",value_tuple)
        classes = self.db_cursor.fetchall()
        
        self.db_cursor.execute ("SELECT * FROM terms WHERE notebook=?;",value_tuple)
        terms = self.db_cursor.fetchall()

        self.db_cursor.execute ("SELECT * FROM terms_for_classes WHERE notebook=?;",value_tuple)
        terms_for_classes = self.db_cursor.fetchall()
        
        returntextlist.append('CLASSES '+','.join([str(x[1]) for x in classes]))
        
        temp_dict = {}
        for x in terms_for_classes:
            if x[1] not in temp_dict:
                temp_dict [x[1]]={x[2]}
                
            else:
                temp_dict[x[1]].add(x[2])
        returntextlist.append('')
        
        for x in sorted(temp_dict.keys()):
            returntextlist.append(('CLASS = '+str(x)+'/')*to_display+', '.join(sorted(temp_dict[x])))
        return '\n'.join(returntextlist)
        
        
    

    def console (self):

        self.add_notebook(self.notebookname)
        

        
        go_on = True 
        while go_on:


            console = DisplayList(['A(dd) new equivalences',
                                      'F(ind)',
                                      'E(liminate) single term',
                                      'D(elete) equivalence class',
                                      'M(erge) equivalence classes',
                                      'S(show)',
                                      'C(lear)',
                                      'L(oad)',
                                      'D(U)mp',
                                      'Q(uit)']+['T(test with iterations','X(=continous test)','V(alid?)']*self.testing,
                                        displayobject=self.display)
            command = input()
            if not command:
                pass
            else:
                if command[0]=='Q':
                    break
                if command[0]=='A':

                    def elim_redundant_parens (x):
                        
                        level = 0
                        x = x.strip()
                        
                        for count, ch in enumerate(x):
                            if ch == '(':
                                level+=1
                            if ch == ')':
                                if count < len(x)-1:
                                    level -= 1
                                else:
                                    return (x[1:-1])
                                if level == 0:
                                    return x
                        return x

                    def add_parens (x):
                        if '&' in x or '|' in x or '(' in x or '|' in x:
                            x = elim_redundant_parens (x)
                            x = '(' + x + ')'
                            
                        return x
                    
                    
                            
                            

                    x = input('List terms to add as equivalence class?')
                    self.join_terms_in_equivalence_class(self.notebookname,
                                                         [add_parens(y.strip()) for y in x.split(',')])
                if command[0]=='F':

                    term = input('Find equivalence class for term=?')

                    found_class = self.get_class_for_term(self.notebookname,
                                                          term)
                    results = self.get_all_terms_for_class(self.notebookname,
                                                           found_class)
                    
                    self.display.noteprint(('EQUIVALENCE CLASS for '+term,', '.join(results)))

                if command[0]=='D':

                    to_delete = input('DELETE TERM and ALL EQUIVALENTS?')
                    if to_delete:      

                        self.delete_all_equivalences(self.notebookname,
                                                     to_delete)
                if command[0]=='M':

                    merge1 = input('Merge first?')
                    merge2 = input('Merge second?')

                    self.merge_equivalence_classes(self.notebookname,
                                                  merge1,
                                                  merge2)
                if command[0] == 'E':
                    to_delete = input('Term to delete?')
                    self.delete_single_term(self.notebookname,
                                            to_delete)

 
                if command[0] in ['T','X']:

                    once = False
                    passed_through = 0
                    while not once or command[0] == 'X':
                        passed_through += 1
                        once = True 

                        if not command[0] == 'X':
                            iterations = None
                        else:
                            iterations = 1
                        while not iterations:
                            try:
                                iterations = int(input('ITERATIONS?'))+1
                            except:
                                print('YOU MUST INPUT AN INTEGER!')
                            
                        for count in range(0,iterations):
                                if not command[0] == 'X':
                                    print(count)
                                    print()
                                
                                
                                all_terms = list(range(500))
                                for x in range(500):
                                    self.add_new_equivalence(self.notebookname,
                                                             str(x%17),
                                                             str(x))
                                                             
                                for x in range(25,500):
                                    x = random.choice(all_terms)
                                    all_terms.pop(all_terms.index(x))
                                    x = str(x)
                                    self.delete_single_term(self.notebookname,x)
                                self.db_connection.commit()

                                current_terms = list(self.get_terms(self.notebookname))
                                a,b,c,d = random.choice(current_terms),random.choice(current_terms),random.choice(current_terms),random.choice(current_terms)
                                self.merge_equivalence_classes(self.notebookname,a,b)
                                self.delete_all_equivalences(self.notebookname,c)
                                self.delete_all_equivalences(self.notebookname,d)

                                def char():
                                    return random.choice(list('abcdefghijklmnopqrstuvwxyz'))
                                concatenate = lambda x:''.join(char() for y in range(x))
                                makelist = lambda x:[concatenate(random.choice(range(1,20))) for y in range(x)]
                                self.join_terms_in_equivalence_class(self.notebookname,makelist(random.choice(range(1,20))))
                                

                                
                        validity = self.is_valid(self.notebookname)
                        self.display.noteprint((str(passed_through),{True:'VALID',
                                                                     False:'INVALID'}[validity]))
                        if not validity:
                            command = 'T'
                            
                if command[0] == 'V':
                    
                    self.display.noteprint(('',{True:'VALID',
                                                        False:'INVALID'}[self.is_valid(self.notebookname)]))
                    
                  

                if command[0] == 'S':
                    self.display.noteprint(('RESULTS for '+self.notebookname,self.show()))

                if command[0] == 'C':
                    if input('ARE YOU SURE YOU WANT TO DELETE ALL EQUIVALENCE CLASSES?') in ['yes','YES']:

                        terms_to_delete = []

                        for class_value in self.get_classes (self.notebookname):
                            terms = sorted(self.get_all_terms_for_class (self.notebookname,class_value))
                            terms_to_delete.append(terms[0])
                        for term in terms_to_delete:
                            self.delete_all_equivalences(self.notebookname,
                                                         term)
                if command[0] == 'L':
                    self.display.noteprint(('TEXT TO LOAD',''))
                    to_load = input('?')
                    to_load = to_load.replace(';','\n')
                    for line in to_load.split('\n'):
                        terms = [x.strip() for x in line.split(',')]
                        self.join_terms_in_equivalence_class(self.notebookname,terms)
                if command[0] == 'U':
                    print(self.show(to_display=False))
                    input('')
                    
                    
                    
                            
                    
                        

                            

                
                        
if __name__ == "__main__":
 
            
    E = Equivalences(testing=True,filename='TEST')
    E.console()


                

                

            

                

        
        
        

        
        

        

        

        

        
