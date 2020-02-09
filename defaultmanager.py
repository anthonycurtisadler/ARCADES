### Class for managing defaults using either pickle or database,
### allowing migration to complete database organization

from complexobjecttransformindexes import transform
import datetime
from display import Display

display = Display()



def convert (x):

     """Converts non-string types to string for storage in database
     Notice that I have to use type instead of instance for boolean"""
     

     if type(x) == int:
          return '<<int>>'+str(x)
     elif type(x) == float:
          return '<<float>>'+str(x)
     elif type(x) == bool:
          return '<<bool>>'+str(x)
     elif type(x) in [list,set,dict]:         
          return '<<eval>>'+str(x)
     elif type(x) == str:
          if x.startswith('<<int>>'):
               return int(x[7:])
          elif x.startswith('<<float>>'):
               return float(x[9:])
          elif x.startswith('<<bool>>'):
               return {'True':True,
                       'False':False}[(x[8:])]
          elif x.startswith('<<eval>>'):
               return eval(x[8:])
          else:
               return x
     else:
          print('ERROR NOT VALID TYPE')
          return x
          
          
     
          

class DefaultManager:

     
     def __init__ (self,
                   default_dictionary=None,
                   notebookname=None,
                   using_shelf=True,
                   using_database=True,
                   connection=None,
                   cursor=None):

          self.default_dictionary = default_dictionary
          self.notebookname = notebookname
          self.using_shelf = using_shelf
          self.using_database = using_database
          self.connection = connection
          self.cursor = cursor
          

     def set (self,
              label,
              value,
              override=False,
              not_db=False):

          """Inserts values into database
          """
              
          if not override and self.using_shelf:
               self.default_dictionary[label] = value
               if label == 'projects':
                    pass
          if not not_db and self.using_database:
               if label in ['projects','sequences']:
                    if not isinstance(value,str):
                         value = str(transform(value),indexstrings=False)
               else:
                    value = convert(value)

               
               value_tuple = (self.notebookname,label,value,)
               self.cursor.execute("INSERT OR REPLACE INTO"
                                   +" defaults (notebook,attribute,content)"
                                   +"  VALUES (?,?,?);",value_tuple)
               self.connection.commit()



     def get (self,
              label,
              show=False):

          """Retrieves values from database
          """
          def print_to(x,to=10):

               return str(x)[0:min([to,len(str(x))])]
               

          if show:

               value_tuple = (self.notebookname,label,)
               self.cursor.execute("SELECT content "
                                   +" FROM defaults WHERE notebook=?"
                                   +"  AND attribute=?;",value_tuple)
               fetched = self.cursor.fetchone()
               if fetched:
                    print('DATABASE',label,print_to(convert(fetched[0])))
               else:
                    print('DATABASE FAIL',label)
          
               try:
                    print('SHELF',label,print_to(self.default_dictionary[label]))
               except:
                    print('SHELF FAIL')
                    
          
          if self.using_database:
               value_tuple = (self.notebookname,label,)
               self.cursor.execute("SELECT content "
                                   +" FROM defaults WHERE notebook=?"
                                   +"  AND attribute=?;",value_tuple)
               fetched = self.cursor.fetchone()
               if label not in ['projects','sequences']:
                    if fetched:
                         
                         return convert(fetched[0])
                    else:
                         try:
                              return self.default_dictionary[label]
                         except:
                              return None
               else:
                    if fetched:
                         return fetched[0]

                    return self.default_dictionary[label]
##                    if fetched:
##
##                         return transform(eval(fetched[0]))
##                    else:
##                         try:
##
##                              return self.default_dictionary[label]
##                         except:
##                              return None
               
          return self.default_dictionary[label]

     def contains (self,
                   label):
          
          """Tests to see if an attribute is in the dictionary"""
          return label in self.default_dictionary

     def database_contains (self,
                            label):

          if self.using_database:
               value_tuple = (self.notebookname,label,)
               self.cursor.execute("SELECT content "
                                   +" FROM defaults WHERE notebook=? "
                                   +" AND attribute=?;",value_tuple)
               fetched = self.cursor.fetchone()
          try:
               return len(fetched)>0
          except:
               return False
        

     def backup (self,
                 label):

          if label not in self.default_dictionary:
               return False

          elif label in ['projects','sequences']:
               if self.default_dictionary['projects']:
                    value = self.default_dictionary['projects'].return_dict()
                    value = str(transform(value))
                    self.set(label,value,override=True)
                    
                    

##          elif isinstance(self.default_dictionary[label],[list,dict,set]):
##
##               if self.default_dictionary[label]:
##                    value = str(transform(self.default_dictionary[label]))
##                    self.set(label,value,override=True)

          elif label in ['knower',
                         'commands',
                         'keymacros',
                         'definitions',
                         'abbreviations',
                         'macros',
                         'indextable']:

               self.set(label,self.default_dictionary[label].export_string(),override=True)
          

     def restore_from_backup (self,
                              label):
  

          if label not in self.default_dictionary:
               return False

          
          elif label == 'sequences':

               value = self.get(label)
               

               if not isinstance(value,dict):
                    table = {"<class 'float'>":"'###float###'",
                              "<class 'str'>":"'###STR###'",
                              "<class 'datetime.date'>":"'###date###'"}
                    for x in table:
                         value = value.replace(x,table[x])

                         
                    
                    
                    
                    
                              

                    value = transform(eval(value),indexstrings=False)


               

               self.default_dictionary['sequences'] = value

####          elif isinstance(self.default_dictionary[label],[list,dict,set]):
####
####               value = self.get(label)
####               value = transform(value)
####               self.default_dictionary[label] = value
               

          elif label in ['knower',
                         'commands',
                         'keymacros',
                         'definitions',
                         'abbreviations',
                         'macros',
                         'indextable',
                         'projects']:

               
               display.noteprint(('','RESTORING '+label))       

               value = self.get(label)

               self.default_dictionary[label].import_string(value)
               
               display.noteprint(('',label+' RESTORED'))       
         

     def activate_database(self):
          self.using_database = True
     def activate_shelf(self):
          self.using_shelf = True
     def deactivate_database(self):
          self.using_database = False
     def deactivate_shelf(self):
          self.using_shelf = False

     
          
     
               

               
                   
