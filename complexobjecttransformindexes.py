### Takes a dictionary, makes a copy of it, and applies
### transformations to INDEXES and DATES, yielding strings 

import copy
from indexclass import Index
import datetime
from globalconstants import DASH, COLON, PERIOD, BLANK, PLUS, EMPTYCHAR
from orderedlist import OrderedList

ordlist_example = OrderedList(['1'],indexstrings=True)


def is_date(entry,returndate=False):


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

        if entry.count(DASH)>1 and entry.count(COLON)>1 and entry.count(PERIOD)==1:
             entry = entry.replace(DASH,BLANK).replace(COLON,BLANK).replace(PERIOD,BLANK).split(BLANK)
             entry = [int(a.strip()) for a in entry]
             if returndate:
                    return datetime.datetime(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
             
        else:
             
             if entry and entry[0] == DASH:
                 entry = entry[0].replace(DASH,PLUS)+entry[1:]
             entry = entry.split(DASH)

             for x_temp in entry:
                 if not x_temp.isnumeric():
                     False
             entry = [int(x_temp.replace(PLUS,DASH)) for x_temp in entry]

               
    

    for counter,x_temp in enumerate(entry):
        if not isinstance(x_temp,int):
            return False
        if not (date_constraints[counter][0]<=x_temp<=date_constraints[counter][1]):
            return False
    if returndate:

        if len(entry) == 3:
            return datetime.date(entry[0],entry[1],entry[2])
        elif len(entry) == 5:
            return datetime.datetime(entry[0],entry[1],entry[2],entry[3],entry[4])
        elif len(entry) == 7:
            return datetime.datetime(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6])
    
    return True 


def transform(complexobject,start=True):

     """ copies dictionary, and applies tranformations
     """

     def dummy (y):
          return y
     if start:
          complexobject = copy.deepcopy(complexobject)
          start = False
          
          

     if isinstance(complexobject,dict):
          for x in list(complexobject.keys()):
              complexobject[x]=transform(complexobject[x],start=start)
          return complexobject
     elif isinstance(complexobject,list):
          newlist = []
          for x in complexobject:
               newlist += [transform(x,start=start)]
          return newlist
     elif isinstance(complexobject,set):
          newset = set()
          for x in complexobject:
               newset.add(transform(x,start=start))
          return newset
     elif isinstance(complexobject,tuple):
          newlist = []
          for x in complexobject:
               newlist += [transform(x,start=start)]
          return tuple(newlist)

               
     else:
               if type(complexobject) == type(Index(0)):
                    return '<'+str(complexobject)+'>'
               elif isinstance(complexobject,str) and len(complexobject)>4\
                    and complexobject[0:2] == '<<'\
                    and complexobject[-2:] == '>>':
                    return OrderedList(eval(complexobject[2:-2]),indexstrings=True)
                   
               elif isinstance(complexobject,str) and len(complexobject)>2\
                    and complexobject[0] == '<' \
                    and complexobject[-1] == '>':
                    return Index(complexobject[1:-1])
               elif type(complexobject) == type(datetime.datetime.now()):
                    return str(complexobject)
               elif isinstance(complexobject,str) and COLON in complexobject and DASH in complexobject and PERIOD in complexobject and \
                    complexobject.replace(DASH,EMPTYCHAR).replace(PERIOD,EMPTYCHAR).replace(COLON,EMPTYCHAR).replace(BLANK,EMPTYCHAR).isnumeric():
                    return is_date(complexobject,returndate=True)
##               elif isinstance(complexobject,str) and complexobject.startswith('datetime.datetime'):
##                        return eval(complexobject)
               elif type(complexobject) == type(ordlist_example):
                    return '<<['+str(complexobject)+']>>'
               else:
                    return complexobject
               
               
               
                    
                    
               
              
