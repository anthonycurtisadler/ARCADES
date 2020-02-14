from orderedlist import OrderedList
import datetime
import sqlite3
from indexclass import Index

SLASH = '/'
type_table = {str(str):str,
             str(float):float,
             str(datetime.date):datetime.date,
             str(Index):Index}

from globalconstants import DASH, COLON, PERIOD, BLANK, PLUS 



def is_date(entry,returndate=True,maxlen=0):



    """Utility to test if a string constitutes a date, returning either
    a boolean value or a converted date """

    date_constraints = {0:(-800000000000,+80000000000),
                        1:(1,12),
                        2:(1,31),
                        3:(0,23),
                        4:(0,59),
                        5:(0,59),
                        6:(0,1000000)}

    if not isinstance(entry,(tuple,list)):

        if entry.count(DASH)>1 \
           and entry.count(COLON)>1 \
           and entry.count(PERIOD)==1:
             entry = entry.replace(DASH,BLANK).\
                     replace(COLON,BLANK).\
                     replace(PERIOD,BLANK).split(BLANK)
             entry = [int(a.strip())
                      for a in entry]
             if returndate:
                    return datetime.datetime(entry[0],
                                             entry[1],
                                             entry[2],
                                             entry[3],
                                             entry[4],
                                             entry[5],
                                             entry[6])
             
        else:
             
             if entry and entry[0] == DASH:
                 entry = entry[0].replace(DASH,PLUS)+entry[1:]
             entry = entry.split(DASH)

             for x_temp in entry:
                 if not x_temp.isnumeric():
                     False
             entry = [int(x_temp.replace(PLUS,DASH))
                      for x_temp in entry]

               
    

    for counter,x_temp in enumerate(entry):
        if not isinstance(x_temp,int):
            return False
        if not (date_constraints[counter][0]
                <= x_temp
                <= date_constraints[counter][1]):
            return False
    if returndate:

        if len(entry) <4 or maxlen <= 3:
            entry+=[1,1,1]
            return datetime.date(entry[0],
                                 entry[1],
                                 entry[2])
        elif len(entry) == 5 or maxlen <= 5:
            return datetime.datetime(entry[0],
                                     entry[1],
                                     entry[2],
                                     entry[3],
                                     entry[4])
        elif len(entry) == 7:
            return datetime.datetime(entry[0],
                                     entry[1],
                                     entry[2],
                                     entry[3],
                                     entry[4],
                                     entry[5],
                                     entry[6])
    
    return True 

def convert(x):

     if type(x) == str:
          return x
     if type(x) == float:
          return x
     if type(x) == type(datetime.datetime.now()):
          return '<<DATE>>'+str(x)
     if type(x) == type(Index(0)):
          return '<<INDEX>>'+str(x)
     return str(x)
    

def deconvert(x):

    if isinstance(x,float):
        return x
    

     
    if x.startswith('<<DATE>>'):
      return is_date(x[8:])
    if x.startswith('<<INDEX>>'):
      return Index(x[9:])
    return x




