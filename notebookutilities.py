#The following are utilies that access the notebook,
#which is sent in as an object in the function call

from generalutilities import isindex
from plainenglish import Alerts
alerts = Alerts

def next_next(index,
              index_list=None,
              rightat=False,
              notebook=None):


    """ returns the next available 'next' note"""

    #For an unrestricted index domain 
    if index_list is None:
        index_list = notebook.indexes()

    #If no note exists at the given index, then return given index
    if rightat:

        if str(index) not in index_list:
            return index

    #Otherwise, fetch the next index.    
    while True:
        if str(index.next()) not in index_list:
            return index.next()
        index = index.next()


def next_child(index,
               index_list=None,
               notebook=None):


    """ returns the next available 'child' note"""

    #For an unrestricted index domain
    if index_list is None:
        index_list = notebook.indexes()

    #If no note exists at the given index, then return given index
    if str(index.child()) not in index_list:
        return index.child()

    #Return child index 
    return index.child().next()


def check_hyperlinks(entry=[],
                     purge=False,
                     display=None,
                     notebook=None):

    
    """Checks to see if hyperlinks
    are contained in notebook; assigns new if not"""

    

    if not entry:
        return []
    if isinstance(entry,set):
        is_set = True
        entry = list(entry)

    else:
        is_set = False

   
    


    if isinstance(entry,list):
        returning = []

        for x_temp in entry:
            x_temp = str(x_temp)
            if isindex(x_temp):
                if x_temp not in notebook.indexes():
                    display.noteprint((alerts.ATTENTION,
                                       alerts.INDEX + x_temp
                                       + alerts.NOT_FOUND_IN_NOTEBASE))
                else:
                    if x_temp not in notebook.default_dict['indextable'].all_from():
                        x_temp = notebook.default_dict['indextable'].assign(x_temp)
                        
                    else:
                        x_temp = notebook.default_dict['indextable'].get_assigned(x_temp)
                    returning.append(x_temp)
            
            elif x_temp and x_temp[0] == '#':
                if x_temp in notebook.default_dict['indextable'].all_from():
                    returning.append(x_temp)

            else:
                if not purge:
                    
                    returning.append(x_temp)

                
    if is_set:
        returning = set(returning)
    return returning


def transpose_keys(entry_list=None,
                   surround=True,
                   notebook=None):

    """Transpose keys that are indexes"""

    to_return = []

    if isinstance(entry_list,list):
        to_return = []
        
        for x_temp in entry_list:
            to_return.append(str(notebook.default_dict['indextable']
                                 .transform(x_temp,surround=surround)))
        return to_return

    elif isinstance(entry_list,set):
        to_return = set()
        
        for x_temp in entry_list:
            to_return.add(str(notebook.default_dict['indextable']
                              .transform(x_temp,surround=surround)))
        return to_return

    else:
        to_return = notebook.default_dict['indextable']\
                    .transform(entry_list,surround=surround)

    return to_return


def how_common(entrylist,
               dictionaryobject=None,
               display=None):

    """ For a given dictionaryobject, returns a
    sorted list of tuples containing two entries:
    the key in the dictionary, and either
    the size of its value, if a set or list,
    or the integer value.
    """


    returnlist = []


    if dictionaryobject:

        for w_temp in entrylist:
            if w_temp in dictionaryobject:
                if isinstance(dictionaryobject[w_temp],
                              (set,list)):
                    returnlist.append((w_temp,
                                       len(dictionaryobject[w_temp])))
                if isinstance(dictionaryobject[w_temp],int):
                    returnlist.append((w_temp,
                                       dictionaryobject[w_temp]))

        return sorted(returnlist,
                      key=lambda x_temp: x_temp[1])
    else:
        display.noteprint((alerts.ATTENTION,
                           alerts.NO_DICTIONARY_OBJECT))
