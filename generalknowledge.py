
## Expanded version of the  knowledgebase
##

import shelve
from globalconstants import SLASH
from printcomplexobject import print_complex_object
import sqlite3




def listprint(x):
     returntext = ''
     for item in x:
          returntext+=str(item) + '\n'
     return returntext

def openshelf(path_and_name,shelfobject=None,createnew=False):
     
     flag = 'w'
     try:
          if createnew:
               print(1+'g') #create an exception
          shelfobject = shelve.open(path_and_name, flag)
          return 'w'
                    
               

     except:
          try:
               flag = 'c'
               shelfobject = shelve.open(path_and_name, flag)
               return 'c'
          except:
               return 'f'

class GeneralizedKnowledge:

     def __init__ (self,find_paths=False,directoryname=None,filename=None,using_shelf=False,using_database=True):

          self.using_database = using_database
          self.using_shelf = using_shelf

          if filename:
               self.notebookname = filename
          else:
               self.notebookname = 'GENERALKNOWLEDGE'
               
          if using_database:          
               self.open_connection()          
               self.create_database()
##               if input('CASCADE DELETE?') == 'yes':
##                    self.db_cursor.execute("PRAGMA foreign_keys = on")
##               
               self.db_cursor.execute("INSERT OR REPLACE INTO notebooks (notebook) VALUES (?);",(self.notebookname,))
               self.knowledge = {}
               self.relations = {}
               self.converses = {}
               self.complexes = {}

          if  using_shelf:

               if directoryname and filename:
                    # TO OPEN SHELVES 

                    self.shelf = {}

                    self.shelf['knowledge'] = None
                    self.shelf['relations'] = None 
                    self.shelf['converses'] = None
                    self.shelf['complexes'] = None

                    try:
                         flag = 'w'
                                   
                         self.shelf['knowledge'] = shelve.open(directoryname+SLASH+filename +'GKK',flag)
                         self.shelf['relations'] = shelve.open(directoryname+SLASH+filename +'GKR',flag)
                         self.shelf['converses'] = shelve.open(directoryname+SLASH+filename +'GKC',flag)
                         self.shelf['complexes'] = shelve.open(directoryname+SLASH+filename +'GKX',flag)
                         print(flag)
                         print(self.shelf['knowledge'])

                    except:

                         flag = 'c'
                         
                         self.shelf['knowledge'] = shelve.open(directoryname+SLASH+filename +'GKK',flag)
                         self.shelf['relations'] = shelve.open(directoryname+SLASH+filename +'GKR',flag)
                         self.shelf['converses'] = shelve.open(directoryname+SLASH+filename +'GKC',flag)
                         self.shelf['complexes'] = shelve.open(directoryname+SLASH+filename +'GKX',flag)
                         print(flag)
                         print(self.shelf['knowledge'])

                    

                    
                    self.knowledge = self.shelf['knowledge']
                    self.relations = self.shelf['relations']
                    self.converses = self.shelf['converses']
                    self.complexes = self.shelf['complexes']

                    self.is_shelf = True
                    
                    
          self.query_flag = 'd'*using_database + 'o'*using_shelf # flag for generic get and set
                          # = use dictionary or shelf
                          # = use database 
          
          self.find_paths = find_paths

     def open_connection (self):

          self.db_connection = sqlite3.connect('notebooks'+'/'+'knowledge.db')
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
          
          CREATE TABLE IF NOT EXISTS nodes (
          
               notebook TEXT NOT NULL,
               node TEXT NOT NULL,
               UNIQUE (notebook, node)
               PRIMARY KEY (notebook, node)
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
          );
          
          CREATE TABLE IF NOT EXISTS relations (
          
               notebook TEXT NOT NULL,
               relation TEXT NOT NULL,
               type INT NOT NULL,
               PRIMARY KEY (notebook, relation)
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
          );
          
          CREATE TABLE IF NOT EXISTS knowledge (
          
               notebook TEXT NOT NULL,
               node TEXT NOT NULL,
               relation TEXT NOT NULL,
               content TEXT NOT NULL,
               PRIMARY KEY (notebook, node, relation, content)
               FOREIGN KEY (notebook, relation) REFERENCES relations (notebook, relation) ON DELETE CASCADE
               FOREIGN KEY (notebook, content) REFERENCES nodes (notebook, node) ON DELETE CASCADE
               FOREIGN KEY (notebook, node) REFERENCES nodes (notebook, node) ON DELETE CASCADE
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
               
          );
          
          CREATE TABLE IF NOT EXISTS converses (

               notebook TEXT NOT NULL,
               relation TEXT NOT NULL,
               converse TEXT NOT NULL,
               PRIMARY KEY (notebook, relation)

               FOREIGN KEY (notebook, converse) REFERENCES relations (notebook, relation) ON DELETE CASCADE 
               FOREIGN KEY (notebook, relation) REFERENCES relations (notebook, relation) ON DELETE CASCADE 
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
               
          );
          
          CREATE TABLE IF NOT EXISTS complexes (

               notebook TEXT NOT NULL,
               relation TEXT NOT NULL,
               complex TEXT NOT NULL,
               UNIQUE (notebook, relation)
               
               FOREIGN KEY (notebook, relation) REFERENCES relations (notebook, relation) ON DELETE CASCADE 
               FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
               
          );
          """)

          
     def expose (self):

          if self.using_database:

               self.db_cursor.execute("SELECT * FROM knowledge")
               print('   KNOWLEDGE       ')
               print(self.db_cursor.fetchall())
               print()
               self.db_cursor.execute("SELECT * FROM relations")
               print('   RELATIONS      ')
               print(self.db_cursor.fetchall())
               print()
               self.db_cursor.execute("SELECT * FROM converses")
               print('   CONVERSES     ')
               print(self.db_cursor.fetchall())
               print()
               self.db_cursor.execute("SELECT * FROM nodes")
               print('   NODES      ')     
               print(self.db_cursor.fetchall())
               print()
               self.db_cursor.execute("SELECT * FROM complexes")
               print('   COMPLEXES     ')
               print(self.db_cursor.fetchall())
               print()

          if self.using_shelf:

               print(self.knowledge)
               print(self.relations)
               print(self.converses)
               print(self.complexes)

               

     def query (self,
                phrase=None,
                action=None,
                flag=None,
                term1=None,
                term2=None,
                term3=None,
                term4=None,
                delete_if_empty=False):

          """ function for getting and setting through queries
          This could be generalized to allow for undetermined levels, but
          I chose not to do this so that I can intergrate the database
          """
          not_getting = False
          
          types = {'<dict>':{},
                   '<list>':[],
                   '<set>':set()}

          dict_result = None
          db_result = None

          if not flag:
               flag = self.query_flag

          if action not in ['in','get','set','delete']:
               return False

          if not term1:

               term1,term2,term3,term4 = (phrase.split('|')+[None,None,None,None])[0:4]
           

          def to_int (x):
               if isinstance(x,str) and x.isnumeric():
                    return int(x)
               else:
                    return x
              
          term1, term2, term3, term4 = to_int(term1), to_int(term2), to_int(term3), to_int(term4)
               

          if not term1:
               return False

          elif term1 in ('knowledge','relations','converses','complexes'):

               dict_obj = {'knowledge':self.knowledge,
                           'relations':self.relations,
                           'converses':self.converses,
                           'complexes':self.complexes}[term1]
               
               
                          

               if not term2:
                    # to get the keys of the dictionary object

                    if 'd' in flag:
                         if action == 'get':


                              value_tuple = (self.notebookname,)

                              if term1 == 'knowledge':

                                   self.db_cursor.execute("SELECT node FROM nodes"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)

                              elif term1 == 'relations':

                                   self.db_cursor.execute("SELECT relation FROM relations"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)

                              elif term1 == 'converses':

                                   self.db_cursor.execute("SELECT relation FROM converses"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)


                                   
                              temp_results = self.db_cursor.fetchall()

                              db_result = {x[0] for x in temp_results}
                              

                    if 'o' in flag:
                         if action == 'get':
                              dict_result = set(dict_obj.keys())

                    if not not_getting and 'd' in flag:
                         return  db_result
                    else:
                         return dict_result
                              

               elif term2 and not term3:

                    if action == 'in':
                         # to test whether term2 is the dictionary object 
                         if  'd' in flag:
                              value_tuple = (self.notebookname,)

                              if term1 == 'knowledge':

                                   self.db_cursor.execute("SELECT node FROM nodes"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)

                              elif term1 == 'relations':

                                   self.db_cursor.execute("SELECT relation FROM relations"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)
                              elif term1 == 'converses':
                                   self.db_cursor.execute("SELECT relation FROM converses"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)
                              elif term1 == 'complexes':
                                   self.db_cursor.execute("SELECT complex FROM complexes"+
                                                          " WHERE notebook=?;",
                                                          value_tuple)
                              
                               
                              temp_results = self.db_cursor.fetchall()
                              temp_results = {x[0] for x in temp_results}
                              db_result = term2 in temp_results
                              


                              
                         if 'o' in flag:                              
                              dict_result = term2 in dict_obj.keys()

                    
                         if not not_getting and 'd' in flag:
                              return  db_result
                         else:
                              return dict_result
                         
                    elif action == 'get':
                         
                         if 'd' in flag:
                              value_tuple = (self.notebookname,
                                             term2)
                                             
                              if term1 == 'knowledge':

                                   self.db_cursor.execute("SELECT relation FROM knowledge"+
                                                          " WHERE notebook=? and node=?;",
                                                          value_tuple)

                              elif term1 == 'relations':

                                   self.db_cursor.execute("SELECT type FROM relations"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)

                              elif term1 == 'converses':

                                   self.db_cursor.execute("SELECT converse FROM converses"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)

                              elif term1 == 'complexes':

                                   self.db_cursor.execute("SELECT complex FROM complexes"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)


                              if term1 == 'knowledge':                                        
                                   temp_results = self.db_cursor.fetchall()
                                   temp_results = {x[0] for x in temp_results}
                                   db_result = temp_results
                              else:
                                   temp_results = self.db_cursor.fetchone()
                                   db_result = temp_results[0]

                                   
                         if 'o' in flag:
                              if term2 in dict_obj.keys():
                                   # to return contents of object dictionary at index 
                                   dict_result =  dict_obj[term2]


                         if not not_getting and 'd' in flag:
                              return  db_result
                         else:
                              return dict_result



                                   
                    elif action == 'set':
                         if 'd' in flag:
                              pass

                         if 'o' in flag:
                              if term2 in types:
                                   dict_obj = types[term2]
                                   # to create as dictionary, list, or set                                    
                         
                              
                    elif action == 'delete':
                         
                         

                         if 'd' in flag:

                              value_tuple = (self.notebookname,
                                        term2,)

                              if term1 == 'knowledge':

                                   self.db_cursor.execute("DELETE FROM nodes "+
                                                          " WHERE notebook=? and node=?;",
                                                          value_tuple)

                                   self.db_connection.commit()
                                   

                              elif term1 == 'relations':

                                   self.db_cursor.execute("DELETE FROM relations"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)


                              elif term1 == 'converses':

                                   self.db_cursor.execute("DELETE FROM converses"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)
                                   

                              elif term1 == 'complexes':

                                   self.db_cursor.execute("DELETE FROM complexes"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)
                              self.db_connection.commit()
                              


                                   

                         if 'o' in flag:

                              if term2 in dict_obj:

                                   if isinstance(dict_obj,dict):

                                        del dict_obj[term2]
     
                                   elif isinstance(dict_obj,(list,set)):
                                        x = dict_obj
                                        x.remove(term2)
                                        dict_obj = x
                                   if delete_if_empty and not dict_obj:
                                        del dict_obj

                         
                                   

               elif term2 and term3 and not term4:
                    if action == 'in':

                         if  'd' in flag:
                              value_tuple = (self.notebookname,
                                                  term2)

                              if term1 == 'knowledge':

                                        self.db_cursor.execute("SELECT relation FROM knowledge"+
                                                               " WHERE notebook=? and node=?;",
                                                               value_tuple)

                              if term1 == 'relations':

                                   self.db_cursor.execute("SELECT type FROM relations"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)

                              if term1 == 'converses':

                                   self.db_cursor.execute("SELECT converse FROM converses"+
                                                          " WHERE notebook=? and relation=?;",
                                                          value_tuple)

                                   
                              temp_results = self.db_cursor.fetchall() 
                              temp_results = {x[0] for x in temp_results}
                              db_result = term3 in temp_results     
                        
                         if 'o' in flag:
                         
                              if term2 in dict_obj.keys():
                                   dict_result = term3 in dict_obj[term2]

                         if not not_getting and 'd' in flag:
                              return  db_result
                         else:
                              return dict_result

                         
                    elif action == 'get':

                         if  'd' in flag:

                              value_tuple = (self.notebookname,
                                             term2,
                                             term3)
                                             
                              if term1 == 'knowledge':

                                   self.db_cursor.execute("SELECT content FROM knowledge"+
                                                          " WHERE notebook=? and node=? and relation=?;",
                                                          value_tuple)
                              
                                   temp_results = self.db_cursor.fetchall()
                                   db_result = {x[0] for x in temp_results}



                         if 'o' in flag:
                              if term2 in dict_obj.keys() and term3 in dict_obj[term2]:
                                   dict_result = dict_obj[term2][term3]

                         if not not_getting and 'd' in flag:
                              return  db_result
                         else:
                              return dict_result
                         
                    elif action == 'set':

                         if 'd' in flag:

                              if term1 == 'knowledge':


                                   if term3 in types:

                                        value_tuple = (self.notebookname,
                                                       term2)

                                        self.db_cursor.execute("INSERT OR REPLACE"+
                                                     " INTO nodes "+
                                                     "(notebook, node) VALUES (?,?);",
                                                     value_tuple)
                                        self.db_connection.commit()
                                        
                                   else:
                                        

                                        value_tuple = (self.notebookname,
                                                       term2,
                                                       term3)
                                        

                                        self.db_cursor.execute("INSERT OR REPLACE"+
                                                          " INTO knowledge "+
                                                          "(notebook, node, relation) VALUES (?,?,?);",
                                                          value_tuple)
                                        self.db_connection.commit()
                                        

                              elif term1 == 'relations':

                                   value_tuple = (self.notebookname,
                                                       term2,
                                                       term3)
                                        

                                   self.db_cursor.execute("INSERT OR REPLACE"+
                                                     " INTO relations "+
                                                     "(notebook, relation, type) VALUES (?,?,?);",
                                                     value_tuple)
                                   self.db_connection.commit()

                              elif term1 == 'converses':

                                   value_tuple = (self.notebookname,
                                                       term2,
                                                       term3)
                                        

                                   self.db_cursor.execute("INSERT OR REPLACE"+
                                                     " INTO converses"+
                                                     "(notebook, relation, converse) VALUES (?,?,?);",
                                                     value_tuple)
                                   self.db_connection.commit()

                              elif term1 == 'complexes':

                                   value_tuple = (self.notebookname,
                                                       term2,
                                                       term3)
                                        

                                   self.db_cursor.execute("INSERT OR REPLACE"+
                                                     " INTO complexes"+
                                                     "(notebook, relation, complex) VALUES (?,?,?);",
                                                     value_tuple)
                                   self.db_connection.commit()


                         if 'o' in flag:
                              
                              if isinstance(dict_obj,dict):

                                   if term3 in types:
                                        dict_obj[term2] = types[term3]

                                   elif term2 in dict_obj and isinstance(dict_obj[term2],list):
                                        x = dict_obj[term2]
                                        x.append(term3)
                                        dict_obj[term2] = x

                                   elif term2 in dict_obj and isinstance(dict_obj[term2],set):
                                        x= dict_obj[term2]
                                        x.add(term3)
                                        dict_obj[term2] = x 
                                   else:
                                        dict_obj[term2] = term3

                    elif action == 'delete':
                                                                         

                              if 'o' in flag:

                                   if term2 in dict_obj:
                              
                                        if term3 not in dict_obj[term2]:
                                             # nullifies object - Maybe I shouldn't have this
                                             dict_obj[term2] = None
                                        elif term3 in dict_obj[term2]:
                                             if isinstance(dict_obj,dict) and not isinstance(dict_obj[term2],(set,list)):
                                                  del dict_obj[term2]
                                             elif isinstance(dict_obj[term2],(list,set)):
                                                  x = dict_obj[term2]
                                                  x.remove(term3)
                                                  dict_obj[term2] = x

                                             if delete_if_empty and not dict_obj[term2]:
                                                  del dict_obj[term2]
                                        
                                   
               elif term1 and term2 and term3 and term4:

                    if action == 'in':
                         if 'd' in flag:

                              value_tuple = (self.notebookname,
                                             term2,
                                             term3)
                                             
                              if term1 == 'knowledge':

                                   self.db_cursor.execute("SELECT content FROM knowledge"+
                                                          " WHERE notebook=? and node=? and relation=?;",
                                                          value_tuple)
                              
                                   temp_results = self.db_cursor.fetchall()
                                   temp_results = [x[0] for x in temp_results]
                                   db_result = term4 in temp_results 


                         if 'o' in flag:
                              if term2 in dict_obj.keys() and term3 in dict_obj[term2]:
                                   dict_result = term4 in dict_obj[term2][term3]
                                   
                         if not not_getting and 'd' in flag:
                              return  db_result
                         else:
                              return dict_result
                         
                    elif action == 'get':

                         if 'd' in flag:
                              pass
                         
                         if 'o' in flag:
                              if term2 in dict_obj.keys() and term3 in dict_obj[term2] and term4 in dict_obj[term3]:
                                   return dict_obj[term2][term3][term4]

                    elif action == 'set':

                         if 'd' in flag:

                              if term1 == 'knowledge':

                                   if term4 not in types:
                                        
                                        value_tuple = (self.notebookname,
                                                       term2,
                                                       term3,
                                                       term4)
                                        self.db_cursor.execute("INSERT OR REPLACE"+
                                                          " INTO knowledge "+
                                                          "(notebook, node, relation, content) VALUES (?,?,?,?);",
                                                          value_tuple)                                            
                                        self.db_connection.commit()

                                        


                              
                              

                         if 'o' in flag:
                              if term2 in dict_obj.keys():
                                   if isinstance(dict_obj[term2],dict):

                                        if term4 in types:
                                             dict_obj[term2][term3] = types[term4]

                                        elif  term3 in dict_obj[term2] and isinstance(dict_obj[term2][term3],list):
                                             x = dict_obj[term2][term3]
                                             x.append(term4)
                                             dict_obj[term2][term3] = x
                                        elif  term3 in dict_obj[term2] and isinstance(dict_obj[term2][term3],set):
                                             x = dict_obj[term2][term3]
                                             x.add(term4)
                                             dict_obj[term2][term3] = x

                                        else:
                                             dict_obj[term2][term3] = term4

                    elif action == 'delete':

                         if 'd' in flag:

                              value_tuple = (self.notebookname,
                                             term2,
                                             term3,
                                             term4)
                              
                              if term1 == 'knowledge':

                                   self.db_cursor.execute("DELETE FROM knowledge"+
                                                          " WHERE notebook=? AND node=? "+
                                                          "AND relation=? AND content=?;",
                                                          value_tuple)
                                   
                                   self.db_connection.commit()

                                   

                         if 'o' in flag:
                              if term3 in dict_obj[term2]:
                                   
                                   if term4 not in dict_obj[term2][term3]:
                                        # nullifies object - Maybe I shouldn't have this
                                        dict_obj[term2][term3]= None
                                   elif term4 in dict_obj[term2][term3]:
                                        if isinstance(dict_obj[term2],dict):
                                             del dict_obj[term2][term3]
                                        elif isinstance(dict_obj[term2][term3],(list,set)):
                                             x = dict_obj[term2][term3]
                                             x.remove(term4)
                                             dict_obj[term2][term3] = x

                                        try:
                                             if delete_if_empty and not dict_obj[term2][term3]:
                                                  del dict_obj[term2][term3]
                                        except:
                                             pass
                                        
                                        
                                   
                         

                              

     def clear (self):

          def empty_shelf(shelfobject):

               for key in list(shelfobject.keys()):
                    del shelfobject[key]

          if input('DO YOU REALLY WANT TO CLEAR THE ENTIRE KNOWLEDGE SHELF?? Type "yes" to continue!') == 'yes':
               empty_shelf(self.knowledge)
               empty_shelf(self.relations)
               empty_shelf(self.converses)
               empty_shelf(self.complexes)

          print('DELETED')

     def node_exists (self,node):

          return self.query(term1='knowledge',term2=node,action='in')
     
     def relation_exists (self,relation):

          return self.query(term1='relations',term2=relation,action='in')

     def restart (self,directoryname=None,filename=None):

          if self.using_shelf:

               if self.is_shelf and directoryname and filename:

                    
                    flag = 'w'
                              
                    self.shelf['knowledge'] = shelve.open(directoryname+SLASH+filename +'GKK',flag)
                    self.shelf['relations'] = shelve.open(directoryname+SLASH+filename +'GKR',flag)
                    self.shelf['converses'] = shelve.open(directoryname+SLASH+filename +'GKC',flag)
                    self.shelf['complexes'] = shelve.open(directoryname+SLASH+filename +'GKX',flag)
                    print('REOPENING '+ directoryname+SLASH+filename +'GK')


     def add_relation (self,relation,typeof=0,converse=None):

          """ 1for DIRECTED
          2 for non-DIRECTED
          3 for attribute
          4 for reciprocal
          5 for complex"""


          if not typeof in (1,2,3,4,5) or self.query(term1='relations',term2=relation,action='in'):
               return False
          
          else:
               if typeof in (1,2,3):
                    # for directed, non-directed, or attributes 
                    self.query(term1='relations',term2=relation,term3=typeof,action='set')
               elif typeof==4:
                    # for a converse relation
                    if not self.query(term1='relations',
                                  term2=converse,
                                  action='in'):
                         self.query(term1='relations',
                                    term2=relation,
                                    term3=typeof,
                                    action='set')
                         self.query(term1='relations',
                                    term2=converse,
                                    term3=typeof,
                                    action='set')
                         self.query(term1='converses',
                                    term2=relation,
                                    term3=converse,
                                    action='set')
                         self.query(term1='converses',
                                    term2=converse,
                                    term3=relation,
                                    action='set')
               else:
                    print('FIRST SETTING COMPLEX')
                    #for a complex relation
                    self.query(term1='relations',
                               term2=relation,
                               term3=typeof,
                               action='set')
                    self.query(term1='complexes',
                               term2=relation,
                               term3=converse,
                               action='set')

               

     def delete_relation (self,relation):

          if self.query(term1='relations',
                        term2=relation,
                        action='in'):
                self.query(term1='relations',
                           term2=relation,
                           action='delete')
          if self.query(term1='converses',
                        term2=relation,
                        action='in'):
               con_relation = self.query(term1='converses',
                                         term2=relation,
                                         action='get')
               if self.query(term1='converses',
                             term2=con_relation,
                             action='in'):
                    self.query(term1='converses',
                               term2=relation,
                               action='delete')
                    self.query(term1='converses',
                               term2=con_relation,
                               action='delete')
               
                    self.query(term1='converses',
                               term2=con_relation,
                               action='delete')
                    self.query(term1='converses',
                               term2=relation,
                               action='delete')
                    if self.query(term1='relations',
                                  term2=con_relation,
                                  action='in'):
                         self.query(term1='converses',
                                    term2=con_relation,
                                    action='delete')

     def show_relations (self,typeof=None):
          
          returnlist = []
          for relation in self.query(term1='relations',action='get'):

               if typeof is None or self.query(term1='relations',
                                               term2=relation,
                                               action='get') == typeof:
                    returnlist.append(relation + ' = ' + {1:'DIRECTED',
                                                          2:'NONDIRECTED',
                                                          3:'ATTRIBUTE',
                                                          4:'RECIPROCAL',
                                                          5:'COMPLEX'}[self.query(term1='relations',
                                                                                  term2=relation,
                                                                                  action='get')])
          return returnlist
     
     def add_attribute (self,
                        node,
                        relation,
                        content):

          if self.query(term1='knowledge',term2=node,action='in') and relation.strip() and content.strip():
               if not self.query(term1='knowledge',
                                 term2=node,
                                 term3=relation,
                                 action='in'):
                    self.query(term1='knowledge',
                               term2=node,
                               term3=relation,
                               term4='<list>',
                               action=set)
                    self.query(term1='knowledge',
                               term2=node,
                               term3=relation,
                               term4=content,
                               action=set)
                    return True
               else:
                    self.query(term1='knowledge',
                               term2=node,
                               term3=relation,
                               term4=content,
                               action=set)
                    return True
          return False

     def delete_attribute (self,
                           node,
                           relation,
                           content):

          if self.query(term1='knowledge',
                        term2=node,
                        action='in') and relation.strip() and content.strip():
               if self.query(term1='knowledge',
                             term2=node,
                             term3=relation,
                             action='in'):
                    self.query(term1='knowledge',
                               term2=node,
                               term3=relation,
                               term4=content,
                               action='delete')						
                    

     def add_definition (self,
                         node,
                         content):

          if not self.query(term1='relations',
                            term2='DEFINITION',
                            action='in'):
               self.add_relation(relation='DEFINITION',
                                 typeof=2)
          self.add_attribute(node=node,
                             relation='DEFINITION',
                             content=content)
          

     def add_node (self,node):

          if not self.query(term1='knowledge',
                            term2=node,
                            action='in'):
               self.query(term1='knowledge',
                          term2=node,
                          term3='<dict>',
                          action='set')


     def delete_node (self, node):

          if self.query(term1='knowledge',
                        term2=node,
                        action='in'):

               self.query(term1='knowledge',
                          term2=node,
                          action='delete')

          for n_temp in self.query(term1='knowledge',
                                   action='get'):

               for relation in list(self.query(term1='knowledge',
                                               term2=n_temp,
                                               action='get')):

                    if self.query(term1='knowledge',
                                  term2=n_temp,
                                  term3=relation,
                                  term4=node):
                         self.delete_directed_edge (relation,n_temp,node)

     def add_directed_edge (self,
                            relation,
                            nodefrom,
                            nodeto):

          if self.query(term1='knowledge',
                        term2=nodefrom,
                        action='in') \
             and self.query(term1='knowledge',
                            term2=nodeto,
                            action='in'):

               if self.query(term1='knowledge',
                             term2=nodefrom,
                             term3=relation,
                             action='in'):

                    self.query(term1='knowledge',
                               term2=nodefrom,
                               term3=relation,
                               term4=nodeto,
                               action='set')
                    
               else:
                    self.query(term1='knowledge',
                               term2=nodefrom,
                               term3=relation,
                               term4='<set>',
                               action='set')
                    self.query(term1='knowledge',
                               term2=nodefrom,
                               term3=relation,
                               term4=nodeto,
                               action='set')


     def add_edge (self,
                   relation,
                   nodeone,
                   nodetwo):

          self.add_directed_edge (relation,
                                  nodeone,
                                  nodetwo)
          self.add_directed_edge (relation,
                                  nodetwo,
                                  nodeone)

     def delete_directed_edge (self,
                               relation,
                               nodefrom,
                               nodeto):

          if self.query(term1='knowledge',
                        term2=nodefrom,
                        action='in'):

               if self.query(term1='knowledge',
                             term2=nodefrom,
                             term3=relation,
                             action='in'):
                    if self.query(term1='knowledge',
                                  term2=nodefrom,
                                  term3=relation,
                                  term4=nodeto,
                                  action='in'):

                         self.query(term1='knowledge',
                                    term2=nodefrom,
                                    term3=relation,
                                    term4=nodeto,
                                    action='delete',
                                    delete_if_empty=True)
                         return True
          return False

     def delete_edge (self,
                      relation,
                      nodeone,
                      nodetwo):

          if self.delete_directed_edge (relation,
                                        nodeone,
                                        nodetwo) and self.delete_directed_edge (relation,
                                                                                nodetwo,
                                                                                nodeone):
               return True

     def find_nodes_with_attributes (self,
                                     relation,
                                     content,
                                     findin=True):

          
          if not self.query(term1='relations',
                            term2=relation,
                            action='in'):
               return set()
          returnset = set()

          for node in self.query(term1='knowledge',action='get'):

               if self.query(term1='knowledge',
                             term2=node,
                             term3=relation,
                             action='in'):

                    if not findin:

                         if self.query(term1='knowledge',
                                       term2=node,
                                       term3=relation,
                                       term4=content,
                                       action='in'):

                              returnset.add(node)
                    else:

                         for phrase in self.query(term1='knowledge',
                                                  term2=node,
                                                  term3=relation,
                                                  action='get'):
                              if content in phrase:
                                   returnset.add(node)
          return returnset 

     def find_nodes (self,
                     relation,
                     nodeset=None,
                     resultlist=None,
                     pathlist=None,
                     searched_nodes=None):

          last_paths = []
          if resultlist == None:
               resultlist = []

          if searched_nodes == None:
               searched_nodes = set()

          if pathlist == None and self.find_paths:
               pathlist == []
               
          found_nodes = set()
          new_paths = [] 
          for node in nodeset:
               if pathlist:
                    last_paths = [path[0:path.index(node)+1] for path in pathlist if path and node in path]

               if not self.query(term1='knowledge',
                                 term2=node,
                                 action='in') or not self.query(term1='knowledge',
                                                                term2=node,
                                                                term3=relation,
                                                                action='in'):
                    pass
               else:
                    found_nodes.update(self.query(term1='knowledge',
                                                  term2=node,
                                                  term3=relation,
                                                  action='get'))
                    searched_nodes.add(node)
                    for related_node  in  self.query(term1='knowledge',
                                                     term2=node,
                                                     term3=relation,
                                                     action='get'):
                         resultlist.append(str(related_node)+' is the '+str(relation)+' of ' + str(node))
                         if last_paths:
                              for path in last_paths:
                                   path_to_add = path+[related_node]
                                   
                                   new_paths.append(path_to_add)
          if pathlist:
               for path in new_paths:
                    if path not in pathlist:
                         pathlist.append(path)
         
          return found_nodes

     def unpack_complex_relation (self,enterstring):

          def unpack(enterstring):

               last = enterstring.count('>')

               while True:
                    for r in enterstring.split('>'):

                         if self.query(term1='relations',
                                       term2=r,
                                       action='in'):
                              if self.query(term1='relations',
                                            term2=r,
                                            action='get') == 5:
                                   if  self.query(term1='complexes',
                                                  term2=r,
                                                  action='in'):
                                        enterstring = enterstring.replace(r,
                                                                          self.query(term1='complexes',
                                                                                     term2=r,
                                                                                     action='get'))
                    if enterstring.count('>') == last:
                         break
                    last = enterstring.count('>')
               return enterstring 

          returnlist = []
          for seg in enterstring.split(','):
               returnlist += reversed(unpack(seg).split('>'))

          return returnlist 
                               

     def find_all_relations (self,relation,node):

          many = False 

          if not isinstance(relation,list):
               relations = [relation]
          else:
               relations = relation
               many = True
          results = []


          

          last_nodes = set()

          last_found_nodes = set() #for the nodes found with the last relation
                                   # and hence the results of the search
          
          starting_nodes = set()

          for count, relation in enumerate(relations):
                    


               find_all = True
               if (not many and '/' not in relation) or relation.endswith('*'):
                    if relation.endswith('*'):
                         #TO indicate a search for all mediate relata
                         relation = relation[0:-1]
                    find_all = True
                    how_many = 1000
               elif '/' in relation:
                    try:
                         how_many = int(relation.split('/')[1])
                         find_all = False
                    except:

                         how_many = 1
               else:
                    how_many = 1
                    find_all = False


          
               searched_nodes = set()

               while True:
                    if not starting_nodes:
                         #For initiating
                         starting_nodes = self.find_nodes (relations[0].split('/')[0].split('*')[0],{node},results)
                           #get the starting nodes 
                         temp_result = starting_nodes
                         found_nodes = set(starting_nodes)
                         paths = [[node,result]
                                  for result in starting_nodes]
                         if not starting_nodes:
                              return [],[],[]


                         
                    else:
                         #When not ititiating 
                         temp_result = self.find_nodes (relation,
                                                        found_nodes-searched_nodes,
                                                        resultlist=results,
                                                        pathlist=paths,
                                                        searched_nodes=searched_nodes)
                         found_nodes.update(temp_result)

                    if count == len(relations)-1:
                         #if at the end of the list of relations 
                         last_found_nodes.update(temp_result)

                    how_many -=1
                    if not found_nodes > last_nodes or (not find_all and how_many<1):
                         # Break from the while-routine if the search is exhausted
                         break
                    last_nodes = set(found_nodes)


          return last_found_nodes,results,paths

     def dump (self):

          def wrap(x):
               return '{{' + x + '}}'
               

          nodelist = []
          knowledgelist = []
          relationlist = []

          for key in self.query(term1='knowledge',action='get'):

               nodelist.append(wrap(key))
               for relation in self.query(term1='knowledge',
                                          term2=key,
                                          action='get'):

                    other_nodes = self.query(term1='knowledge',
                                             term2=key,
                                             term3=relation,
                                             action='get')
                    knowledgelist.append(wrap(key+':'+relation+';'+','.join(other_nodes)))
          for key in self.query(term1='knowledge',action='get'):
               complement = ''

               relation_type = {1:'DIRECTED',
                                2:'NONDIRECTED',
                                3:'ATTRIBUTE',
                                4:'RECIPROCAL',
                                5:'COMPLEX'}[self.query(term1='relations',
                                                        term2=key,
                                                        action='get')]

               if self.query(term1='relations',
                             term2=key,
                             action='get') in (4,5) and key in self.query(term1='converses',
                                                                          action='get'):

                    complement = ';'+self.query(term1='converses',
                                                term2=key,
                                                action='get')

               relationlist.append(wrap(key+':'+relation_type+complement))

          return '\n'.join(nodelist)+'\n'+'\n'.join(relationlist)+'\n'+'\n'.join(knowledgelist)
               

     def text_interpret (self,command):

          ## "are nodes"
          ## "is a RELATION of"
          ## " and "
          ## " is a directed relation"
          ## " is a nondirected relation"
          ## " is a reciprocal relation with"

          def reduce_blanks (command):
               while '  ' in command:
                    command = command.replace('  ',' ')
               return command

          if ':' in command:
               return(self.interpret(command,reverse_order=False))
               
          
          ARE_NODES = ' are nodes'
          IS_A_NODE = ' is a node'
          IS_A = ' is a '
          OF = ' of '
          AND = ' and '
          IS_A_DIRECTED_RELATION = ' is a directed relation'
          IS_A_NONDIRECTED_ELATION = ' is a nondirected relation'
          IS_A_RECIPROCAL_RELATION = ' is a reciprocal relation with'
          IS_A_COMPLEX_RELATION = ' is a complex relation meaning the'
          SHOW_NODES = 'Show nodes'
          SHOW_RELATIONS = 'Show relations'
          SHOW_ALL = 'Show everything'
          WHAT_ARE = 'Show '
          APOSTROPHE = "'s "
          APOSTROPHE2 = "'"
          IS_AN = ' is an '
          IS_A = ' is a '
          IS = ' is '
          IS_THE = ' is the '
          ARE_THE = ' are the '
          reverse_order = False


          table = {ARE_NODES:':;',
                   IS_A_NODE:':;',
                   IS_A_DIRECTED_RELATION:':DIRECTED',
                   IS_A_NONDIRECTED_ELATION:':NONDIRECTED',
                   IS_A_RECIPROCAL_RELATION:':RECIPROCAL;',
                   IS_A_COMPLEX_RELATION:':COMPLEX;',
                   SHOW_NODES:'$',
                   SHOW_RELATIONS:'$$$',
                   SHOW_ALL:'$$$',
                   APOSTROPHE:':'}

          command = reduce_blanks(command)
          command = command.strip()

          
          if IS_AN in command:
               command = command.replace(IS_AN,IS_A)
          if ((' is ' in command or ' are ' in command)
              and (' relation' not in command)
              and ('Show ' not in command)
              and ('nodes' not in command)):
               reverse_order = True 
          for t in table:
               command = command.replace(t,table[t])
          if command.startswith('show'):
               command = 'Show' + command[4:]
          command = command.replace(WHAT_ARE,'$$')
          command = command.replace(IS_A,':')
          command = command.replace(OF,';')
          command = command.replace(OF,';')
          command = command.replace(APOSTROPHE2,':')
          command = command.replace(AND,',')
          command = command.replace(IS,';')
          command = command.replace(IS_THE,' is a ')
          command = command.replace(ARE_THE,' are a ')
          all_true = ' all ' in command
          command = command.replace(' all ',' ')

          command_beginning = command.split(':')[0]
          command_middle, command_end = '',''
          if ':' in command:
               command_middle = command.split(':')[1].split(';')[0]
               if ';' in command.split(':')[1]:
                    command_end = command.split(':')[1].split(';')[1]
          command_end = command_end.replace(' from ','>').replace(' from ','>')
          if 'self' in command_end or 'self' in command_end:
               command_end = command_beginning
          if all_true:
               command_middle_list = command_middle.split(',')
               new_command_list = []
               for cml in command_middle_list:
                    if cml.endswith('s') and self.query(term1='relations',term2=cml[0:-1],action='in'):
                         new_command_list.append(cml[0:-1]+'*')
                    else:
                         new_command_list.append(cml+'*')
               command_middle = ','.join(new_command_list)

          command = command_beginning + ':' + command_middle + ';' + command_end
               
           
          return(self.interpret(command,reverse_order=reverse_order))
          

     def interpret (self,command,reverse_order):

          """Accepts commands and interprets them to control the
          knowledgebase class.

          node1,node2,node3 ... (a list of nodes) = CREATES NEW NODES
          node:DEFINITION;DEFINITION_CONTENT1,DEFCONT2,DEFCONT2 = DEFINES A NODE
          relation:DIRECTED/NONDIRECTED/ATTRIBUTE = DEFINES A RELATION
          fromnode:relation;tonode1,tonode2,tonode3... = establishes a relation between fromnode and tonode

          $ = shows all the nodes 
          $node:; = shows all the relations of the node
          $$node:relation; =  finds all the related nodes for the given relation
           USE * after relation to find mediate relations
          $$$ = shows all the relations
          
 
          """          

          def splitcommand(command,reverse_order=None):

               node = [x.strip() for x in command.split(':')[0].split(',')]
               relation = [x.strip() for x in command.split(':')[1].split(';')[0].split(',')]
               content_string = command.split(':')[1].split(';')[1]
               contents = [x.strip() for x in content_string.split(',')]
               
               if reverse_order:
                    node, contents = contents, node
               
                    
               return node,relation,contents

          returntext = ''
          header = ''
          
          if ':' not in command:
                    command += ':'
          if ';' not in command.split(':')[1]:
                    command += ';'     
          # THE SHOW COMMANDS

          if command.startswith('$$$$') or command.startswith('????'):
               
               header = 'ALL SHELVES'
               returntext += 'RELATIONS \n'
               returntext += print_complex_object(self.relations)
               returntext += '\n KNOWLEDGE \n'
               returntext += print_complex_object(self.knowledge)
               returntext += '\n CONVERSES \n'
               returntext += print_complex_object(self.converses)
               returntext += '\n'
               return header, returntext
          
          elif command.startswith('$$$') or command.startswith('???'):
               # to show all the defined relations
               header = 'ALL RELATIONS '

               returntext += listprint(self.show_relations())
               returntext += '\n'
               return header, returntext
          
          elif command.startswith('$$') or command.startswith('??'):
               
               # to show all the relatives of a node 

               nodes,all_relations,contents = splitcommand(command[2:],reverse_order)
               found_nodes = set()

               if self.query(term1='relations',
                             term2=nodes[0],
                             action='in') and  self.query(term1='relations',
                                                          term2=nodes[0],
                                                          action='get') == 3:
                    attribute_search = True
                    all_relations, contents = nodes,all_relations
               else:
                    attribute_search = False
                    

          

               for relation in all_relations:

                    if self.query(term1='relations',
                                  term2=relation,
                                  action='in') and self.query(term1='relations',
                                                              term2=relation,
                                                              action='get')==3:

                         header = 'ATTRIBUTE'
                         if not attribute_search:
                              for node in nodes:

                                   returntext += '// \n'

                                   if self.query(term1='knowledge',
                                                 term2=node,
                                                 action='in') and self.query(term1='knowledge',
                                                                             term2=node,
                                                                             term3=relation,
                                                                             action='in'):
                                        
                                        returntext += node + ' is ' + ', '.join(self.query(term1='knowledge',
                                                                                           term2=node,
                                                                                           term3=relation,
                                                                                           action='get')) + '\n'
                         else:
                              for content in contents:
                                        found_nodes.update(self.find_nodes_with_attributes(relation,content))
               if attribute_search:

                    returntext += ','.join(sorted(found_nodes)) + '// \n'
                    
                                   
                                   

                              

 

               relation = self.unpack_complex_relation(','.join(all_relations))
               if not relation:
                    pass
               print('Relation/NODE',relation,nodes)
                
               for node in nodes:
                    header = str(relation) + '(s) of '+node+ ''
                    results = self.find_all_relations(relation,node)
                    print('RESULTS',results)
                    
                    returntext += ','.join(results[0])
                    returntext += '// \n'
                    returntext += listprint(list(set(results[1])))
                    returntext += '\n'
                    listprint(results[2])
                    returntext += '\n'
               return header, returntext



          elif command.startswith('$') or command.startswith('?'):
               # to show the immediate relations of a node

               all_nodes,all_relations,contents = splitcommand(command[1:])
               for relation in all_relations:
                    for node in all_nodes:
                         header = 'IMMEDIATE RELATIONS of ' + node + ''
                         if not node:
                              returntext += ', '.join(sorted(list(self.query(term1='knowledge',
                                                                             action='get')))) + '\n'
                         elif not relation:
                              if self.query(term1='knowledge',term2=node,action='in'):
                                   returntext += node + ': ' + '\n\n'

                                   for relation in self.query(term1='knowledge',
                                                              term2=node,
                                                              action='get'):
                                        returntext +='  ' + relation + '\n'
                                        
                                        for item in self.query(term1='knowledge',
                                                               term2=node,
                                                               term3=relation,
                                                               action='get'):
                                             returntext += '     ' + item + '\n'                   
                                   
                         elif self.query(term1='knowledge',
                                         term2=node,
                                         action='in') and self.query(term1='knowledge',
                                                                     term2=node,
                                                                     term3=relation,
                                                                     action='in'):

                         
                              returntext += ', '.join(sorted(list(self.query(term1='knowledge',
                                                                             term2=node,
                                                                             term3=relation,
                                                                             action='get')))) + '\n'
               return header, returntext
          # THE ENTRY COMMANDS 
          else:
               if command.startswith('-'):
 
                    deleting = True
                    command = command[1:]
               else:
                    deleting = False
               
               all_nodes,all_relations,contents = splitcommand(command,reverse_order)



               if not all_relations:
                    all_relations = [None]
               for relation in all_relations:
                    for node in all_nodes:

                         if node:

                              if (((deleting and self.query(term1='knowledge',
                                                            term2=node,
                                                            action='in')
                                  or (not deleting and not  self.query(term1='knowledge',
                                                                       term2=node,
                                                                       action='in'))))
                                  and (relation not in ('DIRECTED',
                                                        'NONDIRECTED',
                                                        'ATTRIBUTE',
                                                        'RECIPROCAL',
                                                        'COMPLEX'))) and not relation:
                                   
                                   # To add a single node or nodes
##                                   if not relation:

                                        main_function = self.add_node
                                        if deleting:
                                             main_function = self.delete_node
                                        header = 'NEW NODES'
                                        main_function(node)
                                        returntext += node + ', '

                              else:
                                   if relation == 'DEFINITION':
                                        # to define a node
                                        header = 'DEFINITION of ' + node 
                                        returntext += node + ':'
                                        for content in contents:
                                             self.add_definition(node,content)
                                             returntext += content + ', '
                                        returntext = returntext.rstrip(', ')
                                        returntext += '\n'

                                   
                                   else:
                                        if not deleting and not self.query(term1='relations',
                                                                           term2=node,
                                                                           action='in') and relation in ('DIRECTED',
                                                                                                         'NONDIRECTED',
                                                                                                         'ATTRIBUTE',
                                                                                                         'RECIPROCAL',
                                                                                                         'COMPLEX'):
                                             # to define a definition
                                             header = 'NEW RELATION  '

                                             if not contents:
                                                  contents = ['none']
                                             for content in contents:
                                                  print('CONTENT',content)
                                                  
                                                  if relation in ('DIRECTED',
                                                                  'NONDIRECTED',
                                                                  'ATTRIBUTE',
                                                                  'RECIPROCAL',
                                                                  'COMPLEX') \
                                                     and not ((relation in ('RECIPROCAL'
                                                                            or 'COMPLEX'))
                                                              and content == 'none'):
                                                       
                                                       self.add_relation(node,{'DIRECTED':1,
                                                                               'NONDIRECTED':2,
                                                                               'ATTRIBUTE':3,
                                                                               'RECIPROCAL':4,
                                                                               'COMPLEX':5}[relation],content)
                                                       if relation == 'RECIPROCAL':
                                                            returntext += node + ': ' + relation + '; reciprocal with '+content
                                                       else:
                                                            returntext += node + ': ' + relation
                                                       returntext += '\n'
                                                       
                                            
                                        elif deleting and self.query(term1='relations',
                                                                     term2=node,
                                                                     action='in'):
                                             
                                             self.delete_relation(node)
                                             
                                             
                                        elif self.query(term1='relations',
                                                        term2=relation,
                                                        action='in'):

                                             print('relation in')

                                             
                                             for content in contents:

                                                  if (len(contents)<2 and len(all_nodes)<2) or node!=content:

                                                       if deleting:

                                                            func_one = self.delete_directed_edge
                                                            func_two = self.delete_edge
                                                            func_three = self.delete_attribute

                                                       else:
                                                            
                                                            func_one = self.add_directed_edge
                                                            func_two = self.add_edge
                                                            func_three = self.add_attribute 


                                                       header = 'NEW ATTRIBUTE  '
                                                       
                                                       if self.query(term1='relations',
                                                                     term2=relation,
                                                                     action='get') == 1:
                                                            func_one(relation,node,content)
                                                            returntext += node + ' - ' + relation + '\ ' + content + '\n'
                                                       elif self.query(term1='relations',
                                                                       term2=relation,
                                                                       action='get') == 2:
                                                            func_two(relation,node,content)
                                                            returntext += node + ' ' + relation + '-\ ' + content + '\n'
                                                       elif self.query(term1='relations',
                                                                       term2=relation,
                                                                       action='get') == 3:
                                                            func_three(node,
                                                                       relation,
                                                                       content)
                                                            returntext += node + ' =' + relation + '= ' + content  + '\n'
                                                       elif self.query(term1='relations',
                                                                       term2=relation,
                                                                       action='get') == 4:
                                                            func_one(relation,
                                                                     node,
                                                                     content)
                                                            func_one(self.query(term1='converses',
                                                                                term2=relation,
                                                                                action='get'),content,node)
                                                            returntext += node + ' - ' + relation + '\ ' + content + '\n'
                                                            returntext += content + ' - ' + self.query(term1='converses',
                                                                                                       term2=relation,
                                                                                                       action='get') + '\ ' + node + '\n'
                                        
               return header, returntext.rstrip(', ').rstrip(',')
          return '',''

          
                                   
                                   

if __name__ == '__main__':


     b = GeneralizedKnowledge(find_paths=True)
##
##     while True:
##
##          print('QUERYRESULT',b.query(phrase=input('PHRASE?'),action=input('ACTION?')))
##          print('KNOWLEDGE',b.knowledge)
##          print('RELATIONS',b.relations)
##          print('CONVERSES',b.converses)
##          b.expose()
          

     while True:
          x= input('?')
          print(listprint(b.text_interpret(x)))
          b.expose()
          
 

          if not x:
               break

          if x=='?':
               while True:
                    
                    y = input('???')
                    if '/' in y:
                         print(b.find_nodes_with_attributes(y.split('/')[0],y.split('/')[1]))

                    if not y:
                         break

     b.close()
                    
                    
          
     
               
               

               
               
     
     
               
               

     
          

          
