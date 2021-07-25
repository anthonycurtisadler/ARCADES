import copy
import rangelist
from globalconstants import VERTLINE
from plainenglish import Labels
from indexclass import Index
from generalutilities import abridge, show_list
import nformat
from indexutilities import index_reduce
from rangelist import split_up_range


labels = Labels()

def formkeys(entry_temp):

    """ combines format key and transpose keys """

    return nformat.format_keys(transpose_keys(entry_temp))

class histogram:



    def __init__(self,displayobject=None,
                 for_indexes=True,
                 db_connection_cursor=None,
                 notebookname=''):

        

        self.histo_dict = {}
        self.displayobject = displayobject
        self.for_indexes=for_indexes
        self.database_mode = False
        self.db_connection_cursor = db_connection_cursor
        self.notebookname = notebookname 
        
        
    def load_dictionary(self,entrydictionary=None,
                        flag="w",
                        histo_word_dict = None,
                        histo_key_dict = None,
                        histo_tag_dict = None,
                        projects=None,
                        func=lambda x,y:x,
                        truncatespecs=''): #idnta  index date number text all

        #flag 'w' for words
        #flag 'k' for keys
        #flag 't' for tags
        self.histo_word_dict = histo_word_dict
        self.histo_key_dict =  histo_key_dict
        self.histo_tag_dict =  histo_tag_dict
        print('TRUNCATING: ',truncatespecs)
        
        
        def trunckey (x):

            if '@' not in x:
                return x
            else:
                for spec in truncatespecs:

                    if spec == 'p' and x.split('@')[0] in projects:
                        return x.split('@')[0]+'@'
                    elif spec == 'i' and '@_' in x:  #For index sequences
                        return  x.split('@_')[0]+'@'
                    elif spec == 'd' and '@#' in x: #Dor date sequences 
                        return x.split('@#')[0]+'@'  #For numeric 
                    elif ((spec == 'n' and x.split('@')[1].replace('.','').isnumeric()) or
                          (spec in ['t'] and not x.split('@')[1].replace('.','').isnumeric()) or
                          (spec in ['a'])): #For others 
                        return x.split('@')[0]+'@'
            return x
                          

                    
                

        if entrydictionary:

            self.histo_dict = copy.deepcopy(entrydictionary)

        else:

            if 'w' in flag:

                if not self.histo_word_dict or 'n' in flag:

                    self.displayobject.noteprint(('ATTENTION',
                                       'Making temporary word dictionary!'))

                    value_tuple = (self.notebookname,)
                    self.db_connection_cursor.execute("SELECT word "
                                      +"FROM word_to_indexes "
                                      +"WHERE notebook=?;",
                                      value_tuple)
                    fetched = self.db_connection_cursor.fetchall()
                    for word in fetched:

                        value_tuple = (self.notebookname,word[0],)
                        self.db_connection_cursor.execute("SELECT note_index "
                                          +"FROM word_to_indexes "
                                          +"WHERE notebook=? and word=?;",
                                          value_tuple)

                        fetched = self.db_connection_cursor.fetchall()
                        if fetched:
                            indexes = {index[0].strip() for index in fetched}
                            self.histo_dict[word[0]] = indexes
                    self.displayobject.noteprint(('ATTENTION','Word dictionary finished!'))
                    self.histo_word_dict = copy.deepcopy(self.histo_dict)
                else:
                    self.displayobject.noteprint(('Using word dictionary'))
                    self.histo_dict = self.histo_word_dict 

            if 'k' in flag:

                if not self.histo_key_dict or 'n' in flag:

                    self.displayobject.noteprint(('ATTENTION',
                                       'Making temporary key dictionary!'))

                    value_tuple = (self.notebookname,)
                    self.db_connection_cursor.execute("SELECT keyword"
                                      +" FROM keys_to_indexes"
                                      +" WHERE notebook=?;",
                                      value_tuple)
                    fetched = self.db_connection_cursor.fetchall()
                    for key in func([x[0] for x in fetched],projects):

                        value_tuple = (self.notebookname,key,)
                        self.db_connection_cursor.execute("SELECT note_index "
                                          +"FROM keys_to_indexes "
                                          +"WHERE notebook=? and keyword=?;",
                                          value_tuple)

                        fetched = self.db_connection_cursor.fetchall()
                        if fetched:
                            indexes = {index[0].strip() for index in fetched}
                            self.histo_dict[trunckey(key)] = indexes
                    self.displayobject.noteprint(('ATTENTION','Key dictionary finished!'))
                    self.histo_key_dict = copy.deepcopy(self.histo_dict)
                    

                else:
                    self.displayobject.noteprint(('Using Existing Key Dictionary'))
                    self.histo_dict = self.histo_key_dict 


            if 't' in flag:

                if not self.histo_tag_dict or 'n' in flag:
                    self.displayobject.noteprint(('ATTENTION',
                                       'Making temporary tag dictionary!'))

                    value_tuple = (self.notebookname,)
                    self.db_connection_cursor.execute("SELECT tag"
                                      +" FROM tags_to_keys"
                                      +" WHERE notebook=?;",value_tuple)
                    fetched = self.db_connection_cursor.fetchall()
                    for tag in fetched:

                        value_tuple = (self.notebookname,tag[0],)
                        self.db_connection_cursor.execute("SELECT keyword "
                                          +"FROM tags_to_keys"
                                          +" WHERE notebook=? and tag=?;",
                                          value_tuple)

                        fetched = self.db_connection_cursor.fetchall()
                        if fetched:
                            keys = {key[0].strip() for key in fetched}
                            self.histo_dict[tag[0]] = keys
                    self.displayobject.noteprint(('ATTENTION','Tag dictionary finished!'))
                    self.histo_tag_dict = copy.deepcopy(self.histo_dict)

                else:
                    self.displayobject.noteprint(('Using existing tag dctionary'))
                    self.histo_dict = self.histo_tag_dict 

        return self.histo_word_dict, self.histo_key_dict, self.histo_tag_dict  
        

   

    def contract(self,entrylist):

        if entrylist:

            entryset = set(entrylist)

            for key in list(self.histo_dict.keys()):
                self.histo_dict[key] = self.histo_dict[key].intersection(entryset)
                if not self.histo_dict[key]:
                    del self.histo_dict[key]

    def implode (self,entrylist):

        for key in list(self.histo_dict):
            if key not in entrylist:
                del self.histo_dict[key]


    def show (self):


        def dict_format(x_temp):

            """formats output of the list of search results"""

            if self.for_indexes:
                shown_indexes = rangelist.range_find([Index(a_temp)
                                                      for a_temp in x_temp[1]],
                                                     reduce=True)
            else:
                shown_indexes = formkeys({abridge(index_reduce(x_temp),
                                                      maxlength=20)
                                              for x_temp in x_temp[1]})
            
                
            if len(shown_indexes) < 20:
                return (abridge(x_temp[0],maxlength=20)
                        +VERTLINE
                        +shown_indexes)

            returnlist = []
            sp_temp = split_up_range(shown_indexes,seg_length=3)
            
                                        
            returnlist.append(abridge(x_temp[0],maxlength=20)
                              +VERTLINE+sp_temp[0])
            for s_temp in sp_temp[1:]:
                returnlist.append(VERTLINE+s_temp)

            return returnlist
        
        list_to_show = []
        for key in sorted(self.histo_dict):
            list_to_show.append((key,self.histo_dict[key]))
        show_list(list_to_show,
                  labels.CONCORDANCE,
                  0, 30,
                  func=dict_format,
                  present=True,
                  display=self.displayobject)       