class Sequences:

     def __init__ (self,
                   db_cursor=None,
                   db_connection=None,
                   notebookname=None,
                   sequence_dictionary=None,
                   using_database=False,
                   using_shelf=False):

          self.db_cursor = db_cursor
          self.db_connection = db_connection
          if using_database:
               self.create_database()
          self.notebookname = notebookname
          self.using_database=using_database
          self.using_shelf=using_shelf

          

          self.temp_sequences = {'###type###':{}}
          self.sequence_dictionary = sequence_dictionary
          self.testing=False


     def empty(self):

          if self.using_shelf:
               self.sequence_dictionary.clear()

          if self.using_database:


               self.db_cursor.execute("DELETE FROM sequence_names")
               self.db_cursor.execute("DELETE FROM sequence_types")
               self.db_cursor.execute("DELETE FROM sequence_values")
               self.db_connection.commit()
               
               

     def create_database (self):
          
          self.db_cursor.executescript("""
               CREATE TABLE IF NOT EXISTS sequence_names (
             notebook TEXT NOT NULL,
             name NOT NULL,
             UNIQUE (notebook, name)
             FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
             );""")


          self.db_cursor.executescript("""
               CREATE TABLE IF NOT EXISTS sequence_types (
             notebook TEXT NOT NULL,
             name NOT NULL,
             type NOT NULL,
             UNIQUE (notebook, name)
             FOREIGN KEY (notebook, name) REFERENCES sequence_names (notebook, name) ON DELETE CASCADE
             );""")

          self.db_cursor.executescript("""
               CREATE TABLE IF NOT EXISTS sequence_values (
             notebook TEXT NOT NULL,
             name NOT NULL,
             value NOT NULL,
             UNIQUE (notebook, name, value)
             FOREIGN KEY (notebook, name) REFERENCES sequence_names (notebook, name) ON DELETE CASCADE
             );""")

     def purge_connection (self):

          self.db_cursor = None
          self.db_connection = None 
          

     def add_sequence_name_db (self,name):

          value_tuple = (self.notebookname,
                         name)

          self.db_cursor.execute("INSERT OR REPLACE INTO "+
                                 "sequence_names (notebook, name) "+
                                 "VALUES (?,?);",value_tuple)
          self.db_connection.commit()

     def add_type_db (self,name,seq_type):
          

          value_tuple = (self.notebookname,
                         name,str(seq_type))
          self.db_cursor.execute("INSERT OR REPLACE INTO "+
                                 "sequence_types (notebook, name, type) "+
                                 "VALUES (?,?,?);",value_tuple)
          self.db_connection.commit()

     def delete_type_db (self,name):

          value_tuple = (self.notebookname,
                         name,)
          self.db_cursor.execute("DELETE FROM sequence_types "+
                                 "WHERE notebook=? AND name=?;",value_tuple)
          self.db_connection.commit()

     def delete_sequence_name_db (self,name):

          value_tuple = (self.notebookname,
                         name,)
          self.db_cursor.execute("DELETE FROM sequence_names "+
                                 "WHERE notebook=? AND name=?;",value_tuple)
          self.db_connection.commit()


     def delete_value_db (self,name,value):

          value_tuple = (self.notebookname,
               name,value)
          self.db_cursor.execute("DELETE FROM "+
                                 "sequence_values WHERE notebook=? AND name=? "+
                                 "AND value=?;",value_tuple)
          
          self.db_connection.commit()

          if name in self.temp_sequences:

               self.temp_sequences[name].delete(value)

     def delete_all_values_db (self,name):

          value_tuple = (self.notebookname,
               name)
          self.db_cursor.execute("DELETE FROM "+
                                 "sequence_values"
                                 +" WHERE notebook=? AND name=?;",
                                 value_tuple)
          
          self.db_connection.commit()

          if name in self.temp_sequences:

               del self.temp_sequences[name]
          

        

     def add_value_db (self,name,value):

          value = convert(value)

          value_tuple = (self.notebookname,
                         name,
                         value,)
          self.db_cursor.execute("INSERT OR REPLACE INTO "+
                                 "sequence_values (notebook, name, value) "+
                                 "VALUES (?,?,?);",value_tuple)
          self.db_connection.commit()

          if name in self.temp_sequences:

               self.temp_sequences[name].add(value)
          

          

     def get_type_db (self,name):

          self.db_cursor.execute("SELECT type FROM sequence_types "+
                                 " WHERE notebook=? AND name=?",
                                 (self.notebookname, name))
          result = self.db_cursor.fetchone()
               
          if result:
               return result[0]
          else:
               return None

     def get_all_types_db (self):

          self.db_cursor.execute("SELECT name FROM sequence_types "+
                                 " WHERE notebook=?",
                                 (self.notebookname,))
          return [x[0] for x in self.db_cursor.fetchall()]

     def get_all_names_db (self):

          self.db_cursor.execute("SELECT name FROM sequence_names "+
                                 " WHERE notebook=?",
                                 (self.notebookname,))
          result = self.db_cursor.fetchall()
          result = [x[0] for x in result]

          return result
     
     def contains_type_db (self,name):

          self.db_cursor.execute("SELECT * FROM sequence_types "+
                                 " WHERE notebook=? AND name=?",
                                 (self.notebookname, name,))
          result = self.db_cursor.fetchone()

          try:
               if result[0]:
                    return True
               return False
          except:
               return False

     def contains_name_db (self,name):

          self.db_cursor.execute("SELECT * FROM sequence_names "+
                                 " WHERE notebook=? AND name=?",
                                 (self.notebookname, name))
          try:
               if self.db_cursor.fetchone()[0]:
                    return True
               return False
          except:
               return False
          
     
     def return_ordered_from_db (self,name):

          self.db_cursor.execute("SELECT value FROM sequence_values "+
                                      " WHERE notebook=? AND name=?",
                                      (self.notebookname, name))
          fetched = self.db_cursor.fetchall()
          values = [deconvert(x[0]) for x in fetched]

          if self.get_type_db(name) == "<class 'datetime.date'>":
              
              values = [is_date(x) for x in values]
              

          if values:           

               if name not in self.temp_sequences:

                    self.temp_sequences['###type###'][name] = self.get_type_db(name)
                    self.temp_sequences[name] = OrderedList(values)

                    return self.temp_sequences[name]
               if not self.temp_sequences[name]:
                    self.temp_sequences[name] = OrderedList()
               return self.temp_sequences[name]
        
          return OrderedList()

     def return_value (self,s_value=None,db_value=None,phrase=None):

          if self.testing:
               print(phrase,s_value,db_value)
               print('USING DATABASE',self.using_database)
          

          if not s_value and not db_value:
               return None
          elif not db_value:
               return s_value
          elif not s_value:
               return db_value
          else:
               if self.using_database:
                    return db_value
               return s_value


     def query (self,term1='',term2='',term3='',action=None):
          sv=None
          dbv=None

          if action=='get':

               if term1=='#TYPE#' and not term2:

                    if self.using_shelf:
                         sv = list(self.sequence_dictionary[term1].keys())
                         
                         if not sv:
                              
                              sv = []
                         print(sv)

                    if self.using_database:
                         dbv = self.get_all_types_db()
                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)

               elif term1=='#TYPE#':

                    if self.using_shelf:
                         if term2 in self.sequence_dictionary[term1]:
                              sv = self.sequence_dictionary[term1][term2]
                         else:
                              sv = ''
                    if self.using_database:
                         dbv = self.get_type_db(term2)
                         if dbv in type_table:
                              dbv = type_table[dbv]
                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)


               elif term1 and not term2:


                    if self.using_shelf:
                         if term1 in self.sequence_dictionary:
                              sv = self.sequence_dictionary[term1]
                         else:
                              sv = OrderedList()
                    if self.using_database:
                         dbv = self.return_ordered_from_db(term1)
                    

                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)
            
           

               elif not term1:

                    if self.using_shelf:
                         sv = list(self.sequence_dictionary.keys())
                         if not sv:
                              sv = []

                    if self.using_database:
                         dbv = self.get_all_names_db()
                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)
                         

          if action=='in':

               if term1=='#TYPE#':

                    if self.using_shelf:

                         sv = term2 in self.sequence_dictionary[term1]

                    if self.using_database:

                         dbv = self.contains_type_db (term2)
                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)

               elif not term2:

                    if self.using_shelf:

                         sv = term1 in self.sequence_dictionary

                    if self.using_database:

                         dbv = self.contains_name_db (term1)
                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)

               elif term1 and term2:

                    if self.using_shelf:
                         if term1 in self.sequence_dictionary:
                              sv = term2 in self.sequence_dictionary[term1].list
                    if self.using_database:
                         dbv = term2 in self.return_ordered_from_db(term1).list
                    return self.return_value(sv,dbv,str(term1)+'/'+str(term2)+str(term3)+'/'+action)
                    

          if action=='set':

               if term1=='#TYPE#' and term2 and term3:

                    if self.using_shelf:

                         self.sequence_dictionary[term1][term2] = term3

                         

                    if self.using_database:

                         if term3 in [float,str,datetime.date,Index]:
                              term = str(term3)
                         
                         self.add_sequence_name_db (term2)
                         self.add_type_db (term2,term3)


               elif term1 and term2 and not term3:

                    if self.using_shelf:

                         if term1 not in self.sequence_dictionary:

                              self.sequence_dictionary[term1] = OrderedList()
                              self.sequence_dictionary[term1].add(term2)
                         else:
                              try:
                                   self.sequence_dictionary[term1].add(term2)
                              except:
                                   print('SEQUENCE ERROR')
                    if self.using_database:

                         self.add_value_db(term1,term2)

          if action=='delete':

               if term1=='#TYPE#' and term2:
                    
                    if self.using_shelf:

                         if term2 in self.sequence_dictionary[term1]:

                              del self.sequence_dictionary[term1][term2]

                    if self.using_database:
                         self.delete_type_db (term2)
                         self.delete_sequence_name_db (term2)

               elif term1 and term2:

                    if self.using_shelf:

                         if term1 in self.sequence_dictionary:

                              self.sequence_dictionary[term1].delete(term2)
                              
                    if self.using_database:

                         self.delete_value_db(term1,term2)

               elif not term2:

                    if self.using_shelf:

                         del self.sequence_dictionary[term1]

                    if self.using_database:

                         self.delete_all_values_db(term1)


          if action == 'initiate':

               if term1 and not term2 and not term2:

                    if self.using_shelf:

                         self.sequence_dictionary[term1] = OrderedList()




          
def expose():

          db_cursor.execute("SELECT * FROM sequence_names")
          print(db_cursor.fetchall())
          db_cursor.execute("SELECT * FROM sequence_types")
          print(db_cursor.fetchall())
          db_cursor.execute("SELECT * FROM sequence_values")
          print(db_cursor.fetchall())

          print(shelf)
     
                         
if __name__ == "__main__":

     db_connection = sqlite3.connect('notebooks'+SLASH+'girin.db')
     db_cursor = db_connection.cursor()
     shelf = {'#TYPE#':{}}
     

     seq = Sequences(db_cursor=db_cursor,
                     db_connection=db_connection,
                     notebookname='defaultnotebook',
                     sequence_dictionary=shelf,
                     using_database=True,
                     using_shelf=True)


 
