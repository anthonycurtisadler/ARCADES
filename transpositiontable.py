## IMPORTED UTILITIES

from globalconstants import LEFTPAREN, RIGHTPAREN, PERIOD
from indexutilities import index_is_reduced, index_reduce, index_expand
from copy import deepcopy

## CLASS DEFINITION

class TranspositionTable:

    def __init__(self,
                 index_list=None,
                 using_dict=True,
                 connection=None,
                 cursor=None,
                 notebookname=None):
        

        self.table = {}
        if isinstance(index_list,dict):
            self.table = deepcopy(index_list)
        elif index_list:
            self.table ={str(x_temp):str(x_temp) for x_temp in index_list}
        self.connection = connection
        self.cursor = cursor
        self.using_database = False
        self.using_dict = True
        self.notebookname = notebookname 
        

        if self.connection and self.cursor:

            self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS indextable (

                notebook TEXT NOT NULL,
                index_from TEXT NOT NULL,
                index_to TEXT NOT NULL,
                UNIQUE (notebook, index_from),
                FOREIGN KEY (notebook, index_to) REFERENCES notebooks (notebook, note_index) ON DELETE CASCADE
                );""")
            self.using_database = True

    def restore_connection (self,
                         connection=None,
                         cursor=None):

        self.cursor = cursor
        self.connection = connection

    def purge_connection (self):
        
        self.cursor = None
        self.connection = None
         

    def __str__ (self):
        return_list = []
        for x_temp in self.table:
            return_list.append(x_temp+':'+self.table[x_temp])
        return ', '.join(return_list)

    def add_to_db (self,index_from,index_to):
        self.cursor.execute("INSERT OR REPLACE INTO indextable (notebook, index_from, index_to) VALUES (?,?,?);",
                            (self.notebookname,index_from,index_to))
        self.connection.commit()

    def delete_from_db (self,index_from=None,index_to=None):
        
        
        if index_from and index_to:
            value_tuple = (self.notebookname,index_from,index_to)
            self.cursor.execute("DELETE FROM"
                              +" indextable"
                              +" WHERE notebook=?"
                              +" and index_from=?"
                              +" and index_to=?;",
                              value_tuple)
        elif index_from:

            value_tuple = (self.notebookname,index_from)
            self.cursor.execute("DELETE FROM"
                              +" indextable"
                              +" WHERE notebook=?"
                              +" and index_from=?;",
                              value_tuple)
        elif index_to:

            value_tuple = (self.notebookname,index_to)
            self.cursor.execute("DELETE FROM"
                              +" indextable"
                              +" WHERE notebook=?"
                              +" and index_to=?;",
                              value_tuple)
        self.connection.commit()

    def db_contains (self,index_from=None,index_to=None):
        
        if index_from and index_to:

            value_tuple = (self.notebookname,index_from,index_to)            
            self.cursor.execute("SELECT * FROM indextable WHERE notebook=? and index_from=? and index_to=?;",
                                value_tuple)
        elif index_from:
            value_tuple = (self.notebookname,index_from)            
            self.cursor.execute("SELECT * FROM indextable WHERE notebook=? and index_from=?;",
                                value_tuple)
        elif index_to:
            value_tuple = (self.notebookname,index_to)            
            self.cursor.execute("SELECT * FROM indextable WHERE notebook=? and index_to=?;",
                                value_tuple)

        try:
            if self.cursor.fetchone()[0]:
                return True
            return False
        except:
            return False

    def db_get_to (self,index_from):

        self.cursor.execute("SELECT index_to FROM indextable WHERE notebook=? and index_from=?",
                            (self.notebookname,index_from))
        return self.cursor.fetchone()[0]

    def db_get_from (self,index_to):
        self.cursor.execute("SELECT index_from FROM indextable WHERE notebook=? and index_to=?",
                            (self.notebookname,index_to))
        return self.cursor.fetchone()[0]


        
                                       

    def load(self,index_list=None):

        # loads in a single list of non-transposed indexes 

        if index_list:
            if self.using_dict:
                self.table ={str(x_temp):str(x_temp) for x_temp in index_list}

            if self.using_database:
                for x_temp in index_list:
                    self.add_to_db(str(x_temp),str(x_temp))
                    
                
        

    def move(self,ind_from,ind_to):
 
        ind_from = str(ind_from)
        ind_to = str(ind_to)

        if self.using_dict:
            if ind_from in self.table and ind_to not in self.table.values():
                self.table[ind_from] = ind_to
            if ind_from not in self.table and\
               ind_from in self.table.values() and\
               ind_to not in self.table.values():
                for x_temp in self.table:
                    if self.table[x_temp] == ind_from:
                        self.table[x_temp] = ind_to
                        
        if self.using_database:
            if self.db_contains(index_from=ind_from) and not self.db_contains(index_to=ind_to):
                self.add_to_db(ind_from,ind_to)
            if not self.db_contains(index_from=ind_from) and self.db_contains(index_to=ind_from) and \
               not self.db_contains(index_to=ind_to):
                original_from= self.db_get_from(index_to=ind_from)
                self.delete_from_db(index_to=ind_from)
                self.add_to_db(index_from=original_from,index_to=ind_to)
            

    def transpose(self,index_list=None):

        #returns a list of transposed indexes 
        return_list = []
        if self.using_database:
            for x_temp in index_list:
                return_list.append(self.db_get_to(x_temp))
            return return_list

    
        for x_temp in index_list:
            if x_temp in self.table:                
                return_list.append(self.table[x_temp])
        return return_list

    def add(self,new_index):
        new_index = str(new_index)
        if self.using_dict:
            if new_index not in self.table and new_index not in self.table.values():
                self.table[new_index]=new_index
        if self.using_database:
            if not self.db_contains(index_from=new_index) and not self.db_contains(index_to=new_index):
                self.add_to_db(index_from=new_index,index_to=new_index)
            

    def delete(self,to_delete):
        to_delete = str(to_delete)
        if self.using_dict:
            if to_delete in self.table:
                del self.table[to_delete]
        if self.using_database:
            if self.db_contains(index_from=to_delete):
                self.delete_from_db(index_from=to_delete)

    def transform(self,new_index,surround=True):
        #returns a transposed index if in the table, otherwise returns the value
        new_index = str(new_index)
        if self.using_database:
            if self.db_contains(index_from=new_index):
                return '<<'*surround+index_reduce(self.db_get_to(new_index))+'>>'*surround
            return new_index

            
        if new_index in self.table:
            return '<<'*surround+index_reduce(self.table[new_index])+'>>'*surround
        return new_index

    def export_string(self):
        #for exporting the content of the table as a string

        returnstring = ''

        for x_temp in self.table:
            returnstring+=x_temp+'/'+self.table[x_temp]+','
        return returnstring[:-1]
    

    def import_string(self,enter_string):
        # for importing the content of the table as a string 

        if self.using_dict:
            del self.table
            self.table = {}
            
            if enter_string:

                for x_temp in enter_string.split(','):
                    key, value = x_temp.split('/')[0],x_temp.split('/')[1]
                    self.table[key] = value
                    
        if self.using_database:
            if enter_string:
                self.cursor.execute("SELECT * FROM indextable")
                temp_results = self.cursor.fetchall()
                if len(temp_results) < len(enter_string.split(',')):
                

                    for x_temp in enter_string.split(','):
                        
                        key, value = x_temp.split('/')[0],x_temp.split('/')[1]
                        self.add_to_db(index_from=key,index_to=value)
                
                
        
        
                
            
    


##starting_list = index_list=input('?').split(',')
##xtable = TranspositionTable(starting_list)
##print(str(xtable))
##while True:
##    xtable.change(input('?'),input('??'))
##    print(str(xtable))
##    print(', '.join(xtable.transpose(starting_list)))
##    if input('delete?') in ['y']:
##        xtable.delete(input('?'))
##    print(str(xtable))
##    if input('add') in ['y']:
##        xtable.add(input('?'))
        
    
