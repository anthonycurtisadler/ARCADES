#pylint: disable=C0103, W0108, W0201, E1101, R0913, R0914, R0912, R0915, W0123, W0122, W0631, W0107, R1702, W0621, W0612
#pylint rated 9.83/10 with exclusions
"""NOTESCRIPTION"""


import codecs
import datetime
from itertools import cycle, product
import math
import os
import shelve
import string
import json
import sys
import sqlite3

def aprint(x):
    return
    print(x)





import _pickle as pickle

from abbreviate import Abbreviate                                       #pylint 9.63/10
from globalconstants import BOX_CHAR,\
     INTROSCRIPT, ENTERSCRIPT, FORMATTINGSCRIPT, OPENING_WIDTH, DASH, SLASH,\
     SMALLWORDS, LEFTNOTE, RIGHTNOTE, EOL, TAB,\
     BLANK, VERTLINE, DOLLAR, PERCENTAGE, EMPTYCHAR, EXCLAMATION,\
     COMMA, EQUAL, QUESTIONMARK, PERIOD, COLON, SEMICOLON, VOIDTERM, PLUS, \
     STAR, CARET, POUND, ATSIGN, LEFTBRACKET, RIGHTBRACKET, \
     LEFTCURLY, RIGHTCURLY, LEFTPAREN, RIGHTPAREN, ANDSIGN, KEYLENGTH, \
     TILDA, UNDERLINE, DELETECHARACTERS, LONGDASH, BACKSLASH


                                                                        #pylint 10.0/10

import commandscript                                                    #pylint 10.0/10
from complexobjecttransformindexes import transform
import consolidate                                                      #Stack Overflow
from convert import Convert
import copy
import curses 
from defaultscripts import COMMANDMACROSCRIPT
from defaultmanager import DefaultManager
from diagnostics import DiagnosticTracking
from display import Display                                             #pylint 9.2/10
from displaylist import DisplayList                                     #pylint 9.6/10
import emptymovingwindow
import extract                                                          #pylint 9.64/10
import flatten                                                          #pylint 10.0/10
from indexutilities import index_is_reduced, index_reduce, index_expand
from generalknowledge import GeneralizedKnowledge 
from lexical import English_frequent_words
from keydefinitions import KeyDefinitions                               #pylint 10.0/10
from keymacrodefinitions import KeyMacroDefinitions
import nformat                                                          #pylint 9.61/10
from ninput import q_input, s_input                                     #pylint 10.0/10
from indexclass import Index                                            #pylint 10.0/10
from keyauto import KeyAuto
from knowledgebase_ns_db import KnowledgeBase                              #pylint  8.62/10
from lexical import English_frequent_words
import movingwindow
from multidisplay import Note_Display                                   #pylint 9.6/10
from noteclass import Note                                              #pylint 10.0/10
from orderedlist import OrderedList
import pointerclass                                                     #pylint 9.62/10
from plainenglish import Queries, Alerts, Labels, Spelling, DefaultConsoles,\
     BREAKTERMS, NEWTERMS, QUITALLTERMS, QUITTERMS, YESTERMS, NOTERMS, ADDTERMS,\
     QUITTERMS, SHOWTERMS, DELETETERMS, CLEARTERMS, binary_settings, simple_commands
import presets
from projectmanager import ProjectManager
from purgekeys import PurgeKeys 
import rangelist                                                        #pylint 9.68/10
from registry import Registry
from sequencedefaultdictionary import SequenceDefaultDictionary
try:
    from spellcheck import SpellCheck                                       #pylint 8.83/10
    spellcheck_on = True

except:
    spellcheck_on = False
from sheetshelf import SheetShelf
import stack                                                            #pylint 10.0/10     
from temporaryholder import TemporaryHolder                             #pylint 10.0/10
import terminalsize                                                     #Stack Overflow
from transpositiontable import TranspositionTable
import random
##client = False
try:
    from PIL import Image
except:
    pass
if not os.altsep:
    os.altsep = '/'

SMALLWORDS += English_frequent_words 


#Instantiate objects standard messages for main program and modules
queries = Queries()  
alerts = Alerts()
labels = Labels()
spellingheadings = Spelling() # headings sent to spelling object
defaultheadings = DefaultConsoles() #headings sent to default consoles

defaultterms= (ADDTERMS, DELETETERMS, SHOWTERMS, QUITTERMS, CLEARTERMS)



# Constitute list of possible determinants for sorting by date
DETERMINANTS = [] 
for l_temp,r_temp in product(['y','m','d','ym','ymd',
                              'yd','md',EMPTYCHAR],
                             ['*hmsx','*hms','*hm','*h',
                              '*h','*m','*s','*x','*ms',
                              '*sx','*hx','*mx',EMPTYCHAR]):
    DETERMINANTS.append(l_temp+r_temp)

    
# Make Note objects for formatiing characters
BREAKNOTE = Note(set(),EOL+'/BREAK/'+EOL)
NEWNOTE = Note (set(),EOL+'/NEW/'+EOL)
COLUMNBEGIN = Note (set(),'/COL/' + EOL)
COLUMNEND = Note (set(),'/ENDCOL/' +EOL)


globaldirectoryname = os.getcwd() + os.altsep + 'notebooks'

# Change terminal color to white
os.system('color F0')

# Create stack object for storing commands
command_stack = stack.Stack()


## global variables ##

override = True #Overrides exception handling on main loop
multi_dict = {}#Dictionary for story display outputs
#For copyto/copyfrom -- holds notes for transfer from one notebase to another.
temporary = TemporaryHolder()

histo_word_dict = None
histo_key_dict = None
histo_tag_dict = None



# other utilities

def repeat_function_on_set(enterset,function=None):

    if function is None:
        function = dummy

    returnset = set()
    for x_temp in enterset:
        returnset.update(function(x_temp))
    return returnset 

def nprint(*entries):
    text = ''
    for entry in entries:
        text += entry + BLANK

    if text.strip:    
        display.noteprint(('',text))
    else:
        print()
    

    

def si_input (prompt=EMPTYCHAR,
              inputtext=EMPTYCHAR,
              inputrange=range(-100000,100000),
              alert=(EMPTYCHAR,EMPTYCHAR)):

    """Inputs an integer value"""

    while True:
        if inputtext  in [EMPTYCHAR, QUESTIONMARK]:
            inputtext = input(prompt)
        if inputtext.isnumeric() and int(inputtext) in inputrange:
              return int(inputtext)
        inputtext = EMPTYCHAR
        display.noteprint(alert)

def is_date(entry,returndate=False,maxlen=0):



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

        if len(entry) == 3 or maxlen <= 3:
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



def isindex(entry):

    """Utility to test if input is the
    string representation of an index"""

    if not entry:
        return False

    if isinstance(entry,int):
        return True

    if isinstance(entry,str):
        if '..' not in entry and \
           entry[0] != '.' and \
           entry[-1] != '.' and \
           entry.replace('.',EMPTYCHAR).isnumeric():
            return True

    return False

def check_hyperlinks(entry=[],purge=False):

    """Checks to see if hyperlinks
    are contained in notebook"""

    if not entry:
        return []

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
                    returning.append(x_temp)
            else:
                if not purge:
                    
                    returning.append(x_temp)
                    
    if isinstance(entry,set):
        returning = set()
        for x_temp in entry:
            x_temp = str(x_temp)
            if isindex(x_temp):
                if x_temp not in notebook.indexes():
                    display.noteprint((alerts.ATTENTION,
                                       'Index ' + x_temp
                                       + ' not found in notebase!'))
                else:
                    returning.add(x_temp)
            else:
                if not purge:
                    returning.add(x_temp)
    return returning


def transpose_keys(entry_list=None,
                   surround=True):

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
               dictionaryobject=None):

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

def formkeys(entry_temp):

    """ combines format key and transpose keys """

    return nformat.format_keys(transpose_keys(entry_temp))


def switchlanguage(language='ple'):

    """ switches from the instruction set
    in one language to another language.
    loads definitions from appropriate module
    and then also runs the language_switching method
    in the necessary objects, sending the default terms to them.
    """
    
    global Queries, Alerts, Labels, queries, alerts, labels

    del Queries
    del Alerts
    del Labels

    if language == 'ple':
        from plainenglish import Queries, Alerts,\
             Labels, Spelling, DefaultConsoles,\
             BREAKTERMS, NEWTERMS, QUITALLTERMS,\
             QUITTERMS, YESTERMS, NOTERMS,\
             DELETETERMS, SHOWTERMS, ADDTERMS, \
             CLEARTERMS, LEARNTERMS, UNLEARNTERMS,\
             binary_settings, simple_commands
        
        

    if language == 'poe':
        from politeenglish import Queries, Alerts,\
             Labels, Spelling, DefaultConsoles,\
             BREAKTERMS, NEWTERMS, QUITALLTERMS, \
             QUITTERMS, YESTERMS, NOTERMS,\
             DELETETERMS, SHOWTERMS, ADDTERMS, \
             CLEARTERMS, LEARNTERMS, UNLEARNTERMS,\
             binary_settings, simple_commands

    if language == 'rue':
        from rudeenglish import Queries, Alerts,\
             Labels, Spelling, DefaultConsoles,\
             BREAKTERMS, NEWTERMS, QUITALLTERMS,\
             QUITTERMS, YESTERMS, NOTERMS,\
             DELETETERMS, SHOWTERMS, ADDTERMS,\
             CLEARTERMS, LEARNTERMS, UNLEARNTERMS,\
             binary_settings, simple_commands
        
    spellingheadings = Spelling() 
    notebook.speller = SpellCheck(display,
                                  headings=spellingheadings)
    defaultheadings = DefaultConsoles()
    defaultterms = (ADDTERMS,
                    DELETETERMS,
                    SHOWTERMS,
                    QUITTERMS,
                    CLEARTERMS,
                    LEARNTERMS,
                    UNLEARNTERMS,
                    YESTERMS,
                    NOTERMS)
    queries = Queries()
    alerts = Alerts()
    labels = Labels()
    
    # To set language for persistent objects 
    notebook.default_dict['keymacros'].change_language(headings=defaultheadings,
                                                   terms=defaultterms)
    notebook.default_dict['definitions'].change_language(headings=defaultheadings,
                                                   terms=defaultterms)
    notebook.default_dict['macros'].change_language(headings=defaultheadings,
                                                   terms=defaultterms)
    notebook.default_dict['abbreviations'].change_language(headings=defaultheadings,
                                                   terms=defaultterms)
    notebook.default_dict['commands'].change_language(headings=defaultheadings,
                                                   terms=defaultterms)
    notebook.default_dict['knower'].change_language(headings=defaultheadings,
                                                   terms=defaultterms)
    
 
def stack_input(query,stack_object):

    """if the stack is not empty, pulls from the stack.
    otherwise, queries use
    """

    if stack_object.size() > 0:
        return stack_object.pop()
    else:
        return input (query)

def dummy(x_temp):


    """#dummy function to be passed as argument"""

    return x_temp


def side_note(texts,
              widths=[30]+[20]*10,
              counters=False,
              columnchar=UNDERLINE):

    """Joinds texts together into columns
    """

    def divide_into_lines(entrytext,width,splitchar=BLANK):


        """Takes entrytext and returns a
        list of lines less than width, unless
        the word runs over.
        """
        
        returnlist = []
        line = EMPTYCHAR
        for word in entrytext.split(splitchar):
            if len(line+word) <= width and not word.endswith(PERIOD):
                line += word + BLANK
            else:
                if word.endswith(PERIOD+PERIOD):
                    word = word[:-2]
                returnlist.append(line + word)
                line = EMPTYCHAR
        if line:
            returnlist.append(line)
        return returnlist

    linelists = []
    for column in range(len(texts)):
        linelists.append(divide_into_lines(texts[column],widths[column]))
    maxrows = max(len(l_temp)
                  for l_temp in linelists)
    for column in range(len(texts)):
        linelists[column].extend([EMPTYCHAR]*(maxrows-len(linelists[column])))


    returntext =  EOL + '/COL/' + EOL 
        
    for counter in range(0,maxrows):
        returntext += (str(counter)
                       + COLON + BLANK
                       + columnchar)*counters 
        for column in range(len(texts)):
            returntext += linelists[column][counter] \
                          + BLANK + columnchar * (column < len(texts)-1)
        returntext += EOL

    return returntext + '/ENDCOL/'

def split_up_string(string,
                    line_length=30):

    """splits us a string into a series segments of less then line_length.
    Used for displaying long sequences of keys/indexes in columns
    """

    if len(string) < line_length:
        return [string]
    returnlist = []
    segments = string.split(COMMA)

    length = 0
    newline = EMPTYCHAR
    for segment in segments:
        if len(segment) > ((line_length * 2)/3):
            if length > (line_length/3):
                returnlist.append(newline
                                  + COMMA
                                  + BLANK)
                returnlist.append(segment
                                  + COMMA
                                  + BLANK)
                length = 0
                newline = EMPTYCHAR
            else:
                returnlist.append(newline
                                  + segment
                                  + COMMA
                                  + BLANK)
                length = 0
                newline = EMPTYCHAR
        elif length + len(segment) <= line_length:
            newline += segment + COMMA + BLANK
            length += len(segment)
        else:
            returnlist.append(newline
                              + segment
                              + COMMA
                              + BLANK)
            length = 0
            newline = EMPTYCHAR
    if newline:
        returnlist.append(newline)
    if len(returnlist) > 0 and len(returnlist[-1]) > 2:
        returnlist[-1] = returnlist[-1][:-2]

    return returnlist


def split_into_columns (t_temp,
                        breaker=BLANK,
                        width=80,
                        columns=3):

    """ splits text into columns.
    """

    t_temp = nformat.purgeformatting(t_temp)
    
    t_temp = t_temp.split(breaker)

    columnwords = int(len(t_temp)/columns)
    columnwidth = int(width/columns)
    columnlist =  [columnwidth]*(columns-1) \
                 + [width-columnwidth*(columns-1)]

    textlist = []
    for c_temp in range(columns):
        if c_temp != columns-1:
            textlist.append(breaker.join(t_temp[c_temp*columnwords:
                                                (c_temp+1)*columnwords])
                            .replace(POUND*5,UNDERLINE))
        else:
            textlist.append(breaker.join(t_temp[c_temp*columnwords:])
                            .replace(POUND*5,UNDERLINE))

    return side_note(textlist,columnlist)

def abridge (string,
             maxlength=60,
             overmark=BLANK+PERIOD*3+BLANK,rev=False):

    """abridges a string if it is longer than maxlength"""
    
    if len(string) > maxlength:

        if not rev:

            return (string[0:maxlength]+overmark)
        return overmark + string[-maxlength:]
    else:
        return string


def split_up_range(string,
                   seg_length=5):

    """splits up the string with search result
    output to allow it to be formatted for display
    """

    returnlist = []
    l_temp = string.split(COMMA)
    if len(l_temp) < seg_length:
        return [COMMA.join(l_temp)]
    multip = int(len(l_temp)/seg_length)
    rem = len(l_temp)-(multip*seg_length)
    for a_temp in range(multip):
        returnlist.append(COMMA.join(l_temp[a_temp*seg_length:
                                          (a_temp+1)*seg_length-1]))
    returnlist.append(COMMA.join
                      (l_temp[multip*seg_length :
                              multip*seg_length+rem-1]))
    return returnlist

def clip_date(date,include='ymd'):

    """utily for clipping a date string
    include = 'ymd*mhsx' shows the full date.
    Even though you can show the year and the microsecond,
    I can't think of any reason why you would want to!!!
    """

    if not isinstance(date,str):
        date = str(date)

    yearmonthday = date.split(BLANK)[0].split(DASH)
    hourminutesecond = date.split(BLANK)[1].split(COLON)

    leftinclude=include.split(STAR)[0]
    year = yearmonthday[0]*('y' in leftinclude)
    month = yearmonthday[1]*('m' in leftinclude)
    day = yearmonthday[2]*('d' in leftinclude)

    lefthalf = (year+DASH+month+DASH+day).lstrip(DASH).rstrip(DASH)
    if STAR not in include:
        return lefthalf 
    rightinclude = include.split(STAR)[1]

    hour = hourminutesecond[0]*('h' in rightinclude)
    minute = hourminutesecond[1]*('m' in rightinclude)

    second = hourminutesecond [2]
    microsecond = EMPTYCHAR
    if len(second.split(PERIOD)) > 1:
        microsecond = second.split(PERIOD)[1]*('x' in rightinclude)
    second = second.split(PERIOD)[0]*('s' in rightinclude)

    return (lefthalf+BLANK+((hour+COLON+minute
                           +COLON+second).lstrip(COLON).rstrip(COLON)
                          +PERIOD+microsecond).rstrip(PERIOD)).lstrip()

  

def get_range(entryterm,
              orequal=True,
              complete=False,
              sort=True,
              many=False,
              indexes=True):

    """gets a range of indexes from a string of index ranges
    IR1, IR2, IR3... Each indexrange is formated INDEXFROM-INDEXTO
    or -INDEXFROM/-INDEXTO. orequal True is less than equal to
    upper range. if complete true find top level indexes between
    top-level form of entered indexes. Sort is true to sort output.
    Many is true if term includes a number of ranges
    """
    term = entryterm


    # For more than one range of indexes
    returnrange = []
    bigterm = term
    for term in bigterm.split(COMMA):
        if term.strip():
            term = term.strip()
            if (term[0]!=DASH and (SLASH in term or DASH in term)) \
               or (term[0]==DASH and (SLASH in term[1:] or DASH in term[1:])):

                if DASH + DASH in term:
                    term = term.replace(DASH+DASH,
                                        SLASH+DASH)
                if SLASH not in term:
                    if term[0] != DASH:
                        term = term.replace(DASH,
                                            SLASH)
                    else:
                        term = term[0] + term[1:].replace(DASH,SLASH)

                if POUND not in term:
                    termfrom = Index(index_expand(term.split(SLASH)[0]))
                    termto = Index(index_expand(term.split(SLASH)[1]))

                else:
                    termfrom = term.split(SLASH)[0]
                    termto = term.split(SLASH)[1]
    
                    
                if indexes:
                    returnrange += notebook.find_within(termfrom,
                                                            termto,
                                                            orequal=orequal)
                else:
                    returnrange += [str(a_temp)
                                    for a_temp
                                    in notebook.find_within(termfrom,
                                                            termto,
                                                            orequal=orequal)]

            else:
                if indexes:
                    returnrange += [Index(term)]
                else:
                    returnrange += [int(term)]
        if complete and returnrange == []:
            if indexes:
                returnrange = [Index(a_temp) for a_temp
                               in range(int(termfrom), int(termto)+1)]
            else:
                returnrange = [a_temp for a_temp in range(int(termfrom),
                                                          int(termto)+1)]
            if sort:


                return sorted(returnrange,
                          key=lambda x_temp: Index(str(x_temp)))

            return returnrange


    if sort:


        return sorted(returnrange,
                          key=lambda x_temp: Index(str(x_temp)))

    return returnrange




def get_text_file(filename,folder=os.altsep+'textfiles',suffix='.txt'):


    """opens a text file a returns the text"""

    directoryname = os.getcwd()+folder
    if os.altsep+'notebooks'+os.altsep+'textfiles' in directoryname:
        nprint(directoryname)
        directoryname = directoryname.replace(os.altsep + 'notebooks'
                                              + os.altsep+'textfiles',
                                              os.altsep+'textfiles')
        nprint(directoryname)
    if  os.altsep+'notebooks'+'/'+'textfiles' in directoryname:
        nprint(directoryname)
        directoryname = directoryname.replace(os.altsep + 'notebooks'
                                              + '/' + 'textfiles',
                                              os.altsep+'textfiles')
        nprint(directoryname)
        
    
    with open(directoryname+os.altsep+filename+suffix,'r',
                    encoding='utf-8') as textfile:
        returntext = textfile.read().replace('\ufeff',
                                         EMPTYCHAR)
    return returntext

def get_words(text):


    """ parses text into words"""

    for a_temp in string.punctuation:
        text = text.replace(a_temp,
                            BLANK+a_temp
                            +BLANK)
    for a_temp in string.whitespace:
        text = text.replace(a_temp,
                            BLANK)
    text = nformat.reduce_blanks(text)
    return text.split(BLANK)


def get_keys_to_add(keys_to_add):

    """ Expands the list of keys by applying
    keymacros and checks hyperlinks """

    keyset = set()
    for k_temp in keys_to_add:
       if k_temp != EMPTYCHAR:
           if k_temp[0] == DOLLAR:
               keyset.update(self.default_dict['keymacros'].
                             get_definition(k_temp[1:]))
           else:
               keyset.add(k_temp)
    return list(check_hyperlinks(keyset))


def frequency_count(text):


    """returns a histogram of the word
    frequency count of text"""

    returndictionary = {}
    
    if isinstance(text,str):
        word_set = get_words(text)
    else:
        word_set = text
    for word in word_set:
        if word not in returndictionary:
            returndictionary[word] = 1
        else:
            returndictionary[word] += 1
    return returndictionary


def concatenate(lista,
                listb,
                infix=EMPTYCHAR):


    """Concatenates the strings from two lists,
    joining them with index
    """

    return [a_temp+(infix*max([len(b_temp), 1]))
            +b_temp for a_temp,
            b_temp in product(lista, listb)]



def textedit_new(text,
                 size=60,
                 splitchar=BLANK,
                 annotate=False):

    """ updated text editing function.
    Allows the user to edit inputed text"""

    text = text.replace(EOL,VERTLINE)
    # add the annotation mark if needed.
    if annotate and '/COL/' not in text:
        text = '/COL/|' + text
    maxlen = 0
    text = text.replace('/COL/|',
                        '/COL/'+EOL).replace(VERTLINE+'/ENDCOL/',
                                             EOL+'/ENDCOL/')
    # to establish the maximum length of the line.
    maxlen = max(len(l_temp)
                 for l_temp
                 in text.split(VERTLINE))
    # the actual size of the note.
    size = min(size, maxlen+5)
    go_on_deleting = False
    


    linelist = [] 
    # either add line, if less than size,
    #or split into smaller lines.
    for l_temp in text.split(VERTLINE):
        if len(l_temp) < size:
            linelist.append(l_temp+VERTLINE)
        else:
            nextline = EMPTYCHAR
            for word in format(l_temp).split(splitchar):
                nextline += str(word)+splitchar
                if len(nextline) > size-int(size/3) or EOL in nextline:
                    linelist.append(nextline)
                    nextline = EMPTYCHAR
            if nextline != EMPTYCHAR:
                linelist.append(nextline+VERTLINE)
            else:
                linelist.append(VERTLINE)

    returnlist = []
    returntext = EMPTYCHAR
    counter = 1

    display.noteprint((alerts.EDITING,
                       queries.EDIT_OPTIONS))
    maxcolumns = max(x_temp.count(UNDERLINE) for x_temp in linelist)
    # Goes through linelist line by line and requests changes
    for l_temp in linelist:



        annotation = UNDERLINE * annotate
        if not go_on_deleting:
            nl_temp = input(DOLLAR+str(counter)
                        +(4-len(str(counter)))
                        *BLANK+l_temp+(size-len(l_temp)-5)*BLANK+VERTLINE)

            if UNDERLINE in nl_temp:
                # if an ANNOTATION
                annotation +=' _'.join(nl_temp.split(UNDERLINE)[1:])
                nl_temp = nl_temp.split(UNDERLINE)[0]

            if UNDERLINE in l_temp and SLASH in nl_temp:
                    # replacing a previous annotation

                    ls_temp = nl_temp.split(SLASH)
                    nls_temp = l_temp.split(UNDERLINE)
                    if len(ls_temp) <= len(nls_temp):

                        l_temp=UNDERLINE.join(nls_temp[0:len(nls_temp)
                                                       -len(ls_temp)]+ls_temp)

                    returnlist.append(l_temp+(maxcolumns-len(nls_temp))
                                      *' _ '*(len(annotation)>1)
                                      +annotation+VERTLINE)

            elif not nl_temp:
                # if RETURN then keep as it was.
                counter += 1
                if annotate:
                    returnlist.append(l_temp.replace(VERTLINE,
                                                     EMPTYCHAR)
                                      +annotation+VERTLINE)
                else:
                    returnlist.append(l_temp)
                print(returnlist[-1])
            elif nl_temp == DASH:
                # DASH to delete the line. 
                pass
            elif nl_temp == DASH+DASH:
                go_on_deleting = True
                pass
            elif nl_temp[0] == DOLLAR:
                # to add to the LEFT.
                counter += 1
                returnlist.append(nl_temp[1:]+l_temp)
            elif nl_temp[0] == POUND:
                counter += 1
                # to add to the RIGHT 
                returnlist.append(l_temp.replace(EOL,
                                                 EMPTYCHAR)
                                  +nl_temp[1:]+VERTLINE)
            elif nl_temp[0] in [PLUS,
                                CARET]:
                # to insert new lines before 
                keepgoing = True
                addline = EOL
                
                while keepgoing:
                    if len(nl_temp) > 1:  #to carry over text after plus or caret
                        nnl_temp = nl_temp[1:]
                        nl_temp = EMPTYCHAR
                    else:
                        nnl_temp = input(PLUS+str(counter)
                                         +(4-len(str(counter)))
                                         *BLANK+l_temp
                                         +(size-len(l_temp)-5)
                                         *BLANK+VERTLINE)
                    if nnl_temp and nnl_temp[-1] != VERTLINE:
                        addline += nnl_temp + BLANK
                    elif nnl_temp and nnl_temp[-1] == VERTLINE:
                        addline += nnl_temp[:-1]
                        returnlist.append(addline+VERTLINE)
                        addline = EMPTYCHAR
                    else:
                        keepgoing = False
                        returnlist.append(addline+VERTLINE)
                    counter += 1
                if nl_temp == PLUS:
                    returnlist.append(l_temp)
            else:

                # to replace with new line/lines
                for ll in nl_temp.split(VERTLINE):
                    returnlist.append(ll+annotation
                                      +VERTLINE*annotate)
                    annotation = UNDERLINE * annotate
                    counter += 1
    for l_temp in returnlist:
        # to replcae VERTLINE with EOL

        l_temp = l_temp.replace(VERTLINE+VERTLINE,
                                VERTLINE).replace(EOL+VERTLINE,
                                                  VERTLINE)\
                      .replace(VERTLINE+EOL,VERTLINE)\
                      .replace(VERTLINE,EOL)
        if l_temp:
            returntext += l_temp + BLANK*(l_temp[-1]!=EOL)

    #if annotated, add mark 
    if annotate and '/ENDCOL/' not in returntext:
        returntext = returntext + EOL + '/ENDCOL/'
    return returntext



def next_next(index,
              index_list=None,
              rightat=False):


    """ returns the next available 'next' note"""

    if index_list is None:
        index_list = notebook.indexes()

    if rightat:
        if str(index) not in index_list:
            return index

    while True:
        if str(index.next()) not in index_list:
            return index.next()
        index = index.next()


def next_child(index,
               index_list=None):


    """ returns the next available 'child' note"""

    if index_list is None:
        index_list = notebook.indexes()

    if str(index.child()) not in index_list:
        return index.child()
    return index.child().next()


def reduce_tupples(entrylist):


    """provides a list of tupples giving the 'moves'
    needed to reduce a NoteBook"""

    entrylist = [a_temp for a_temp in entrylist if a_temp.is_top()]

    returnlist = []
    last_e = Index(0)
    for e_temp in entrylist:

        if e_temp-1 == last_e:
            pass
        else:
            returnlist.append((e_temp,
                               last_e+1))
        last_e += 1
    return returnlist

def add_form(keyset,
             text,
             meta=None,
             right_at=False,
             as_next=False,
             as_child=False,
             index=0):

    """ formats note data including metadata into textformat """
    if meta is None:
        meta = {}
    returntext = LEFTNOTE

    returntext += DOLLAR
    # adds key definition in arrow brackets
    for k_temp in keyset:
        returntext += k_temp.replace(RIGHTNOTE, EQUAL) + COMMA
    returntext = returntext[0:-1]
    returntext += BLANK + RIGHTNOTE + EOL
    metatext = EMPTYCHAR
    if 'date' in meta and not isinstance(meta['date'], list):
        if not isinstance(meta['date'], str):
            meta['date'] = [str(meta['date'])]
        else:
            meta['date'] = [meta['date']]
    for key in meta.keys():
        metatext += (CARET+COLON+str(key) + VERTLINE
                     + {"<class 'str'>":'S',
                        "<class 'int'>":'I',
                        "<class 'list'>":'L'}
                     [str(type(meta[key]))]+VERTLINE
                     + str(meta[key])+COLON+CARET+EOL)

    returntext += LEFTNOTE
    #adds text in arrow brackets
    if right_at:

        if not as_child:
            returntext += ATSIGN + str(index) + ATSIGN + BLANK
            # to specify the index position
        else:
            returntext += PERCENTAGE + str(index) + PERCENTAGE + BLANK

    else:
        if as_child:
            returntext += '" '    # mark for a child note
        if as_next:
            returntext += "' "    # mark for a next note

    returntext += (text.replace(LEFTNOTE,
                                LEFTBRACKET).replace(RIGHTNOTE,
                                                     RIGHTBRACKET)
                   +EOL+metatext[0:-1]+' >'+EOL*2)
    # transforms the arrow brackets into square brackets
    #to make sure  that encoding is possible

    return returntext

def select_func (entrylist):

    """ passed-in function to select form menu """

    to_keep = input(queries.ENTER_KEYWORDS)
    to_keep = rangelist.range_set(to_keep)
    return [entrylist[a_temp]
            for a_temp in to_keep
            if a_temp in range(len(entrylist))]

def show_list(entrylist,
              label=EMPTYCHAR,
              from_here=0,
              to_here=40,
              select=False,
              func=dummy,
              sfunc=select_func,
              accumulate=False,
              present=False,
              columnwidth=None,
              compactwidth=None):

    """displays elements from_here to to-here of a list
    in a note with label. Select if a selection is to be
    made from the elements in the list
    """

    showlist = DisplayList(displayobject=display)
    text = EMPTYCHAR
    counter = 1

    for log in entrylist:


        funky = func(log)

        #This is in order to handle very long number of indexes
        if funky:
            if isinstance(funky, str):
                # func returns a simple string
                # if there are only a few indexes,
                # but otherwise it returns a list
                text += (str(counter)+COLON+BLANK
                         +funky+EOL)
                # which is then carried over to the next line
                #+((3-len(str(counter)))*BLANK)
                       #  +BLANK+BLANK

                counter += 1
            else:   #for a list of indexes
                text += str(counter)+COLON+BLANK+funky[0]+EOL

                counter += 1
                for f_temp in funky[1:]:
                    # for subsequent lines
                    text += f_temp + EOL
    ##                    showlist.append(f_temp+EOL)

    width = nformat.columns(text,   #formats as columns while appending to
                            showlist,
                            not_centered={0, 1, 2, 3, 4},
                            columnwidth=columnwidth,
                            compactwidth=compactwidth)

    if not present:
        showlist.show(from_here,
                      to_here,
                      nformat.center(label,
                                     width+6))
        if select:

            return sfunc(entrylist)

    if present and not accumulate:
        showlist.present(header=label,
                                centered=True)
    if present and accumulate:
        return showlist.present(header=label,centered=True,accumulate=True)
        

    return False


def save_file(returntext=EMPTYCHAR,
              filename=EMPTYCHAR,
              folder=os.altsep+'textfiles'):

    """for saving a file"""
    
              
    directoryname = os.getcwd()+folder
    nprint(directoryname)
    with open(directoryname+os.altsep
                    +filename+'.txt',
                    'x',
                    encoding='utf-8') as textfile:
        textfile.write(returntext.replace('\ufeff', ' '))

    return 'Saved to ' + directoryname+SLASH+filename+'.txt' 


def get_file_name(file_path=EMPTYCHAR,
                  file_suffix=EMPTYCHAR,
                  file_prefix=EMPTYCHAR,
                  get_filename=EMPTYCHAR,
                  justshow=False,
                  show_notebooks_too=False):

    """Lists files in directory asks the user to make a selection.
    returns the name of the file
    """

    def directory ():

        """gets directory"""

            
        allfiles = os.listdir(file_path)

        filelist = [a_temp[0: -len(file_suffix)]
                    for a_temp in allfiles
                    if (a_temp.startswith(file_prefix)
                        and a_temp.endswith(file_suffix))]

        if show_notebooks_too:
            db_cursor.execute("SELECT notebook FROM notebooks")
            filelist += list([i[0] for i in db_cursor.fetchall()])
        
        dirlist = [a_temp for a_temp in allfiles if PERIOD not in a_temp]
        
        textlist = []
        display_path = abridge(file_path,30,rev=True)

        for temp_counter, filename in enumerate(filelist):
            #Files
            l_temp = filename
            textlist.append((l_temp,file_suffix))

        for temp_counter, filename in enumerate(dirlist):
            #Directories
            l_temp = filename
            textlist.append((l_temp,'DIR'))

        show_list(textlist,display_path+'\n'+\
                  (max([(int(len(file_path)/2))-5,0])*BLANK),0,20,
                  select=True,func=zformat,sfunc=dummy,present=True)

        return filelist,dirlist
    
    def zformat (x_temp):

        """formating function for columns"""
        
        return x_temp[0] + VERTLINE + x_temp[1] 
    
    def select_file (filelist):

        """selecting function"""
        
        go_on = True
        while go_on:
            newfile = input(queries.SELECT_FILE)
            nprint()

            if newfile in ['b','B','BACK','back']:
                return 'BACK', EMPTYCHAR
            elif (newfile.isnumeric() and int(newfile) > 0
                    and int(newfile) < len(filelist)+1):
                newfile = filelist[int(newfile)-1]
                tag = 'w'
            else:
                newfile = file_prefix+newfile
                tag = 'c'
            if input(queries.OPEN_CONFIRM+newfile+QUESTIONMARK+BLANK) in YESTERMS:
                go_on = False

        return newfile, tag

    """fetches a filename to load"""

    if get_filename != EMPTYCHAR:
        return get_filename, EMPTYCHAR
##    if 'simple note' in os.getcwd():
##        file_path = os.getcwd() + file_path
##    else:
##        file_path = os.getcwd()
    file_path = os.getcwd() + file_path
        
    old_file_path = file_path
    added_path = EMPTYCHAR


    filelist,dirlist = directory()



    if not justshow:

        while True:

            selected = select_file(filelist+dirlist)

            if selected[0] != 'BACK' and selected[0] not in dirlist:
                #to go back to last directory
                return added_path + selected[0],selected[1]
            else:
                if selected[0] == 'BACK':
                    file_path = old_file_path
                    added_path = EMPTYCHAR

                else:
                    file_path += os.altsep + selected[0]
                    added_path += os.altsep + selected[0]
                os.chdir (file_path)
                    


                filelist,dirlist = directory()
                if not filelist and not dirlist:
                    display.noteprint((file_path,'EMPTY'))
                

    return EMPTYCHAR, EMPTYCHAR


def show_setting(message,
                 toggle):


    """prints a dialogue box showing status of a binary setting"""

    if toggle:
        display.noteprint((message,alerts.ON))
    else:
        display.noteprint((message,alerts.OFF))

def modify_keys(keyset,
                func=dummy,
                strip=False):

    """ Modifies keys in set by applying func"""

    returnset = set()
    for key in keyset:
        key = func(key)
        if strip:
            key = key.strip()
        returnset.add(key)
    return returnset

def vertical_display (enterlist,
                      leftmargin=7):
    """Specialized function for displaying a list"""

    showlist = []
    display = ''
    maxlen = max([len(x_temp) for x_temp in enterlist])
    addition = int(maxlen/len(enterlist))

    for counter, el_temp in enumerate(enterlist):
        showlist.append(str(counter) +
                        (2-len(str(counter)))*BLANK+BOX_CHAR['h']
                        +(counter*addition)*BLANK+el_temp)

    maxlen = max([len(x_temp) for x_temp in showlist])
    showlist = [x_temp + (maxlen - len(x_temp))*BLANK for x_temp in showlist]
    maxlen = len(showlist[0])
    
    for y_temp in range(maxlen):
        display += leftmargin * BLANK
        for x_temp in range(len(showlist)):
  
                display += showlist[x_temp][y_temp] + VERTLINE
        display += '\n'
    return display
            
        


def edit_keys (keyobject,
               displayobject=None,
               prompt='Default Keys',
               deletekeys=True,
               addkeys=False,
               ddkeys=False,
               askabort=False,
               vertmode=True,
               notebookobject=None):

    """ Adds to and deletes to the autokeys.
    """

    if notebookobject is None:
        notebookobject=notebook

    if deletekeys:

        keylist = DisplayList(displayobject=displayobject)
        listcopy = list(keyobject)
        for counter, key in enumerate(listcopy):
            keylist.append(str(counter)+' : '+key)

        if not vertmode:
             keylist.show(header=prompt,
                          centered=True)

             
             i_temp = input(queries.AUTOKEYS_KEEP+askabort*queries.ALSO_ABORT)

             if i_temp:
                 if askabort  and i_temp.lower() == 'abort':
                     return {'ABORTNOW'}
                 if i_temp.lower()[0] == 'a':
                     keyobject = []
                 elif i_temp.lower()[0] == 's':
                      command_stack.add('deletedefaultkeys')
                      command_stack.add('keyeditmode')
                      
                 
                 else:
                     if i_temp[0] == DOLLAR:
                         i_temp = i_temp[1:]
                         keyobject = [listcopy[int(a_temp)]  for a_temp in range(0,
                                                                                 len(listcopy))
                                                             if Index(a_temp) not in get_range
                                                             (i_temp, orequal=True,
                                                              complete=False,
                                                              many=True,
                                                              indexes=False)]
                     else:

                         keyobject = [listcopy[int(a_temp)] for a_temp in get_range(i_temp,
                                                                                     orequal=True,
                                                                                     complete=False,
                                                                                     many=True,
                                                                                     indexes=False)
                                                             if int(a_temp) < len(listcopy)
                                                             and int(a_temp) >= 0]
        else:
             nprint('X to delete, O to keep, or SWITCH to change to regular mode')
             print(vertical_display(listcopy))
             tokeep = input(7*BLANK)
             keeplist = []
             for counter in range(len(tokeep)):
                  if counter%2 == 0:
                       if tokeep[counter] != BLANK:
                            keeplist.append(int(counter/2))
             if 'O' in tokeep:
                  keyobject = [listcopy[int(a_temp)]
                               for a_temp in range(0, len(listcopy))
                               if Index(a_temp) in keeplist]
             elif tokeep and tokeep.lower()[0] == 's':
                  command_stack.add('deletedefaultkeys')
                  command_stack.add('keyeditmode')
                  
             else:
                  keyobject = [listcopy[int(a_temp)]
                               for a_temp in range(0, len(listcopy))
                               if Index(a_temp) not in keeplist]
                     

        display.noteprint((alerts.OLD+prompt,
                           formkeys(keyobject)))

    if addkeys:

        in_temp = notebookobject.default_dict['abbreviations'].undo(input(queries.KEYS))
        if in_temp:
                
            keyobject += in_temp.split(COMMA)

        
    return keyobject

def remove_tags(keyset,
                override=False):

    """returns a set of keys with the tags removed"""
    if override:
        return keyset

    returnset = set()
    for k_temp in keyset:

        if SLASH in k_temp:
            k_temp = k_temp.split(SLASH)[0]
        returnset.add(k_temp)

    return returnset

def sort_keyset(keyset):


    """Divides a set of keys into three groups
    and returns a tuple=(ALL CAPS, Capitalized, no caps)"""

    value1 = [k_temp for k_temp
              in keyset
              if k_temp.upper() == k_temp]

    value2 = [k_temp for k_temp in keyset
              if k_temp.upper() != k_temp
              and k_temp[0].upper() == k_temp[0]]

    value3 = [k_temp for k_temp in keyset
              if k_temp.upper() != k_temp
              and k_temp[0].upper() != k_temp[0]]

    return value1, value2, value3

def reform_text(text):

    """reformats text to get rid of tabs,
    spaces between punctuation etc.
    """

    text = text.replace((PERIOD+BLANK)*3,
                        PERIOD*3)
    text = text.replace(PERIOD*3+BLANK,
                        PERIOD*3)    
    text = text.replace(BLANK*4,
                        BLANK)    
    for a_temp in range(4):
        text = text.replace(BLANK*2,
                            BLANK)
        
##    text = text.replace(PERIOD+BLANK,
##                        PERIOD+EOL+TAB)
    text = text.replace(TAB,
                        BLANK*4)    
    text = text.replace(EOL*3,
                        EOL*2)

    return text

def remove_tag(key):

    """removes a tag from a single key"""

    return key.split(SLASH)[0]



## Class Definitions ##




class Note_Shelf:


    """ database OBJECT using a combination of a shelve and
        pickled dictionary THE pickled file is entirely dependent
        on the shelve, and can be reconstructed from it.
        If pickle errors emerge, the database can usually
        be saved by deleting the pickled file!"""

    def autodefaults (self):

        """ To fetch the default command macros """

        self.defaults_from_notes(identifying_key=EMPTYCHAR,
                                 mark=EQUAL,
                                 obj=self.default_dict['commands'],
                                 entrytext=COMMANDMACROSCRIPT)

    ## EXIT ROUTINE ##

    def close(self):
        """closes database"""

        for t_temp in ['commands',
                       'knower',
                       'projects',
                       'definitions',
                       'keymacros',
                       'abbreviations',
                       'macros',
                       'indextable']:
            self.defaults.backup(t_temp)
            

        if not self.using_database:
            self.note_dict.close()
        else:
            self.dumpprojects()
        self.default_dict['indextable'].purge_connection()
        self.default_dict['projects'].purge_connection()
        self.default_dict['generalknowledge'].purge_connection()
        self.default_dict['knower'].purge_connection()
        self.default_dict['definitions'].purge_connection()
        self.default_dict['abbreviations'].purge_connection()
        self.default_dict['macros'].purge_connection()
        self.default_dict['keymacros'].purge_connection()
        self.default_dict['commands'].purge_connection()

        if self.using_shelf: 
        
            if not self.divide_no_query:
                q_temp = input(queries.DIVIDE_PICKLE)
                if self.divided or q_temp in YESTERMS:
                    for suffix in ('d','k','w','t'):
                        with open(self.directoryname
                                        +SLASH+self.filename
                                        +suffix.upper()+'.pkl','wb') as tempfile:
                            pickle.dump(self.pickle_dictionary[suffix],
                                        tempfile)
                            #globaldirectoryname+SLASH+self.filename+'PIC'
                            nprint(suffix,'saved')
                if q_temp in ['R','r']:
                    self.divide_no_query = True
                    
            else:
                
                with open(self.directoryname
                                +SLASH+self.filename
                                +'.pkl',
                                'wb') as tempfile:
                    pickle.dump(self.pickle_dictionary,
                                tempfile)
                    #globaldirectoryname+SLASH+self.filename+'PIC'

                    
    def default_save(self,suffix=EMPTYCHAR,extra=EMPTYCHAR):
        """saves default dictionary etc."""

        pass
        
##        with open(self.directoryname
##                        +SLASH+self.filename+extra
##                        +'.pkl',
##                        'wb') as tempfile:
##            if not suffix:
##                pickle.dump(self.pickle_dictionary,
##                            tempfile)
##            else:
##                pickle.dump(self.pickle_dictionary[suffix],tempfile)
##                
##            #globaldirectoryname+SLASH+self.filename+'PIC'

    

    ## TAG and KEY METHODS ##

    def parse_sequence_key(self,
                           seq_value):

            """ takes the value of a sequence, following
            the identifier, and returns a tuple indicating
            the mark used for the sequence, the value itself,
            and the type of the value.
            """

        

            seq_type = str
            seq_mark = EMPTYCHAR

            if seq_value in [DOLLAR,PLUS,POUND,UNDERLINE,CARET]:
                seq_type,seq_mark,seq_value = {DOLLAR:(str,EMPTYCHAR,EMPTYCHAR),
                            PLUS:(int,EMPTYCHAR,EMPTYCHAR),
                            POUND:(type(datetime.date(1972,3,13)),POUND,EMPTYCHAR),
                            UNDERLINE:(type(Index(0)),UNDERLINE,EMPTYCHAR),
                            CARET:(float,EMPTYCHAR,EMPTYCHAR)}[seq_value]
                return seq_mark,seq_value,seq_type
                            



            if seq_value and seq_value[0] in [POUND,UNDERLINE]:
                seq_mark = seq_value[0]
                seq_value = seq_value[1:]
 
                if seq_mark == POUND:
                    seq_value += '-01-01'
                    seq_value = DASH.join(seq_value.split(DASH)[0:3])


                    if is_date(seq_value):
                        seq_value = is_date(seq_value,returndate=True)
                        
                        seq_type = type(datetime.date(1972,3,13))

                    
                elif seq_mark == UNDERLINE:
                    seq_value = Index(seq_value)
                    seq_type = type(Index(0))
                    

            elif (((DASH in seq_value
                    and len(seq_value) > 1
                    and seq_value[0] == DASH
                    and DASH not in seq_value[1:])
                or DASH not in seq_value)
                  and ((PERIOD in seq_value
                        and seq_value.count(PERIOD) == 1
                        and PERIOD not in seq_value[0] and PERIOD not in seq_value[-1])
                       or PERIOD not in seq_value) and
                seq_value.replace(PERIOD,
                                  EMPTYCHAR).replace(DASH,
                                                     EMPTYCHAR).isnumeric()):
                
                seq_type = float
            if seq_type == float:
                seq_value = float(seq_value)

            return seq_mark, seq_value, seq_type
        

    def add_keys_tags(self,
                      index=None,
                      keyset=None,
                      addkeys=True,
                      sequences=True):

        """adds keys to the dictionary of keys,
        and tags to the dictionary of tags
        And also captures knowledge and
        sends it to the knowledge base

        ?KEY?RELATION?CONTENT/TAG.TAG.TAG

        """


        newkeyset = set()
##        is_sequence = False
        for key in keyset:
            key = key.strip()

            if key.startswith(QUESTIONMARK):
                #For keywords that engage with the knowledge base 

                key = key[1:]
                after_slash = EMPTYCHAR
                if SLASH in key:
                    after_slash = key.split(SLASH)[1]
                    key = key.split(SLASH)[0]

                key += '??' # TO prevent index error!
                    
                node,relation,other_node = key.split(QUESTIONMARK)[0], \
                                           key.split(QUESTIONMARK)[1], \
                                           key.split(QUESTIONMARK)[2]
                if node and not relation and not other_node:
                    if not self.default_dict['generalknowledge'].node_exists(node):
                        display.noteprint(self.default_dict['generalknowledge'].text_interpret(node))
                elif node and relation and other_node:
                    if self.default_dict['generalknowledge'].relation_exists(relation):
                        if not self.default_dict['generalknowledge'].node_exists(node):
                            display.noteprint(self.default_dict['generalknowledge'].text_interpret(node))
                        if not self.default_dict['generalknowledge'].node_exists(other_node):
                            display.noteprint(self.default_dict['generalknowledge'].text_interpret(other_node))
                        display.noteprint(self.default_dict['generalknowledge'].text_interpret(node+':'
                                                                                               +relation
                                                                                               +';'+other_node))
                    else:
                        display.noteprint(('ATTENTION!',
                                           'RELATION not defined'))
                else:
                    display.noteprint(('ATTENTION',
                                       'Incomplete knowledge phrase!'))

                key = node
                if after_slash:
                    key = node + '/' + after_slash


            if SLASH in key:
                # if there is a tag in the keyword 
                
                if PERIOD in key:
                    tags = key.split(SLASH)[1].split(PERIOD)
                else:
                    tags = [key.split(SLASH)[1]]
                tagkey = key.split(SLASH)[0]
                for tag in tags:
                    if EQUAL in tag:

                        definitions = tag.split(EQUAL)[1:]
                        tag = tag.split(EQUAL)[0]
                        definitions = [tag]+definitions
                        if len(definitions) > 1:
                            for r in range(0, len(definitions)-1):
                                self.default_dict['knower'].learn(definitions[r],
                                                                  definitions[r+1])
                                self.display_buffer.append(alerts.LEARNED_BEG
                                                           +definitions[r]
                                                           +alerts.LEARNED_MIDDLE
                                                           +definitions[r+1])


                    if self.tag_dict_contains(tag):
                        self.add_tag(tag,tagkey)

                    else:
                        self.initiate_new_tag(tag,tagkey)

        
            if addkeys:

                if SLASH in key:
                    # adds keys to keylist 
                    
                    if PERIOD in key:

                        # If there are multiple tags
                        
                        tags = key.split(SLASH)[1].split(PERIOD)
                    else:
                        tags = [key.split(SLASH)[1]]
                    tagkey = key.split(SLASH)[0]
                    for tag in tags:
                        key = tagkey+SLASH+tag.split(EQUAL)[0]
                        newkeyset.add(key)
                    
                        if self.key_dict_contains(key):
                            self.add_key(key,index)
                        else:
                            self.initiate_new_key(key,index)
                            
                        
                else:
                    # If there are no tags

                    
                    newkeyset.add(key)
                    if self.key_dict_contains(key):
                        self.add_key(key,index)
                        
                    else:
                        self.initiate_new_key(key,index)


            if sequences:

                # For sequences 

                if ATSIGN in key and key[0] != ATSIGN and key[-1] !=ATSIGN:
                    # Parses the sequence key 
                    identifier = key.split(ATSIGN)[0]
                    seq_value = key.split(ATSIGN)[1]
                    
##                        is_sequence = True

                    seq_mark, seq_value, seq_type = self.parse_sequence_key(seq_value)
                
                    if identifier not in self.default_dict['sequences']:
                        if identifier not in self.default_dict['sequences']['#TYPE#']:
                            # Initiates a new sequence 
                            self.default_dict['sequences']['#TYPE#'][identifier] = seq_type
                            print()
                            display.noteprint((alerts.ATTENTION,alerts.NEW_SEQUENCE+str(seq_type)))
                        else:
                            # For existing sequences 
                            del self.default_dict['sequences']['#TYPE#'][identifier]
                            self.default_dict['sequences']['#TYPE#'][identifier] = type(seq_value)
                            display.noteprint((alerts.ATTENTION,alerts.OVERWRITTEN+str(seq_type)))
                        self.default_dict['sequences'][identifier] = OrderedList()
                        self.default_dict['sequences'][identifier].add(seq_value)

                    else:
                        if seq_type == self.default_dict['sequences']['#TYPE#'][identifier]:
                            self.default_dict['sequences'][identifier].add(seq_value)
                         
        return newkeyset
    

    

    def update_user(self,
                    olduser,
                    newuser,
                    entrylist=None):

        """changes the user in the metadata over a range of notes"""

        if entrylist is None:
            entrylist = self.apply_limit(self.find_within(indexfrom=0,orequal=True))

        if not isinstance(entrylist[0], str):
            entrylist = [str(a_temp)
                         for a_temp in entrylist]

        for i in entrylist:
            if i in self.indexes():
                if self.get_metadata_from_note(i)['user'] == olduser:
                    tempnote = self.get_note(i).change_user(newuser)
                    self.add_note(i,note=tempnote)

    def update_size(self,
                    entrylist=None,
                    newsize=60):

        """changes the size in the metadata over a range of notes"""
        if entrylist is None:
            entrylist = []

        for i in entrylist:

            if str(i) in self.indexes():

                tempnote = self.get_note(i).change_size(newsize)
                self.add_note(i,note=tempnote)

    def delete_keys_tags(self,
                         index,
                         deletedkeys):

        """deletes keys to the dictionary of keys, and tags to the dictionary of tags"""


        for k_temp in deletedkeys:
##            k_temp = k_temp.split(SLASH)[0]
            k_temp = k_temp.strip()
            if k_temp in set(self.get_keys()):
                self.discard_index_from_key(k_temp, index) 
                if self.get_indexes_for_key(k_temp) == set():
                    self.eliminate_key(k_temp)  
            for t_temp in self.get_tags():
                if k_temp in self.get_keys_for_tag(t_temp):
                    self.discard_key_from_tag(t_temp,k_temp)
                    if not self.get_keys_for_tag(t_temp):
                        self.delete_tag(t_temp)


    def delete_key(self,
                   dkey):

        """deletes key from the note_dictionary and the key_dictionary"""


        if (input(queries.DELETE_CONF_BEG
                  +dkey+queries.DELETE_CONF_END) in YESTERMS):

            if dkey in self.keys():

                for i_temp in self.get_all_indexes():
                    if dkey in self.get_keys_from_note(i_temp):
                        tempnote = self.get_note(i_temp).delete_keys({dkey})
                        self.add_note(i_temp,note=tempnote)
                        if self.get_keys_from_note(i_temp) == set():
                            temp = self.get_keys_from_note(i_temp)
                            temp.add(VOIDTERM)
                            self.add_note(i_temp,
                                          keyset_only=temp)
                            self.add_keys_tags(i_temp,
                                               {VOIDTERM})

                        self.delete_keys_tags(i_temp, {dkey})

    def add_search_words(self,
                         index,
                         entrytext):

        """adds words from entrytext to the dictionary of words"""


        for a_temp in DELETECHARACTERS:
            entrytext = entrytext.replace(a_temp, BLANK)

        for w in set(entrytext.split()):

            w = w.strip()
            if self.word_dict_contains(w):
                self.add_word(w,index)

            else:
                if w not in SMALLWORDS+[BLANK,EMPTYCHAR]:

                    self.initiate_new_word(w,index)

    def delete_search_words(self,
                            index,
                            entrytext):

        """deletes words from entrytext to the dictionary of words"""

        for a_temp in DELETECHARACTERS:
            entrytext = entrytext.replace(a_temp, BLANK)

        for w in set(entrytext.split()):
            w = w.strip()

            if (self.word_dict_contains(w)
                and w not in SMALLWORDS+[BLANK,EMPTYCHAR]):

                if str(index) in self.get_indexes_for_word(w):
                    self.discard_index_from_word(w,index)
                if not self.get_indexes_for_word(w):
                    self.delete_word(w)


    def grab_keys(self,
                  entrylist,
                  all_caps=True,
                  first_caps=True):

        """ fetches the keys from a range of indexes"""

        returnkeys = set()
        for a_temp in entrylist:
            returnkeys = returnkeys.union(self.get_keys_from_note(a_temp))
        returnlist = [k_temp for k_temp in returnkeys
                      if (all_caps
                          or k_temp != k_temp.upper())
                      and (first_caps
                           or k_temp[0]+k_temp[1:]
                           != k_temp[0].upper()+k_temp[1:])]
        return returnlist

    def most_common_words(self,
                          words,
                          number=10,
                          dictionaryobject=None,
                          reverse=False):

        if not dictionaryobject:
            dictionaryobject = self.word_dict 

        temp_words = how_common(entrylist=words,
                                dictionaryobject=dictionaryobject)
        number = min([number,len(temp_words)])



        if not reverse:
            temp_words = temp_words[0:number]
        else:
            temp_words = temp_words[len(temp_words)-number:len(temp_words)]

        return [x_temp[0] for x_temp in temp_words]


    ### index management ###


    def deepest(self,
                entrylist=None,
                is_string=False,
                abridged=False,
                always=False):

        if not always:
        
            if abridged and self.abr_maxdepth_found>0:
                return self.abr_maxdepth_found
            if not abridged and self.maxdepth_found>0:
                return self.maxdepth_found

        """discovers the deepest level of any index across the given range"""

        if entrylist is None:
            entrylist = self.default_dict['indexlist_indexes'].list
        maxdepth = 1

        for i_temp in entrylist:
            if not is_string:
                if i_temp.level() > maxdepth:
                    maxdepth = i_temp.level()
            else:
                if abridged:
                    if len(index_reduce(str(i_temp))) > maxdepth:
                        maxdepth = len(index_reduce(str(i_temp)))
                else:
                    if len(str(i_temp)) > maxdepth:
                        maxdepth = len(str(i_temp))
        if not abridged:
            self.maxdepth_found = maxdepth
        if abridged:
            self.abr_maxdepth_found = maxdepth

        return maxdepth

    def field_length(self,
                     entrylist=None):

        """identifies the length of the longest field name
        within a given range of fields. Used for formatting note output
        """


        if entrylist is None:
            entrylist = list(self.default_dict['field'].keys())
        maxlength = 0
        for i_temp in entrylist:
            if len(self.default_dict['field'][i_temp]) > maxlength:
                maxlength = len(self.default_dict['field'][i_temp])
        return maxlength


    def find_space(self,
                   index,
                   indexlist=None):

        """finds the first free index equal or greater
        to the index entered
        """
        if indexlist is None:
            indexlist = []

        freespaces = iter(indexlist)

        while str(index) in self.indexes():
            if indexlist != []:
                index = self.find_space(next(freespaces))
            else:
                index = index.next()
        return index

    def find_within(self,
                    indexfrom=None,
                    indexto=None,
                    withinrange=None,
                    orequal=False):

        """Find indexes lying between indexfrom and indexto
        searching over withinrange orequal is True if less
        than equal to upper range. Converts indexfrom and
        indexto to indextype if string or integer"""


        if self.usesequence:
            if not indexfrom:
                indexfrom = self.default_dict['indexlist'].list[0]
            if not indexto==0 and not indexto: 
                indexto = self.default_dict['indexlist'].list[-1]

            if len(self.default_dict['indexlist'])  < len(self.indexes()):
                display.noteprint((alerts.ATTENTION,alerts.RECONSTITUTING_INDEXES))
                self.default_dict['indexlist'] = OrderedList(self.indexes(),indexstrings=True)
                self.dd_changed = True
            allindexes = False
            if withinrange is None:
                withinrange = self.indexes()
                allindexes = True


            if POUND not in str(indexfrom)+str(indexto):
                if isinstance(indexfrom, (str, int)):
                    indexfrom = Index(index_expand(indexfrom))
                if isinstance(indexto, (str, int)):
                    indexto = Index(index_expand(indexto))

                if not allindexes:
                    
                    x_temp = [a_temp for a_temp
                              in self.default_dict['indexlist'].find_within(indexfrom,
                                                                            indexto,
                                                                            fromequal=orequal,
                                                                            toequal=orequal)
                              if a_temp in withinrange]
                    return x_temp
                x_temp = self.default_dict['indexlist'].find_within(indexfrom,
                                                                    indexto,
                                                                    fromequal=orequal,
                                                                    toequal=orequal)
                return x_temp
 
            else:
                if POUND in str(indexfrom) and POUND in str(indexto) and \
                   isinstance(indexfrom,str) and isinstance(indexto,str):
                    
                    datefrom = indexfrom.replace(POUND,EMPTYCHAR)
                    dateto = indexto.replace(POUND,EMPTYCHAR)

                    return self.find_within_dates(datefrom,
                                                  dateto,
                                                  withinrange=withinrange,
                                                  orequal=orequal)
                else:

                    return []

        else:
            if not indexfrom:
                indexfrom = self.indexes()[0]
            if not indexto:
                indexto = self.indexes()[-1]

            if withinrange is None:
                withinrange = self.indexes()
            if POUND not in str(indexfrom)+str(indexto):
                if isinstance(indexfrom, (str, int)):
                    indexfrom = Index(indexfrom)
                if isinstance(indexto, (str, int)):
                    indexto = Index(indexto)
                if not orequal:
                    return [a_temp for a_temp in withinrange
                            if Index(a_temp) > indexfrom and Index(a_temp) < indexto]
                return [a_temp for a_temp in withinrange
                        if Index(a_temp) >= indexfrom and Index(a_temp) <= indexto]
            else:
                if POUND in str(indexfrom) and POUND in str(indexto) and \
                   isinstance(indexfrom,str) and isinstance(indexto,str):
                    
                    datefrom = indexfrom.replace(POUND,EMPTYCHAR)
                    dateto = indexto.replace(POUND,EMPTYCHAR)

                    return self.find_within_dates(datefrom,
                                                  dateto,
                                                  withinrange=withinrange,
                                                  orequal=orequal)
                else:
  
                    return []
            
            
    def get_range_from_results (self,resultstring,listobject=None,indexobject=None):

 
        
        """Transforms string with results into a range of indexes"""
        if listobject is None:
            listobject = []
            returnyes = True
        else:
            returnyes = False
        
        for r_temp in resultstring.split(COMMA):
            r_temp = r_temp.strip()
            if SLASH not in r_temp:
                if r_temp in indexobject:
                    listobject.append(r_temp)
            else:
                listobject += self.find_within(r_temp.split(SLASH)[0],
                                               r_temp.split(SLASH)[1],
                                               orequal=True)
        if returnyes:
            return listobject

    def find_within_dates(self,
                          datefrom=(1,1,1),
                          dateto=(3000,12,31),
                          withinrange=None,
                          orequal=False,
                          most_recent=False):

        """ To find notes with a range of dates"""

        def convert (date):

            if isinstance(date,str):
            #If input is a string convert to a tuple
                date += '-01-01'
                date = datefrom.split(DASH)
                year, month, day = date[0].replace(PLUS,DASH), date[1], date[2]
                date = int(year), int(month), int(day)
            if isinstance(date, (list,tuple)):
                #If a tuple, convert to a datetime object 
                date = datetime.datetime(date[0],date[1],date[2])
            return date 
            
        if withinrange is None:
            #If not range assigned, default to all indexes 
            withinrange = self.indexes()

        datefrom = convert(datefrom)
        dateto = convert(dateto)
            

        if not orequal:
            return [a_temp for a_temp in withinrange
                    if self.get_note(str(Index(a_temp))).date(most_recent=most_recent,
                                                               short=True,
                                                               convert=True)>  datefrom
                    and self.get_note(str(Index(a_temp))).date(most_recent=most_recent,
                                                                short=True,
                                                                convert=True) < dateto]
        return [a_temp for a_temp in withinrange
                if self.get_note(str(Index(a_temp))).date(most_recent=most_recent,
                                                           short=True,
                                                           convert=True) >=  datefrom and
                self.get_note(str(Index(a_temp))).date(most_recent=most_recent,
                                                        short=True,
                                                        convert=True) <= dateto]

    def index_sort(self,indexlist,
                   by_date=False, #changed from true 
                   most_recent=False,
                   quick=True,
                   no_check=True,
                   check_object=None):


        """sorts an list of the type Index"""


        if not by_date:

            if quick:

                return self.find_within(indexlist[0],indexlist[-1],orequal=True)
            return sorted(indexlist,
                          key=lambda x_temp: Index(str(x_temp)))

        if not no_check:
            if not check_object:
                check_object = self.get_all_indexes()
            indexlist = [x_temp for x_temp in indexlist if str(x_temp) in check_object]
        return sorted(indexlist,
                     key=lambda x_temp: \
                         self.get_note(x_temp).date(convert=False,
                                                    most_recent=most_recent))
      

    ### FUNCTIONS CORE ACCESS


    
    

    def add_note (self,
                  index,
                  keyset=None,
                  text=None,
                  metadata=None,
                  note=None,
                  keyset_only=None,
                  meta_only=None,
                  text_only=None):

        # USING SHELF
        
        if note:
            if self.using_shelf:
                self.note_dict[str(index)] = note
            text = note.text
            keyset = note.keyset
            metadata = note.meta

            
        elif keyset_only:
            if self.using_shelf:
                self.note_dict[str(index)].keyset = keyset_only
            keyset = keyset_only 
        elif text_only:
            if self.using_shelf:
                self.note_dict[str(index)].text = text_only
            text = text_only
        elif meta_only:
            if self.using_shelf:
                self.note_dict[str(index)].meta = meta_only

            metadata = meta_only

        else:
            if self.using_shelf:
                self.note_dict[str(index)] = Note(keyset,
                                                  text,
                                                  metadata)
        if not text:
            text = ''
        if not keyset:
            keyset = set()
        if not metadata:
            metadata = {'size':self.defaults.get('size'),
                        'date':[str(datetime.datetime.now())],
                        'user':self.defaults.get('user')}

        # USING DATABASE
        if self.using_database:
            aprint('ADDING NOTE')
            
            text = text.replace("'","''")
            db_cursor.execute("SELECT * FROM notes")
            

            value_tuple = (notebookname,str(index),text,metadata['size'],metadata['user'])
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO notes"
                              +" (notebook, note_index, note_body, size, user)"
                              +" VALUES (?,?,?,?,?);",
                              value_tuple)
            if not isinstance(metadata['date'],list):
                metadata['date'] = [metadata['date']]
            metadata['date'] = [str(d) for d in metadata['date']]
            
            for d_temp in metadata['date']:
            
                value_tuple = (notebookname, str(index), d_temp,)
                db_cursor.execute("INSERT OR REPLACE"
                                  +" INTO timestamps"
                                  +" (notebook, note_index, timestamp)"
                                  +" VALUES (?,?,?);",
                                  value_tuple)
            

            for k_temp in keyset:
                value_tuple = (notebookname, str(index), k_temp,)
                db_cursor.execute("INSERT OR REPLACE "
                                  +"INTO all_note_keys "
                                  +"(notebook, note_index, keyword)"
                                  +" VALUES (?,?,?);",
                                  value_tuple)
                
                   
                




    def delete_note (self,
                     index):

        if self.using_shelf:

            try:
                del self.note_dict[str(index)]
            except:
                display.noteprint((alerts.ATTENTION,alerts.DELETE+str(index)+alerts.FAILED))

        if self.using_database:
            aprint('DELETING NOTE')
            value_tuple = (notebookname,str(index),)
            db_cursor.execute("DELETE FROM "
                              +"notes WHERE notebook=?"
                              +" AND note_index=?;",
                              value_tuple)
            db_cursor.execute("DELETE FROM"
                              +" all_note_keys"
                              +" WHERE notebook=?"
                              +" and note_index=?;",
                              value_tuple)
            db_cursor.execute("DELETE FROM"
                              +" timestamps"
                              +" WHERE notebook=?"
                              +" and note_index=?;",
                              value_tuple)
            db_cursor.execute("SELECT note_index"
                              +" FROM notes"
                              +" WHERE notebook=?;",
                              (notebookname,))
            
           

    def get_note (self,
                  index):

        if self.using_database:
            aprint('GETTING NOTE')
            value_tuple = (notebookname, str(index),)
            db_cursor.execute("SELECT note_body  "
                              +"FROM notes WHERE notebook=?"
                              +" AND note_index=?;",
                              value_tuple)
                        
            text = db_cursor.fetchone()[0].replace("''","'")
            db_cursor.execute("SELECT user"
                              +" FROM notes"
                              +" WHERE notebook=?"
                              +" AND note_index=?;",
                              value_tuple)
            user = db_cursor.fetchone()[0]
            db_cursor.execute("SELECT size"
                              +" FROM notes"
                              +" WHERE notebook=? "
                              +"AND note_index=?;",
                              value_tuple)
            size = db_cursor.fetchone()[0]
            db_cursor.execute("SELECT timestamp "
                              +"FROM timestamps"
                              +" WHERE notebook=?"
                              +" AND note_index=?"
                              +" ORDER BY timestamp",
                              value_tuple)
            dates = db_cursor.fetchall()
            date_list = [date[0] for date in dates]
            db_cursor.execute("SELECT keyword"
                              +" FROM all_note_keys"
                              +" WHERE notebook=?"
                              +" AND note_index=?",
                              value_tuple)
            keyset = db_cursor.fetchall()
            keyset = {key[0] for key in keyset}

            metadata = {'user':user,
                        'date':date_list,
                        'size':size}
            return Note(keyset,text,metadata)        

        if str(index) in self.note_dict:
            return self.note_dict[str(index)]
            
        return False
        
 
    
    def notebook_contains (self,
                           index):

        
    
        if self.using_database:
            aprint('NOTEBOOK CONTAINS')
            
            value_tuple = (notebookname, str(index),)
            db_cursor.execute("SELECT rowid "
                              +"FROM notes"
                              +" WHERE notebook=?"
                              +" AND note_index=?;",
                              value_tuple)
            try:
                return db_cursor.fetchone()[0] # MIGHT BE PROBLEMATIC
            except:
                return False 
        
        return str(index) in self.note_dict

    def key_dict_contains (self,
                           key):

        
    
        if self.using_database:

            aprint('KEYDICT CONTAINS')
            value_tuple = (notebookname, key,)
            db_cursor.execute("SELECT note_index"
                              +" FROM keys_to_indexes"
                              +" WHERE notebook=?"
                              +" AND keyword=?;",
                              value_tuple)
            try:
                if db_cursor.fetchone()[0]:
                    return True
                return False # MIGHT BE PROBLEMATIC
            except:
                return False 
        
        return str(key) in self.key_dict

    def tag_dict_contains (self,
                           tag):

        
    
        if self.using_database:
            aprint('TAGDICT CONTAINS')
            value_tuple = (notebookname, tag,)
            db_cursor.execute("SELECT rowid "
                              +"FROM tags_to_keys"
                              +" WHERE notebook=?"
                              +" AND tag=?;",
                              value_tuple)
            try:
                return db_cursor.fetchone()[0] # MIGHT BE PROBLEMATIC
            except:
                return False 
        
        return str(tag) in self.tag_dict


    def word_dict_contains (self,
                           word):

        
    
        if self.using_database:
            aprint('WORDDICT CONTAINS')
            
            value_tuple = (notebookname, word,)
            db_cursor.execute("SELECT rowid"
                              +" FROM word_to_indexes"
                              +" WHERE notebook=?"
                              +" AND word=?;",
                              value_tuple)
            try:
                return db_cursor.fetchone()[0] # MIGHT BE PROBLEMATIC
            except:
                return False 
        
        return str(word) in self.word_dict


        
        

    def get_all_indexes (self):

        
        if self.using_database:
            aprint('GET ALL INDEXES')
            
            value_tuple = (notebookname,)
            db_cursor.execute("SELECT note_index"
                              +" FROM notes"
                              +" WHERE notebook=?",value_tuple)
            indexes = db_cursor.fetchall()
            indexes = {str(index[0]).strip() for index in indexes}
            return indexes
            
            
        return self.note_dict.keys()


    def get_keys_from_note (self,
                      index):

        if self.using_database:
            aprint('GETTING KEYS FROM NOTE')
            value_tuple = (notebookname, str(index),)
            db_cursor.execute("SELECT keyword "+
                              "FROM all_note_keys"+ " WHERE notebook=?"
                              + " AND note_index=?",value_tuple)
            keyset = db_cursor.fetchall()
            keyset = {key[0] for key in keyset}
            return keyset 

        if str(index) in self.note_dict:

            return self.note_dict[str(index)].keyset
        return set()

    def get_text_from_note (self,
                            index):

        if self.using_database:
            aprint('GETTING TEXT DROM NOTE')
            value_tuple = (notebookname, str(index),)
            db_cursor.execute("SELECT note_body"+
                              " FROM notes WHERE notebook=?"+
                              " AND note_index=?;",value_tuple)
            try:
                text = db_cursor.fetchone()[0].replace("''","'")
            except:
                text = ''
            
            return text
            
        if str(index) in self.note_dict:
            return self.note_dict[str(index)].text
        return ''

    def get_metadata_from_note (self,
                                index):

        if self.using_database:
            aprint('GET METADATA')
            value_tuple = (notebookname, str(index),)
            db_cursor.execute("SELECT user "+
                              "FROM notes WHERE notebook=? "+
                              "AND note_index=?;",
                              value_tuple)
            try:
                user = db_cursor.fetchone()[0]
            except:
                user = "USER"
            db_cursor.execute("SELECT size "
                              +" FROM notes WHERE notebook=?"
                              +" AND note_index=?;",
                              value_tuple)
            try:
                size = db_cursor.fetchone()[0]
            except:
                size = 60
            db_cursor.execute("SELECT timestamp"
                              +" FROM timestamps WHERE notebook=? "
                              +" AND note_index=?"
                              +" ORDER BY timestamp",
                              value_tuple)
            dates = db_cursor.fetchall()
            try:
                date_list = [str(date[0]) for date in dates]
            except:
                date_list = [str(datetime.datetime.now())]

            metadata = {'user':user,
                        'date':date_list,
                        'size':size}

            return metadata
            
        if str(index) in self.note_dict:

            return self.note_dict[str(index)].meta
        return {}

    def get_keys(self):

        #using database
        
        if self.using_database:
            aprint('GET KEYS')
            value_tuple = (notebookname,)
            db_cursor.execute("SELECT keyword"
                              +" FROM keys_to_indexes"
                              +" WHERE notebook=?;",
                              value_tuple)
            fetched = db_cursor.fetchall()
            if fetched:
                return {key[0] for key in fetched}
            
            return set()

        #using shelf

        return self.key_dict.keys()

    def get_tags(self):

        #using database
        
        if self.using_database:
            aprint('GET TAGS')
            value_tuple = (notebookname,)
            db_cursor.execute("SELECT tag"
                              +" FROM tags_to_keys"
                              +" WHERE notebook=?;",
                              value_tuple)
            fetched = db_cursor.fetchall()
            if fetched:
                return {tag[0] for tag in fetched}
            
            return set()

        #using shelf

        return self.tag_dict.keys()

    def get_words(self):

        #using database
        
        if self.using_database:
            value_tuple = (notebookname,)
            db_cursor.execute("SELECT word"
                              +" FROM word_to_indexes"
                              +" WHERE notebook=?;",
                              value_tuple)
            fetched = db_cursor.fetchall()
            if fetched:
                return {word[0] for word in fetched}
            
            return set()

        #using shelf

        return self.word_dict.keys()

    def get_keys_for_tag(self,tag):

        #using database
        if self.using_database:
            value_tuple = (notebookname, tag,)
            db_cursor.execute("SELECT keyword"
                              +" FROM tags_to_keys"
                              +" WHERE notebook=?"
                              +" AND tag=?;",
                              value_tuple)   
            fetched = db_cursor.fetchall()
            if fetched:
                return {tag[0] for tag in fetched}
            
            return set()
        #using shelf
        if self.using_shelf:
            if self.tag_dict_contains(tag):
                return self.tag_dict[tag]
            return set()
        


    def add_key(self,key,index):

        #with shelf

        if self.using_shelf:
        
            if key in self.key_dict:

                self.key_dict[key].add(str(index))

            else:
                self.key_dict[key] = {str(index)}

        #with database
        if self.using_database:

            value_tuple = (notebookname, key,)
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO all_keys (keyword, notebook)"
                              +" VALUES (?,?);",
                              value_tuple)
            value_tuple = (notebookname, key, str(index))
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO keys_to_indexes"
                              +" (notebook, keyword, note_index)"
                              +" VALUES (?,?,?);",
                              value_tuple)
           

    def add_word(self,word,index):

        #with shelf
        if self.using_shelf:

            if word in self.word_dict:

                self.word_dict[word].add(str(index))
            else:
                self.word_dict[word] = {str(index)}
                

        #with database
        if self.using_database:

            value_tuple = (notebookname, word,)
            db_cursor.execute("INSERT OR REPLACE "
                              +"INTO all_words "
                              +"(word, notebook)"
                              +" VALUES (?,?);",value_tuple)
            value_tuple = (notebookname, word, str(index))
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO word_to_indexes "
                              +"(notebook, word, note_index)"
                              +" VALUES (?,?,?);",
                              value_tuple)
           

    def initiate_new_word(self,word,index):

        #with shelf
        if self.using_shelf:

            self.word_dict[word] = {str(index)}

        #with database
        if self.using_database:

            value_tuple = (notebookname, word,)
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO all_words (word, notebook)"
                              +" VALUES (?,?);",value_tuple)
            value_tuple = (notebookname, word, str(index))
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO word_to_indexes (notebook, word, note_index)"
                              +" VALUES (?,?,?);",
                              value_tuple)
           

        

    def add_tag (self,tag,key):

        #with shelf
        
        if self.using_shelf:

            if tag in self.tag_dict:

                self.tag_dict[tag].add(key)

            else:

                self.tag_dict[tag] = {key}

        #with database
            
        if self.using_database:

            value_tuple = (notebookname, tag, key,)
            db_cursor.execute("INSERT OR REPLACE "
                              +"INTO tags_to_keys "
                              +"(notebook, tag, keyword) "
                              +"VALUES (?,?,?);",value_tuple)
           

        

    def discard_index_from_key(self,key,index):

        # with shelf
        if self.using_shelf:

            if key in self.key_dict:
        
                self.key_dict[key].discard(str(index))

        
        #with database
        if self.using_database:
            value_tuple = (notebookname,key,str(index),)
            db_cursor.execute("DELETE FROM"
                              +" keys_to_indexes"
                              +" WHERE notebook=?"
                              +" AND keyword=?"
                              +" AND note_index=?;",
                              value_tuple)

            db_cursor.execute("SELECT * FROM"
                              +" keys_to_indexes"
                              +" WHERE notebook=?"
                              +" and keyword=?;",
                              value_tuple[0:2])
            if db_cursor.fetchone():
                db_cursor.execute("DELETE FROM"
                                  +" all_keys WHERE notebook=?"
                                  +" AND keyword=?;",
                                  value_tuple[0:2])       

           

    def remove_index_from_word(self,word,index):

        # with shelf
        if self.using_shelf:

            if word in self.word_dict:
        
                self.word_dict[word].remove(str(index))

        
        #with database
        if self.using_database:
            
            value_tuple = (notebookname,word,str(index),)
            db_cursor.execute("DELETE FROM"
                              +" word_to_indexes"
                              +" WHERE notebook=?"
                              +" AND word=?"
                              +" AND note_index=?;",
                              value_tuple)

            db_cursor.execute("SELECT * FROM word_to_indexes"
                              +" WHERE notebook=?"
                              +" and word=?;",
                              value_tuple[0:2])
            if db_cursor.fetchone():
                db_cursor.execute("DELETE FROM"
                                  +" all_words"
                                  +" WHERE notebook=?"
                                  +" AND word=?;",
                                  value_tuple[0:2])

    def discard_index_from_word(self,word,index):

        # with shelf
        if self.using_shelf:

            if word in self.word_dict:
        
                self.word_dict[word].discard(str(index))

        
        #with database
        if self.using_database:
            
            value_tuple = (notebookname,word,str(index),)
            db_cursor.execute("DELETE FROM word_to_indexes "
                              +"WHERE notebook=? AND word=? "
                              +"AND note_index=?;",
                              value_tuple)

            db_cursor.execute("SELECT * FROM word_to_indexes"
                              +" WHERE notebook=? and word=?;",
                              value_tuple[0:2])
            if db_cursor.fetchone():
                db_cursor.execute("DELETE FROM all_words"
                                  +" WHERE notebook=?"
                                  +" AND word=?;",
                                  value_tuple[0:2])      

           

    def delete_word(self,word):

        # with shelf
        if self.using_shelf:
        
            del self.word_dict[word]

    def discard_key_from_tag(self,tag,key):

        # with shelf
        if self.using_shelf:
        
            self.tag_dict[tag].discard(key)

        
        #with database
        if self.using_database:
            value_tuple = (notebookname,tag,key,)
            db_cursor.execute("DELETE FROM tags_to_keys"
                              +" WHERE notebook=? AND tag=?"
                              +" AND keyword=?;",
                              value_tuple)    
           

    def delete_tag(self,tag):

        # with shelf
        if self.using_shelf:
            del self.tag_dict[tag]
        
    def remove_index_from_key(self,key,index):

        #with shelf
        if self.using_shelf:

            self.key_dict[key].remove(str(index))

        #with database
        if self.using_database:
            value_tuple = (notebookname,key,str(index))
            db_cursor.execute("DELETE FROM "
                              +"keys_to_indexes "
                              +"WHERE notebook=? "
                              +"AND keyword=? "
                              +"AND note_index=?;",
                              value_tuple)

            db_cursor.execute("SELECT * FROM "
                              +"keys_to_indexes "
                              +"WHERE notebook=? and keyword=?;",
                              value_tuple[0:2])
            if db_cursor.fetchone():
                db_cursor.execute("DELETE FROM "
                                  +"all_keys WHERE notebook=? "
                                  +"AND keyword=?;",
                                  value_tuple[0:2])       

           

    def initiate_new_key (self,key,index):

        #with shelf
        if self.using_shelf:


            self.key_dict[key] = {str(index)}

        #with database
        if self.using_database:

            value_tuple = (notebookname, key,)
            db_cursor.execute("INSERT OR REPLACE "
                              +"INTO all_keys (keyword, notebook)"
                              +" VALUES (?,?);",
                              value_tuple)
            value_tuple = (notebookname, key, str(index))
            db_cursor.execute("INSERT OR REPLACE "
                              +"INTO keys_to_indexes"
                              +" (notebook, keyword, note_index)"
                              +" VALUES (?,?,?);",
                              value_tuple)
           

    def initiate_new_tag (self,tag,key):

        #with shelf
        if self.using_shelf:
            self.tag_dict[tag] = {key}
        #with database

        if self.using_database:

            value_tuple = (notebookname, tag, key)
            db_cursor.execute("INSERT OR REPLACE"
                              +" INTO tags_to_keys"
                              +" (notebook, tag, keyword)"
                              +" VALUES (?,?,?);",
                              value_tuple)
           


    def get_indexes_for_key (self,key):
        
        if self.using_database:
            aprint('GETTING INDEXES FOR KEY')
            value_tuple = (notebookname,key,)
            db_cursor.execute("SELECT note_index"
                              +" FROM keys_to_indexes"
                              +" WHERE notebook=? and keyword=?;",
                              value_tuple)

            fetched = db_cursor.fetchall()
            if fetched:
                return {index[0].strip() for index in fetched}
            return set()
        
       
        return self.key_dict[str(key)]

    def get_indexes_for_word (self,word):
        
        if self.using_database:
            value_tuple = (notebookname,word,)
            db_cursor.execute("SELECT note_index"
                              +" FROM word_to_indexes"
                              +" WHERE notebook=? and word=?;",
                              value_tuple)

            fetched = db_cursor.fetchall()
            if fetched:
                return {index[0].strip() for index in fetched}
            return set()
        
       
        return self.word_dict[word]


    def eliminate_key (self,key):

        if self.using_shelf:

            del self.key_dict[str(key)]

##        #with database
##        value_tuple = (notebookname,key,)
##        if db_cursor.fetchone():
##            db_cursor.execute("DELETE FROM all_keys WHERE notebook=? AND keyword=?;",value_tuple)   

    def key_dict_values (self):

        if self.using_database:
            value_tuple = (notebookname,)
            db_cursor.execute("SELECT note_index "
                              +"FROM keys_to_indexes"
                              +" WHERE notebook=?;",
                              value_tuple)

            fetched = db_cursor.fetchall()
            if fetched:
                return  {index[0].strip() for index in fetched}
            return set()

        return self.key_dict.values()

    def tag_dict_values (self):

        if self.using_database:
            value_tuple = (notebookname,)
            db_cursor.execute("SELECT keyword "
                              +"FROM keys_to_indexes"
                              +" WHERE notebook=?;",
                              value_tuple)

            fetched = db_cursor.fetchall()
            if fetched:
                return  {index[0].strip() for index in fetched}
            return set()

        return self.tag_dict.values()



    def get_key_dict (self):

        return self.key_dict

    def dumpprojects (self):

        

        datesuffix=str(datetime.datetime.now()).split(' ')[0]
        project = str(transform(self.default_dict['projects'].return_dict()))

        if self.using_shelf:
            
            save_file(returntext=project,
                      filename='PROJ'+notebookname+datesuffix,
                      folder='/textfiles')
        if self.using_database:
            value_tuple = (notebookname, project,)
            db_cursor.execute("INSERT OR REPLACE "
                              +"INTO projects "
                              +"(notebook, projectfile) "
                              +"VALUES (?,?);",
                              value_tuple)
            db_connection.commit()

 
    
    ### CORE METHODS
    ### operations that modify shelf, key dictionary,
    ###tag dictionary, and word dictionary restricted
    ###to these core functions

    def addnew(self,
               keyset,
               text,
               notundoing=True,
               metadata=None,
               show=False,
               right_at=False,
               as_next=False,
               as_child=False,
               ind=Index(-1),
               re_entering=False,
               suspend=False,
               carrying_keys=True,
               quick=False,
               update_table=True):


        """adds a new note (keyset&text) Includes metadata if entered;
        otherwise creates new metadata. Notundoing is TRUE if the action
        is not the undoing of a previous deletion. Show is TRUE if the
        note is to be displayed
        """

        if self.read_only:
            display.noteprint((alerts.ATTENTION,'CANNOT EXECUTE: READ ONLY'))
            return index
        
        self.indexchanged, self.indexchanged_key, self.indexchanged_tag = True, True, True
        self.indexchanges += 1


        if quick and not self.notebook_contains(ind):

            self.add_note(str(ind),keyset,text,metadata)


            self.add_search_words(ind,text)
            self.iterator.add(ind)

            return None

        else:    
            
            entered_keys = keyset
            
            if metadata is None:
                metadata = {}
            text = self.default_dict['abbreviations'].undo(text)

            if isinstance(ind, (int, str)):
                ind = Index(ind)


            keyset = {a_temp.strip()
                      for a_temp in keyset.union(set(self.suspend_default_keys
                                                     *self.defaults.get('defaultkeys')))
                                                     if a_temp not in [EMPTYCHAR,
                                                                       BLANK,
                                                                       BLANK*2,
                                                                       BLANK*3,
                                                                       VOIDTERM]
                      and ATSIGN + QUESTIONMARK not in a_temp
                      and ATSIGN + UNDERLINE + QUESTIONMARK not in a_temp
                      and ATSIGN + POUND + QUESTIONMARK not in a_temp} 
                      #Add keywords from default list

            if self.linking:
                if not self.starting_linking:
                    keyset.add(str(self.lastindex))
                
                
            if not self.linking and self.looping:
                keyset.add(str(self.first_of_loop))
                keyset.add(str(self.lastindex))
                self.looping = False
                
                    

            

            if self.indexes():
                index = self.default_dict['indexlist_indexes'].list[-1]
            else:
                index = Index(1)

            if right_at:
                # right at is true if the note the index
                #position for the note has been passed into the function
                if not re_entering:
                    if not as_child:
                        index = next_next(ind,rightat=True)
                        if not ind.is_top():
                            if self.defaults.get('carryoverkeys'):
                                if self.defaults.get('carryall'):
                                    for x_temp in index.all_parents():
                                        if self.notebook_contains(x_temp):
                                            keyset = keyset.union({y_temp for y_temp
                                                                   in self.get_keys_from_note(x_temp)
                                                                   if ATSIGN not in y_temp})
                                            
                                else:
                                    x_temp = index.all_parents()[-2]
                                    if self.notebook_contains(x_temp):
                                        keyset = keyset.union({y_temp for y_temp
                                                               in self.get_keys_from_note(x_temp)
                                                               if ATSIGN not in y_temp})
                                        
                                    

                    else:
                        index = next_child(ind)
                        if self.defaults.get('carryoverkeys'):
                            if self.defaults.get('carryall'):
                                for x_temp in index.all_parents():
                                    if self.notebook_contains(x_temp):
                                        keyset = keyset.union({y_temp for y_temp
                                                               in self.get_keys_from_note(x_temp)
                                                               if ATSIGN not in y_temp})
                                        
                            else:
                                x_temp = index.all_parents()[-2]
                                if self.notebook_contains(x_temp):
                                   keyset = keyset.union({y_temp for y_temp
                                                          in self.get_keys_from_note(x_temp)
                                                          if ATSIGN not in y_temp})
                                
                else:
                    index = ind

            else:

                if as_child:
                    index = ind.child()
                elif as_next:
                    index = ind.next()
                else:

                    index = Index(int(index)).next()

            if str(index) in notebook.indexes():
                index = self.find_space(index)
            if not carrying_keys:
                keyset = entered_keys
            keyset.discard(VOIDTERM)
            if keyset == set():
                keyset = {VOIDTERM}

            if suspend:
                return index
            keyset = {index_expand(x_temp) for x_temp in keyset}
            newkeyset = self.add_keys_tags(index, keyset)

            if metadata == {}:

                self.add_note(index,newkeyset,text,{'size':self.defaults.get('size'),
                                                   'date':[str(datetime.datetime.now())],
                                                   'user':self.defaults.get('user')})

                

                #here the note is added to the shelf
            else:
                self.add_note(index,newkeyset,text,metadata)

                

            if notundoing:
                self.done.add(('add',
                               index,
                               newkeyset,
                               text))


            self.add_search_words(index, text)
            self.display_buffer.append(alerts.NOTE_ADDED+BLANK+index_reduce(str(index)))
            a_temp = display.noteprint(self.show(index,
                                                 yestags=self.tagdefault,
                                                 shortform=True),
                                       param_width=self.defaults.get('size'),
                                       np_temp=True,leftmargin=self.defaults.get('leftmargin'))
            self.default_dict['display'].append(a_temp)
            if show:

                display.noteprint(self.show(index),
                                  param_width=display.width_needed(self.show(index),
                                                                   self.get_metadata_from_note(index)['size'],
                                                                   leftmargin=self.defaults.get('leftmargin')),
                                  leftmargin=self.defaults.get('leftmargin'))

            self.lastindex = index
            self.iterator.add(index)
            if update_table:
                self.default_dict['indextable'].add(index)
                self.default_dict['indexlist'].add(index)
                self.default_dict['indexlist_indexes'].add(Index(index))
                self.changed = True
            if self.project:
                for p_temp in self.project:
                    self.default_dict['projects'].add_index(index,
                                                           project=p_temp)
            self.last_results = [index]

            if self.linking and self.starting_linking:
                
                self.starting_linking = False
                self.first_of_loop = index

            if len(str(index)) > self.maxdepth_found:
                self.maxdepth_found = len(str(index))
            if len(index_reduce(str(index))) > self.abr_maxdepth_found:
                self.abr_maxdepth_found = len(index_reduce(str(index)))
            
            return index

    def delete(self,
               index,
               notundoing=True,
               update_table=True):

        """permenently deletes the note at index.
        notundoing is true if it is not undoing a previous action
        Note that the command 'delete' moves a note to a negative index, rather than
        permanently deleting it"""

        if self.read_only:
            display.noteprint((alerts.ATTENTION,'CANNOT EXECUTE: READ ONLY'))
            return {'keys': set(),
                    'text': '',
                    'meta': {}}
        self.indexchanged, self.indexchanged_key, self.indexchanged_tag = True, True, True        
        self.indexchanges += 1


        if str(index) in self.indexes():
            self.display_buffer.append(index_reduce(str(index))+alerts.WAS_DELETED)
            self.delete_search_words(index,
                                     self.get_text_from_note(index))
            self.delete_keys_tags(index,
                                  self.get_keys_from_note(index))

            deletedmeta = self.get_metadata_from_note(index)
            deletedtext = self.get_text_from_note(index)
            deletedkeys = self.get_keys_from_note(index)

            if notundoing:
                self.done.add(('del',
                               index,
                               deletedkeys,
                               deletedtext))

            self.delete_note(index)

            if update_table:   
                self.default_dict['indextable'].delete(index)
                self.default_dict['indexlist'].delete(index)
                self.default_dict['indexlist_indexes'].delete(Index(index))
                self.changed = True
            if len(str(index)) == self.maxdepth_found:
                self.deepest(is_string=True,abridged=False)
            if len(index_reduce(str(index))) == self.abr_maxdepth_found:
                self.deepest(is_string=True,abridged=True)
            if self.project:
                for p_temp in self.project:
                    self.default_dict['projects'].delete_index(index,
                                                               project=p_temp)
                
            return {'keys': deletedkeys,
                    'text': deletedtext,
                    'meta': deletedmeta}

    def move(self,
             indexfrom,
             indexto,
             notundoing=True,
             withchildren=False,
             flatten=False,
             copy=False,
             update_table=True):

        if self.read_only:
            display.noteprint((alerts.ATTENTION,'CANNOT EXECUTE: READ ONLY'))
            return False

        if isinstance(indexfrom,str):
            indexfrom = Index(indexfrom)
        if isinstance(indexto,str):
            indexto = Index(indexto)


        """Moves a note from indexfrom to indexto, or next available space"""
        self.indexchanged, self.indexchanged_key, self.indexchanged_tag = True, True, True
        self.indexchanges += 1

        if str(indexfrom) not in self.indexes():
            return False


        if str(indexto) in self.indexes():

            indexto = self.find_space(indexto)
            if not copy:
                self.display_buffer.append(alerts.MOVING_TO+str(indexto))
            else:
                self.display_buffer.append(alerts.COPYING_TO+str(indexto))


        self.add_search_words(indexto, self.get_text_from_note(indexfrom))
        if not copy:
            self.delete_search_words(indexfrom, self.get_text_from_note(indexfrom))
        self.add_note(indexto,
                      self.get_keys_from_note(indexfrom),
                      self.get_text_from_note(indexfrom),
                      {'size':60,
                       'date':[str(datetime.datetime.now())],
                       'user':self.defaults.get('user')})
        if not copy:
            self.delete_note(indexfrom)
            

        for k_temp in self.get_keys():
            if str(indexfrom) in self.get_indexes_for_key(k_temp):
                
                if not copy:
                    self.discard_index_from_key(k_temp,indexfrom)
                self.add_key(k_temp,indexto)

        if notundoing:
            if not copy:
                
                self.done.add(('move',
                               indexfrom,
                               indexto))
            else:
               self.done.add(('add',
                              indexto,
                              self.get_keys_from_note(indexfrom),
                              self.get_text_from_note(indexfrom)))

        if not copy:
            self.display_buffer.append(alerts.NOTE
                                       +index_reduce(str(indexfrom))
                                       +alerts.MOVED_TO
                                       +index_reduce(str(indexto)))
        else:
            self.display_buffer.append(alerts.NOTE
                                       +index_reduce(str(indexfrom))
                                       +alerts.COPIED_TO
                                       +index_reduce(str(indexto)))

        if (withchildren or flatten) and indexfrom.is_top():
            for a_temp in self.find_within(str(indexfrom),
                                           str(indexfrom+Index(1))):

                if isinstance(indexto, (int, str)):
                    indexto = Index(indexto)
                if not flatten:
                    self.move(a_temp,
                              indexto+Index(a_temp)-Index(int(Index(a_temp))),
                              notundoing=True,
                              withchildren=False,
                              copy=copy)
                else:
                    self.move(a_temp,
                              indexto+Index(len(self.find_within(indexfrom, a_temp))-2),
                              notundoing=True,
                              withchildren=False,
                              copy=copy)
        if not copy:
            self.iterator.delete(indexfrom)
        self.iterator.add(indexto)
        if update_table:
            self.default_dict['indextable'].move(indexfrom,indexto)
            self.default_dict['indexlist'].delete(indexfrom)
            self.default_dict['indexlist_indexes'].delete(Index(indexfrom))
            self.default_dict['indexlist'].add(indexto)
            self.default_dict['indexlist_indexes'].add(Index(indexto))
            self.changed = True
            self.indexchanged = True
        return True



    def is_consistent(self,
                      notindexes=False,
                      notkeys=False):

        """Checks whether the database is consistent --- i.e. whether
        there is a one-to-one correspondence between the index
        numbers present as keys of the note_dict and values of the key_dict,
        as well as between the keys present as values of the note_dict
        and keys of the key_dict. Returns a tupple consisting of a boolean
        value, representing whether consistency is met for the requested
        attributes, the set of key discrepencies, set of index discrepencies
        Apologies for the equivocal use of 'keys,' referring both to
        python dictionary keys and the keys in the notes...
        """


        if len(self.indexes())>20000:
            return True, set(), set()

        val = self.key_dict_values()  
            #retrieve index numbers in key_dict
        val = {str(Index(a_temp))
               for a_temp in flatten.flatten(list(val))}
            #produce a set of integers for indexes
        indexes = set(self.indexes()) == val
            #TRUE if the indexes in the note_dict equals the set of values
        kset = set()
        for i_temp in self.indexes():
            kset = kset.union(self.get_keys_from_note(i_temp))
            #create a set of all the keys
        keys = (self.get_keys() == kset)
            # TRUE if the set of keys in the note_dict is
            #equal to the keys in the key dictionary

        if (len(self.default_dict['indextable'].table)
            != len(set(self.default_dict['indextable'].table.values()))):
            display.noteprint((alerts.ATTENTION,'Inconsistent'))



        return (indexes or notindexes) and (keys or notkeys),\
                set(self.get_keys()).symmetric_difference(kset),\
               set(self.indexes()).symmetric_difference(val)

    def add_field(self,
                  fieldname,
                  entrylist,
                  check=False):

        """ adds a new field, named fieldname, covering the index #s in entrylist """
        if self.read_only:
            display.noteprint((alerts.ATTENTION,'CANNOT EXECUTE: READ ONLY'))
            return False

        for e_temp in entrylist:
            if str(e_temp) in self.default_dict['field'] and check:
                temp_query = alerts.CHANGE+BLANK+self.default_dict['field'][str(e_temp)]\
                           +BLANK+alerts.TO+BLANK+fieldname+QUESTIONMARK
                if input(temp_query) not in YESTERMS:
                    self.default_dict['field'][str(e_temp)] = fieldname
            else:
                self.default_dict['field'][str(e_temp)] = fieldname
        self.dd_changed = True


    def delete_field(self,
                     fieldname,
                     rl=None):
        """ deletes a field"""
        if self.read_only:
            display.noteprint((alerts.ATTENTION,'CANNOT EXECUTE: READ ONLY'))
            return False

        if rl is None:
            searchset = set(self.indexes())
        else:
            searchset = {str(a_temp) for a_temp in rl}
        for k_temp in self.default_dict['field'].keys()&searchset:
            if self.default_dict['field'][k_temp] == fieldname:
                self.default_dict['field'].pop(k_temp)
        self.dd_changed = True

    def give_field(self,
                   fieldname):

        """return all the indexes correspondending to a given field"""

        return [a_temp for a_temp in self.default_dict['field']
                if self.default_dict['field'][a_temp] == fieldname]


    ### CORE DISPLAY METHODS ###


    def showmeta(self,
                 index):

        """show metadata of anote"""

        return self.get_metadata_from_note(index)

    def mark (self,
              index):

        if str(index) in self.default_dict['marked']:
            return POUND
        else:
            return BLANK

    def field(self,
              index):

        """returns the field name identified with a given index"""

        if str(index) in self.default_dict['field']:
            return self.default_dict['field'][str(index)]
        return EMPTYCHAR

    def show(self,
             index,
             shortform=False,
             length=None,
             yestags=True,
             highlight=None,
             show_date=True,
             most_recent=False,
             curtail=0,
             deepest=None):

 

        """returns 2-entry list for note at given index;
        list[0]=keys; list[1]=text
        """
        if not self.notebook_contains(index):
            display.noteprint((alerts.ATTENTION,'INDEX NOT FOUND'))
            return [set(),EMPTYCHAR]
        if not deepest:
            deepest = self.deepest(is_string=True,abridged=True)
        deepest += 3
        if not length:
            length = self.defaults.get('texttrim')
        d_index = str(index)
        if len(d_index) > 10:
            d_index = index_reduce(d_index) # to display long indexes in compact form
        if highlight is None:
            highlight = set()
        l_temp = []
        if show_date:
            date_insert = VERTLINE + \
                          self.get_note(index).date(short=True,
                                                          most_recent=most_recent,
                                                          convert=False)\
                                                          + BLANK
        else:
            date_insert = EMPTYCHAR
            

        if str(index) not in self.indexes():
            return [EMPTYCHAR, EMPTYCHAR]

        keyset_temp = self.get_keys_from_note(index)
        seq_keys = set()
        if self.defaults.get('sequences_in_text') and not shortform:
            oldkeys = set(keyset_temp)
            seq_keys = set()
            keyset_temp = set()
            seq_keys = {x_temp for x_temp in oldkeys if ATSIGN  in x_temp}
            keyset_temp = oldkeys - seq_keys

        kl = self.abridged_str_from_list(remove_tags(
            self.return_least_keys(transpose_keys(keyset_temp),
                                   override=not self.defaults.get('orderkeys'),
                                   add_number=True,no_allcaps=False), override=yestags),
                                         override=not shortform)
        seq_text = EMPTYCHAR

        if seq_keys:
            proj_seq = []
            main_seq = []
            other_seq = []

            for kx_temp in seq_keys:
                ident_temp= kx_temp.split(ATSIGN)[0]
                value_temp = kx_temp.split(ATSIGN)[1]
                if ident_temp in self.default_dict['projects'].get_all_projects():
                    proj_seq.append(kx_temp)
                elif ident_temp in self.default_dict['main_sequences']:
                    main_seq.append(kx_temp)
                else:
                    other_seq.append(kx_temp)
            proj_seq.sort()
            main_seq.sort()
            other_seq.sort()

            if proj_seq:
                seq_text = 'PROJECTS: ' + ', '.join(proj_seq) \
                           + self.defaults.get('seqform1')
            if main_seq: 
                for kx_temp in main_seq:
                    ident_temp= kx_temp.split(ATSIGN)[0]
                    value_temp = kx_temp.split(ATSIGN)[1]
                    seq_text += ident_temp + ':' + value_temp \
                                + self.defaults.get('seqform1')
            if other_seq:
                seq_text += EOL 
                for kx_temp in other_seq:
                    ident_temp= kx_temp.split(ATSIGN)[0]
                    value_temp = kx_temp.split(ATSIGN)[1]
                    seq_text += ident_temp + ':' + value_temp \
                                + self.defaults.get('seqform1')
            if seq_text:
                seq_text += EOL + self.defaults.get('seqform2')

            seq_text = seq_text.replace(BLANK+EOL,EOL)

            if COMMA + EOL in seq_text or COLON +EOL \
               in seq_text or SEMICOLON + EOL in seq_text:
                seq_text = seq_text\
                           .replace(COMMA+EOL,EOL)\
                           .replace(COLON+EOL,EOL)\
                           .replace(SEMICOLON+EOL,EOL)
                

        
        for char in string.whitespace[1:]:
            kl = kl.replace(char, EMPTYCHAR)
        
        kl = kl.replace(UNDERLINE, BLANK)
            
        
        if not shortform:

            tex_temp = self.get_text_from_note(index).replace(TAB,BLANK*4).replace('/T',BLANK*4)
            
            for rep_temp in range(0,tex_temp.count('}}')):
                if '{{' in tex_temp and '}}' in tex_temp:
                    n_temp = tex_temp.split('{{')[1].split('}}')[0]


                    if n_temp and n_temp[0] in [ATSIGN, STAR]:
                        pass
                        if self.show_text:
                            folder_temp = {ATSIGN:'/textfiles',
                                           STAR:'/attachments'}[n_temp[0]]
                            n_temp = n_temp[1:]
                            try:
                                textfile = get_text_file(n_temp,
                                                         folder=folder_temp)
                                tex_temp = tex_temp.replace('{{'+ATSIGN+n_temp+'}}',
                                                            textfile)
                            except:
                                display.noteprint((alerts.ATTENTION,
                                                   labels.FILE_ERROR))
                    elif n_temp and n_temp[0] in ['^']:
                        if self.show_images:
                            folder_temp = '/pictures'
                            directoryname = os.getcwd()+folder_temp
                            picture = Image.open(directoryname
                                                 +'/'+n_temp[1:]
                                                 +'.jpg')
                            picture.show()
                            
                        

            suffix = EMPTYCHAR
            if self.no_flash:
                tex_temp = tex_temp.replace('/FC/','\n  /BREAK/  \n')
            if '/FC/' in tex_temp:
                sides_temp = tex_temp.split('/FC/')
                if self.flexflip:
                    self.sides = len(sides_temp)
                    if self.last_sides != self.sides:
                        self.side=0
                        self.last_sides = self.sides
                tex_temp =  sides_temp[self.side%len(sides_temp)]          
                suffix =  '[' + str(self.side%len(sides_temp)+1) + ']' 
                
                
            

            if curtail != 0 and len(tex_temp) > curtail:
                tex_temp = tex_temp[0:curtail]
            # Adds the first and second element on the list 
            l_temp.append(d_index+self.mark(index)+suffix
                          +BLANK+VERTLINE+BLANK
                          +self.field(index)
                          +date_insert
                          +BLANK+VERTLINE+BLANK+kl
                          +BLANK+VERTLINE)
            l_temp.append(seq_text + nformat.encase(tex_temp,
                                         highlight))
            if len(l_temp) > 1: 
                if self.defaults.get('curtail'):
                    l_temp[1] = l_temp[1].strip(EOL)
                l_temp[1] = EOL * self.defaults.get('header') \
                            + l_temp[1] + EOL \
                            * self.defaults.get('footer') 

        else:

            t_temp = self.get_text_from_note(index)
            t_temp = t_temp[0 : min([len(t_temp), length])]
            t_temp = nformat\
                     .purgeformatting(t_temp)\
                     .replace(EOL,EMPTYCHAR)\
                     .replace(TAB,EMPTYCHAR)\
                     .replace(VERTLINE,EMPTYCHAR)\
                     .replace(UNDERLINE,EMPTYCHAR)
        
            t_temp = nformat.encase(t_temp,highlight)
            
            
            
            l_temp.append(d_index+self.mark(index)
                          +max([deepest-(len(d_index+self.mark(index))),0])
                          *BLANK+BLANK+VERTLINE+BLANK
                          +self.field(index)
                          +max([self.field_length()
                                -(len(self.field(index))), 0])*BLANK+BLANK
                          +date_insert
                          +BLANK
                          +VERTLINE+BLANK+kl
                          +(self.defaults.get('keytrim')-len(kl))*BLANK\
                          +BLANK+VERTLINE
                          +BLANK+t_temp)

        return l_temp

    def indexes(self):

        """show all indexes for existing notes"""
        

        if not self.usesequence:

            if len(self.get_all_indexes()) != len(self.sortedindexes) \
               or self.indexchanged or not self.sortedindexes:
                self.indexchanged = False 
                self.sortedindexes = sorted(self.get_all_indexes(),
                                            key=lambda x_temp: Index(x_temp))
                return self.sortedindexes
            return self.sortedindexes
        else:
            if self.indexchanged:
                self.sortedindexes = self.default_dict['indexlist'].strings()
                return self.sortedindexes
            else:
                return self.sortedindexes

    def keys(self):

        """show all keys for existing notes"""
        if self.indexchanged_key or not self.sortedkeys:
            self.indexchanged_key = False
            self.sortedkeys = sorted(self.get_keys())
            return self.sortedkeys
        return self.sortedkeys


    def tags(self):

        """show all tags for existing notes"""
        if self.indexchanged or not self.sortedtags:
            self.indexchanged_tag = False
            self.sortedtags = sorted(self.get_tags())
            return self.sortedtags
        return self.sortedtags

    def keys_for_tags(self):

        """Show keys listed in different tags"""

        for counter, t_temp in enumerate(sorted(self.get_tags())):
            display.noteprint((labels.TAGS[3:]+POUND+BLANK+str(counter+1)
                               +BLANK+COLON+BLANK+t_temp,
                               formkeys(self.get_keys_for_tag(t_temp))))

    def set_limit_list(self,
                       entry,
                       predicate=False,
                       intersection=False):


        """sets the list of indexes for the range of
        notes over which functions are to be executed
        """

        if isinstance(entry, list):
            self.limitlist += entry
        elif entry == 'F':   #set to flipbook
            self.limitlist = [str(x_temp) for x_temp in self.default_dict['flipbook']]
        elif entry == 'E':  
            self.limitlist = []  #empty limit list
        elif entry == 'R':   
            self.limitlist = self.indexes()  #reset limit list
        elif entry.replace(PERIOD, EMPTYCHAR).isnumeric():
            self.limitlist += [str(Index(entry))]

        elif SLASH in entry:
            # if a range separed by a SLASH
            from_temp = entry.split(SLASH)[0] + '-01-01'
            from_temp = from_temp.split(DASH)
            to_temp = entry.split(SLASH)[1] + '-12-31'
            to_temp = to_temp.split(DASH)

            
            datefrom = (int(from_temp[0]),int(from_temp[1]),int(from_temp[2]))
            dateto = (int(to_temp[0]),int(to_temp[1]),int(to_temp[2]))

            if not intersection:
                self.limitlist += self.find_within_dates(datefrom=datefrom,
                                                         dateto=dateto,
                                                         orequal=True,
                                                         most_recent=predicate)
            else:
                
                self.limitlist = list(set(self.limitlist).\
                                      intersection(set(self.find_within_dates(datefrom=datefrom,
                                                                              dateto=dateto,
                                                                              orequal=True,
                                                                              most_recent=predicate))))

                    
 
        elif DASH in entry:
            # If a range separated by a DASH.
            frompoint = Index(entry.split(DASH)[0])
            topoint = Index(entry.split(DASH)[1])


            if not intersection:
                self.limitlist += self.find_within(frompoint,
                                                   topoint,
                                                   orequal=True)
            else:
                self.limitlist = list(set(self.limitlist)\
                                      .intersection(set(self.find_within(frompoint,
                                                                         topoint,
                                                                         orequal=True))))



        else:
            for a_temp in entry.split(COMMA+BLANK):

                if not intersection:

                    self.limitlist += self.give_field(a_temp)

                else:
                    self.limitlist = list(set(self.limitlist)\
                                          .intersection(set(self.give_field(a_temp))))

    def apply_limit(self, entrylist):
        
        """excludes from the entrylist all the values that are not in self.limitlist"""

        entryset = set(entrylist)
        limitset = set(self.limitlist)
        if not limitset:
            limitset = set(self.indexes())
        if isinstance(entrylist, set):
            return entryset.intersection(limitset)
        if isinstance(entrylist, list):
            return list(entryset.intersection(limitset))
        return list(entryset.intersection(limitset))

##    def show_limit_list(self):
##        """shows the limit list"""
##        return list(self.limitlist)

    ### SECONDARY METHODS###


    def copy_to_temp(self,
                     index,
                     tempobject):

        """Loads note at index into tempobject """

        tempobject.load(index,
                        self.get_note(index))
        self.display_buffer.append(index_reduce(str(index))+alerts.COPIED_TO_TEMP)

    def copy_from_temp(self,
                       tempobject):

        """Copies a note back from tempobject"""

        copy_note = tempobject.get()
        if not isinstance(copy_note, bool):
            index = copy_note[0]
            c_note = copy_note[1]
            nprint(PERIOD,end=EMPTYCHAR)


            self.addnew(c_note.keyset,
                        c_note.text,
                        metadata=c_note.meta,
                        right_at=True,
                        ind=index,
                        quick=True)
        else:
            pass


    def copy_many_to_temp(self,
                          sourcerange=None):

        """Copies a range of notes to temporary object"""

        if sourcerange is None:
            sourcerange = []

        for a_temp in sourcerange:

            self.copy_to_temp(a_temp,
                              self.tempobject)




    def copy_many_from_temp(self,
                            count):

        """Copies X number of notes from temporary object"""

        for counter in range(count):
            nprint(PERIOD,end=EMPTYCHAR)
            self.copy_from_temp(self.tempobject)
        self.constitute_key_freq_dict()
        print()

    def move_many(self,
                  sourcerange=None,
                  destinationrange=None,
                  subordinate=False,
                  makecompact=False,
                  all_children=False,
                  withchildren=True,
                  copy=False):

        """Moves a range of notes to a new locations.
        Can also be used to make a range of notes a child of one note.
        With children: include children in the move.
        In this case: subordinate preserves hierarchy.
        Makecompact destroys hierarachy.
        All_children --- makes each moved note a child of the note before.
        """

        if sourcerange is None:
            sourcerange = []
        if destinationrange is None:
            destinationrange = []
        flatten = False



        if not withchildren:
            sourcerange = [a_temp for a_temp in sourcerange if a_temp.is_top()]

        if len(destinationrange)==1 and \
           (subordinate and str(destinationrange[0]) in self.indexes()
            and str(destinationrange[0].child()) not in self.indexes()):

            for i_temp in sourcerange:

                self.move(i_temp,
                          destinationrange[0].subordinate(i_temp),
                          withchildren=False, 
                          copy=copy)

        elif len(destinationrange)==1 and (makecompact
                                           and str(destinationrange[0])
                                           in self.indexes()
              and str(destinationrange[0].child()) not in self.indexes()):

            j_temp = destinationrange[0].child()
            for i_temp in sourcerange:
                self.move(i_temp,
                          j_temp,
                          withchildren=False,
                          copy=copy)
                j_temp = j_temp.next()

        elif len(destinationrange)==1 and all_children \
             and str(destinationrange[0]) in self.indexes():

            childcount = 1
            for i_temp in sourcerange:
                j_temp = destinationrange[0]
                for a_temp in range(childcount):
                    j_temp = j_temp.child()
                childcount += 1
                self.move(i_temp,
                          j_temp,
                          withchildren=withchildren,
                          copy=copy)

        else:

            sourcecycle = cycle(sourcerange)
            destinationcycle = cycle(destinationrange)
            if withchildren:  #not deleted
                flatten = True

            for a_temp in range(len(sourcerange)):

                i_temp = next(sourcecycle)
                j_temp = next(destinationcycle)

                self.move(i_temp,
                          j_temp,
                          withchildren=withchildren,
                          flatten=flatten,
                          copy=copy)


    def find_parent(self,
                    index):

        """Finds the parent of a detached note."""

        if not index.level() > 1:
            return False
        go_on = True
        while not index.is_top() or index.level() < 1:


            if str(index.parent()) in self.indexes():
                return index.parent()
            index = index.parent()

        return False

    def rehome_orphans(self,
                       entrylist):

        """provides a list of tupples giving
        the 'moves' needed to reduce a NoteBook
        """

        entrylist = [a_temp for a_temp in entrylist if not Index(a_temp).is_top()]

        last_e = Index(0)

        for e_temp in entrylist:

            e_temp = Index(e_temp)
            if str(e_temp.parent()) not in self.indexes():
                if self.find_parent(e_temp):

                    if str(self.find_parent(e_temp)) in self.indexes():
                        self.move(e_temp,
                                  next_child(self.find_parent(e_temp)))
                    else: self.move(e_temp,
                                    self.find_parent(e_temp))
                else:

                    if str(Index(int(e_temp))) not in self.indexes():
                        self.move(e_temp,
                                  Index(int(e_temp)))
                    else:
                        self.move(e_temp,
                                  self.find_space(Index(int(e_temp))))


        self.display_buffer.append(alerts.REHOMED)

    def conflate(self,
                 indexlist,
                 destinationindex=None,
                 inbetween='|/BREAK/|',
                 return_text=False):

        """creates a single note from one or more notes"""


        
        addkeyset = set()
        addtext = EMPTYCHAR

        for i_temp in [Index(i_temp)
                       for i_temp in indexlist
                       if str(i_temp) in self.indexes()]:

            addkeyset.update(self.get_keys_from_note(i_temp))
            addtext += inbetween + \
                       nformat.purgeformatting(self.get_text_from_note(i_temp),'nb')

        addtext = addtext.replace('/ENDCOL//COL/','/ENDCOL/'+EOL+'/COL/')
        if return_text:
            return addtext

        if not destinationindex:
            self.addnew(addkeyset,
                        addtext,
                        show=True)
            

        else:
            if isinstance(destinationindex,str) or isinstance(destinationindex,int):
                destinationindex = Index(destinationindex)
            
            self.addnew(addkeyset,
                        addtext,
                        right_at=True,
                        ind=destinationindex,
                        show=True)
        return None

    def menu_correct_keys(self,
                          indexrange=None,
                          allindexes=True,
                          keysonly=True):



        def dict_format(x_temp):

            """formats output of the list of search results"""

            shown_indexes = rangelist.range_find([Index(a_temp)
                                                  for a_temp in x_temp[1]])
            if len(shown_indexes) < 20:
                return (abridge(x_temp[0],maxlength=30)
                        +VERTLINE
                        +shown_indexes)

            returnlist = []
            sp_temp = split_up_range(shown_indexes,seg_length=3)
            
                                        
            returnlist.append(abridge(x_temp[0],maxlength=20)
                              +VERTLINE+sp_temp[0])
            for s_temp in sp_temp[1:]:
                returnlist.append(VERTLINE+s_temp)

            return returnlist 

        keyset = set()
        key_index_dict = {}
        
        
        if not indexrange:
            indexrange = self.apply_limit(self.indexes())

        for i_temp in indexrange:
            temp_keys = self.get_keys_from_note(i_temp)
            if not keysonly:
                newkeys = [(x_temp,x_temp) for x_temp in temp_keys]
            else:
                newkeys = [(x_temp.split(SLASH)[0],x_temp)
                           for x_temp in temp_keys]
            
                
            keyset.update({x_temp[0] for x_temp in newkeys})
            for key, keytag in newkeys:

                if not keysonly:
                    if allindexes:
                        if key not in key_index_dict:
                            key_index_dict[key]=self.get_indexes_for_key(key)
                    if not allindexes:
                        if key not in key_index_dict:
                            key_index_dict[key]={i_temp}
                        else:
                            key_index_dict[key].add(i_temp)
                            
                else:
                    if allindexes:
                        if key not in key_index_dict:
                            key_index_dict[key]=self.get_indexes_for_key(keytag)
                    if not allindexes:
                        if key not in key_index_dict:
                            key_index_dict[key]={i_temp}
                        else:
                            key_index_dict[key].add(i_temp)
                    
        list_to_show = []
        

        for counter, key in enumerate(sorted (keyset,
                                              key=lambda x: x.lower())):

            list_to_show.append((key,key_index_dict[key]))
        key_list = []
        accumulated_set = show_list(list_to_show,labels.KEYS[3:],0,30,
                                    func=dict_format,
                                    accumulate=True,
                                    present=True)
        if accumulated_set:
            for a_temp in accumulated_set:
                if int(a_temp)-1 < len(list_to_show) and int(a_temp)-1 > -1:
                    key_list.append(list_to_show[int(a_temp)-1])
        for k_temp in key_list:
            k_temp,il_temp = k_temp[0], k_temp[1]
            display.noteprint((k_temp,rangelist.range_find([Index(x_temp)
                                                            for x_temp in il_temp],reduce=True)))
            nk_temp = input(queries.REVISE_DELETE_BEG
                            +BLANK+k_temp+BLANK
                            +alerts.REVISE_DELETE_END)

            if nk_temp not in ['delete', 'Delete','d','D']:
                if nk_temp in self.keys() and nk_temp != EMPTYCHAR:
                    display.noteprint((alerts.ATTENTION,
                                       nk_temp+alerts.ALREADY_IN_USE
                                       +self.get_indexes_for_key(nk_temp)))
                    tp_temp = alerts.STILL_CHANGED + nk_temp+QUESTIONMARK
                    if input(tp_temp) not in YESTERMS:
                        nk_temp = k_temp.strip()
                elif nk_temp == EMPTYCHAR:
                    nk_temp = k_temp.strip()
                elif nk_temp in NOTERMS:
                    nk_temp = k_temp.strip()
                display.noteprint((EMPTYCHAR,
                                   alerts.CHANGE+BLANK\
                                   +k_temp+BLANK+alerts.TO\
                                   +BLANK+nk_temp))
            else:
                xx_temp = set(il_temp)
                self.delete_key(k_temp)
                nk_temp = EMPTYCHAR
                il_temp = set(xx_temp)


            if not nk_temp or nk_temp != k_temp:
                for i_temp in [x_temp for x_temp \
                               in set(il_temp) \
                               if Index(x_temp)>Index(0)]:
                    nprint(i_temp)


                    tempks = self.get_keys_from_note(i_temp)
                    if not keysonly:
                        tempks.discard(k_temp)
                        if nk_temp: 
                            tempks.add(nk_temp)
                    if keysonly:
                        for temp_x in list(tempks):
                            if temp_x.split(SLASH)[0] == k_temp:
                                oldkey = temp_x
                                if SLASH in temp_x:
                                    newkey = nk_temp + SLASH + temp_x.split(SLASH)[1]
                                else:
                                    newkey = nk_temp
                                tempks.discard(oldkey)
                                tempks.add(newkey)    

                    temptext = self.get_text_from_note(i_temp)
                    tempmeta = self.get_metadata_from_note(i_temp)
                    self.softdelete(i_temp)
                    self.addnew(keyset=tempks,
                                text=temptext,
                                metadata=tempmeta,
                                show=True,
                                right_at=True,
                                ind=i_temp)

                    

    def edit(self,
             index,
             newkeyset=None,
             newtext=None,
             changekeys=False,
             changetext=True,
             annotate=False,
             askabort=False,
             update_table=True):

        """deletes old note, and adds new edited note...!
        """

        oldkeyset = self.get_keys_from_note(index)
        oldtext = self.get_text_from_note(index)
        oldmeta = dict(self.get_metadata_from_note(index))
        if not isinstance(oldmeta['date'],list):
            oldmeta['date'] = [str(oldmeta['date'])]
        oldmeta['date'].append(str(datetime.datetime.now()))

        if not newkeyset:
            newkeyset = oldkeyset
            

        if changekeys:
            newkeyset = set(edit_keys(keyobject=list(oldkeyset),
                                      displayobject=display,
                                      prompt='Keys',
                                      deletekeys=True,
                                      addkeys=True,
                                      askabort=askabort,
                                      vertmode=self.vertmode,
                                      notebookobject=self))

            if 'ABORTNOW' in newkeyset:
                return False


            
        if not newtext:
            if changetext:
                newtext = textedit_new(oldtext,
                                       size=display.width_needed(
                                           self.show(str(index)),
                                           self.get_metadata_from_note(index)['size']),
                                       annotate=annotate)
            else:
                newtext = oldtext
        

        if self.delete_by_edit:
            self.delete(index,update_table=update_table)
        else:
            self.softdelete(index,update_table=update_table)
        self.addnew(newkeyset,
                    newtext,
                    metadata=oldmeta,
                    ind=index,
                    right_at=True,
                    update_table=update_table)
        return True

    def add_keyword(self,
                    index,
                    keywords):

        """Adds keyswords to note at index"""

        if isinstance(keywords, str):
            keywords = {keywords}

        self.edit(index,
                  self.get_keys_from_note(index).union(keywords),
                  self.get_text_from_note(index))

    def delete_keyword(self,
                       index,
                       keywords):

        """Deletes keywords from note at index"""

        if isinstance(keywords, str):
            keywords = {keywords}
        self.edit(index,
                  self.get_keys_from_note(index).difference(keywords),
                  self.get_text_from_note(index))

    def add_text(self,
                 index,
                 addtext):

        """adds entered text to an existing note"""

        oldkeyset = self.get_keys_from_note(index)
        oldtext = self.get_text_from_note(index)
        oldmeta = dict(self.get_metadata_from_note(index))
        oldmeta['date'].append(str(datetime.datetime.now()))

        self.delete(index)
        self.addnew(oldkeyset,
                    oldtext+addtext,
                    metadata=oldmeta)

    def merge_notes(self,
                    indexrange,
                    indexdestination=Index(-1)):
        """merges two notes together"""

        newnote = Note(set(),
                       EMPTYCHAR,
                       {'size': 60,
                        'date': [str(datetime.datetime.now())],
                        'user': self.defaults.get('user')})
        for n in indexrange:
            if str(n) in self.indexes():
                newnote += self.get_note(n)
            if indexdestination == Index(-1):
                self.addnew(keyset=newnote.keyset,
                            text=newnote.text,
                            metadata=newnote.meta)

        else:

            self.addnew(keyset=newnote.keyset,
                        text=newnote.text,
                        metadata=newnote.meta,
                        right_at=True,
                        ind=indexdestination)


    def merge_many(self,
                   indexrange,
                   dindex,
                   showkeys=True):

        """ merges many notes together. Whereas
        'conflate' merely merges text and keywords,
        'merge_many' creates embedded notes.
        Does not save to backup!
        """

        def embedcount(line):

            """return size adjusted for number of embedded notes"""

            x_temp = line.count(BOX_CHAR['lu'])
            return self.defaults.get('size')-(4*x_temp)

        tempkeys = set()
        temptext = EMPTYCHAR
        counter = 0

        for i_temp in indexrange:

            if str(i_temp) in self.indexes():
                counter += 1
                if showkeys:
                    tempkeys = tempkeys.union(self.get_keys_from_note(i_temp))
                temptext += EOL+display.noteprint(self.show(i_temp),
                                                   notenumber=counter,
                                                   param_width=embedcount(self.show(i_temp)),
                                                   np_temp=True)+EOL
        maxsize = 0
        for i_temp in indexrange:

            if str(i_temp) in self.indexes():
                if self.get_metadata_from_note(i_temp)['size'] > maxsize:
                    maxsize = self.get_metadata_from_note(i_temp)['size']

        oldsize = self.defaults.get('size')
        self.defaults.set('size',maxsize)
        self.addnew(tempkeys, temptext, show=True,ind=dindex,right_at=(dindex!=0))
        self.defaults.set('size',oldsize)
        self.dd_changed = True

    def columnize(self,
                  index,
                  convert=SEMICOLON,
                  columnchar=UNDERLINE,
                  undo=False,
                  counters=False,
                  only_counter=True):

        """ create a new note divided into columns """

        if index in self.indexes():

            note_temp = self.get_note(index)

            

            if not undo:

                if not only_counter:
                    note_temp.text = note_temp.text.replace(convert,
                                                            BLANK+columnchar+BLANK)


                    
                    if '/COL/' not in note_temp.text:
                        note_temp = COLUMNBEGIN + note_temp
                    if '/ENDCOL/' not in note_temp.text:
                        note_temp = note_temp + COLUMNEND

                newtext = EMPTYCHAR
                lines = note_temp.text.split(EOL)
                endline = len(lines)
                for counter, line in enumerate(lines):
                    if columnchar not in line:
                        newtext += (POUND+ str(counter) + BLANK + columnchar) \
                                   *(counters and counter not in [0,endline]) \
                                   + line + BLANK + columnchar + EOL
                    else:
                        newtext += (POUND+ str(counter) + BLANK + columnchar)\
                                   *(counters and counter not in [0,endline])\
                                   + line + EOL

            else:
                newtext = EMPTYCHAR
                lines = note_temp.text.split(EOL)
                for counter, line in enumerate(lines):
                    if counter == 0 and '/COL/' in line:
                        line = line.replace('/COL/',EMPTYCHAR)
                    if counter == len(lines) and '/ENDCOL/' in line:
                        line = line.replace('/ENDCOL/',EMPTYCHAR)
                    newtext += line + EOL
                newtext = newtext.replace(BLANK + columnchar + BLANK,convert)
                

                
            self.softdelete(index)
            self.addnew(note_temp.keyset,
                        newtext,
                        note_temp.meta,
                        right_at=True,
                        ind=index)
                
            




    def revise(self,
               index,
               oldindex=None,
               infront=True,
               inback=False,
               breaker=Note(set(),EMPTYCHAR)):

        """enters a new note at index 0.
        Merges with existing note at given index.
        Moves 'merged' note back into index.
        """
##        self.default_dict['currentindex'] = Index(0)
        if str(index) in self.indexes():

            newnote = self.get_note(index)
            if not oldindex or str(oldindex) not in self.indexes():
                if infront:
                   newnote = self.enter(returnnote=True) + breaker + newnote
                if inback:
                   newnote = newnote + breaker + self.enter(returnnote=True)
            else:
                if infront:
                   newnote = self.get_note(oldindex) +  breaker + newnote
                if inback:
                   newnote = newnote + breaker + self.get_note(oldindex)
                

            self.softdelete(index)
            self.addnew(newnote.keyset,
                        newnote.text,
                        newnote.meta,
                        right_at=True,
                        ind=index)
        else:
            display.noteprint((alerts.ATTENTION,'Fail'))


    def revise_range(self,
                     indexrange):

        """ revises over a range of notes"""

        for i_temp in indexrange:
            if str(i_temp) in self.indexes():
                display.noteprint(self.show(i_temp),
                                  param_width=self.defaults.get('size'))
                self.revise(i_temp)

##    def change_index(self,
##                     index):
##
##        """Changes the current index position to a new position"""
##
##        if isinstance(index, (str, int)):
##            index = Index(index)
##
####        if str(index) in self.indexes():
####            self.default_dict['currentindex'] = self.find_space(index)
##
##        else:
##            while True:
##
##                if str(index) in self.indexes() or index < Index(2):
##                    self.default_dict['currentindex'] = self.find_space(index)
##                    break
##                index -= Index(1)
##        display.noteprint(('/C/INDEX CHANGED TO',
##                           str(self.default_dict['currentindex'])))


    def undo_many(self):

        """Undo many commands"""

        undo_list = DisplayList(displayobject=display)
        commands = reversed(list(self.done.show()))

        for counter, command in enumerate(commands):
            undo_list.append(str(counter+1)
                             +BLANK+COLON+BLANK+str(command[0])
                             +SLASH+str(command[1]))
        undo_list.show(header=labels.TO_UNDO)
        reps = int(input(queries.UNDO_UP_TO))
        for r_temp in range(0, reps+1):
            self.undo()

    def undo(self):

        """Undoes a command that has been executes"""

        if self.done.size() > 0:
            command = self.done.pop()
            if command[0] == 'add':
                uncommand = (('del'),
                             command[1],
                             command[2],
                             command[3])
                self.delete(uncommand[1],
                            False)
            if command[0] == 'del':
                uncommand = (('add'),
                             command[1],
                             command[2],
                             command[3])
                self.addnew(uncommand[2],
                            uncommand[3],
                            False)
            if command[0] == 'move':
                uncommand = (('move'),
                             command[2],
                             command[1])
                self.move(uncommand[1],
                          uncommand[2],
                          False)
            self.undone.add(uncommand)

    def redo(self):

        """Reexecutes an undone command"""

        if self.undone.size() > 0:
            command = self.undone.pop()
            if command[0] == 'add':
                uncommand = (('del'),
                             command[1],
                             command[2],
                             command[3])
                self.delete(uncommand[1],
                            False)
            if command[0] == 'del':
                uncommand = (('add'),
                             command[1],
                             command[2],
                             command[3])
                self.addnew(uncommand[2],
                            uncommand[3],
                            False)
            if command[0] == 'move':
                uncommand = (('move'),
                             command[2],
                             command[1])
                self.move(uncommand[1],
                          uncommand[2],
                          False)
            self.done.add(uncommand)

    def mass_move(self,
                  entrylist1,
                  entrylist2):

        """moves a group of notes from entrylist1(list of indexes)
        to entrylist2
        """


        if len(entrylist1) > len(entrylist2):
            entrylist2 = entrylist2+list(range(entrylist2[-1]+1,
                                               (entrylist2[-1]
                                                +len(entrylist1)
                                                -len(entrylist2))))
        lastindexto = entrylist2[0]

        e1 = iter(entrylist1)
        e2 = iter(entrylist2)
        gofurther = True

        while gofurther:
            try:
                indexfrom = next(e1)
            except StopIteration:
                indexfrom = StopIteration
            try:
                indexto = self.find_space(next(e2), entrylist2)
            except StopIteration:
                indexto = StopIteration
            if indexto != StopIteration:
                lastindexto = indexto
            if indexto == StopIteration:
                indexto = self.find_space(lastindexto)

            if indexfrom != StopIteration:
                self.display_buffer.append(alerts.MOVING_FROM
                                           +index_reduce(str(indexfrom))
                                           +queries.TOTO+str(indexto))
                self.move(indexfrom, indexto)
            else:
                gofurther = False

    def add_iterator(self,
                     entrylist,
                     keyset=None):

        """Add a new interator and reset the cyclical iterator
        which iterates over the list of  iterators
        """

        if keyset is None:
            keyset = set()

        self.default_dict['iterators'].append(entrylist)
        self.iter_list_iterator = cycle(list
                                        (range
                                         (len
                                          (self.default_dict['iterators']))))
##        display.noteprint((alerts.ADDED,
##                           formkeys(entrylist)))

        iname = EMPTYCHAR
        keylist = self.return_least_keys(keyset)
        if len(keylist) > 5:
            keylist = keylist[0:5]
            
        for t_temp in keylist:
            iname += t_temp+DASH
        iname = iname[:-1]
    
        self.add_iterator_name(len(self.default_dict['iterator_names']),
                               iname)
        self.dd_changed = True

    def add_iterator_name(self,
                          number,
                          name):

        """Add a new iterator name to the list of iterator names
        according to position = number
        """

        self.default_dict['iterator_names'][number] = name
        self.dd_changed = True


    def reset_iterators(self):

        """Reset all the iterators"""

        self.default_dict['iterators'] = []
        self.default_dict['iterator_names'] = {}
        self.dd_changed = True

    def set_iterator(self,
                     entrylist=None,
                     nextiterator=False,
                     children_too=False,
                     flag=False,
                     starting=None):

        """Set the active iterator from the next iterator in the cyclically
        iterated list of iterators
        flagvalues: TRUE to show all.
                    FALSE to show min and max
        """

        if nextiterator:
            count = next(self.iter_list_iterator)
            entrylist = self.default_dict['iterators'][count]

        if entrylist is None:
            entrylist = [i_temp for i_temp in self.default_dict['indexlist_indexes'].list
                                if i_temp > Index(0)
                                and (children_too
                                     or i_temp.is_top())]
        else:
            entrylist = [Index(str(i_temp)) for i_temp in entrylist if Index(str(i_temp)) > Index(0)]

        if not entrylist:
            entrylist = [i_temp for i_temp in self.default_dict['indexlist_indexes'].list
                                if i_temp > Index(0)
                                and (children_too
                                     or i_temp.is_top())]

        self.iterator = pointerclass.Pointer(entrylist)
        if starting:
            self.iterator.go_to(starting)

        if flag or len(entrylist)<1:

            if nextiterator:
                display.noteprint((alerts.ITERATOR_RESET+'| '
                                   +rangelist.range_find(entrylist,reduce=True),
                                   self.default_dict['iterator_names'][count+1]))
            else:
                display.noteprint((alerts.ITERATOR_RESET,
                                   rangelist.range_find(entrylist,reduce=True)))

        else:

            display.noteprint((alerts.ITERATOR_RESET,
                               str(entrylist[0])+LONGDASH+str(entrylist[-1])))
            
    def show_iterators(self):

        show_note = EMPTYCHAR
        for counter in range(min([len(self.default_dict['iterators']),
                                  len(self.default_dict['iterator_names'])])):
            show_note += 'Cluster #'+str(counter+1)+' : '\
                         +self.default_dict['iterator_names'][counter]\
                         +EOL+formkeys(self.default_dict['iterators'][counter])\
                         +EOL+'/BREAK/'+EOL
            

        display.noteprint((labels.CLUSTERS,show_note))


    def softdelete(self,
                   index,
                   reverse=False,
                   withchildren=False,
                   update_table=True):

        """deletes by moving a note into negative index.
        reverse is TRUE only if the operation
        is undoing a previous operation"""

        if isinstance(index, (int, str)):
            index = Index(index)

        if not reverse and index > Index(0):
            self.move(index,
                      min(Index(self.indexes()[0])
                          -Index(1), Index(0)-Index(1)),
                      withchildren=withchildren,
                      update_table=update_table)

    def undelete(self,
                 undeletelist=None,
                 update_table=True):

        """Undoes a soft delete"""

        m_temp = iter([a_temp for a_temp
                          in range(1,len(self.indexes()*2))
                          if str(a_temp)
                          not in self.indexes()])


        # iter function is used to find free spots for the notes to be undeleted

        if undeletelist is None:
            undeletelist = [Index(x_temp)
                            for x_temp in
                            self.find_within(indexfrom=None,
                                             indexto=0)]

        for u in undeletelist:
            print(u)

            nprint(PERIOD,end=EMPTYCHAR)
            
            self.move(u,
                      Index(next(m_temp)),
                      withchildren=True,
                      update_table=update_table)
        print()

    def purge(self,
              noterange=None):

        """gets rid of  notes"""

        if noterange is None:
            noterange = [str(Index(a_temp))
                         for a_temp
                         in self.indexes()]
        for i_temp in [str(Index(n))
                       for n in self.indexes()
                       if Index(n) > Index(str(0))
                       and str(Index(n)) in noterange]:
            if (len(str(self.get_keys_from_note(i_temp))) < 5
                    and self.get_text_from_note(i_temp).replace(EOL,
                                                                 EMPTYCHAR).strip() == EMPTYCHAR):

                self.softdelete(i_temp)

    def enter(self,
              ek=None,
              et=EMPTYCHAR,
              em=None,
              query=True,
              not_parsing=True,
              show=False,
              right_at=False,
              as_child=False,
              ind=Index(0),
              re_entering=False,
              returnnote=False,
              carrying_keys=True,
              usedefaultkeys=True):

        """ For entering in new notes into the note base.
        If keyset and/or text is not passed into the function,
        imput from user is requested. query = False to skip asking
        to accept extracted keys not_parsing - True if it is not
        in the process of parsing; in this case, will call parsetext
        if there are embeded notes show - True is passed into the
        addnew function if the note is to be displayed after
        being added to the note base right_at, as_child, ind,
        reentering also passed into addnew function returnnote
        -- returns the Note, rathing then calling addnote.
        """
        projects_old = list(self.project)
        returnquit_setting = self.defaults.get('returnquiton')
        text_fed_in = False
        if et:
            self.defaults.set('returnquiton',False)
            text_fed_in = True
            
        


        def no_arrows(x_temp):

            """replaces arrow with equal sign---
            used for keys with ontological information
            """
            return x_temp.replace(RIGHTNOTE, EQUAL)
        
        def order_sequence_keys(key):
            
            """ arranges the sequence keys in the order that they should
            be queried.
            """

            if QUESTIONMARK not in key:
                return 300
            elif key not in presets.keymacro_order:
                return 200
            else:
                return presets.keymacro_order.index(key)
            
            
        
        def get_keys_from_projects():

            """ fetches sequence keys from existing projects
            """
            
            returnkeys = set()
            for project in self.project:
                if project in self.default_dict['projects'].get_all_projects():
                    returnkeys = returnkeys.union(set(self.default_dict['projects'].get_default_keys(project=project)))
            return returnkeys

        def query_keys(keysetobject=None):


            for k_temp in check_hyperlinks(self.default_dict['abbreviations'].undo(input(queries.KEYS)).split(COMMA)):
                if k_temp != EMPTYCHAR:
                    if k_temp[0] == DOLLAR:
                        keysetobject.update(self.default_dict['keymacros'].get_definition(k_temp[1:]))
                    elif k_temp[0] == PLUS and k_temp[1:] in self.default_dict['projects'].get_all_projects():
                        # to add a project
                        self.project.append(k_temp[1:])
                    elif k_temp[0] == DASH and k_temp[1:] in self.project:
                        # to remove a project 
                        self.project.pop(self.project.index(k_temp[1:]))
                    
                    else:
                        if k_temp.endswith('.'):
                            k_temp = self.keyauto.complete(k_temp.rstrip('.'))
                        keysetobject.add(k_temp)
                        self.keyauto.add(k_temp)
                        
        def sequence_keys(keysetobject=None):

            """ Queries the sequence keys with question marks in them
            """

            for k_temp in sorted(usedefaultkeys*(self.defaults.get('defaultkeys')
                                                 +list(get_keys_from_projects()))
                                 +list(keysetobject),
                                 key=lambda x:order_sequence_keys(x)):
                if (not et
                    and ATSIGN in k_temp
                    and QUESTIONMARK in k_temp):  #for sequence keywords with a question mark 
                    satisfied=False
                    while satisfied==False:

                        
                        xt_temp = self.lastsequencevalue.change(k_temp,
                                                                input(k_temp.split(QUESTIONMARK)[0]
                                                                      +self.lastsequencevalue.show(k_temp)
                                                                      +QUESTIONMARK))
                        for x_temp in xt_temp.split(COMMA):
                            x_temp = self.default_dict['abbreviations'].undo(x_temp)
                            
                        
                            if not x_temp:
                                satisfied = True
                            elif ATSIGN + POUND + QUESTIONMARK in k_temp: # for date sequences
                                    if  (SLASH not in x_temp
                                         and is_date(x_temp)) or (x_temp.count(SLASH)==1
                                                                  and is_date(x_temp.split(SLASH)[0])
                                                                  and is_date(x_temp.split(SLASH)[1])):
                                        if SLASH not in x_temp:
                                            keysetobject.add(k_temp.replace(QUESTIONMARK,x_temp))
                                            satisfied = True
                                        elif x_temp.count(SLASH) == 1 and x_temp[-1] != SLASH:
                                            keysetobject.add(k_temp.replace(ATSIGN+POUND+QUESTIONMARK,
                                                                            'from'+ATSIGN+POUND
                                                                            +x_temp.split(SLASH)[0]))
                                            keysetobject.add(k_temp.replace(ATSIGN+POUND+QUESTIONMARK,
                                                                            'to'+ATSIGN+POUND
                                                                            +x_temp.split(SLASH)[1]))
                                            satisfied = True 

                            elif x_temp.replace(PERIOD,
                                                EMPTYCHAR).replace(DASH,
                                                                   EMPTYCHAR).replace(SLASH,
                                                                                      EMPTYCHAR).isnumeric():
                                #for indexes or floating sequences
                                
                                if ATSIGN + QUESTIONMARK in k_temp:   #for floating sequences 
                                    if x_temp.count(PERIOD) <= 1 or (x_temp.count(DASH) ==1
                                                                     and x_temp.count(PERIOD) == 2):
                                        if DASH not in x_temp or (x_temp.count(DASH)==1
                                                                  and x_temp[0]==DASH):

                                            keysetobject.add(k_temp.replace(QUESTIONMARK,x_temp))
                                            satisfied = True
                                        elif x_temp.count(DASH) == 1 and x_temp[-1] != DASH and x_temp[0] != DASH:
                                            keysetobject.add(k_temp.replace(ATSIGN+QUESTIONMARK,
                                                                            'from'+ATSIGN+x_temp.split(DASH)[0]))
                                            keysetobject.add(k_temp.replace(ATSIGN+QUESTIONMARK,
                                                                            'to'+ATSIGN+x_temp.split(DASH)[1]))
                                            satisfied = True      
                                   
                                elif ATSIGN + UNDERLINE + QUESTIONMARK in k_temp:  # for index sequences 
                                    if PERIOD+PERIOD not in x_temp\
                                       and x_temp[0] != PERIOD and x_temp[-1] != PERIOD:
                                        if DASH not in x_temp or (x_temp.count(DASH)==1 and x_temp[0]==DASH):
                                            keysetobject.add(k_temp.replace(QUESTIONMARK,x_temp))
                                            satisfied = True
                                        elif x_temp.count(DASH) == 1 and x_temp[-1] != DASH and x_temp[0] != DASH:
                                            keysetobject.add(k_temp.replace(ATSIGN+UNDERLINE+QUESTIONMARK,
                                                                            'from'+ATSIGN+UNDERLINE+x_temp.split(DASH)[0]))
                                            keysetobject.add(k_temp.replace(ATSIGN+UNDERLINE+QUESTIONMARK,
                                                                            'to'+ATSIGN+UNDERLINE+x_temp.split(DASH)[1]))
                                            satisfied = True 
                                            

                            else: # for text sequences
                                
                                if x_temp.count(DASH) == 2 and DASH+DASH in x_temp and x_temp[-1] != DASH:
                                    keysetobject.add(k_temp.replace(ATSIGN+QUESTIONMARK,
                                                                    'from'+ATSIGN+x_temp.split(DASH+DASH)[0]))
                                    keysetobject.add(k_temp.replace(ATSIGN+QUESTIONMARK,
                                                                    'to'+ATSIGN+x_temp.split(DASH+DASH)[1]))
                                    satisfied = True
                                else:
                                    keysetobject.add(k_temp.replace(QUESTIONMARK,x_temp))
                                    satisfied = True
                                    
                else:
                    keysetobject.add(k_temp)
                        
        def auto_sequence_keys(keysetobject=None):

            """adds to the number for the automatic sequence keys
            """
            
            if self.project:
                for p_temp in self.project:
                    found_temp = False
                    for x_temp in range(1,10000):
                        if p_temp + ATSIGN + str(x_temp)+'.0' in self.keys():
                            found_temp = True
                            break
                    if not found_temp:

                        self.default_dict['sequences']['#TYPE#'][p_temp] = float
                        self.default_dict['sequences'][p_temp] =  OrderedList()
                        next_temp = float(input('start from?'))
                    else:
                        next_temp = self.default_dict['sequences'][p_temp].next()
                        
                        
                            
                    keysetobject.add(p_temp + ATSIGN + str(next_temp))

        #MAIN BODY OF FUNCTION BEGINS 

        from_keys = True
        keyset = set()
        if ek is None:
            from_keys = False
            
        if not et and not em and not ek and (self.defaults.get('enterhelp')\
                                             or self.defaults.get('formattinghelp')):
            display.noteprint((labels.ENTRYCOMMANDS,
                               ENTERSCRIPT*self.defaults.get('enterhelp')
                               +EOL+FORMATTINGSCRIPT*self.defaults.get('formattinghelp')),
                               param_width=60,
                              override=True)

        
        if em is None:
            em = {}
        oldtext = EMPTYCHAR
        oldkeys = set()
        if  (self.last_keys != set()
                and input(queries.RESUME_ABORTED_NOTE) in YESTERMS):
            #IF last entry was aborted ...
            oldkeys = set(self.last_keys)
            if self.entry_buffer:
                oldtext = self.entry_buffer.dump()
                self.entry_buffer.clear()
                self.last_keys = set()

        if not from_keys:
            print('<<'+nformat.format_keys(usedefaultkeys*(self.defaults.get('defaultkeys')
                                                           +list(get_keys_from_projects())))+'>>')


                        
                            

        if not from_keys and self.defaults.get('keysbefore')\
           and not self.defaults.get('fromtext'):
                query_keys(keyset)


        elif from_keys:
            keyset = ek

        keyset.update(oldkeys)
        self.last_keys = set(keyset)

        imp_list = []
        if et != EMPTYCHAR:
            imp_list = et.split(EOL)
            

            #split fed-in-text into lines

        poetry = False
        lastline = False
        editover = False
        text = EMPTYCHAR+oldtext
        counter = 1
        lasttext = EMPTYCHAR
        splitting = False
        returns_entered = 0
        poetrytoggled = False
        
        if et == EMPTYCHAR:
            print(POUND*7+self.defaults.get('size')*UNDERLINE+VERTLINE)

    
        # The following block of code enters 
        # in new text for a note line by line

        while not lastline:
##                try:
            if imp_list:
                #otherwise, pops the next line from list
                #of lines from text that has been fed in
                t_temp = imp_list.pop(0)

                
            elif et == EMPTYCHAR:
                #asks for input if text has not been fed into the function
                t_temp = input('PO '*poetry
                               +'PR '*(not poetry)
                               +str(counter)+(4-len(str(counter)))*BLANK)
                if self.defaults.get('convertbyline'):
                    if self.by_line.interpret(t_temp)[0]:
                        keyset.update(self.by_line.interpret(t_temp)[0])
                        t_temp = EMPTYCHAR

            else:
                lastline = True
                t_temp = EMPTYCHAR
  
##                except: pass

            if t_temp == PERCENTAGE+PERCENTAGE:
                # TO THE POETRY MODE WHICH INSERTS
                #A HARD RETURN AFTER EACH LINE
                poetry = True
                counter += 1
                text += EOL

            elif t_temp == PERCENTAGE:
                poetry = False  #THE PROSE MODE

            else:
                if len(t_temp)>len(t_temp.lstrip()):
                    t_temp = VERTLINE*(not poetry)\
                             + '_'*(len(t_temp)-len(t_temp.lstrip()))\
                             + t_temp.lstrip()
                if not poetry:  # prosaic text entry mode

                    counter += 1
                    if t_temp == EMPTYCHAR or len(t_temp) < 2:
                        # to automatically quit if there is a last line
                        lasttext = text
                        text += t_temp+EOL
                        returns_entered += 1
                        if self.defaults.get('returnquiton')\
                           and(len(text) > self.defaults.get('returnquit')
                               and text[-self.defaults.get('returnquit')]
                               == EOL*self.defaults.get('returnquit')):
                            lastline = True

                    elif (t_temp[-1] == PERIOD or (t_temp[-1:] == VERTLINE
                                                and (BLANK+t_temp)[-2] != VERTLINE)):
                        at_temp = t_temp[:-1]+t_temp[-1].replace(VERTLINE, EMPTYCHAR)+EOL
                        lasttext = text
                        text += at_temp
                        #if the entry line ends with |
                        #or a period, then add a break.
                        self.entry_buffer.append(at_temp)
                    elif t_temp[-1] == TILDA:   #to discard line
                          counter -= 1
                    elif t_temp[-1] == POUND:  #to replace last line with new line
                          text = EMPTYCHAR.join(text.split(EOL)[0:-2])
                          at_temp = t_temp[:-1]+t_temp[-1].replace(POUND, EMPTYCHAR)+EOL
                          lasttext = text
                          text += at_temp
                    elif t_temp[-1] == ATSIGN:  #to replace entered line with new entry
                          text = EMPTYCHAR.join(text.split(EOL)[0:-2])
                          at_temp = t_temp[:-1]+t_temp[-1].replace(ATSIGN, EMPTYCHAR)+EOL
                          lasttext = text
                          text =  lasttext + EOL + at_temp
                    elif t_temp[-1] == DOLLAR:  #to replace entered line with new entry but no EOL
                          text = EMPTYCHAR.join(text.split(EOL)[0:-2])
                          at_temp = t_temp[:-1]+t_temp[-1].replace(DOLLAR, EMPTYCHAR)+EOL
                          lasttext = text
                          text =  lasttext + at_temp                   
                
                    else:
                        if len(t_temp) <= 1 or  t_temp[-2] != VERTLINE:
                            at_temp = (t_temp.replace
                                       (string.whitespace[1], BLANK)+BLANK)
                            lasttext = text
                            text += at_temp
                            #if a simple return, then no break
                            self.entry_buffer.append(at_temp)
                        elif not text_fed_in and (len(t_temp) >2
                                                  and  t_temp[-3] == TILDA): #to edit
                            at_temp = (t_temp[:-2].replace
                                       (string.whitespace[1:], BLANK)+EOL)
                            lasttext = text
                            text += at_temp
                            # if || then finish entry
                            self.entry_buffer.append(at_temp)
                            lastline = True
                            editover = True
                            
                        elif not text_fed_in and (len(t_temp) <3
                                                  or t_temp[-3] != VERTLINE):
                            at_temp = (t_temp[:-2].replace
                                       (string.whitespace[1:], BLANK)+EOL)
                            lasttext = text
                            text += at_temp
                            # if || then finish entry
                            self.entry_buffer.append(at_temp)
                            lastline = True

                        elif not text_fed_in:
                            at_temp = (t_temp[:-2].replace
                                       (string.whitespace[1:],
                                        BLANK)+EOL)
                            lasttext = text
                            text += at_temp
                            # if || then finish entry
                            self.entry_buffer.append(at_temp)
                            lastline = True
                            splitting = True 
                            
                            

                if poetry:
                    poetrytoggled = True
                    counter += 1
                    if t_temp == EMPTYCHAR or len(t_temp) < 2:
                        at_temp = t_temp+EOL
                        lasttext = text
                        text += at_temp
                        self.entry_buffer.append(at_temp)

                    elif t_temp[-1:] == VERTLINE and (BLANK+t_temp)[-2] != VERTLINE:
                        at_temp = (t_temp.replace
                                   (string.whitespace[1:], BLANK)[:-1]+BLANK)
                        lasttext = text
                        text += at_temp
                        self.entry_buffer.append(at_temp)

                    else:
                        if len(t_temp) <= 1 or t_temp[-2] != VERTLINE:
                            at_temp = t_temp+EOL
                            lasttext = text
                            text += at_temp
                            self.entry_buffer.append(at_temp)
                        elif len(t_temp) <= 2 or t_temp[-3] != VERTLINE :
                            at_temp = (t_temp[:-2].replace
                                       (string.whitespace[1:],
                                        BLANK)+EOL)
                            lasttext = text
                            text += at_temp
                            self.entry_buffer.append(at_temp)
                            lastline = True
                            ##text = text.replace(VERTLINE, EOL+BLANK)  WHY IS THIS HERE?
                        else:
                            at_temp = (t_temp[:-2].replace
                                       (string.whitespace[1:],
                                        BLANK)+EOL)
                            lasttext = text
                            text += at_temp
                            self.entry_buffer.append(at_temp)
                            lastline = True
                            splitting = True 

        
        if len(text) > 1 and text[-2:] == VERTLINE + VERTLINE:
            text = text[0:-2]

        if self.abridgedformat:
            text = text.replace('///','/NEW/')
            text = text.replace('//','/BREAK/')

        text = text.replace('/BREAK/',VERTLINE+'/BREAK/'+VERTLINE)
        text = text.replace('/NEW/',VERTLINE+'/NEW/'+VERTLINE)
        
        text = text.replace(VERTLINE, EOL)
        if splitting and '/M/' in text:
            text = '/SPLIT/'+EOL+text+EOL+'/ENDSPLIT/'
        if self.check_spelling:
            text, added = self.speller.checktext(text)
            self.default_dict['spelling'].update(added)

            
        if editover:
            text = textedit_new(text)
        text = reform_text(text)
        text = self.default_dict['abbreviations'].do(text)
        text = self.default_dict['macros'].do(text)
        self.dd_changed = True
        

##        else:
##            text = et

        knowledgephrases = [self.default_dict['abbreviations'].undo(x_temp)
                            for x_temp in extract.extract(text,
                                                          LEFTCURLY + LEFTCURLY,
                                                          RIGHTCURLY + RIGHTCURLY)]

        # extract knowledge phrases embedded within text

        if query:

            for kp_temp in knowledgephrases:

                interpreted = self.default_dict['generalknowledge'].text_interpret(kp_temp)

                display.noteprint((interpreted[0],interpreted[1]))
                
                text = text.replace(LEFTCURLY+LEFTCURLY+kp_temp+RIGHTCURLY+RIGHTCURLY,
                                    LEFTCURLY+LEFTCURLY
                                    +interpreted[1].replace('\n','; ').rstrip(';')
                                    +RIGHTCURLY+RIGHTCURLY)
                
                                    
        text = text.replace(LEFTCURLY + LEFTCURLY, '@@DCL@@')
        text = text.replace(RIGHTCURLY + RIGHTCURLY, '@@DCR@@')

        newkeylist = [self.default_dict['abbreviations'].undo(x_temp)
                      for x_temp
                      in extract.extract(text,
                                         LEFTCURLY,
                                         RIGHTCURLY)]
        text = text.replace('@@DCL@@',LEFTCURLY
                            + LEFTCURLY)
        text = text.replace('@@DCR@@',RIGHTCURLY
                            + RIGHTCURLY)

        
        #extract keywords embedded within text

        if query:
            #if query = True then ask if
            #the new keywords extracted from text are to be kept

            for a_temp in newkeylist:
                print(newkeylist.index(a_temp), EQUAL, a_temp)

            if newkeylist:
                it_temp = input(queries.NEW_KEY_LIST)
                if it_temp in NOTERMS:
                    newkeylist = []
                if it_temp in YESTERMS+[BLANK]:
                    pass
                else:
                    newkeylist = [k_temp for k_temp in newkeylist
                                  if newkeylist.index(k_temp)
                                  in rangelist.range_set(it_temp)]
                display.noteprint((alerts.ATTENTION,
                                   ', '.join(newkeylist)
                                   + alerts.ADDED_TO_KEYLIST))
                

        keyset.update(set(newkeylist))
##        print(', '.join(keyset))
        #add new kewords to existing set of keywords





        
        if not from_keys and self.defaults.get('keysafter') and not self.defaults.get('fromtext'):
             query_keys(keyset)


        old_fromtext = self.defaults.get('fromtext')  # Save old settings
        old_mode = self.defaults.get('convertmode')
        
        if '//' in text and '//' in text:
            mode = text.split('//')[1].split('//')[0]
            if mode in self.default_dict['convert']:
                self.defaults.set('convertmode',mode)
            display.noteprint(('MODE',self.defaults.get('convertmode')))
            self.defaults.set('fromtext',True)
            text = text.replace('//'+mode+'//',EMPTYCHAR)
      
        if self.defaults.get('fromtext') and not self.defaults.get('convertbyline'):
            conv_keys, text = self.default_dict['convert'][self.defaults.get('convertmode')].interpret(text)
            text = reform_text(text)
            text = self.default_dict['abbreviations'].do(text)
            text = self.default_dict['macros'].do(text)
            keyset.update(conv_keys)



   
        auto_sequence_keys(keysetobject=keyset) # calls function to add autonomatically numbered sequence keys 
        sequence_keys(keysetobject=keyset)# calls function to evaluate sequence keys if they exist
        
        if (not from_keys    # use old keys if new keys are not to be queried or taken from the text
            and not self.defaults.get('keysbefore')
            and not self.defaults.get('keysafter')):
            keyset.update(oldkeys)

        keyset = {k_temp for k_temp in keyset
                  if len(k_temp) > 1
                  and k_temp[-1]
                  not in [QUESTIONMARK, POUND, ATSIGN, UNDERLINE]}
        keyset = modify_keys(keyset, no_arrows, strip=True)
        keyset = modify_keys(keyset, self.default_dict['macros'].do)



        if em == {}:
            if not poetrytoggled:
                metatext = {'user': self.defaults.get('user'),
                            'size': self.defaults.get('size'),
                            'date': [str(datetime.datetime.now())]}
            else:
                temp_size = max([len(x_temp)+20 for x_temp in text.split(EOL)])
                metatext = {'user': self.defaults.get('user'),
                            'size': temp_size,
                            'date': [str(datetime.datetime.now())]}
            

        else:
            metatext = em
        if self.autobackup:
            self.update(keyset,
                        self.default_dict['abbreviations'].undo(text),
                        meta=metatext,
                        right_at=right_at,
                        as_child=as_child)
                        #call autobackup

        if returnnote:

            return Note(keyset,
                        self.default_dict['abbreviations'].undo(text),
                        metatext)

        if not_parsing and extract.embedded_extract(text)[2] > 0:
            #call parsing if there are embedded notes,
            #and it is not already in the middle of parsing

            next_index = Index(int(ind))+Index(1)
            self.textparse(self.default_dict['abbreviations'].undo(text),
                           keys=keyset,
                           newindex=next_index)
            index = self.addnew(keyset,
                                extract.embedded_extract
                                (self.default_dict['abbreviations'].undo(text),
                                 eliminate=True)[1],
                                metadata=metatext,
                                show=True,
                                right_at=right_at,
                                as_child=as_child,
                                re_entering=re_entering,
                                ind=ind,
                                carrying_keys=carrying_keys)
            
        else:

            index = self.addnew(keyset,
                                self.default_dict['abbreviations'].undo(text),
                                metadata=metatext,
                                show=show,
                                right_at=right_at,
                                as_child=as_child,
                                ind=ind,
                                re_entering=re_entering,
                                carrying_keys=carrying_keys)

        self.entry_buffer.clear()
        self.last_keys = set()
        # restore old settings
        self.defaults.set('fromtext',old_fromtext)
        self.defaults.set('convertmode',old_mode)
        self.defaults.set('returnquiton',returnquit_setting)
        if isinstance(projects_old,list):
            self.project = projects_old

        return index

    def ldisplay(self,
                 indexlist):

        """display a list"""

        for i_temp in sorted(list(set(indexlist))):
            display.noteprint(self.show(i_temp),
                              param_width=self.defaults.get('size'))

    def show_project_dates (self,
                            entrylist=None,
                            determinant='ymd',
                            dictionaryobject=None):

        """ makes a dictionary of the dates in projects
        """

        if not dictionaryobject:
            if 'PROJ'+determinant not in self.default_dict['date_dict']:
                self.default_dict['date_dict']['PROJ'+determinant] = {}
            dictionaryobject = self.default_dict['date_dict']['PROJ'+determinant]
            self.default_dict['date_dict']['PROJ'+determinant].clear()


        if entrylist is None:

            entrylist = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))
            indexrange=False
        else:
            indexrange=True
            entryset = set(entrylist)
        
            

        for project_temp in self.default_dict['projects'].get_all_projects():
            dates_temp = self.default_dict['projects'].get_date_list(project=project_temp)
            dates_temp = {clip_date(d_temp,determinant) for d_temp in dates_temp}
            for date in dates_temp:
                if date not in dictionaryobject:
                    dictionaryobject[date] = set()
                if not indexrange:
                    dictionaryobject[date].add(project_temp)
                else:
                    if entryset.intersection({str(x_temp)
                                              for x_temp
                                              in self.default_dict['projects'].get_all_indexes(project=project_temp)}):
                        dictionaryobject[date].add(project_temp)

    def find_dates_for_keys_in_indexes (self,
                                        entrylist=None,
                                        flag='o',
                                        determinant='ym',
                                        dictionaryobject=None):
        """ flag value. 'f' first date, 'n' newest date, 'a' all dates
            'i' show indexes 
        """ 

        oldest = False
        newest = False
        alldates = False
        showindexes = False

        if not dictionaryobject:
            if determinant not in self.default_dict['date_dict']:
                self.default_dict['date_dict'][determinant] = {}
            dictionaryobject = self.default_dict['date_dict'][determinant]


        showindexes = 'i' in flag
        alldates = 'a' in flag
        newest = 'n' in flag or not alldates


        if entrylist is None:

            entrylist = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))
##            entrylist = self.apply_limit([str(Index(a_temp))
##                                          for a_temp in self.indexes()
##                                          if Index(a_temp) > Index(str(0))])
            # if entrylist is , default to all notes, with limit applied.

        for index in entrylist:
            


            if not isinstance(index,str):
                index = str(index)
            suffix = EMPTYCHAR
            if showindexes:
                suffix = SLASH + index
            if alldates:
                dates = self.get_note(index).alldates()
            else:
                dates = {self.get_note(index).date(most_recent=newest)}

            dates = {clip_date(d_temp,determinant) + suffix for d_temp in dates}


            for date in dates:


                if date not in dictionaryobject:
                    dictionaryobject[date]=self.get_keys_from_note(index)
                else:
                    dictionaryobject[date].update(self.get_keys_from_note(index))

    def reconstitute_sequences(self,
                               entrylist=None):

        """ Reconstitutes sequences """
        if input('Clear sequences?') in YESTERMS and input('Are you sure?') in YESTERMS:

            del self.default_dict['sequences']
            self.default_dict['sequences'] = {}
            self.default_dict['sequences']['#TYPE#'] = {}
            nprint('Sequences purged!')

            

        if entrylist is None:

            entrylist = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))

        sequencedictionary = {'o':{},
                              'd':{},
                              'i':{}}
        
        for entry in entrylist:
            if self.notebook_contains(entry):
                temp_keys = self.get_keys_from_note(entry)
                for key in temp_keys:
                    if ATSIGN in key:
                        if ATSIGN + UNDERLINE in key:
                            identifier = key.split(ATSIGN)[0]
                            if identifier not in sequencedictionary['i']:
                                sequencedictionary['i'][identifier] = {key.split(ATSIGN+UNDERLINE)[1]}
                            else:
                                sequencedictionary['i'][identifier].add(key.split(ATSIGN+UNDERLINE)[1])
                        elif ATSIGN + POUND in key:
                            identifier = key.split(ATSIGN)[0]
                            if identifier not in sequencedictionary['d']:
                                sequencedictionary['d'][identifier] = {key.split(ATSIGN+POUND)[1]}
                                
                            else:
                                sequencedictionary['d'][identifier].add(key.split(ATSIGN+POUND)[1])
                        else:
                            identifier = key.split(ATSIGN)[0]
                            if identifier not in sequencedictionary['o']:
                                sequencedictionary['o'][identifier] = {key.split(ATSIGN)[1]}
                                
                            else:
                                sequencedictionary['o'][identifier].add(key.split(ATSIGN)[1])
            print(PERIOD,end=EMPTYCHAR)
        print()

                                
        for identifier in set(sequencedictionary['o'].keys())\
            .union(set(sequencedictionary['d'].keys()))\
            .union(set(sequencedictionary['i'].keys())):

            if identifier in sequencedictionary['o']:
            
                if identifier not in sequencedictionary['d'] and identifier not in sequencedictionary['i']:

                    all_float = True
                    for x_temp in sequencedictionary['o'][identifier]:
                        if (x_temp.count(PERIOD)>1
                            or x_temp[-1]==PERIOD
                            or not x_temp.replace(PERIOD,EMPTYCHAR).isnumeric()):
                            all_float = False
                    if all_float:
                        seq_type = float
                    else:
                        seq_type = str


                elif (identifier in sequencedictionary['d']
                      and identifier not in sequencedictionary['i']):
                    nprint('Sequence '+identifier+' is inconsistent!')
                    if input('Date sequence?') in YESTERMS:
                        seq_type = type(datetime.date(1970,5,17))
                    else:
                        seq_type = str

                elif (identifier in sequencedictionary['i']
                      and identifier not in sequencedictionary['d']):
                    nprint('Sequence '+identifier+' is inconsistent!')
                    if input('Index sequence?') in YESTERMS:
                        seq_type = type(Index(0))
                    else:
                        seq_type = str
                else:
                    nprint('Sequence '+identifier+' is inconsistent!')
                    entry_temp = input('Date or Index or Float')
                    if entry_temp:
                        entry_temp = entry_temp[0].lower()
                    if entry_temp == 'i':
                        seq_type = type(Index(0))
                    elif entry_temp == 'd':
                        seq_type = type(datetime.date(1970,5,17))
                    elif entry_temp == 'f':
                        seq_type = float
                    else:
                        seq_type = str

            elif identifier in sequencedictionary['d']:
                if identifier not in sequencedictionary['i']: 
                    seq_type = type(datetime.date(1970,5,17))
                else:
                    nprint('Sequence '+identifier+' is inconsistent!')
                    entry_temp = input('Date or Index')
                    if entry_temp:
                        entry_temp = entry_temp[0].lower()
                    if entry_temp == 'i':
                        seq_type = type(Index(0))
                    else:
                        seq_type = type(datetime.date(1970,5,17))

                    
                    

            else:
                seq_type = type(Index(0))

            seq_values = set()
            for t_temp in ['o','i','d']:
                if identifier in sequencedictionary[t_temp]:
                    seq_values = seq_values.union(sequencedictionary[t_temp][identifier])

                
            for seq_value in seq_values:
                if seq_type != str:
                    if seq_type == float:
                        seq_value = float(seq_value)
                    if seq_type == type(datetime.date(1970,5,17)):
                        if BLANK in seq_value:
                            seq_value = seq_value.split(BLANK)[0]
                        if DASH not in seq_value:
                            seq_value += '-01-01'
                        try:
                            seq_value = is_date(seq_value,returndate=True,maxlen=3)
                        except:
                            nprint('DATE CONVERSION ERROR')
                            seq_value = False
                    if seq_type == type(Index(0)):
                        if seq_value[0] != PERIOD and seq_value[-1] != PERIOD\
                           and PERIOD+PERIOD not in seq_value \
                           and seq_value.replace(PERIOD,EMPTYCHAR).isnumeric():
                            seq_value = Index(seq_value)
                        else:
                            seq_value = False


                        
                    
                if seq_value and not isinstance(seq_value,bool):
                    if identifier not in self.default_dict['sequences']:

                        if identifier not in self.default_dict['sequences']['#TYPE#']:
                            self.default_dict['sequences']['#TYPE#'][identifier] = seq_type
                            display.noteprint((alerts.ATTENTION,alerts.NEW_SEQUENCE+str(seq_type)))
                        else:
                            del self.default_dict['sequences']['#TYPE#'][identifier]
                            self.default_dict['sequences']['#TYPE#'][identifier] = type(seq_value)
                            display.noteprint((alerts.ATTENTION,alerts.OVERWRITTEN+str(seq_type)))
                        self.default_dict['sequences'][identifier] = OrderedList()
                        try:
                            self.default_dict['sequences'][identifier].add(seq_value)
                        except:
                            nprint('SEQUENCE ERROR')

                                            

                    else:
                        if seq_type == self.default_dict['sequences']['#TYPE#'][identifier]:
                            try:
                                self.default_dict['sequences'][identifier].add(seq_value)                       
                            except:
                                nprint('SEQUENCE ERROR')

            print(PERIOD,end=EMPTYCHAR)
        print()
                        
    def find_projects (self,query=True):

        found_projects = set()

        for identifier in self.default_dict['sequences']['#TYPE#']:
            is_project = False
            if self.default_dict['sequences']['#TYPE#'][identifier] == float:
                if 'page' not in identifier:
                    if identifier in self.default_dict['sequences']:
                        lowest = self.default_dict['sequences'][identifier].list[0]
                        highest = self.default_dict['sequences'][identifier].list[-1]
                        try:
                            lowest = float(lowest)
                            highest = float(highest)
                        except:
                            pass
                        if isinstance(lowest,float) and isinstance(highest,float):
                                
                            length = len(self.default_dict['sequences'][identifier])

                            if highest-lowest + 1 == length:
                                is_project = True
                            else:
                                if abs(((highest-lowest + 1) / length - 1)) < .1:
                                    is_project = True
                                elif abs(((highest-lowest + 1) / length - 1)) < .3:
                                        nprint(identifier)
                                        nprint(', '.join([str(x_temp)
                                                          for x_temp
                                                          in self.default_dict['sequences'][identifier].list]))
                                        if not query or input('Is this a project?') in YESTERMS:
                                            is_project = True
                                else:
                                    pass
                        else:
                            pass
                    if is_project:
                        found_projects.add(identifier)

        return found_projects

    def get_project (self,identifier):
        
        if identifier in self.default_dict['sequences']:

            found_indexes = set()
            for x_temp in self.default_dict['sequences'][identifier].list:
                key_temp = identifier+ATSIGN+str(x_temp)
                if  self.key_dict_contains(key_temp):
                    found_indexes.update(self.get_indexes_for_key(key_temp))
            found_indexes = list(found_indexes)
            found_indexes.sort(key=lambda x_temp:Index(x_temp))
            return_dict = {}

            if found_indexes:
                return_dict['indexes'] = OrderedList(found_indexes)
                return_dict['position'] = (Index(found_indexes[-1]),Index(found_indexes[-1]))
                return_dict['going'] = (EMPTYCHAR,EMPTYCHAR)
                return_dict['status'] = {}
                return_dict['status']['started'] = datetime.datetime.now()
                return_dict['status']['open'] = False
                return_dict['status']['lastmodified'] = []
                
                found_dates = set()
                for x_temp in found_indexes:

                    if self.notebook_contains(x_temp):
                        found_dates.update(set(self.get_metadata_from_note(x_temp)['date']))
                dates_temp = sorted([str(y_temp) for y_temp in found_dates])
                if dates_temp:
                    return_dict['date']= [dates_temp[0],dates_temp[-1]]
                else:
                    return_dict['date'] = []
                found_keys = set()
                first = True
                for x_temp in found_indexes:
                    if first:
                        found_keys = {y_temp for y_temp
                                      in self.get_keys_from_note(x_temp)
                                      if ATSIGN not in y_temp}\
                                     .union({y_temp.split(ATSIGN)[0]+ATSIGN+QUESTIONMARK
                                             for y_temp in self.get_keys_from_note(x_temp)
                                             if ATSIGN in y_temp and y_temp.split(ATSIGN)[0] != identifier})
                        first = False
                    else:
                        found_keys_new = {y_temp for y_temp
                                          in self.get_keys_from_note(x_temp)
                                          if ATSIGN not in y_temp}\
                                         .union({y_temp.split(ATSIGN)[0]+ATSIGN+QUESTIONMARK
                                                 for y_temp in self.get_keys_from_note(x_temp)
                                                 if ATSIGN in y_temp and y_temp.split(ATSIGN)[0] != identifier})
                        found_keys = found_keys.intersection(found_keys_new)
                return_dict['defaultkeys'] = list(found_keys)
                
                
                    
                    
                    

                
        return return_dict


    def restore_project(self,project,query=True):
        

        if project in self.default_dict['projects'].get_all_projects():
            if not query or input('Delete '+project+ '?') in YESTERMS :                    
                self.default_dict['projects'].delete_project(project)
            self.default_dict['projects'].set_project(project=project,
                                                     project_dict=self.get_project(project))
            nprint(project,' ERASED AND RESTORED!')
            
        else:
            self.default_dict['projects'].set_project(project=project,
                                                     project_dict=self.get_project(project))
            nprint(project,' RESTORED!')

    def restore_projects(self,query=True):
            

        for fp_temp in self.find_projects(query=query):
            self.restore_project(fp_temp,query=query)
       
    def show_date_dictionary (self,
                              dictionaryobject=None,
                              determinant='ym',
                              func=dummy,
                              prefix=EMPTYCHAR):

        """ Takes a date-dictionary and displays it
            The date-dictionary has dates for keys, and contains
            a list of keywords or other info as values
        """

        if not dictionaryobject:
            if prefix+determinant not in self.default_dict['date_dict']:
                self.default_dict['date_dict'][prefix+determinant] = {}
            dictionaryobject = self.default_dict['date_dict'][prefix+determinant]


        def dformat (x_temp):
            i_temp = EMPTYCHAR
            xx_temp = x_temp
            x_temp = x_temp.split(SLASH)
            if len(x_temp)>1:
                i_temp = x_temp[1]
            x_temp = x_temp[0]
            
            
            keys = formkeys(func(dictionaryobject[xx_temp])).replace(UNDERLINE,BLANK)
            if 'VOID' in keys:
                return None
            if len(keys) < 20:
                return (x_temp+VERTLINE+keys+VERTLINE+i_temp)

            returnlist = []
            sp_temp = split_up_string(keys)
            returnlist.append(x_temp+VERTLINE+sp_temp[0]+VERTLINE+i_temp)
            for s_temp in sp_temp[1:]:
                returnlist.append(VERTLINE+s_temp+BLANK)
            return returnlist

        all_dates = sorted(list(dictionaryobject.keys()))


        show_list(all_dates,
                  alerts.KEYS_FOR_DATES,0,40,
                  func=dformat,present=True,
                  compactwidth=(0,90,5))

        
    def get_indexes(self,
                    childrentoo=True,
                    levels=0):

        """ gets all  positive-valued indexes in the notebook
            For only top-level notes, childrentoo False.
            For all level notes, childrentoo True, levels=0
        """

        if childrentoo:
            if levels==0:
                entrylist = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))
                # if entrylist is , default to all notes, with limit applied.

            else:
                entrylist = self.apply_limit([a_temp for a_temp in self.indexes()
                                              if Index(a_temp) > Index(str(0))
                                              and Index(a_temp).level()<=levels])
        
        else:
            entrylist = self.apply_limit([a_temp for a_temp in self.indexes()
                                          if Index(a_temp) > Index(str(0))
                                          and Index(a_temp).is_top()])

        return entrylist
    

            

    def showall(self,
                entrylist=None,
                multi=False,
                output=None,
                vary=False,
                highlight=None,
                shortshow=None,
                show_date=False,
                quick=False,
                childrentoo=False,
                levels=0,
                alternateobject=None,
                header=EMPTYCHAR,
                brackets=True,
                curtail=0,
                groupsize=None):
        
        if not groupsize:
            groupsize = self.how_many

        """ shows a group of notes"""


        if not quick and shortshow:
            self.buf_abr_depth = self.abr_maxdepth_found
            self.abr_maxdepth_found = self.deepest(entrylist=entrylist,
                                                   is_string=True,
                                                   abridged=True)


        def xformat (x_temp):

            return (x_temp)

        if quick and not entrylist and self.indexchanges < 20:
            show_list(self.default_dict['all'],
                      'INDEXES',0,40,
                      func=xformat,
                      present=True)

        else:
            if self.indexchanges == 20:
                self.indexchanges = 0

            if highlight is None:
                highlight = set()

            if isinstance(entrylist, set):
                entrylist = list(entrylist)

            if entrylist is None:
                entrylist = self.get_indexes(childrentoo=childrentoo,
                                             levels=levels)
              
                    
            
            if entrylist and not isinstance(entrylist[0], str):
                entrylist = [str(a_temp) for a_temp in entrylist]

            

 
            if shortshow is None:
                shortform =  (self.shortshow
                              or len(entrylist) > self.longmax)\
                              and len(entrylist)!=1
            else:
                shortform = shortshow

            if not multi and shortshow:
               
                if 'display' in self.default_dict:
                    del self.default_dict['display']
                    self.dd_changed = True
                    

                self.default_dict['display'] = DisplayList(displayobject=display)


            lastcounter = 0
    ##        if shortform:
    ##            display.noteprint(('ATTENTION!', 'Please wait a moment!'))

            if quick:
                self.default_dict['all'] = []
                self.dd_changed = True

            deepest_temp = self.deepest(is_string=True,abridged=True,always=True)
            total_length_temp = len(entrylist)
            lastgroup=-1

            if not self.defaults.get('sortbydate'):

                to_enumerate =  [x_temp for x_temp
                                 in self.default_dict['indexlist_indexes'].list
                                 if str(x_temp) in entrylist]
            else:
                to_enumerate = self.index_sort([Index(a_temp)
                                                         for a_temp in entrylist],
                                                             by_date=self.defaults.get('sortbydate'),
                                               quick=False,
                                               no_check=False)


            for counter, i_temp in enumerate(to_enumerate):
                
                group, remainder = divmod(counter,groupsize)
                min_temp = group * groupsize
                max_temp = min([(group+1)*groupsize,total_length_temp])
 
                try:


                    if group> lastgroup:
                        deepest_temp = self.deepest(to_enumerate[min_temp:max_temp],
                                                    is_string=True,
                                                    abridged=True,
                                                    always=True)
                        lastgroup = group

                    if quick:


                        ind_temp = index_reduce(str(i_temp)) 
                        k_temp = formkeys(self.get_keys_from_note(i_temp))
                        k_temp = k_temp[0:min([len(k_temp),30])]
                        t_temp = self.get_text_from_note(i_temp)
                        t_temp = nformat.purgeformatting(t_temp[0:min([len(t_temp),40])])
                        t_temp = t_temp.replace(VERTLINE,EMPTYCHAR)\
                                 .replace(UNDERLINE,EMPTYCHAR)\
                                 .replace(EOL,EMPTYCHAR)
                        d_temp = self.get_note(i_temp).date(most_recent=True,
                                                                      short=True,
                                                                      convert=False)

                        
                        self.default_dict['all'].append(ind_temp+self.mark(str(i_temp))
                                                        +VERTLINE+d_temp
                                                        +VERTLINE+k_temp
                                                        +VERTLINE+t_temp)
                        self.dd_changed = True
                        
                                                        

                        

                    elif not multi:


                        # Not automulti, but variable size

                        if self.default_dict['variablesize']:

                            if not shortshow:

                                self.text_result += \
                                                 display.noteprint(self.show(i_temp, shortform=shortform,
                                                                           yestags=self.tagdefault,
                                                                           highlight=highlight,
                                                                           show_date=show_date),
                                                                          param_width=display.width_needed(
                                                                              self.show(i_temp,
                                                                                        shortform=shortform,
                                                                                        yestags=self.tagdefault,
                                                                                        highlight=highlight,
                                                                                        show_date=show_date),
                                                                              self.get_metadata_from_note(i_temp)['size'],
                                                                              leftmargin=self.defaults.get('leftmargin')),
                                                                          np_temp=shortform,
                                                                          leftmargin=self.defaults.get('leftmargin'),
                                                                                  brackets=brackets)
                                
                            else:
                                
                                self.default_dict['display'].append(display.noteprint(self.show
                                                                              (i_temp, shortform=shortform,
                                                                               yestags=self.tagdefault,
                                                                               highlight=highlight,
                                                                               show_date=show_date,
                                                                               deepest=deepest_temp),
                                                                              param_width=display.width_needed(
                                                                                  self.show(i_temp,
                                                                                            shortform=shortform,
                                                                                            yestags=self.tagdefault,
                                                                                            highlight=highlight,
                                                                                            show_date=show_date,deepest=deepest_temp),
                                                                                  self.get_metadata_from_note(i_temp)['size'],
                                                                                  leftmargin=self.defaults.get('leftmargin')),
                                                                              np_temp=shortform,
                                                                              leftmargin=self.defaults.get('leftmargin'),
                                                                                      brackets=brackets))
                                self.dd_changed = True

                        # not automulti, not variable size
                        else:
                            if not shortshow:
                                self.text_result +=  \
                                                 display.noteprint(self.show(i_temp,
                                                            shortform=shortform,
                                                            yestags=self.tagdefault,
                                                            show_date=show_date),
                                                                   param_width=self.defaults.get('size'),
                                                                   np_temp=shortform,
                                                                   leftmargin=self.defaults.get('leftmargin'),
                                                                   brackets=brackets)
                            else:
                                self.default_dict['display'].append(display.noteprint(self.show(i_temp,
                                                                shortform=shortform,
                                                                yestags=self.tagdefault,
                                                                show_date=show_date,deepest=deepest_temp),
                                                      param_width=self.defaults.get('size'),
                                                      np_temp=shortform,
                                                      leftmargin=self.defaults.get('leftmargin'),
                                                                                      brackets=brackets))
                                self.dd_changed = True




                    elif multi:

                        if not vary:

                            if self.default_dict['variablesize']:
                                output.load(
                                    display.noteprint(self.show(i_temp,
                                                                yestags=self.tagdefault,
                                                                show_date=show_date,curtail=curtail),
                                                      np_temp=True,
                                                      param_width=display.width_needed
                                                      (self.show(i_temp,
                                                                 yestags=self.tagdefault,
                                                                 show_date=show_date,
                                                                 curtail=curtail),
                                                       self.get_metadata_from_note(i_temp)['size'],
                                                       leftmargin=self.default_dict['leftmargin']),
                                                      leftmargin=self.default_dict['leftmargin'],
                                                      brackets=brackets))
                            else:
                                output.load(display.noteprint
                                            (self.show(i_temp,
                                                       yestags=self.tagdefault,
                                                       show_date=show_date,curtail=curtail),
                                             np_temp=True,
                                             param_width=self.default_dict['size'],
                                             leftmargin=self.default_dict['leftmargin'],
                                             brackets=brackets))

                        else:

                            if self.default_dict['variablesize']:
                                output.load(display.noteprint
                                            (self.show(i_temp,
                                                       yestags=self.tagdefault,
                                                       show_date=show_date,
                                                       curtail=curtail),
                                             np_temp=True,
                                             param_width=display.width_needed
                                             (self.show(i_temp,
                                                        yestags=self.tagdefault,
                                                        show_date=show_date,
                                                        curtail=curtail),
                                              p_width=max([int
                                                           (math.sqrt
                                                            (len
                                                             (self.show(i_temp,
                                                                        yestags=self.tagdefault,
                                                                        show_date=show_date,
                                                                        curtail=curtail)[1]))),20])),
                                             leftmargin=self.default_dict['leftmargin'],
                                             brackets=brackets))
                            else:

                                output.load(display.noteprint(self.show
                                                              (i_temp, yestags=self.tagdefault,
                                                               show_date=show_date),
                                                              np_temp=True,
                                                              param_width=max([int
                                                                               (math.sqrt(
                                                                                   len(self.show(
                                                                                       i_temp,
                                                                                       yestags=self.tagdefault,
                                                                                       show_date=show_date)[1]))), 20]),
                                                              leftmargin=self.default_dict['leftmargin'],
                                                              brackets=brackets,
                                                              curtail=curtail))
                except:
                    display.noteprint((alerts.ATTENTION,'cannot show '+str(i_temp)))

            if not quick and shortform and not multi:

                if not header:
                    self.text_result = self.default_dict['display']\
                                       .present(dump=True,
                                                howmany=self.how_many)
                else:
                    self.text_result = self.default_dict['display']\
                                       .present(header=header,
                                                dump=True,
                                                howmany=self.how_many)
            if quick:

                show_list(self.default_dict['all'],
                          'INDEXES',0,40,
                          func=xformat,present=True)
            if not quick and shortshow:
                self.abr_maxdepth_found = self.buf_abr_depth
               

    def showall_incremental (self,
                             entrylist=None,
                             highlight=None,
                             childrentoo=True,
                             levels=0,
                             index=None,
                             beforeafter=10):

        """ shows only a single group of notes, rather than all notes at once.
            The regular show-all is quite quick, so this is probably no longer necesary
        """

        

        if entrylist is None:

            if not self.default_dict['sortbydate']:
                entrylist = self.default_dict['indexlist_indexes'].list
            else:
                entrylist = self.default_dict['indexlist_indexes'].list
                entrylist = self.index_sort([Index(a_temp)
                                             for a_temp
                                             in entrylist],
                                            by_date=self.default_dict['sortbydate'],quick=True)

        else:
            entrylist = self.index_sort([Index(a_temp)
                                         for a_temp
                                         in entrylist],
                                        by_date=self.default_dict['sortbydate'],quick=False)



        if not isinstance(entrylist[0], str):
            entrylist = [str(a_temp) for a_temp in entrylist]
        
        keep_on = True
        inp_temp = EMPTYCHAR
        while keep_on:
    
        
            if index is None:
                index = entrylist[0]

            if index in entrylist:
                
                indexpoint = entrylist.index(index) # index is the index of the note
            else:
                indexpoint = 0
            begin_point = max([0,indexpoint-beforeafter])
            end_point = min([len(entrylist)-1,indexpoint+beforeafter])

            segment = entrylist[begin_point:end_point]

            inc_displaylist = DisplayList (displayobject=display)
            header_temp = str(segment[0]) + LONGDASH + str(segment[-1])

            self.showall(entrylist=segment,
                         highlight=highlight,
                         childrentoo=childrentoo,
                         levels=levels,
                         shortshow=True,
                         multi=False,
                         quick=False,
                         header=header_temp)
            
            if not inp_temp:
                inp_temp = input(queries.MENU_ONE+BLANK)
            if inp_temp[0].lower() == 'q':
                inp_temp = EMPTYCHAR
            if inp_temp:
                if inp_temp[0] == '>':

                    index = segment[-1]
                elif inp_temp[0] == '<':
                    index = segment[0]
                elif inp_temp[0] == '[':
                    index = entrylist[0]
                elif inp_temp[0] == ']':
                    index = entrylist[-1]
                inp_temp = inp_temp[1:]
                
            else:
                keep_on = False
                              

    def child_show(self,
                   entrylist=None,
                   highlight=None,
                   not_all=False):

        """ shows a group of notes with their children"""

        if highlight is None:
            highlight = set()
        if entrylist is None and not not_all:
            entrylist = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))
##            entrylist = self.apply_limit([a_temp for a_temp
##                                          in sorted([str(Index(a_temp))
##                                                     for a_temp in self.indexes()
##                                                     if Index(a_temp) > Index(str(0))],
##                                                    key=lambda x_temp: Index(x_temp))])

            # if entrylist is , default to all notes,
            #with limit applied.

        def recursive_show(dictionary, level=1):

            """recursive function to show children of a note"""

            for k_temp in dictionary:


                if dictionary[k_temp] == {}:

                    if self.default_dict['variablesize']:
                        if not self.notebook_contains(k_temp):
                            display.noteprint((alerts.ATTENTION,str(k_temp)+' '+'NOT FOUND'))
                        else:
                            display.noteprint(self.show(k_temp,
                                                        shortform=(self.shortshow
                                                                   or len(entrylist) > self.longmax),
                                                        yestags=self.tagdefault,
                                                        highlight=highlight),
                                              param_width=display.width_needed
                                              (self.show(k_temp),
                                               self.get_metadata_from_note(k_temp)['size'],
                                               leftmargin=self.default_dict['leftmargin']),
                                              param_indent=(level-1)*self.default_dict['indentmultiplier'],
                                              leftmargin=self.default_dict['leftmargin'])
                    else:
                        if not self.notebook_contains(k_temp):
                            display.noteprint((alerts.ATTENTION,str(k_temp)+' '+'NOT FOUND'))
                        else:
                            display.noteprint(
                                self.show(k_temp,
                                          yestags=self.tagdefault,
                                          shortform=(self.shortshow
                                                     or len(entrylist) > self.longmax)),
                                param_width=self.default_dict['size'],
                                param_indent=(level-1)*self.default_dict['indentmultiplier'],leftmargin=self.default_dict['leftmargin'])

                else:
                    if self.default_dict['variablesize']:
                        if not self.notebook_contains(k_temp):
                            display.noteprint((alerts.ATTENTION,str(k_temp)+' '+'NOT FOUND'))
                        else:
                            display.noteprint(
                                self.show(k_temp,
                                          shortform=(self.shortshow
                                                     or len(entrylist) > self.longmax),
                                          yestags=self.tagdefault,
                                          highlight=highlight),
                                param_width=display.width_needed(self.show(k_temp),
                                                                 self.get_metadata_from_note(k_temp)['size']),
                                param_indent=(level-1)*self.default_dict['indentmultiplier'],leftmargin=self.default_dict['leftmargin'])
                    else:
                        if not self.notebook_contains(k_temp):
                            display.noteprint((alerts.ATTENTION,str(k_temp)+' '+'NOT FOUND'))
                        else:
                            display.noteprint(self.show
                                              (k_temp, yestags=self.tagdefault,
                                               shortform=(self.shortshow
                                                          or len(entrylist) > self.longmax)),
                                              param_width=self.default_dict['size'],
                                              param_indent=(level-1)*self.default_dict['indentmultiplier'],
                                              leftmargin=self.default_dict['leftmargin'])
                    recursive_show(dictionary[k_temp],
                                   level=level+1)


        maxlevel = 0
        for i_temp in entrylist:
            if len(i_temp) > maxlevel:
                maxlevel = len(i_temp)


        tempdict_a = {}
        tempdict_b = {}

        for i_temp in range(1, maxlevel+1):
            tempdict_a[i_temp] = []

        for i_temp in entrylist:
            tempdict_a[len(i_temp)].append(str(i_temp))

        for a_temp in range(1, len(tempdict_a)+1):
            #ranges over lengths of indexes

            for b_temp in range(len(tempdict_a[a_temp])):
                # ranges through the list of
                #indexes for a give length a
                if a_temp == 1:
                    tempdict_b[str(tempdict_a[a_temp][b_temp])] = {}


                else:
                    temp = Index(tempdict_a[a_temp][b_temp])

                    ancestors = []
                    while not temp.is_top():

                        ancestors = [str(temp.parent())]+ancestors
                        temp = temp.parent()

                    ancestorstring = EMPTYCHAR
                    for d_temp in ancestors:
                        ancestorstring += "['"+str(d_temp)+"']"

                    try:
                        if isinstance(eval('tempdict_b'+
                                           ancestorstring), dict):


                            if isinstance(eval('tempdict_b'+
                                               ancestorstring), dict):

                                e_temp = ('tempdict_b'
                                          +ancestorstring
                                          +'={str(tempdict_a[a_temp][b_temp]):{}}')
                                exec(e_temp)

                            else:
                                e_temp = ('tempdict_b'
                                          +ancestorstring
                                          +'[str(tempdict_a[a_temp][b_temp])]'+'={}')
                                exec(e_temp)

                    except KeyError:

                        e_temp = ('tempdict_b'
                                  +ancestorstring+'={}')
                        try:
                            exec(e_temp)
                        except KeyError:
                            pass
                        except SyntaxError:
                            print('Syntax Error')

                        e_temp = ('tempdict_b'
                                  +ancestorstring
                                  +'[str(tempdict_a[a_temp][b_temp])]'
                                  +'={}')
                        try:
                            exec(e_temp)
                        except KeyError:
                            pass
                        except SyntaxError:
                            print('Syntax Error')


        recursive_show(tempdict_b)

    def tagkeys(self,
                tag):

        """shows keys listed under a tag"""

        return sorted(list(self.get_keys_for_tag(tag)))

    def tagkeyindex(self,tag):

        """find the indexes the keys with the tag"""

        returnset = set()
        if self.tag_dict_contains(tag):

            for x_temp in self.get_keys_for_tag(tag):
                if self.key_dict_contains(x_temp+'/'+tag):
                    for y_temp in self.get_indexes_for_key(x_temp+'/'+tag):
                        returnset.add(y_temp)
        return returnset 


    def show_variables(self):

        """ show all the variables """

        variablelist = [(x_temp,self.variables[x_temp]) for x_temp in sorted(self.variables.keys())]
        display.noteprint(('/C/ '+labels.VARIABLES.upper(), EOL.join([x_temp[0]+BLANK
                                                  +COLON+BLANK
                                                  +abridge(str(x_temp[1]),40)
                                                  for x_temp in variablelist])))
        
        


    def reduce(self,
               noterange=None):

        """eliminates gaps between notes"""

        if noterange is None:
            noterange = self.apply_limit([str(Index(a_temp))
                                          for a_temp in self.indexes()
                                          if Index(a_temp).is_top()])


        for tup in reduce_tupples([Index(x_temp) for x_temp in self.find_within(indexfrom=Index(0),orequal=True,withinrange=noterange)]):
            self.move(tup[0], tup[1], withchildren=True)  

    def show_fields(self,
                    ef_temp=None):

        """shows all the fields with the indexes that belong to them"""

        returnstr = EMPTYCHAR
        temp_dict = {}
        returnset = set()
        for k_temp in self.default_dict['field']:
            k_temp = str(k_temp)
            
            if self.default_dict['field'][k_temp] in temp_dict:
                temp_dict[self.default_dict['field'][k_temp]].add(k_temp)
            else:
                temp_dict[self.default_dict['field'][k_temp]] = {k_temp}

        for k_temp in temp_dict:
            returnstr += (k_temp+' : '
                         +str(rangelist.range_find([Index(a_temp)
                                                     for a_temp
                                                     in temp_dict[k_temp]],reduce=True)).replace(SLASH,LONGDASH)+EOL)
        if ef_temp is None:
            
            return returnstr

        for f_temp in ef_temp:
            returnset = returnset.union(temp_dict[f_temp]) 
        return returnset

    def display_fields(self):

        """ displays the fields currently actice """

        field_text = self.show_fields()
        field_text_list = field_text.split(EOL)[0:-1]
        
        def fld_format (x_temp):

            x_temp = x_temp.split(COLON)[0], x_temp.split(COLON)[1]

            """formats output of the list of search results"""

            if not isinstance(x_temp[1],str):
                shown_indexes = rangelist.range_find([int(Index(a_temp))
                                                      for a_temp in x_temp[1]],reduce=True)
            else:
                shown_indexes = x_temp[1]

            if len(shown_indexes) < 20:
                return (abridge(x_temp[0]).replace(VERTLINE,SLASH)
                        +VERTLINE
                        +shown_indexes)
                        

            returnlist = []
            sp_temp = split_up_range(shown_indexes)
            
                                        
            returnlist.append(x_temp[0].replace(VERTLINE,SLASH)[0:min([60,len(x_temp[0])])]
                              +VERTLINE+sp_temp[0])
            for s_temp in sp_temp[1:]:
                returnlist.append(VERTLINE+s_temp)

            return returnlist

        show_list(field_text_list,alerts.FIELDS[3:],0,40,func=fld_format,present=True)

    def show_search_log(self,
                        enterlist=None,
                        label=labels.SEARCHES,
                        query=True):
        
        """shows the log that keeps track of searches"""

        if not enterlist:
            enterlist = list(self.searchlog)

        def lformat(x_temp):

            third_term = (x_temp and len(x_temp)>2)
            if not third_term:
                temp_st = BLANK
##            print(x_temp[0])

            """formats output of the list of search results"""

            if not isinstance(x_temp[1],str):
                shown_indexes = rangelist.range_find([Index(a_temp)
                                                      for a_temp in x_temp[1]],reduce=True)
            else:
                shown_indexes = x_temp[1]
            if third_term:
                temp_st=formkeys(x_temp[2])
            if len(shown_indexes) < 20:
                if len(temp_st) > 30:
                    temp_st = temp_st[0:30] + PERIOD + PERIOD + PERIOD
                
                return (abridge(x_temp[0]).replace(VERTLINE,SLASH)
                        +VERTLINE
                        +shown_indexes
                        +VERTLINE+temp_st+VERTLINE)

            returnlist = []
            sp_temp = split_up_range(shown_indexes)

            if len(temp_st) > 30:
                temp_st = temp_st[0:30] + PERIOD + PERIOD + PERIOD
            
                                        
            returnlist.append(x_temp[0].replace(VERTLINE,SLASH)[0:min([60,len(x_temp[0])])]
                              +VERTLINE+sp_temp[0]
                              +VERTLINE+temp_st+VERTLINE)
            for s_temp in sp_temp[1:]:
                returnlist.append(VERTLINE+s_temp+VERTLINE+' |')

            return returnlist

        searchlogcopy = enterlist

        searchlogcopy.reverse()

        show_list(searchlogcopy,
                  label, 0, 40, func=lformat)

        if query:

            show = False
            prompt = queries.ENTER_SEARCH_TERM
            searchterm = input(prompt)
            if searchterm == EMPTYCHAR:
                return
            if searchterm[0] == DOLLAR:
                show = True
                searchterm = searchterm[1:]
            numberlist = extract.extract(searchterm, LEFTBRACKET, RIGHTBRACKET)
            for number in numberlist:
                searchterm = searchterm.replace(LEFTBRACKET+number+RIGHTBRACKET,
                                                searchlogcopy[int(number)-1][0])

            sr_temp = self.new_search(searchterm)

            display.noteprint((labels.RESULT_FOR
                               +formkeys(sorted(list(sr_temp[2]))),
                               rangelist.range_find([Index(a_temp)
                                                     for a_temp in sr_temp[1]],reduce=True)))

            #formkeys(sorted(list(sr_temp[2])))
            if show:
                self.showall(sr_temp[1], highlight=sr_temp[2])


    def sequence_key_search(self,key,return_found_terms=False):

        """finds all the indexes that are in a ordered relation to a sequence key"""
        if not return_found_terms:
            returnvalue = set()
        else:
            returnvalue = (set(),set())


        if key.startswith('GT_'):
             func_pred = '>='
             pred_len = 3
        elif key.startswith('LT_'):
             func_pred = '<='
             pred_len = 3
        elif key.startswith('=_'):
             func_pred = '='
             pred_len = 2
        elif key.startswith('G_'):
             func_pred = '>'
             pred_len = 2
        elif key.startswith('L_'):
             func_pred = '<'
             pred_len = 2
        elif key.startswith('E_'):
             func_pred = '='
             pred_len = 2
        elif key.startswith('R_'):
             func_pred = '/'
             pred_len = 2
        elif key.startswith('ALL_'):
             func_pred = '?'
             pred_len = 4

        else:
            return returnvalue 

        key = key[pred_len:]

 

        if ATSIGN not in key:
            return returnvalue 
        else:
            if SLASH in key:
                afterslash = key.split(SLASH)[1]\
                             .split(ATSIGN)[1]\
                             .replace(POUND,EMPTYCHAR)\
                             .replace(UNDERLINE,EMPTYCHAR)
                key = key.split(SLASH)[0]
            else:
                afterslash = EMPTYCHAR
            identifier = key.split(ATSIGN)[0]
            key_value = key.split(ATSIGN)[1]
            
            


        key_mark, key_value, key_type = self.parse_sequence_key(key_value)


        if identifier not in self.default_dict['sequences']:
                return returnvalue
        sub_sequence = []


        if key_type == self.default_dict['sequences']['#TYPE#'][identifier]:

            sequence = self.default_dict['sequences'][identifier]

            sub_sequence = sequence.get(func=func_pred,
                                        item=key_value,
                                        item2=afterslash)




        returnset = set()
        returnfound = set()


        for x_temp in sub_sequence:
            x_temp = identifier+ATSIGN+key_mark+str(x_temp)

            if x_temp.endswith('.0'):

                x_temp = x_temp[:-2]

            for y_temp in [x_temp+'.0',x_temp,DASH.join(x_temp.split(DASH)[0:2]),
                           DASH.join(x_temp.split(DASH)[0:1])]:

                if y_temp in self.keys():
                    returnset = returnset.union(self.get_indexes_for_key(y_temp))
                    returnfound.add(y_temp)

            
        if not return_found_terms:
            return returnset
        else:
            return returnset, returnfound 
    

    def new_search(self,
                   query,
                   onlyterms=False):

        """Search function for performing complex searches over the notebase.
        Searches are formitted as follows:
            | : or
            & : and
            ~ : not
            * : wildcard
            () parantheses can be nested
            term   word in text
            <TERM> keyword
            ALLCAPS non-case sensitive
            #TERM tag
            ##TERM class defined through knowledge base

        The search function relies uses the eval function,
        but the string is preformated and tested before
        the eval is run, in order to minimize
        risk of eval function
        """


        def modify(term,
                   todo=EMPTYCHAR):
            """modifies term according to parameter todo"""

            if 'p' in todo:
                term = POUND+term
            if 'b' in todo:
                term = LEFTNOTE+term+RIGHTNOTE
            if 't' in todo:
                term = TILDA+term
            return term

        def is_regular(term):
            """used to test if the term is ready to be evaluated."""

            for a_temp in [PERIOD,
                           DASH,
                           BLANK,
                           LEFTPAREN,
                           RIGHTPAREN,
                           LEFTCURLY,
                           RIGHTCURLY,
                           COMMA,
                           'intersection',
                           'union',
                           'set',
                           "'"]:
                term = nformat.reduce_blanks(term).replace(a_temp, EMPTYCHAR)
            if term.isnumeric():
                return True

            
 
            return False

        def wildcards(term):

            """applies wildcards to the search term"""

            def find_terms(starts_with=EMPTYCHAR,
                           mid_terms=None,
                           ends_with=EMPTYCHAR,
                           searchedlist=None):

                if mid_terms is None:
                    mid_terms = []
                if searchedlist is None:
                    searchedlist = []
                returnlist = []
                for a_temp in searchedlist:
                    yes_start = False
                    yes_end = False
                    yes_mid = False
                    
                    
                    if a_temp.startswith(starts_with):
                        yes_start = True
                    if a_temp.endswith(ends_with):
                        yes_end = True
                    allin = True
                    a_temp_copy = a_temp[1:-1]
                    for mt_temp in mid_terms:
                        if mt_temp in a_temp_copy:
                            a_temp_copy = mt_temp.join(a_temp_copy.split(mt_temp)[1:])

                        elif mt_temp not in a_temp_copy:
                            allin = False
                    if allin:
                        yes_mid = True

                        

                    if (yes_start or starts_with=='@@@') \
                       and (yes_end or ends_with=='@@@') \
                       and (yes_mid or not mid_terms):
                                
                        returnlist.append(modify(a_temp, modifier))
                        

                return returnlist
            # beginning of wildcard main routine 

            if STAR not in term:

                return [term], (POUND in term or LEFTNOTE in term)

            brackets = False
            tilda = False
            pound = False
            caret = False

            if term[0] == TILDA:
                tilda = True
                term = term[1:]
            if term[0] == LEFTNOTE and term[-1] == RIGHTNOTE:
                term = term[1:-1]
                brackets = True

            if term[0] == POUND:
                term = term[1:]
                pound = True

            if term[0] == CARET:
                term = term[1:]
                caret = True

            mid_terms = term.split(STAR)

            if mid_terms[0] == EMPTYCHAR:
                mid_terms.pop(0)
                starts_with = '@@@'
            else:
                starts_with = mid_terms.pop(0)

            if mid_terms[-1] == EMPTYCHAR:
                mid_terms.pop(-1)
                ends_with = '@@@'
            else:
                ends_with = mid_terms.pop(-1)

            if brackets:
                modifier = 'b'+('t'*tilda)
                searched_list = list(self.keys())

            elif pound:
                modifier = 'p'+('t'*tilda)
                searched_list = list(self.tags())
            elif caret:
                modifier = 'c'+('t'*tilda)
                searched_list = list(self.tags())

            else:
                modifier = ('t'*tilda)
                searched_list = list(self.get_words())

##            nprint(starts_with,mid_terms,ends_with)

            return find_terms(starts_with,
                              mid_terms,
                              ends_with,
                              searched_list), (brackets or pound)

        def add_keys(termlist):

            """expand term by adding possible tags to keys"""

            #THIS SHOULD BE RENAMED

            returnlist = []
            for term in termlist:
                if term in self.tag_dict_values():
                    for tag in self.get_tags():
                        if term in self.get_keys_for_tag(tag):
                            returnlist.append(term+SLASH+tag)
            return returnlist

        def expand_term_list(termlist):

            """expand term list """

            returnlist = []
            for term in termlist:

                brackets = False
                tilda = False

                if term[0] in [POUND, CARET] and term[1:].replace(TILDA,EMPTYCHAR) in self.tags():
                    #    #TAG search for a tag
                    returnlist += [a_temp+SLASH+term[1:]
                                   for a_temp
                                   in self.get_keys_for_tag(term[1:])]+[a_temp
                                                                for a_temp
                                                                in self.get_keys_for_tag(term[1:])]
                    # 1) adds keys+tags 2) adds keys without tags
                if (term[:2] == '##' and self.default_dict['knower'].learned(term[2:])
                        and self.default_dict['knower'].genus(term[2:]) is True):
                    definitionlist = self.default_dict['knower'].reveal(term[2:])
                    for d_temp in definitionlist:
                        if self.tag_dict_contains(d_temp):

                            returnlist += [a_temp+SLASH+d_temp
                                           for a_temp in self.get_keys_for_tag(d_temp)]\
                                           +[a_temp for a_temp in self.get_keys_for_tag(d_temp)]

                else:
                    #if / is in the term, then separate it into word and suffixes
                    if SLASH in term:
                        l_term = term.split(SLASH)[0]
                        r_term = term.split(SLASH)[1]

                    else:
                        l_term = term
                        r_term = EMPTYCHAR


                    if l_term == l_term.upper():
                        l_list = [l_term.lower(),
                                  l_term.lower().capitalize(),
                                  l_term.upper()]
                        # if the term is ALL CAPS, then expand to include
                        #lowercase, capitalized, and all-caps versions
                    else:
                        l_list = [l_term]
                    if COMMA in r_term:
                        r_list = r_term.split(COMMA)+[EMPTYCHAR]
                        # divide right term into all the different
                        # suffixes, and then assign to r list.

                    else:
                        r_list = [r_term, EMPTYCHAR]
                        # Otherwise, r list is just the single
                        # suffix plus empty string.



                    returnlist += concatenate(l_list, r_list)
                    #generate all possible combinations
                    # of l list and r list.

            middlelist, returnlist = returnlist, []

            for term in middlelist:
                if term[0] == DOLLAR:
                    returnlist += self.default_dict['keymacros'].get_definition(term[1:])
                else:
                    returnlist += [term]
            return returnlist

        ##beginning of the main routine##

        returnstack = []
        querycopy = query # create a copy of the query
        querycopy2 = query
        foundterms = set()

        if onlyterms:

            foundterms = set()
            for term in querycopy.split(COMMA):

                t_temp = [wildcards(term)[0]]

                for tt_temp in t_temp:

                    foundterms.update(expand_term_list(tt_temp))

            return foundterms
        

            
        if self.negative_results:

            searchset = self.apply_limit(self.indexes())
                    # limit search set to applicable range
        else:
            searchset = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))


        # add spaces around ( ) & |
        for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:  
            query = query.replace(a_temp, '  '+a_temp+'  ')
        for a_temp in [LEFTPAREN, RIGHTPAREN, ANDSIGN, VERTLINE]:
            query = query.replace(a_temp, EMPTYCHAR)

        for a_temp in extract.extract(query, LEFTNOTE, RIGHTNOTE):
            # extract keywords, which are surrounded by arrow brackets.
            a_temp = LEFTNOTE+a_temp+RIGHTNOTE
            query = query.replace(a_temp, a_temp.replace(BLANK, PERCENTAGE))


        query = nformat.reduce_blanks(query)
        termlist = sorted(set(query.strip().split(BLANK)))


        termlist.reverse()

        def knowledge_from_word (word):
            originalword = word
            nonlocal querycopy

            def rebracket (word,brackets=False):

                if brackets:
                    return '<'+word+'>'
                else:
                    return word

            if word.startswith('<') and word.endswith('>'):
                word = word[1:-1]
                is_bracketed = True
            else:
                is_bracketed = False

            node = relation = EMPTYCHAR

            if word.startswith(QUESTIONMARK):
                word = word[1:]
                if QUESTIONMARK  in word:
                    node,relation = word.split(QUESTIONMARK)
                    

            ## to convert word based on general knowledge
            
            if  node and relation and self.default_dict['generalknowledge'].node_exists(node)\
               and self.default_dict['generalknowledge'].relation_exists(relation):
                newwords = [rebracket(x, is_bracketed)
                            for x in self.default_dict['generalknowledge'].text_interpret(DOLLAR
                                                                                          +DOLLAR+node
                                                                                          +COLON+relation)[1].split('//')[0].split(',')]
                querycopy = querycopy.replace(originalword,
                                              '|'.join(newwords))
            else:
                newwords = [rebracket(word, is_bracketed)]
            return newwords
        
        def transform_list (wordlist):

            returnlist = []
            for x in wordlist:
                if QUESTIONMARK in x:
                    newwords = knowledge_from_word(x)
                else:
                    newwords = [x]
                returnlist += newwords
            return returnlist 
                
            
        
        
        termlista = transform_list([a_temp for a_temp
                                    in termlist
                                    if LEFTNOTE in a_temp])
        
            #termlist a = list of keywords
        termlistb = transform_list([a_temp for a_temp
                                    in termlist
                                    if LEFTNOTE not in a_temp])
            #termlist b = list of words in text
        upto = len(termlista)
        result_temp = set()

        for counter, term in enumerate(termlista+termlistb):


            if not counter < upto:  #for the words
                temp_set = set()


                termcopy = term
                keyterm = False


                not_term = False
                if term[0] == TILDA:
                    not_term = True
                    term = term[1:]

                keyterm = False
                t_temp = wildcards(term)

                el_temp = expand_term_list(t_temp[0])

            else:  #for the keywords
                temp_set = set()

                term = term.replace(PERCENTAGE, BLANK)
                termcopy = term

                keyterm = True
                not_term = False
                if term[0] == TILDA:
                    not_term = True
                    term = term[1:]

                term = term[1:-1]

                if SLASH not in term:
                    t_temp = wildcards(term)
                    el_temp = expand_term_list(t_temp[0])
                    el_copy = list(el_temp)
                    for k_temp in el_copy:
                        for j_temp in self.keys():
                            if j_temp.startswith(k_temp+SLASH):
                                el_temp.append(j_temp)

                else:
                    t_temp = [term], True
                    el_temp = [term]


            if t_temp[1] or keyterm:   # if the term is a keyterm
                if not_term:
                    temp_set = set(searchset)
                    
                for word in el_temp:


                    if ATSIGN in word:

                                ft_temp = set()

                                if word[0] == LEFTBRACKET and word[-1] == RIGHTBRACKET:                              
                                    result_temp, ft_temp = self.sequence_key_search('=_'+word[1:-1],
                                                                                    return_found_terms=True)
                                    

                                elif SLASH not in word:
                                    if word and word[0] != LEFTBRACKET:
                                        if word and len(word)>2 and word[-2] == ATSIGN \
                                           and word[-1] in [DOLLAR,CARET,POUND,UNDERLINE,PLUS]:
                                            result_temp, ft_temp = self.sequence_key_search('ALL_'+word,
                                                                                   return_found_terms=True)
                                        else:     
                                            result_temp,ft_temp = self.sequence_key_search('GT_'+word,
                                                                                   return_found_terms=True)
                                    else:
                                        result_temp,ft_temp = self.sequence_key_search('G_'+word[1:],
                                                                                   return_found_terms=True)
                                elif SLASH in word and word and word[0] == SLASH:
                                    if word[-1] == RIGHTBRACKET:
                                        result_temp,ft_temp = self.sequence_key_search('L_'+word[1:-1],
                                                                                   return_found_terms=True)
                                    else:
                                        result_temp,ft_temp = self.sequence_key_search('LT_'+word[1:],
                                                                                   return_found_terms=True)

                                elif SLASH in word and word.count(SLASH) == 1:

                                    result_temp,ft_temp = self.sequence_key_search('R_'+word,
                                                                           return_found_terms=True)
                                    

                                if not not_term:

                                    temp_set = temp_set.union(result_temp)
                                    foundterms.update(ft_temp)

                                else:
                                    if result_temp:
                                    
                                        if not temp_set:
                                            temp_set = set(self.indexes())-result_temp
                                        else:                                            
                                            temp_set = temp_set - result_temp

                                        foundterms.update({'~'+f_temp for f_temp in ft_temp})
                                        

                                

                    elif  self.key_dict_contains(word):
                        if not not_term:

                            temp_set = temp_set.union(self.get_indexes_for_key(word))
                            if self.get_indexes_for_key(word).intersection(searchset):
                                foundterms.add(word)
                        else:

                            if not temp_set:
                                temp_set = set(self.indexes())-self.get_indexes_for_key(word)
                            else:
                                temp_set = temp_set - self.get_indexes_for_key(word)

                            foundterms.add('~'+word)
                    else:
                        if not not_term:
                            pass

##                if not term:                
##                    if not temp_set:
##                        temp_set = searchset
##                        print(word,len(temp_set))

            else:   #if it is not 

                for word in el_temp:

                    

                    if self.word_dict_contains(word):
                        if not not_term:
                            temp_set = temp_set.union(self.get_indexes_for_word(word))
                            if self.get_indexes_for_word(word).intersection(searchset):
                                foundterms.add(word)
                        else:
                            if not temp_set:
                                temp_set = set(self.indexes())-self.get_indexes_for_word(word)
                            else:
                                temp_set = temp_set - self.get_indexes_for_word(word)
                            foundterms.add('~'+word)
                    else:
                        if not not_term:
                            pass
                        else:
                            if not temp_set:
                                temp_set = {a_temp for a_temp
                                            in self.indexes()}
                            else:
                                temp_set = temp_set.intersection(set(self.indexes()))

            temp_set = temp_set.intersection(searchset)

            if termcopy not in [ANDSIGN,
                                VERTLINE,
                                'intersection',
                                '.union',
                                'set']:

                querycopy = querycopy.replace(termcopy,
                                              str(temp_set).replace(LEFTCURLY,
                                                                    '({').replace(RIGHTCURLY,'})'))
            
            querycopy = querycopy.replace(ANDSIGN, '.intersection')
            querycopy = querycopy.replace(VERTLINE, '.union')
            querycopy = querycopy.replace('set()', '({0})')
            while ('.union.union' in querycopy
                   or '.intersection.intersection' in querycopy):
                querycopy = querycopy.replace('.union.union',
                                              '.union')
                querycopy = querycopy.replace('.intersection.intersection',
                                              '.intersection')
            while BLANK+BLANK in querycopy:
                querycopy = querycopy.replace(BLANK+BLANK, BLANK)
            querycopy = querycopy.replace(')(', ').union(')


        if is_regular(querycopy):

            result = (eval(querycopy))-{0}
            if result == set():
                result = {0}
            if foundterms == set():
                foundterms = {'VOID'}
            
            
            self.searchlog.append((querycopy2,
                                   result,
                                   foundterms))
            
            return query, result, foundterms
        if len(querycopy) > 2000:
            len_temp = int(len(querycopy)/1000)
            for x_temp in range(1000):
                try:
                    q_temp = querycopy[x_temp*len_temp:(x_temp+1)*len_temp]
                    for a_temp in [PERIOD,
                           DASH,
                           BLANK,
                           LEFTPAREN,
                           RIGHTPAREN,
                           LEFTCURLY,
                           RIGHTCURLY,
                           COMMA,
                           'intersection',
                           'union',
                           'set',
                           "'"]:
                        q_temp = q_temp.replace(a_temp,BLANK)
                    for a_temp in '0123456789':
                        q_temp = q_temp.replace(a_temp,BLANK)
                    q_temp = q_temp.strip()
                        
                    if q_temp:
                        nprint(q_temp)
                except:
                    nprint('too big')

        display.noteprint((EMPTYCHAR,alerts.NOT_REGULAR))

        return query, set(), foundterms


    def cluster(self,
                indexlist=None,
                iterate_over=True,
                keycount=100,
                usepurge=True):

        """Organizes keywords into clusters ---
        groups of all the keywords that are connected
        through the relation of commonly
        belonging to the same note
        iterator_over --- to iterate over
        clusters when passing through indexes
        keycount === the number of keywords,
        starting from least frequent,
        included from each index
        """
        if indexlist is None:
            indexlist = self.indexes()

        if iterate_over:
            self.reset_iterators()

        keysetlist = []

        if keycount == 100:
            for i_temp in indexlist:
                keysetlist.append(set(self.get_keys_from_note(i_temp)))
                
                #form a list of the keysets

        else:
            for i_temp in indexlist:
                keysetlist.append(set(self.return_least_keys
                                  (set(self.get_keys_from_note(i_temp)),
                                   numberof=keycount, no_allcaps=False)))
                
                    #form a list of the keysets
        if not usepurge:
            clusteredsetlist = nformat.purgesets(consolidate.consolidate(keysetlist),
                                                 self.all_cap_purge,
                                                 self.first_cap_purge,
                                                 self.lower_case_purge,
                                                 self.purgelist)
        else:
            newkeysetlist = []
            for s_temp in keysetlist:
                newkeysetlist.append(self.default_dict['purge'].apply(s_temp))
            clusteredsetlist = consolidate.consolidate(newkeysetlist)
        counter = 1
        for csl in clusteredsetlist:

            t_temp = EMPTYCHAR
            for cs_temp in sorted(csl):
                t_temp += cs_temp + COMMA + BLANK
            display.noteprint((labels.CLUSTER + BLANK + POUND 
                               +str(counter),
                               t_temp[:-2]))
            q_temp = EMPTYCHAR
            for cs_temp in list(csl):
                q_temp += VERTLINE+LEFTNOTE+cs_temp+RIGHTNOTE+VERTLINE

            q_temp = q_temp[1:-1].strip()

            counter += 1
            if iterate_over:
                tl_temp = self.new_search(q_temp)[1]
                tl_temp = [a_temp for a_temp in tl_temp
                           if Index(a_temp) > Index(0)]
                if tl_temp:
                    self.add_iterator(tl_temp, csl)

    def constitute_word_dict(self):

        """ creates a new word dictionary"""

        #IS THIS NECESSARY WITH DATABASE??

        if self.using_shelf:
            for k_temp in self.get_words():
                -self.delete_word(k_temp)

        for i_temp in [a_temp for a_temp in self.indexes()
                       if Index(a_temp) > Index(str(0))]:

            self.add_search_words(Index(i_temp),
                                  self.get_text_from_note(i_temp))
        display.noteprint((alerts.ATTENTION,
                           alerts.WORD_DICT_CONSTITUTED))


    def word_search(self,
                    term):

        """searches for a word in the text
        of notes through the word dictionary"""

        foundset = set()
        term = term.strip().lower()
        if self.word_dict_contains(term):
            foundset = foundset.union(self.get_indexes_for_word(term))
        return foundset

    ### INPUT/OUTPUT


    def update(self,
               keyset,
               text,
               meta=None,
               as_child=False,
               right_at=False):

        """saves a note as text to the backup file"""
        if meta is None:
            meta = {}
        as_next = right_at and not as_child

        returntext = add_form(keyset.union(set(self.defaults.get('defaultkeys'))),
                              text,
                              meta,
                              as_child=as_child,
                              as_next=as_next)
        directoryname = os.getcwd()+'/textfiles'
        textfile = open(directoryname+SLASH+prefix+'backup'+'.txt', 'ab')
        textfile.write(codecs.encode(returntext.replace
                                     ('\ufeff', EMPTYCHAR).replace(EOL, '\r\n')
                                     +'\r\n',
                                     encoding='utf-8',
                                     errors='ignore'))
            #Codecs encoding to prevent unicode error
        textfile.close


    def format_output(self,
                      saveyes=False,
                      selection=None,
                      filename='defaultoutput',
                      metashow=False,
                      index_data=True,
                      include_project=False):

        """ saves notes as text"""

        right_at = False
        if index_data:
            right_at = True

        returntext = EMPTYCHAR
        if selection is None:
            selection = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))

        else:
            selection = sorted([a_temp for a_temp in selection
                                if a_temp in self.indexes()],
                               key=lambda x_temp: Index(x_temp))

        if metashow:
            for i_temp in selection:

                self.display_buffer.append(alerts.SAVING+str(i_temp))

                returntext += (add_form(transpose_keys(self.get_keys_from_note(i_temp),
                                                       surround=False),
                                        self.get_text_from_note(i_temp),
                                        self.get_metadata_from_note(i_temp),
                                        right_at=right_at, index=i_temp))

        else:
            for i_temp in selection:

                self.display_buffer.append(alerts.SAVING+index_reduce(str(i_temp)))
                returntext += (add_form(transpose_keys(self.get_keys_from_note(i_temp),
                                                       surround=False),
                                        self.get_text_from_note(i_temp),
                                        right_at=right_at, index=i_temp))
                lastindex = i_temp

        if include_project:
            returntext += '<<<<PROJECTBEGIN>>>>'\
                          + str(transform(self.default_dict['projects'].return_dict())) \
                          + '<<<<PROJECTEND>>>>'

        if saveyes:
            save_file(returntext,filename)

            display.noteprint((alerts.ATTENTION,filename+alerts.SAVED))

        


        else:
            print(returntext)

        return returntext

    def textinterpret(self,
                      phrase,
                      depth=0,
                      re_entering=False,
                      newindex=Index(-1)):

        

        """ reads a note in text form back into the database"""

        if len(phrase) > 3:
            if phrase[0] == LEFTNOTE and phrase[-1] == RIGHTNOTE and len(phrase) > 1:
                phrase = phrase[1:-1]
                #eliminate enclosing brackets
            keylist = self.pass_key_dict[depth][0]
            addedlist = self.pass_key_dict[depth][1]
            #list to keep track of new key words added on

            if phrase[0] == ATSIGN:
                # at sign signs enclose an index
                right_at = True
                as_child = False
                index_phrase = phrase.split(ATSIGN)[1]
                index = Index(index_phrase)

                phrase = phrase.replace(ATSIGN+index_phrase+ATSIGN, EMPTYCHAR)
                # eliminates index phrase 

            elif phrase[0] == PERCENTAGE:
                # percentage signs enclose a child index
                right_at = True
                as_child = True
                index_phrase = phrase.split(PERCENTAGE)[1]
                index = Index(index_phrase)

                phrase = phrase.replace(PERCENTAGE+index_phrase+PERCENTAGE, EMPTYCHAR)
                #eliminates index phrase 

            elif phrase[0] == '"':
                #for a child note
                phrase = phrase[1:]

                right_at = False
                as_child = True
                as_next = False

                index = self.index_sort([Index(0)]
                                   +[a_temp for a_temp
                                     in self.find_within(Index(0),
                                                         Index(1),
                                                         orequal=False)],
                                        by_date=False,
                                        quick=False)[-1]

            elif phrase[0] == "'":
                #for a next note

                phrase = phrase[1:]
                as_next = True
                as_child = False
                right_at = True
                index = self.index_sort([Index(0)]+[a_temp for a_temp
                                               in self.find_within(Index(0),
                                                                   Index(1),
                                                                   orequal=False)],
                                        by_date=False,
                                        quick=False)[-1]

            elif phrase[0] == ";":
                # to go back to the previous level and add a next note
                phrase = phrase[1:]
                as_next = True
                as_child = False
                right_at = True
                index = self.index_sort([Index(0)]
                                   +[a_temp for a_temp
                                     in self.find_within(Index(0),
                                                         Index(1),
                                                         orequal=False)],
                                        by_date=False,
                                        quick=False)[-1]
                index = Index(index)
                index = index.previous()
#                index = str(index)


            elif phrase[0] not in [DOLLAR, DASH, PLUS, STAR]:
                    # for an ordinary note

                j_temp = Index(int(Index(self.indexes()[-1])))
                    # Procedure for moving notes out of the ZERO range
                for i_temp in self.find_within(Index(0), Index(1)):
                    # j_temp is the next integer index
                    self.move(i_temp, j_temp+Index(i_temp))

                right_at = False
                as_child = False
                as_next = False
                index = Index(0)

            if phrase[0] == DOLLAR:
                #new keyword set
                keylist = []
                if len(phrase) > 1:
                    keylist += phrase[1:].split(COMMA)
            elif phrase[0] == PLUS:
                #add keyword set to existing
                if len(phrase) > 1:
                    for k_temp in phrase[1:].split(COMMA):
                        keylist.append(k_temp)
                    addedlist.append(len(phrase[1:].split(COMMA)))

            elif phrase[0] == DASH:
                #delete keyword
                if addedlist and len(keylist) > addedlist[-1]:
                    for a_temp in range(1, addedlist[-1]+1):
                        keylist.pop()
                    addedlist.pop()

            elif phrase[0] == STAR:
                #adds a single note with new keys,
                #yet without erasing the old keyset.
                # NEED TO CHECK IF THIS FUNCTION WORKS

                ks_temp = set(phrase[1:].split(SEMICOLON)[0].split(COMMA))
                ks_temp.update(extract.extract(phrase.split(SEMICOLON, 1)[1],
                                               LEFTCURLY,
                                               RIGHTCURLY))
                newindex = self.addnew(ks_temp,
                                       phrase.split(SEMICOLON, 1)[1])
            else:

                if not flatten.isflat(keylist):
                    keylist = flatten.flatten(keylist)
                ks_temp = set(keylist)
                meta = {}
                if LEFTCURLY in phrase:
                    ks_temp.update(extract.extract(phrase,
                                                   LEFTCURLY,
                                                   RIGHTCURLY))
                    # extracts keywords that are enclosed
                    #in curly brackets within the text
                if '^:' in phrase:
                    metadatalist = extract.extract(phrase, '^:', ':^')
                    # extract metadata

                    for md_temp in metadatalist:
                        #assigns metadata
                        if VERTLINE in md_temp and len(md_temp.split(VERTLINE)) >= 2:
                            if md_temp.split(VERTLINE)[1] == 'S':
                                meta[md_temp.split(VERTLINE)[0]] = str(md_temp.split(VERTLINE)[2])\
                                                                   .replace('"'+"'","'")\
                                                                   .replace("'"+'"',"'")
                            if md_temp.split(VERTLINE)[1] == 'I':
                                meta[md_temp.split(VERTLINE)[0]] = int(md_temp.split(VERTLINE)[2])
                            if md_temp.split(VERTLINE)[1] == 'L':
                                meta[md_temp.split(VERTLINE)[0]] = [x_temp.replace('"'+"'","'")\
                                                                    .replace("'"+'"',"'") for x_temp in
                                                                    md_temp.split(VERTLINE)[2][1:-1].split(COMMA)]
                phrase = nformat.remove_between(phrase, '^:', ':^')
                newindex = self.enter(ks_temp,
                                      phrase,
                                      meta,
                                      query=False,
                                      not_parsing=False,
                                      right_at=right_at,
                                      as_child=as_child,
                                      ind=str(index),
                                      re_entering=re_entering)
            self.pass_key_dict[depth][0] = keylist
            self.pass_key_dict[depth][1] = addedlist
        return newindex

    def textparse(self,
                  analysetext,
                  depth=0,
                  keys=None,
                  re_entering=False,
                  newindex=Index(1)):

        """ recursive function for interpreting
        embedded notes in text format
        """
        if keys is None:
            keys = set()
        if LEFTNOTE not in analysetext \
           or extract.embedded_extract(analysetext)[2] == 0:
            return
                #test if it contains embedded text

##        ee = extract.embedded_extract(RIGHTNOTE.join(LEFTNOTE.
##join(analysetext.split(LEFTNOTE)[1:]).split(RIGHTNOTE)[:-1]),eliminate = True)

        ee_temp = extract.embedded_extract(analysetext)
        embeddedlist = ee_temp[0]

        if depth-1 in self.pass_key_dict:

            self.pass_key_dict[depth] = self.pass_key_dict[depth-1]
        else:
            self.pass_key_dict[depth] = [[list(keys)], []]

        emb_len = str(len(embeddedlist))

        for a_temp, phrase in enumerate(embeddedlist):
            print(PERIOD,end=EMPTYCHAR)
            if a_temp<10 or (a_temp>9 and a_temp<100
                             and a_temp%10 == 0) or (a_temp>99
                                                     and a_temp%100==0):
                #display counter for embedded notes 
                print()
                print(str(a_temp)+'/'+emb_len)

            

                

            if extract.embedded_extract(phrase)[2] > 1:


                if phrase[0] == LEFTNOTE and phrase[-1] == RIGHTNOTE:
                    newindex = self.textinterpret(
                        extract.embedded_extract(
                            RIGHTNOTE.join(LEFTNOTE.join(phrase.split(LEFTNOTE)[1:])
                                     .split(RIGHTNOTE)[:-1]),
                            eliminate=True)[1],
                        depth,
                        re_entering=re_entering,
                        newindex=newindex)
                else:
                    newindex = self.textinterpret(
                        extract.embedded_extract(
                            phrase,
                            eliminate=True)[1],
                        depth,
                        re_entering=re_entering,
                        newindex=newindex)
                newindex = self.textparse(phrase[1:-1],
                                          depth+1,
                                          re_entering=re_entering,
                                          newindex=newindex)


            else:

                newindex = self.textinterpret(phrase,
                                              depth,
                                              re_entering=re_entering,
                                              newindex=newindex)
        return newindex

    def dictionaryload(self,filename):
        entertext = get_text_file(filename)

        if '<PROGRAM>' in entertext and '</PROGRAM>' in entertext:
            generic_program = EMPTYCHAR.join(entertext.split('<PROGRAM>')[1:]).split('</PROGRAM>')[0]
            entertext = EMPTYCHAR.join(entertext.split('</PROGRAM>')[1:])

            exec(generic_program)
            print(generic_program)
            exec('entertext=generic(entertext)')
            print(entertext.split('\n')[0:10])
            for counter, line in enumerate(entertext.split('\n')):
                if counter % 100==0:
                    print (counter)
                self.addnew(keyset=set(),
                            text=line,
                            ind=Index(counter+3),
                            right_at=True,
                            quick=True)
                
            
            
        else:

            for counter, line in enumerate(entertext.split('\n')[0:1000]):
                if counter % 1000 == 0:
                    print(counter)
                if len(line.strip()) >2:
                    word = line.split(' ')[0]
                    phrase = ' '.join(line.split(' ')[1:])
                    line =  '(' + str(counter) + ')'\
                           + '\n' + word + '\n' \
                           + '/FC/' + '\n' + phrase 
                    self.addnew(keyset=set(),
                                text=line,
                                ind=Index(counter+3),
                                right_at=True,
                                quick=True)

        
    def loadtext(self,
                 filename=EMPTYCHAR,
                 text=EMPTYCHAR,
                 loadproject=False,
                 loadindexes=True):

        analysetext = text
        projecttext = EMPTYCHAR

        """loads in a textfile to be parsed and interpreted"""

        check_spelling_was = self.check_spelling
        self.check_spelling = False


        if not analysetext and filename:
        
            analysetext = get_text_file(filename)

        if '<<<<PROJECTBEGIN>>>>' and '<<<<PROJECTEND>>>>' in analysetext:
            display.noteprint(('ATTENTION!','PROJECT SCRIPT FOUND!'))
            projecttext = analysetext.split('<<<<PROJECTBEGIN>>>>')[1].split('<<<<PROJECTEND>>>>')[0]
            analysetext = analysetext.replace('<<<<PROJECTBEGIN>>>>'
                                              +projecttext+'<<<<PROJECTEND>>>>',
                                              EMPTYCHAR)
            try:
                display.noteprint(('',projecttext[0:100]))
            except:
                display.noteprint(('ATTENTION!',"Can't display PROJECT TEXT"))
        if loadproject and projecttext:

            if self.default_dict['projects'].is_empty():
                
                self.default_dict['projects'].import_string(projecttext)
                if self.default_dict['projects'].is_empty():
                    display.noteprint((alerts.ATTENTION,'SUCCESSFULLY LOADED'))
                self.dd_changed=True

        if loadindexes:

            analysetext = self.default_dict['abbreviations'].do(analysetext)
            display.noteprint((alerts.ATTENTION,'ABBREVIATIONS ANALYSED!'))


            if filename == 'backup':
                default_backup = self.autobackup
                self.autobackup = False
            display.noteprint((alerts.ATTENTION,'INITIATING TEXT PARSING!'))

            newindex = self.textparse(analysetext,
                                      re_entering=True,
                                      newindex=Index(int(Index(self.indexes()[-1]))+1))

            if filename == 'backup':
                self.autobackup = default_backup

            for i_temp in self.find_within(Index(0), Index(1)):
                self.move(i_temp, Index(i_temp)+newindex)

        self.check_spelling = check_spelling_was

    def constitute_key_freq_dict(self):

        """ constitute the histogram of
        the frequencey of keys"""

        self.key_freq_dict = {}

        for k_temp in self.keys():
            self.key_freq_dict[k_temp] = len(self.get_indexes_for_key(k_temp))

##        for k in self.key_freq_dict: print(k, self.key_freq_dict[k])

    def order_keys(self,
                   keyset):

        """ reutrn a list of the keys in a set
        ordered in inverse relation to frequency
        """


        keylist = [k_temp for k_temp in keyset]
        keylist = [(a_temp, b_temp)
                   for a_temp, b_temp
                   in enumerate(keylist)]
        freq_list = []
        not_in_list = []
        for counter, key in keylist:
            if key in self.key_freq_dict:
                freq_list.append((self.key_freq_dict[key],
                                  counter))
            else:
                freq_list.append((0,counter))

        freq_list.sort(key=lambda x_temp: x_temp[0])
        return [(keylist[x_temp[1]][1], x_temp[0])
                for x_temp in freq_list]

    def print_key_freq(self,
                       freq_list):
        """display the frequency of a key"""

        for key, freq in freq_list:

            display.noteprint((EMPTYCHAR,key + alerts.APPEARS_BEG\
                               +len(self.get_indexes_for_key(key)\
                               +alerts.APPEARS_END+freq)))


    def return_least_keys(self,
                          keyset,
                          numberof=0,
                          override=False,
                          no_allcaps=True,
                          add_number=False):

        """ returns the least frequent keys in a keyset."""

        if override:
            return keyset
        if numberof == 0:
            numberof = self.default_dict['numberof']
        if not keyset:
            return []
        freq_list = self.order_keys(keyset)
        freq_list = [a_temp[0]+self.show_key_freq*add_number
                     *(a_temp[1]>0)*(' ('+str(a_temp[1])+')')
                     for a_temp in freq_list][0 : numberof]
        if no_allcaps and len(freq_list) > 3:
            freq_list = [a_temp for a_temp
                         in freq_list
                         if not a_temp.isupper()]
##        freq_list = sorted(freq_list, key=lambda x_temp: len(x_temp))
##        freq_list.reverse()

        return freq_list

    def abridged_str_from_list(self,
                               entrylist,
                               trim_length=0,
                               override=False):

        """returns a string of limited length
        from list of keys. Used for
        formatting note print
        """

        if override:
            trim_length = KEYLENGTH
        if trim_length == 0:
            trim_length = self.default_dict['keytrim']

        returntext = EMPTYCHAR
        for term in entrylist:
            lastlength = len(returntext)
            returntext += term+', '
            if len(returntext) > trim_length:
                if lastlength > trim_length-10:
                    return returntext[0 : lastlength-2]
                return returntext[:trim_length]
        return returntext[:-2]


##    def freq_test(self):
##
##        """testing function"""
##
##        self.constitute_key_freq_dict()
##        self.print_key_freq(self.order_keys(self.keys()))
##        for a_temp in self.note_dict:
##            print(a_temp,
##                  self.abridged_str_from_list(
##                      self.return_least_keys(
##                          self.note_dict[a_temp].keyset)))

    def make_consistent(self):

        """ makes key dictionary consistent with note dictionary"""

        for key in self.get_keys():
            self.eliminate_key(key) 

        for i_temp in self.indexes():    #i will be a note index
            for j_temp in self.get_keys_from_note(i_temp):
                if self.key_dict_contains(j_temp):
                    self.add_key(j_temp,Index(i_temp))
##                    self.key_dict[j_temp].add(str(Index(i_temp)))
                else:
                    self.initiate_new_key(j_temp,Index(i_temp))
                              


    def reform(self,
               entrylist=None):

        """ The can be used to correct the spelling and
        some formatting issues across a range of notes.
        It should not, however, be applied at once to a
        large number of notes, since this seems to
        crash the database and lead to truncation errors."""


        if entrylist is None:
            entrylist = self.apply_limit(self.find_within(indexfrom=Index(0),orequal=True))
                    # if entrylist is empty, default to all notes, with limit applied.

        for i_temp in entrylist:

            display.noteprint(self.show(i_temp),
                              param_width=display.width_needed(self.show(i_temp),
                                                               self.get_metadata_from_note(i_temp)['size']))
            text = self.get_text_from_note(i_temp)
            keyset = self.get_keys_from_note(i_temp)
            metadata = self.get_metadata_from_note(i_temp)
            
            text = reform_text(text)
            
            if self.check_spelling:
                text, added = self.speller.checktext(text)
                self.default_dict['spelling'].update(added)
                self.dd_changed = True
            
            self.softdelete(str(i_temp))
            self.addnew(keyset=keyset,
                        text=text,
                        metadata=metadata,
                        show=True,
                        right_at=True,
                        ind=i_temp)


    def text_by_paragraph(self,
                          filename,
                          splitchar=EOL,
                          keys=True,
                          key_definitions=False,
                          query=True):

        """loads text divided by the splitchar,
        default for paragraphs,
        and assigns keywords to them.
        """


        analysetext = get_text_file(filename)
        #load the text to be analysed

        if keys:

            possible_keys = set()
            if len(self.keys())>50:
                nprint  ("TOO MANY KEYS")
                for key in self.keys():
                    #grab all keys, removing tags.
                    #DESIDERATUM: Make it possible to
                    #restrict the range of notes
                    #from which the keys are grabbed

                    if SLASH in key:
                        if key.split(SLASH)[0] != EMPTYCHAR:
                            possible_keys.add(key.split(SLASH)[0].lower())
                    else:
                        possible_keys.add(key.split(SLASH)[0].lower())


                possible_keys = list(possible_keys)

                possible_keys = show_list(possible_keys,
                                          from_here=0,
                                          to_here=len(possible_keys),
                                          label='KEYS',
                                          select=True)
                    # show the keys through display
                    #object and select which are to be kept
                possible_keys += input(queries.ADDITIONAL_KEYS).split(COMMA)
                display.noteprint((labels.KEYS,
                                   formkeys(possible_keys)))


        for paragraph in analysetext.split(splitchar):
            # iterate over segments of the text to be analysed
            found_words = set()
            keyset = set()

            if keys:
                found_words.update({a_temp for a_temp in get_words(paragraph)
                                    if len(a_temp) > 3}.intersection(set(possible_keys)))
                        # make a set of all the words that have been found
                keyset = found_words
            if key_definitions:
                found_words.update(self.default_dict['definitions']
                                   .return_keys(get_words(paragraph)))
                keyset = found_words

            display.noteprint((formkeys(keyset),
                               nformat.encase(paragraph,
                                              found_words,
                                              surround=False)))
            # display the segment as a note
            #with found words encased
            #in arrow brackets

            if not query:
                if keyset == set():
                    keyset = {VOIDTERM}
                if paragraph.strip() != EMPTYCHAR:
                    self.enter(ek=keyset,
                               et=paragraph)

            else:

                if  input(queries.INCLUDE) in YESTERMS+[EMPTYCHAR]:
                    # ask if the found words
                    #should be included as keys

                    newkeys = set(input(formkeys(keyset)
                                        +queries.KEYWORDS_TO_ADD).split(COMMA)).union(keyset)
                    if paragraph.strip() != EMPTYCHAR:
                        self.enter(ek=newkeys, et=paragraph)
                if input(queries.CONTINUE + BLANK) not in YESTERMS+[EMPTYCHAR]:
                    break

    def defaults_from_notes(self,
                            identifying_key='CODES',
                            mark=EQUAL,
                            mark2=EQUAL,
                            obj=None,
                            entrytext=EMPTYCHAR,
                            directtext=False,
                            language='en'):

        """ loads defaults that have been entered in
        a note with the relevant keyword. Defaults to CODES
        identifying_key: the KEYWORD classifying
        the kind of defaults kept in the note
        mark, mark2 --- character used to
        identify phrase with relevant defaults
        obj --- the object into which the defaults
        will be loaded through the .load method.
        """

        if entrytext:
            text = entrytext
        else:

            indexlist = list(self.new_search(LEFTNOTE+identifying_key+RIGHTNOTE)[1])
            text = self.conflate(indexlist,
                                 return_text=True,
                                 inbetween=EOL)
        phrases = []
        if directtext:
            obj.load(text,language=language)
        for line in text.split(EOL):
            for phrase in line.split(BLANK):
                if phrase != EMPTYCHAR and (mark in phrase or mark2 in phrase):
                    phrases.append(phrase.strip())
        obj.load(phrases)


    def all_descendents (self,ind,from_indexes=None,as_index=True):
        if not from_indexes:
            from_indexes = self.indexes()
        if as_index:
            return [Index(x_temp) for x_temp in from_indexes \
                    if (Index(x_temp)==Index(ind)\
                        or Index(x_temp).is_descendent(Index(ind)))\
                    and Index(x_temp)>Index(0)]
        return [x_temp for x_temp in from_indexes
                if (Index(x_temp)==Index(ind)
                    or Index(x_temp).is_descendent(Index(ind)))
                and Index(x_temp)>Index(0)]

    def group_into_descendents (self,from_indexes=None):
        if not from_indexes:
            from_indexes = self.indexes()
        last_up = None
        last_top = None
        returnlist = []
        for x_temp in from_indexes:
            if Index(x_temp) > Index(0):
                if last_up and last_up.is_top():
                    if Index(x_temp).is_top():
                        returnlist[-1].append(x_temp)
                    else:
                        last_list = returnlist[-1]
                        returnlist = returnlist[0:-1]
                        if len(last_list)>1:
                            new_list = [last_list[-1],x_temp]
                            last_list = last_list[0:-1]
                            returnlist.append(last_list)
                            returnlist.append(new_list)
                        else:
                            last_list.append(x_temp)
                            returnlist.append(last_list)
                elif Index(x_temp).is_top() or not last_top:
                    last_top = Index(x_temp)
                    returnlist.append([x_temp])
                else:
                    if Index(x_temp).is_descendent(last_top):
                        returnlist[-1].append(x_temp)
                    else:
                        last_top = Index(x_temp)
                last_up = Index(x_temp)

        return returnlist

    def iterate_over_descendents(self,index_groups):
        self.reset_iterators()
        for l_temp in index_groups:
            self.add_iterator(l_temp)
        self.show_iterators()

    def choose_from(self,index_list):


        if len(index_list)==1:
            return index_list[0]

        if len(index_list)==2:
            while True:
                imp_temp = input('< >')
                if imp_temp in ['<','>',EMPTYCHAR]:
                    return index_list[{'<':0,
                                       '>':1,
                                       EMPTYCHAR:1}[imp_temp]]
        
        showtext = []
        for counter,index_temp in enumerate(index_list):
            if index_temp in self.indexes():
                showtext.append(str(counter+1)\
                                +' '+str(index_temp)+' : '\
                                +abridge(nformat\
                                         .format_keys(self.get_keys_from_note(index_temp))))
        display.noteprint(('/C/NOTES',EOL.join(showtext)))

        choice_temp = input('?')
        if choice_temp.isnumeric() \
           and 1 <= int(choice_temp) <= len(index_list):
            return index_list[int(choice_temp)-1]
        return index_list[-1]
        
                
                

    def hypermove(self,index):
        if self.hypermovemode == 0:
            # MODE ONE randomly jumps to related notes 

            if str(index) not in self.indexes():

                index = Index(random.choice(self.indexes()))
            keylist_temp = list(self.get_keys_from_note(index))
            
            if keylist_temp:
                key_temp = random.choice(keylist_temp)
            else:
                return index
            if self.key_dict_contains(key_temp):
                indexlist_temp = [x_temp for x_temp
                                  in self.get_indexes_for_key(key_temp)
                                  if Index(x_temp) >= Index(0)]
                if str(index) in indexlist_temp:
                    indexlist_temp.remove(str(index))
                if not indexlist_temp:
                    indexlist_temp = [str(index)]
            else:
                indexlist_temp = [str(index)]
            return Index(random.choice(indexlist_temp))

        if self.hypermovemode in [1,2]:

            if self.hypermovemode == 1:
                # MODE TWO randomly jumps to hyperlinked indexes
                # MODE THREE offers a choice
                
                func_temp = random.choice
            else:
                func_temp = self.choose_from



            if str(index) not in self.indexes():
                index = Index(random.choice(list(self.indexes())))

            keylist_temp = list(self.get_keys_from_note(index))
            keylist_temp = transpose_keys(check_hyperlinks(keylist_temp,purge=True))
            keylist_temp = [x_temp
                            .replace('<',EMPTYCHAR)
                            .replace('>',EMPTYCHAR) for x_temp in keylist_temp]
            if not keylist_temp:
                if isinstance(index,(int,str)):
                    index = Index(index)
                if self.key_dict_contains(str(index)):
                    return Index(func_temp(list(self.get_indexes_for_key(index))))
                return index
            elif len(keylist_temp) == 1:
                return Index(keylist_temp[0])
            else:
                return Index(func_temp(keylist_temp))

    def show_projects(self,projectobject=None):

        trim1 = self.default_dict['keytrim']
        trim2 = self.default_dict['texttrim']

        notelist = DisplayList(displayobject=display)
        text_temp = [labels.PROJECT_DISPLAY,' || ']
        for counter,temp_key in enumerate(sorted(projectobject)):

            if 'indexes' not in projectobject[temp_key]:
                projectobject[temp_key]['indexes'] = OrderedList()
            else:
                if isinstance(projectobject[temp_key]['indexes'],list):
                    projectobject[temp_key]['indexes'] = OrderedList(sorted(projectobject[temp_key]['indexes'],
                                                                            key=lambda x_temp:Index(x_temp)))
            if 'status' not in projectobject[temp_key]:
                projectobject[temp_key]['status'] = {'started':str(datetime.datetime.now()),
                                                                             'open':True,
                                                                             'lastmodified':[str(datetime.datetime.now())]}
            if 'defaultkeys' not in projectobject[temp_key]:
                projectobject[temp_key]['defaultkeys'] = []
            if 'position' not in projectobject[temp_key]:
                projectobject[temp_key]['position'] = (Index(0),Index(0))
                
                
            
            keys_formated = formkeys (projectobject[temp_key]['defaultkeys'])
            fl_temp = max([50,len(keys_formated)])
            keys_formated = keys_formated[0:fl_temp]
            line_temp = str(counter+1)+(5-len(str(counter+1)))*BLANK + VERTLINE
            line_temp += abridge(temp_key,trim1)\
                         +(trim1-len(abridge(temp_key,trim1)))\
                         *BLANK + VERTLINE
            line_temp += str(len(projectobject[temp_key]['indexes'].list))\
                         +(10-len(str(len(projectobject[temp_key]['indexes'].list))))*BLANK
##            line_temp += abridge(str(projectobject[temp_key]['position'][1]),10)\
##                         +(10-len(abridge(str(projectobject[temp_key]['position'][1])))) * BLANK
            line_temp += VERTLINE + '[' + abridge(keys_formated, trim2) \
                         + (trim2 + 6 -  \
                            len(abridge(keys_formated, trim2))) \
                            * BLANK + ']/'
            if len(projectobject[temp_key]['indexes']) > 1:
                   line_temp += index_reduce(str(transpose_keys(projectobject[temp_key]['indexes'].list,
                                                   surround=False)[0]))\
                                                   +':'+index_reduce(str(transpose_keys(projectobject[temp_key]['indexes'].list,
                                                                                            surround=False)[-1]))
            elif len(projectobject[temp_key]['indexes'].list) == 1:
                line_temp += str(projectobject[temp_key]['indexes'].list[0])
                
            else:
                line_temp += EMPTYCHAR
                                 
                             
            text_temp.append(line_temp)
            
        nformat.columns(EOL.join(text_temp),
                        listobject=notelist,
                        columnwidth=(4,10,15,50,15))
        notelist.present() 
        
"""histogram"""

import copy


class histogram:



    def __init__(self,displayobject,for_indexes=True):

        

        self.histo_dict = {}
        self.displayobject = displayobject
        self.for_indexes=for_indexes
        self.database_mode = False

    def load_dictionary(self,entrydictionary=None,flag="w"):

        #flag 'w' for words
        #flag 'k' for keys
        #flag 't' for tags
        global histo_word_dict,histo_tag_dict,histo_key_dict

        if entrydictionary:

            self.histo_dict = copy.deepcopy(entrydictionary)

        else:

            if 'w' in flag:

                if not histo_word_dict or 'n' in flag:

                    display.noteprint(('ATTENTION',
                                       'Making temporary word dictionary!'))

                    value_tuple = (notebookname,)
                    db_cursor.execute("SELECT word "
                                      +"FROM word_to_indexes "
                                      +"WHERE notebook=?;",
                                      value_tuple)
                    fetched = db_cursor.fetchall()
                    for word in fetched:

                        value_tuple = (notebookname,word[0],)
                        db_cursor.execute("SELECT note_index "
                                          +"FROM word_to_indexes "
                                          +"WHERE notebook=? and word=?;",
                                          value_tuple)

                        fetched = db_cursor.fetchall()
                        if fetched:
                            indexes = {index[0].strip() for index in fetched}
                            self.histo_dict[word[0]] = indexes
                    display.noteprint(('ATTENTION','Word dictionary finished!'))
                    histo_word_dict = copy.deepcopy(self.histo_dict)
                else:
                    display.noteprint(('Using word dictionary'))
                    self.histo_dict = histo_word_dict 

            if 'k' in flag:

                if not histo_key_dict or 'n' in flag:

                    display.noteprint(('ATTENTION',
                                       'Making temporary key dictionary!'))

                    value_tuple = (notebookname,)
                    db_cursor.execute("SELECT keyword"
                                      +" FROM keys_to_indexes"
                                      +" WHERE notebook=?;",
                                      value_tuple)
                    fetched = db_cursor.fetchall()
                    for key in fetched:

                        value_tuple = (notebookname,key[0],)
                        db_cursor.execute("SELECT note_index "
                                          +"FROM keys_to_indexes "
                                          +"WHERE notebook=? and keyword=?;",
                                          value_tuple)

                        fetched = db_cursor.fetchall()
                        if fetched:
                            indexes = {index[0].strip() for index in fetched}
                            self.histo_dict[key[0]] = indexes
                    display.noteprint(('ATTENTION','Key dictionary finished!'))
                    histo_key_dict = copy.deepcopy(self.histo_dict)
                    

                else:
                    display.noteprint(('Using Existing Key Dictionary'))
                    self.histo_dict = histo_key_dict 


            if 't' in flag:

                if not histo_tag_dict or 'n' in flag:
                    display.noteprint(('ATTENTION',
                                       'Making temporary tag dictionary!'))

                    value_tuple = (notebookname,)
                    db_cursor.execute("SELECT tag"
                                      +" FROM tags_to_keys"
                                      +" WHERE notebook=?;",value_tuple)
                    fetched = db_cursor.fetchall()
                    for tag in fetched:

                        value_tuple = (notebookname,tag[0],)
                        db_cursor.execute("SELECT keyword "
                                          +"FROM tags_to_keys"
                                          +" WHERE notebook=? and tag=?;",
                                          value_tuple)

                        fetched = db_cursor.fetchall()
                        if fetched:
                            keys = {key[0].strip() for key in fetched}
                            self.histo_dict[tag[0]] = keys
                    display.noteprint(('ATTENTION','Tag dictionary finished!'))
                    histo_tag_dict = copy.deepcopy(self.histo_dict)

                else:
                    display.noteprint(('Using existing tag dctionary'))
                    self.histo_dict = histo_tag_dict 

                    
        

   

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
                                              for x_temp in x_temp[1]},reduce=(len(x_temp[1])>100))
            
                
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
                  0, 30, func=dict_format, present=True)       

class Configuration:


    """This class is used to load, save, and manage user configurations """

    def __init__(self,
                 username):

        self.configuration_names = ['pause',
                                    '_longshow count',
                                    '_shortshow count',
                                    'always next',
                                    'always child',
                                    'quickenter',
                                    '_longmax',
                                    'autobackup',
                                    'flipout',
                                    'shortshow',
                                    'all cap purge',
                                    'first cap purge',
                                    'lower case purge',
                                    'children too',
                                    'box configs',
                                    'auto multi',
                                    'show full top']

        try:

            tempfile = open(globaldirectoryname
                            +SLASH+username
                            +'_config.pkl', 'rb')
            self = pickle.load(tempfile)
            tempfile.close()

        except:
            nprint(alerts.FAILED_CONF_LOAD)


            self.pause = True
            self.longshow_count = 60
            self.shortshow_count = 5
            self.always_next = False
            self.always_child = False
            self.quickenter = False
                # True is quickenter is permitted
            self.longmax = 100
                #the maximum number of notes that
                #will be shown long-form
            self.autobackup = True
                #True is the program will automatically
                #save entered notes to backup textfile
            self.flipout = False
                #True i\nf flipbook will be used
            self.shortshow = False
                #True if notes will always
                #be shown in short format
            self.all_cap_purge = True
                #True if ALL_CAP keys will be
                #excluded when clustering
            self.first_cap_purge = False
                #True if capitalized keys will
                #be excluded when clustering
            self.lower_case_purge = False
            self.children_too = True
            self.box_configs = False

            self.auto_multi = True
            self.show_full_top = True

            display.noteprint((alerts.CREATING_NEW_CONF,
                               username+'_config.pkl'))
            tempfile = open(globaldirectoryname
                            +SLASH+username
                            +'_config.pkl',
                            'wb')
            pickle.dump(self,
                        tempfile)
            tempfile.close()

    def define_other(self):

        """transfer configurations kept as attributes
        of the notebook to the configuration class
        """

        try:

            notebook.pause = self.pause
            notebook.longshow_count = self.longshow_count
            notebook.shortshow_count = self.shortshow_count
            notebook.always_next = self.always_next
            notebook.always_child = self.always_child
            notebook.quickenter = self.quickenter
            notebook.longmax = self.longmax
            notebook.autobackup = self.autobackup
            notebook.flipout = self.flipout
            notebook.shortshow = self.shortshow
            notebook.all_cap_purge = self.all_cap_purge
            notebook.first_cap_purge = self.first_cap_purge
            notebook.lower_case_purge = self.lower_case_purge
            notebook.children_too = self.children_too
            notebook.box_configs = self.box_configs
            notebook.auto_multi = self.auto_multi
            notebook.show_full_top = self.show_full_top
        except:
            notebook.pause = self.pause
            notebook.longshow_count = self.longshow_count
            notebook.shortshow_count = self.shortshow_count
            notebook.always_next = self.always_next
            notebook.always_child = self.always_child
            notebook.quickenter = self.quickenter
            notebook.longmax = self.longmax
            notebook.autobackup = self.autobackup
            notebook.flipout = self.flipout
            notebook.shortshow = self.shortshow
            notebook.all_cap_purge = self.all_cap_purge
            notebook.first_cap_purge = self.first_cap_purge
            notebook.lower_case_purge = False
            notebook.children_too = self.children_too
            notebook.box_configs = self.box_configs
            notebook.auto_multi = self.auto_multi
            notebook.show_full_top = self.show_full_top
            

    def define_self(self):

        """transfer attributes of the
        configuration class to the notebook
        """

        try:
            self.pause = notebook.pause
            self.longshow_count = notebook.longshow_count
            self.shortshow_count = notebook.shortshow_count
            self.always_next = notebook.always_next
            self.always_child = notebook.always_child
            self.quickenter = notebook.quickenter
            self.longmax = notebook.longmax
            self.autobackup = notebook.autobackup
            self.flipout = notebook.flipout
            self.shortshow = notebook.shortshow
            self.all_cap_purge = notebook.all_cap_purge
            self.first_cap_purge = notebook.first_cap_purge
            self.lower_case_purge = notebook.lower_case_purge
            self.children_too = notebook.children_too
            self.box_configs = notebook.box_configs
            self.auto_multi = notebook.auto_multi
            self.show_full_top = notebook.show_full_top
        except:
            self.pause = notebook.pause
            self.longshow_count = notebook.longshow_count
            self.shortshow_count = notebook.shortshow_count
            self.always_next = notebook.always_next
            self.always_child = notebook.always_child
            self.quickenter = notebook.quickenter
            self.longmax = notebook.longmax
            self.autobackup = notebook.autobackup
            self.flipout = notebook.flipout
            self.shortshow = notebook.shortshow
            self.all_cap_purge = notebook.all_cap_purge
            self.first_cap_purge = notebook.first_cap_purge
            self.lower_case_purge = notebook.lower_case_purge
            self.children_too = notebook.children_too
            self.box_configs = notebook.box_configs
            self.auto_multi = notebook.auto_multi
            self.show_full_top = notebook.show_full_top
            self.lower_case_purge = False

    def load(self):
        """load configurations from configuration file"""
        try:
            tempfile = open(globaldirectoryname+SLASH
                            +notebook.defaults.get('user')
                            +'_config.pkl', 'rb')
        except:
            tempfile = open(globaldirectoryname+SLASH
                            +'USER'
                            +'_config.pkl', 'rb')
        self = pickle.load(tempfile)  #pylint flagged this as inproper assignment to self
        tempfile.close()

        self.define_other()
        self.show()

        

    def save(self):
        """save configurations to configuration file"""

        self.define_self()
        tempfile = open(globaldirectoryname+SLASH
                        +notebook.defaults.get('user')
                        +'_config.pkl', 'wb')
        pickle.dump(self, tempfile)   #pylint flagged this as inproper assignment to self
        tempfile.close()
        display.noteprint((EMPTYCHAR,labels.CONFIG_SAVED))

    def show(self,
             big=False):

        """show configurations
        somewhat gratuitous use of eval
        function for the sake of versatility.
        """ 

        width = max([terminalsize.get_terminal_size()[0]-30, 145])

        if big:
            con_display = Note_Display(width)
        if not big:
            con_display = DisplayList(displayobject=display)

        boolconver = {True: 'ON',
                      False: 'Off'}
        smallwidth = 20


        for label in self.configuration_names:

            if label[0] != UNDERLINE:
                value = eval('str(boolconver[notebook.'
                             +label.replace(BLANK, UNDERLINE)+'])')
            else:
                label = label[1:]
                value = eval('str(notebook.'
                             +label.replace(BLANK, UNDERLINE)+RIGHTPAREN)

            if big:
                con_display.load(display.noteprint
                                 ((nformat.center(label,
                                                  width=smallwidth-2,
                                                  char=UNDERLINE),
                                   value),
                                  np_temp=True,
                                  param_width=smallwidth,
                                  param_spacing=0))

            else:
                con_display.append(label+' : '+value+'   ')

        if big:
            display.noteprint((nformat.center('CONFIGURATIONS',
                                              width,
                                              char=STAR),
                               con_display.print_all(pause=False,
                                                     show=False,
                                                     back=True)),
                              param_is_emb=True,
                              param_spacing=0)
        if not big:
            con_display.show(header=labels.CONFIGURATIONS,
                             centered=True)




class Console (Note_Shelf):


    """ Instantiating the Cosole creates a
    NOTEBASE by loading the shelf files
    and pickled files, and inituatializing
    configuration option, defaults,
    and non-persistent attributes, and then
    interpreting commands that have been
    entered and applying them to the NOTEBASE
    """

    def __init__(self,
                 filename,
                 flagvalue='c',
                 tempobject=temporary):
        
        self.read_only = True

        if flagvalue in ['c','w']:
            self.read_only = False 

        self.indexchanged = True    
        self.indexchanged_key = True    
        self.indexchanged_tag = True
        self.usesequence = False
        
        self.indexchanges = 0
        self.sortedindexes = set()
        self.sortedtags = set()
        self.sortedkeys = set()

        self.dd_changed = False 

        

        self.directoryname = globaldirectoryname
        self.filename = filename
        
        if spellcheck_on:
            self.speller = SpellCheck(display,
                                      headings=spellingheadings)
        self.check_spelling = spellcheck_on
        self.tempobject = tempobject
        self.last_term = EMPTYCHAR

        self.last_results = EMPTYCHAR
        self.next_term = EMPTYCHAR
        self.divided = True
        self.divide_no_query = True
        self.add_diagnostics = True
        self.suspend_default_keys = False
        self.vertmode = False
        self.apply_abr_inp = True
        self.abridgedformat = True
        self.sheet_buffer = ''
        self.y_pos = 0
        self.x_pos = 0
        self.pad_y_pos = 0
        self.pad_x_pos = 0
        self.y_max = 130
        self.x_max = 130
        self.window = None
        self.pad_dict = {}
        self.currentpad = 'default'
        self.using_shelf = True
        
        self.using_database = True


        
        self.pickle_dictionary = {}
        loaded = EMPTYCHAR
        failed = False
        display_temp = EMPTYCHAR

        self.key_dict = {}
        self.tag_dict = {}
        self.word_dict = {}
        self.default_dict = {}

        auto_database = False

        if self.using_shelf:
            for suffix in ('d','k','t','w'):
                if not failed:
                    try:
                        tempfile = open(self.directoryname
                                    +SLASH+self.filename+suffix.upper()+'.pkl', 'rb')
                        self.pickle_dictionary[suffix] = pickle.load(tempfile)
                        tempfile.close()
                        display_temp+={'d':'DEFAULT DICTIONARY',
                                       'k':'KEY DICTIONARY',
                                       't':'TAG DICTIONARY',
                                       'w':'WORD DICTIONARY'}[suffix]+' LOADED'+'\n'
                        loaded += suffix
                        
                        
                    except:
                        display_temp+={'d':'DEFAULT DICTIONARY',
                                       'k':'KEY DICTIONARY','t':'TAG DICTIONARY',
                                       'w':'WORD DICTIONARY'}[suffix]+' FAILED'+'\n'+'\n'+\
                                       ' WILL LOAD AS SINGLE PICKLE FILE!'
                        self.pickle_dictionary[suffix] = {}
                        failed = True
            display.noteprint((alerts.ATTENTION,display_temp))    

            if failed:
                try:
                    self.divided = False
                    tempfile = open(self.directoryname
                                    +SLASH+self.filename+'.pkl', 'rb')
              
                    self.pickle_dictionary = pickle.load(tempfile)
                    display.noteprint((alerts.ATTENTION,
                                       'PICKLE DICTIONARY OPENED'))
                    tempfile.close()

                    
                except OSError:

                    db_cursor.execute("SELECT notebook FROM notebooks")
                    filelist = list([i[0] for i in db_cursor.fetchall()])
                    if self.filename in filelist:
                        nprint(self.filename+'ALREADY OPENED AS DATABASE')
                        auto_database = True
                        self.using_shelf = False 

                    else:
               
                        display.noteprint((alerts.ATTENTION,
                                           'CREATING NEW PICKLE DICTIONARY'))
                        display.noteprint((alerts.ATTENTION,alerts.NEW_PICKLE))
                        self.pickle_dictionary = {'k':{},
                                                  't':{},
                                                  'w':{},
                                                  'd':{}}
                        tempfile = open(self.directoryname+SLASH+self.filename+'.pkl', 'wb')
                        pickle.dump(self.pickle_dictionary, tempfile)
                        tempfile.close()

                       

            if self.using_shelf:
                display.noteprint(('DIVIDED',str(self.divided)))
                

                self.key_dict = self.pickle_dictionary['k']
                    # keeps track of keys
                self.tag_dict = self.pickle_dictionary['t']
                    # keeps track of tags
                self.word_dict = self.pickle_dictionary['w']
                    # keeps track of words to facilitate quick searches
                self.default_dict = self.pickle_dictionary['d']
                    # persistent default date


            
        self.by_line = Convert()
        self.purge_objects = False
        

        self.defaults = DefaultManager(default_dictionary=self.default_dict,
                                       notebookname=notebookname,
                                       using_shelf=True,
                                       using_database=self.using_database,
                                       connection=db_connection,
                                       cursor=db_cursor)
                                       
                                       
        
        if self.using_shelf and not self.defaults.contains('usedatabase'):
            self.defaults.set('usedatabase',auto_database or
                              input('Use database?') in YESTERMS)
            self.purge_objects = True 
        if not self.defaults.get('usedatabase'):
            try:
                self.note_dict = shelve.open(self.directoryname
                                         +SLASH+self.filename
                                         +'ND', flag=flagvalue)

                self.using_shelf = True
                self.using_database = False
            except:
                display.noteprint(('ATTENTION!',
                                   'OPENING AS DATABASE'))
                self.using_shelf = False
                self.using_database = True
                
                del self.tag_dict
                del self.word_dict
                self.defaults.set('usedatabase',
                                  True)
            
            
        else:
            del self.tag_dict
            del self.word_dict
            self.using_shelf = False
            self.using_database = True

        def initiate_defaults(label,predicate):

            #Generic routine for initiating defaults   
            if not self.defaults.contains(label):
                if not isinstance(predicate,(bool,str,int)):
                    self.defaults.set(label,predicate)
                else:
                    self.defaults.set(label,predicate)

        def backup_defaults(label):
            nprint('BACKING UP ',label)
            #Generic routine for backing up defaults
            if not self.defaults.database_contains(label):
                self.defaults.backup(label)
            else:
                self.defaults.restore_from_backup(label)
            

        def_dict = {'convertbyline':False,
                    'convertmode':'default',
                    'fromtext':False,
                    'seqform1':EOL,
                    'seqform2':EMPTYCHAR,
                    'main_sequences':['title',
                                      'author',
                                      'date',
                                      'datefrom',
                                      'dateto',
                                      'book',
                                      'page',
                                      'chapter',
                                      'section'],
                    'sequences_in_text':False,
                    'texttrim':40,
                    'enterhelp':True,
                    'formattinghelp':True,
                    'updated data':False,
                    'field':{},
                    'date_dict':{},
                    'flipbook':[],
                    'user':'USER',
                    'displayonstart':True,
                    'defaultkeys':[],
                    'variablesize':True,
                    'size':60,
                    'iterators':[],
                    'iterator_names':{},
                    'keytrim':70,
                    'orderkeys':False,
                    'numberof':5,
                    'curtail':True,
                    'header':1,
                    'setitflag':False,
                    'footer':1,
                    'leftmargin':0,
                    'showdate':False,
                    'marked':set(),
                    'sortbydate':False,
                    'determinant':'ym',
                    'all':[],                
                    'keysbefore':True,
                    'keysafter':False,
                    'carryoverkeys':True,
                    'carryall':True,
                    'returnquit':3,
                    'returnquiton':False,
                    'indentmultiplier':4,
                    'sequences':{'#TYPE#':{}},
                    'smallsize':50}


        #FOR THE SIMPLE DEFAULTS
        for temp_label in def_dict:
            initiate_defaults(temp_label,def_dict[temp_label])

        #FOR THE COMPLEX DEFAULTS


        if self.purge_objects or not self.defaults.contains('projects'):
            if not self.using_database:
                self.default_dict['projects'] = ProjectManager()
            else:
                try:
                    self.default_dict['projects'] = ProjectManager(notebookname=notebookname,
                                                                   project_dictionary=self.default_dict['projects'],
                                                                   connection=db_connection,
                                                                   cursor=db_cursor)
                except:
                    self.default_dict['projects'] = ProjectManager(notebookname=notebookname,
                                                                   project_dictionary=None,
                                                                   connection=db_connection,
                                                                   cursor=db_cursor)
        
        else:
            try:
                self.default_dict['projects'].restore_connection(connection=db_connection,
                                                                 cursor=db_cursor)
            except:
                display.noteprint(('ATTENTION','RESTORE FAILED'))
        print('done')
        if not self.defaults.contains('convert'):
            self.default_dict['convert'] = {'default':Convert()}
        if  not isinstance(self.default_dict['convert'],dict):
            self.default_dict['convert'] = {'default':Convert()}            

        if  not self.defaults.contains('display'):
            self.default_dict['display'] = DisplayList(displayobject=display)
        if not self.defaults.contains('indexlist_indexes'):
            self.default_dict['indexlist_indexes'] = OrderedList([Index(x_temp)
                                                      for x_temp
                                                      in self.indexes()])
        if  not self.defaults.contains('purge'):
            self.default_dict['purge'] = PurgeKeys(),
        
        if self.purge_objects or 'generalknowledge' not in self.default_dict:
            print('general knowledge')
            while True:
                i_temp = input('GENERAL KNOWLEDGE \n (1)  IN COMMON SHELF '*self.using_shelf
                               +'(2) IN UNIQUE SHELF'*self.using_shelf 
                               +'(3) NO SHELF '
                               +'(4) IN SPECIFIC DATABASE '*self.using_database
                               +'(5) IN GENERAL DATABASE'*self.using_database)
                if i_temp in ('1','2')*self.using_shelf + ('3',) + ('4','5')*self.using_database:
                    break
            if i_temp in ('1','2'):
                self.default_dict['generalknowledge'] = GeneralizedKnowledge(directoryname=self.directoryname,
                                                                                     filename={2:self.filename,
                                                                                               1:'GENERALKNOWLEDGE'}[int(i_temp)],using_shelf=True,using_database=False)
            elif i_temp in ('3'):

                self.default_dict['generalknowledge'] = GeneralizedKnowledge(using_shelf=False,using_database=False)
                print('LOCAL')
            else:
                               
                self.default_dict['generalknowledge'] = GeneralizedKnowledge(directoryname=self.directoryname,
                                                                     filename={4:self.filename,
                                                                               5:'GENERALKNOWLEDGE'}[int(i_temp)],using_shelf=False,using_database=True)
                               
                
        else:
            self.default_dict['generalknowledge'].restart(directoryname=None,filename=None)
       

            
        if self.purge_objects or 'macros' not in self.default_dict:
            self.default_dict['macros'] = Abbreviate(displayobject=display,
                                                     use_presets=False,
                                                     headings=defaultheadings,
                                                     terms=defaultterms,
                                                     objectname='macros.db',
                                                     using_database=self.using_database)

            if not self.defaults.database_contains('macros'):
                self.defaults.backup('macros')
            else:
                self.defaults.restore_from_backup('macros')
                


        if self.purge_objects or'keymacros' not in self.default_dict:
            self.default_dict['keymacros'] = KeyMacroDefinitions(displayobject=display,
                                                                 headings=defaultheadings,
                                                                 terms=defaultterms,
                                                                 presets=presets.keymacro)
            if not self.defaults.database_contains('keymacros'):
                self.defaults.backup('keymacros')
            else:
                self.defaults.restore_from_backup('keymacros')

        if self.purge_objects or 'definitions' not in self.default_dict:
            self.default_dict['definitions'] = KeyDefinitions(displayobject=display,
                                                              headings=defaultheadings,
                                                              terms=defaultterms,
                                                              using_database=self.using_database)
            if not self.defaults.database_contains('definitions'):
                self.defaults.backup('definitions')
            else:
                self.defaults.restore_from_backup('definitions')

        if self.purge_objects or 'abbreviations' not in self.default_dict:
            self.default_dict['abbreviations'] = Abbreviate(displayobject=display,
                                                            headings=defaultheadings,
                                                            terms=defaultterms,
                                                            presets=presets.codes,
                                                            objectname='abbreviations.db',
                                                            using_database=self.using_database)
            if not self.defaults.database_contains('abbreviations'):
                self.defaults.backup('abbreviations')
            else:
                self.defaults.restore_from_backup('abbreviations')



        if self.purge_objects or not self.defaults.contains('commands'):
            self.default_dict['commands'] = Abbreviate(displayobject=display,
                                                       use_presets=False,
                                                       headings=defaultheadings,
                                                       terms=defaultterms,
                                                       objectname='commands.db')
            if not self.defaults.database_contains('commands'):
                self.defaults.backup('commands')
            else:
                self.defaults.restore_from_backup('commands')
        if self.purge_objects or not self.defaults.contains('knower'):
            self.default_dict['knower'] = KnowledgeBase(displayobject=display,
                                                        headings=defaultheadings,
                                                        terms=defaultterms,
                                                        using_dict=self.using_shelf,
                                                        using_database=self.using_database)
            display.noteprint(('ATTENTION!','CREATING DEFAULT KNOWLEDGEBASE!'))
        if not self.defaults.database_contains('knower'):
            self.defaults.backup('knower')
            display.noteprint(('ATTENTION!','BACKING UP DEFAULT KNOWLEDGEBASE TO DATABASE!'))
        else:
            self.defaults.restore_from_backup('knower')
            display.noteprint(('ATTENTION!','RESTORING DEFAULT KNOWLEDGEBASE FROM DATABASE!'))


  
        if not self.defaults.contains('spelling'):
            self.default_dict['spelling'] = {'es':set(),
                                             'en':set(),
                                             'fr':set(),
                                             'de':set()}
        try:
            self.configuration = Configuration(self.defaults.get('user'))
        except:
            self.configuration = Configuration('USER')

        if  not self.defaults.get('updated data'):
            self.default_dict['display'] = DisplayList(displayobject=display)
            self.default_dict['definitions'] = KeyDefinitions(displayobject=display,
                                                              headings=defaultheadings,
                                                              terms=defaultterms,
                                                              using_database=self.using_database)
            self.default_dict['abbreviations'] = Abbreviate(displayobject=display,
                                                            headings=defaultheadings,
                                                            terms=defaultterms,
                                                            presets=presets.codes,
                                                            objectname='abbreviations.db',
                                                            using_database=self.using_database)
            nprint('updated')
            self.defaults.set('updated data',True)





        if not self.defaults.database_contains('projects'):
            self.defaults.backup('projects')
            
        else:
            self.defaults.restore_from_backup('projects')

    
        self.default_dict['indexlist'] = OrderedList(self.indexes(),indexstrings=True)

##        if 'indexlist' in self.default_dict:
##            del self.default_dict['indexlist']
##            self.default_dict['indexlist'] = OrderedList(self.indexes(),indexstrings=True)
##            

        if self.purge_objects or not self.defaults.contains('indextable'):
            nprint('LOADING INDEXES INTO TRANSPOSITION TABLE')
            if self.using_database:
                self.default_dict['indextable'] = TranspositionTable(self.indexes(),
                                                                     using_dict=self.using_shelf,
                                                                     connection=db_connection,
                                                                     cursor=db_cursor,
                                                                     notebookname=notebookname)
            else:
                self.default_dict['indextable'] = TranspositionTable(self.indexes())
##        else:
##            if reconstitute and input('Renew transposition table?') in YESTERMS:
##                self.default_dict['indextable'] = TranspositionTable(self.default_dict['indextable'])
        else:
            self.default_dict['indextable'].restore_connection(connection=db_connection,
                                                               cursor=db_cursor)
        nprint('TRANSPOSITION TABLE DONE')
            
        if not self.defaults.database_contains('indextable'):
            nprint('BACKING UP INDEXTABLE')
            self.defaults.backup('indextable')
        else:
            nprint('RESTORING INDEXTABLE FROM BACKUP')
            self.defaults.restore_from_backup('indextable')
        
        nprint('OPENING CONNECTION FOR GENERAL KNOWLEDGE')
        self.default_dict['generalknowledge'].open_connection()
        nprint('OPENING CONNECTION FOR KNOWLEDGE')
        self.default_dict['knower'].open_connection()
        nprint('OPENING CONNECTION FOR DEFINITIONS')
        self.default_dict['definitions'].open_connection()
        nprint('OPENING CONNECTION FOR ABBREVIATIONS')
        self.default_dict['abbreviations'].open_connection()
        nprint('OPENING CONNECTION FOR MACROS')
        self.default_dict['macros'].open_connection()
        nprint('OPENING CONNECTION FOR KEYMACROS')
        self.default_dict['keymacros'].open_connection()
        nprint('OPENING CONNECTION FOR COMMANDS')
        self.default_dict['commands'].open_connection()                
        
        for l_temp in ['projects',
                       'knower',
                       'commands',
                       'keymacros',
                       'definitions',
                       'abbreviations',
                       'macros']:
        
            backup_defaults(l_temp)

##        for l_temp in self.default_dict:
##            self.defaults.get(l_temp,show=True)

        
##         
##

          #Non-persistent attributes
        
        self.variables = {}
        if spellcheck_on:
            self.speller = SpellCheck(display,added_words=self.default_dict['spelling'])
            self.speller.set_language() 
        self.iterator = []
            #iterator for flipping through the notecards
        self.done = stack.Stack()
            #stack of executed operations; for UNDO
        self.undone = stack.Stack()
            # stack of UNDONE operations; for REDO
        self.purgelist = []
            #List of keys to be excluded when clustering
        self.limitlist = []
            #the list of note indexes to which operations are limited
        self.tagdefault = True
            #True if tags will be displayed with keys
        self.pass_key_dict = {}
            # Keeps track of keywords during the
            #recursive function for handling embedded notes
        self.lastindex = Index(1)
        self.key_freq_dict = {}
            # dictionary for storing the frequency
            #of the occurence of keys.
            #Used to prioritize display
            #of least frequence keywords
        self.searchlog = []
            #keeps track of searches
        self.display_buffer = DisplayList(displayobject=display)
        self.entry_buffer = DisplayList(displayobject=display)
        self.last_keys = set()
        self.rectify = False # equalizes width of notes
        self.parent = EMPTYCHAR
        self.display_attributes = (True, True)
        self.project = []
        self.key_results = EMPTYCHAR
        self.text_result = EMPTYCHAR
        self.negative_results = False
        self.changed = False
        self.changes = 0
        self.iteratormode = True
        self.hypermovemode = 2

        self.linking = False
        self.looping = False
        self.first_of_loop = None
        self.last_added = Index(0)
        self.starting_linking = False
 
        self.side = 0
        self.flip_at = 0
        self.flipmode = False
        self.flexflip = True
        self.no_flash = False
        self.sides = 2
        self.def_sides = 2
        self.last_sides = 2
        self.show_images = True
        self.show_text = True
        self.delete_by_edit = False
        self.abr_maxdepth_found = 0
        self.maxdepth_found = 0
        self.show_key_freq = True
        self.how_many = 30
        self.carry_keys = False

        self.first_time = True
            #true if entry loop is running for the first time
        self.counter = 0
        self.lastsequencevalue = SequenceDefaultDictionary()
        self.keyauto = KeyAuto()
        self.sheetshelf = None
        self.sheetname = None
        self.usesequence = True 
        


    ## functions called from within command line ##

    def show_settings (self):

        display_temp = EMPTYCHAR
        for k_temp in self.default_dict:
            if isinstance(self.defaults.get(k_temp),(bool,int,str)):
                display_temp += k_temp + ' : ' + str(self.defaults.get(k_temp)) + EOL
        display.noteprint((labels.SETTINGS,display_temp))

    def show_defaults (self):

        display_temp = EMPTYCHAR
        for k_temp in self.default_dict:
            display_temp += k_temp + ' : ' + str(self.defaults.get(k_temp))[0:min([10,len(str(self.defaults.get(k_temp)))])] + EOL
        display.noteprint(('DEFAULTS',display_temp))

    def menu_com (self):

        # called from command line
        
        menu_list=[]
        mainterm = EMPTYCHAR
        command_menu = DisplayList(displayobject=display)
        for counter, h_temp in enumerate(commandscript.HEADERS):
            command_menu.append(str(counter+1)+': '+h_temp)
        command_menu.show(header='COMMANDS',
                          centered=True)
        choice = input(QUESTIONMARK)
        command_menu.clear()
        if choice.isnumeric() and int(choice) > 0 and int(choice) <= 8:
            new_menu = commandscript.MENU_DICTIONARY[int(choice)-1]
            menu_list = [x_temp for x_temp in new_menu[1].split(EOL)
                         if (x_temp != '||' and 'COMMAND' not in x_temp
                             and VERTLINE in x_temp
                             and x_temp.split(VERTLINE)[0].strip() != EMPTYCHAR)]

            for counter, c_temp in enumerate(menu_list):
                command_menu.append(str(counter+1)
                                    +': '
                                    +c_temp.split(VERTLINE)[0].strip())
            command_menu.show(header=new_menu[0],
                              centered=True)
        choice = input(QUESTIONMARK)
        if choice.isnumeric() \
           and int(choice) > 0 \
           and int(choice) <= len(menu_list):
            mainterm = menu_list[int(choice)-1]\
                       .split(VERTLINE)[0]\
                       .split(COMMA)[0].strip()
            print(mainterm)

        return mainterm
    

    def big_menu_com(self):

        # called from command line

        mainterm=EMPTYCHAR
        command_menu = DisplayList(displayobject=display)
        menu_script = EMPTYCHAR
        longest_menu = []
        for x_temp in range(0, len(commandscript.MENU_DICTIONARY)):
            longest_menu.append(len(commandscript.MENU_DICTIONARY[x_temp][1].split(EOL)))
        longest_menu = max(longest_menu)
        newline = EMPTYCHAR
        for counter, h_temp in enumerate(commandscript.HEADERS):
            newline += str(counter+1)+': '+h_temp+VERTLINE
        menu_script += newline[:-1]+EOL
        for y_temp in range(0, longest_menu):
            newline = EMPTYCHAR
            for x_temp in range(0,len(commandscript.MENU_DICTIONARY)):
                if y_temp < len(commandscript.MENU_DICTIONARY[x_temp][1].split(EOL)):
                    c_temp = commandscript.MENU_DICTIONARY[x_temp][1].\
                             split(EOL)[y_temp].split(VERTLINE)[0].strip()
                    if 'COMMAND' not in c_temp and c_temp != EMPTYCHAR:
                        newline +=  (str(y_temp)+COLON)+c_temp+' |'
                    else: newline += ' |'
                else: 
                    newline += ' |'
            menu_script += newline[:-1]+EOL
        nformat.columns(menu_script,
                        listobject=command_menu,
                        not_centered=set(range(-50,0)))
        command_menu.show(header=labels.ALL_COMMANDS,
                          centered=True)
        choice = input('X:Y? ')
        if COLON in choice:
            x_choice, y_choice = choice.split(COLON)[0],choice.split(COLON)[1]
            if x_choice.isnumeric() and y_choice.isnumeric():
                x_choice = int(x_choice)-1
                y_choice = int(y_choice)
            menu_length = len(commandscript.MENU_DICTIONARY[x_choice][1].split(EOL))
            if x_choice >= 0 and x_choice < 8 and y_choice > 0 and y_choice < menu_length+1:
                menu_list = commandscript.MENU_DICTIONARY[x_choice][1].split(EOL)[y_choice]
                mainterm = menu_list.split(VERTLINE)[0].split(COMMA)[0].strip()

        return mainterm

    def marked_com (self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR):


        # called from command line

        if mainterm in ['marked']:

            self.last_results = rangelist.range_find([Index(a_temp)
                                                     for a_temp
                                                     in self.defaults.get('marked')
                                                      if a_temp in self.indexes()])
            
            display.noteprint((labels.MARKED,self.last_results))

            self.last_results = self.last_results.replace(LONGDASH,SLASH)


        elif mainterm in ['addmarks']:
            self.default_dict['marked'].update({str(a_temp) for a_temp
                                                in get_range(s_input(queries.DELETE_FROM_TO,
                                                                     otherterms[0]),
                                                             True, False,
                                                             sort=True,
                                                             many=True)})
            self.dd_changed = True
        elif mainterm in ['deletemarks']:
            self.default_dict['marked'].difference_update({str(a_temp) \
                                                           for a_temp
                                                           in get_range(s_input(queries.DELETE_FROM_TO,otherterms[0]),
                                                                                   True,False,
                                                                                   sort=True,many=True)})
            self.dd_changed = True

    def documentation_com(self):

        # called from command line
        
        spelling_was = self.check_spelling
        self.check_spelling = False
        self.loadtext('introduction')
        self.check_spelling = spelling_was


    def loadtext_com(self,otherterms=EMPTYCHAR,predicate=EMPTYCHAR):

        # called from command line

        if predicate[0]:
            key_buffer = self.defaults.get('defaultkeys')
            self.defaults.set('defaultkeys',[])
            self.dd_changed = True

        filename_temp = get_file_name(file_path=os.altsep + 'textfiles',
                                    file_suffix='.txt', file_prefix=EMPTYCHAR,
                                    get_filename=otherterms[0])[0].rstrip()
        display.noteprint((alerts.LOADING_FILE,filename_temp))
        
        self.loadtext(filename_temp,loadproject=not predicate[1],loadindexes=not predicate[2])
        
        if predicate[0]:
            self.defaults.set('defaultkeys',key_buffer)
            self.dd_changed = True



    def loadby_com(self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR,predicate=EMPTYCHAR):
        
        if mainterm in ['loadbyparagraph']:
            self.text_by_paragraph(get_file_name(file_path=os.altsep +'textfiles',
                                                 file_suffix='.txt',
                                                 file_prefix=EMPTYCHAR,
                                                 get_filename=otherterms[0])[0],
                                   keys=not predicate[0],
                                   key_definitions=predicate[1],
                                   query=not predicate[2])
        elif mainterm in ['splitload']:
            self.text_by_paragraph(get_file_name(file_path=os.altsep + 'textfiles',
                                                 file_suffix='.txt',
                                                 file_prefix=EMPTYCHAR,
                                                 get_filename=otherterms[0])[0],
                                   splitchar=s_input(queries.DEMARC_MARK,
                                                     otherterms[1]),
                                   keys=not predicate[0],
                                   key_definitions=predicate[1],
                                   query=not predicate[2])


    def  autokey_com(self,
                     mainterm=EMPTYCHAR,
                     otherterms=EMPTYCHAR,
                     predicate=EMPTYCHAR):
        
        # called from command line
        
        if mainterm in ['clearautokeys','clearkeys']:
            
            self.defaults.set('defaultkeys',[])
            self.dd_changed = True
            display.noteprint((labels.DEFAULT_KEYS,
                               formkeys(self.defaults.get('defaultkeys'))))


                    
        elif mainterm in ['addkeys','addautokeys','ak','changekeys']:

            if mainterm == 'changekeys':
                self.defaults.set('defaultkeys',[])
                self.dd_changed = True
                
                
            keys_to_add = self.default_dict['abbreviations'].undo(s_input(queries.KEYS,
                                                                          otherterms[0])).split(COMMA)
            keys_to_add = get_keys_to_add(keys_to_add)

            
            self.defaults.set('defaultkeys',self.defaults.get('defaultkeys')+keys_to_add)

            if predicate[0]:
                
                if not otherterms[1]:
                    key_macro_name = input(queries.KEY_MACRO_NAME)
                else:
                    key_macro_name = otherterms[1]
                    
                self.default_dict['keymacros'].add(key_macro_name,keys_to_add)
            self.dd_changed=True
            display.noteprint((labels.DEFAULT_KEYS,
                               formkeys(self.defaults.get('defaultkeys'))))


        elif mainterm in ['addkey']:
            key_to_add = self.default_dict['abbreviations'].undo(s_input(queries.KEY, otherterms[0]))
            if key_to_add:
                if key_to_add[0] == DOLLAR:
                    self.defaults.set('defaultkeys',
                                      self.defaults.get('defaultkeys')
                                      +self.default_dict['keymacros'].get_definition(key_to_add[1:]))
                    self.dd_changed=True
                else:
                    self.defaults.set('defaultkeys',
                                      self.defaults.get('defaultkeys')
                                      +check_hyperlinks([key_to_add]))
                    self.dd_changed=True
            display.noteprint((labels.DEFAULT_KEYS,
                   formkeys(self.defaults.get('defaultkeys'))))


        elif mainterm in ['deleteautokey', 'deletekey', 'dk'] \
             and self.defaults.get('defaultkeys'):
            self.defaults.set('defaultkeys',self.defaults.get('defaultkeys')[:-1])
            self.dd_changed=True

        elif mainterm in ['deletedefaultkeys','deleteautokeys','editdefaultkeys']:
            if not otherterms[0]:
                self.defaults.set('defaultkeys',edit_keys(keyobject=self.defaults.get('defaultkeys'),
                                                             displayobject=display,
                                                             addkeys=True,
                                                             vertmode=self.vertmode,
                                                             notebookobject=self))
                dd_changed=True
                display.noteprint((labels.DEFAULT_KEYS,
                   formkeys(self.defaults.get('defaultkeys'))))

            else:
                if otherterms[0] in self.default_dict['projects'].get_all_projects():
                    k_temp = edit_keys(keyobject=self.get_default_keys(project=otherterms[0],
                                       displayobject=display,
                                       addkeys=predicate[0] or mainterm=='editdefaultkeys',
                                       vertmode=self.vertmode,
                                       notebookobject=self))
                    
                    self.default_dict['projects'].set_default_keys(k_temp,project=otherterms[0])
                    
                    display.noteprint((labels.DEFAULT_KEYS,
                                       formkeys(self.default_dict['projects'].get_default_keys(project=otherterms[0]))))

        display.noteprint((labels.DEFAULT_KEYS,
                           formkeys(self.defaults.get('defaultkeys'))))

    def limitlist_com(self,
                      mainterm=EMPTYCHAR,
                      otherterms=EMPTYCHAR):

        # called from command line
     
            
        if mainterm in ['resetlimitlist',
                          'resetll']:
            self.set_limit_list('R')
            display.noteprint((labels.LIMIT_LIST_RESET,
                               rangelist.range_find([Index(a_temp)
                                                     for a_temp in self.limitlist],reduce=True)))

        elif  mainterm in ['limitlist']:

            if not self.last_results_used:
                self.set_limit_list(s_input(queries.NEW_LIMIT_LIST,
                                            otherterms[0]))
                display.noteprint((labels.LIMIT_LIST_CHANGED,
                                   rangelist.range_find([Index(a_temp)
                                                         for a_temp in self.limitlist],reduce=True)))
                
            else:
                self.limitlist = []
                
                self.get_range_from_results (self.last_results,self.limitlist,indexobject=self.indexes())
                display.noteprint((labels.LIMIT_LIST_CHANGED,
                                   rangelist.range_find([Index(x_temp)
                                                         for x_temp in self.limitlist],reduce=True)))

                
        else:
            display.noteprint((labels.LIMIT_LIST,rangelist.range_find([int(Index(a_temp))
                                                     for a_temp in self.limitlist],reduce=True)))
            
    def stream_com (self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR,predicate=EMPTYCHAR):
        
        # called from command line
        if mainterm in ['streams']:
            display.noteprint((labels.STREAMS,
                               ", ".join([str(x_temp)
                                          for x_temp in multi_dict[notebookname].keys()
                                          if x_temp not in self.indexes()])))


        if mainterm in ['deletestream']:
            display_stream = s_input(queries.DISPLAY_STREAM,
                                     otherterms[0],
                                     typeflag='str',
                                     must_be_in=[x_temp for x_temp
                                                 in multi_dict[notebookname].keys()
                                                 if x_temp not in self.indexes()])
            if (display_stream in [notebookname]
                    and (predicate[0]
                         or s_input(queries.SURE,typeflag='str',
                                    must_be_in=YESTERMS+NOTERMS) in YESTERMS)):
                del multi_dict[notebookname][display_stream]
              #  $ to circumvent query




    def copy_com (self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR,predicate=EMPTYCHAR):

        if mainterm in ['copyto']:

            sourcerange = get_range(s_input(queries.SOURCE_TO_FROM,
                                            otherterms[0]),
                                    True, False, sort=True,many=True)

            self.copy_many_to_temp(sourcerange)
        elif mainterm in ['copyfrom']:
            if not predicate[0]:
                copy_count = int(s_input(queries.COPY_HOW_MANY,
                                         otherterms[0],
                                         typeflag='int',
                                         conditions=(0,temporary.size()),
                                         returnvalue=0))
            else:
                copy_count = self.tempobject.size()
            self.copy_many_from_temp(copy_count)

    def default_com (self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR):

        if mainterm in ['clearcommandmacros']:
            self.default_dict['commands'] = Abbreviate(displayobject=display,
                                                       use_presets=False,
                                                       headings=defaultheadings,
                                                       terms=defaulttermsm,
                                                       objectname='commands.db',
                                                       using_database=self.using_database)
            self.dd_changed=True
            self.defaults.backup('commands')
        elif mainterm in ['clearknowledge']:
            self.default_dict['knower'] = KnowledgeBase(displayobject=display,
                                                        headings=defaultheadings,
                                                        terms=defaultterms,
                                                        using_dict=self.using_shelf,
                                                        using_database=self.using_database)
            self.dd_changed=True
            self.defaults.backup('knower')
        elif mainterm in ['clearcodes']:
            self.default_dict['abbreviations'] = Abbreviate(displayobject=display,
                                                            headings=defaultheadings,
                                                            terms=defaultterms,
                                                            presets=presets.codes,
                                                            objectname='abbreviations.db',
                                                            using_database=self.using_database)
            self.dd_changed=True
            self.defaults.backup('abbreviations')
        elif mainterm in ['clearmacros']:
            self.default_dict['macros'] = Abbreviate(displayobject=display,
                                                     use_presets=False,
                                                     headings=defaultheadings,
                                                     terms=defaultterms,
                                                     objectname='macros.db',
                                                     using_database=self.using_database)
            self.dd_changed=True
            self.defaults.backup('macros')
        elif mainterm in ['clearkeydefinitions']:
            self.default_dict['definitions'] = KeyDefinitions(displayobject=display)
            self.dd_changed=True
            self.defaults.backup('definitions')
        elif mainterm in ['clearkeymacros']:

            self.default_dict['keymacros'] = KeyMacroDefinitions(displayobject=display,
                                                                 headings=defaultheadings,
                                                                 terms=defaultterms,
                                                                 presets=presets.keymacro,
                                                                 using_database=self.using_database)  
            self.dd_changed=True
            self.defaults.backup('keymacros')
        elif mainterm in ['defaultcommandmacros']:
            
            self.defaults_from_notes(identifying_key='COMMANDMACROS'+s_input('Suffix',
                                                                             otherterms[0]),
                                     mark=EQUAL,
                                     obj=self.default_dict['commands'])
            self.defaults.backup('commands')
        elif mainterm in ['defaultkeymacros']:
            self.defaults_from_notes(identifying_key='KEYMACROS'+s_input(queries.SUFFIX,
                                                                         otherterms[0]),
                                     mark=COLON,
                                     obj=self.default_dict['keymacros'])
            self.defaults.backup('keymacros')
        elif mainterm in ['recordkeydefinitions']:
            self.addnew({'KEYDEFINITIONS'+str(s_input(queries.SUFFIX,
                                              otherterms[0]))},
                        self.default_dict['definitions'].show_kd(returntext=True))
        elif mainterm in ['recordkeymacros']:
            self.addnew({'KEYMACROS'+str(s_input(queries.SUFFIX,otherterms[0]))},
                        self.default_dict['keymacros'].show_kd(returntext=True))
        elif mainterm in ['recordcodes']:
            self.addnew({'CODES'+str(s_input(queries.SUFFIX,
                                                     otherterms[0]))},
                        self.default_dict['abbreviations'].show(returntext=True))
        elif mainterm in ['recordmacros']:
            self.addnew({'MACROS'+str(s_input(queries.SUFFIX,
                                                     otherterms[0]))},
                        self.default_dict['macros'].show(returntext=True))        
        elif mainterm in ['recordknowledge']:
            self.addnew({'KNOWLEDGE'+str(s_input(queries.SUFFIX,otherterms[0]))},
                        self.default_dict['knower'].record())
        elif mainterm in ['recordcommandmacros']:
            self.addnew({'COMMANDMACROS'+str(s_input(queries.SUFFIX,
                                                     otherterms[0]))},
                        self.default_dict['commands'].show(returntext=True))
                
        elif mainterm in ['changekeydefinitions']:
            try:
                self.default_dict['definitions'].console()
                self.dd_changed=True
                self.defaults.backup('definitions')
            except AttributeError:
                self.default_dict['definitions'] = KeyDefinitions(displayobject=display,
                                                                  headings=defaultheadings,
                                                                  terms=defaultterms,
                                                                  using_database=self.using_database)
                self.default_dict['definitions'].console()
                self.dd_changed=True
                self.defaults.backup('definitions')
                
        elif mainterm in ['changecodes']:
            try:
                self.default_dict['abbreviations'].console()
                self.dd_changed=True
                self.defaults.backup('abbreviations')
            except AttributeError:
                self.default_dict['abbreviations'] = Abbreviate(displayobject=display,
                                                                headings=defaultheadings,
                                                                terms=defaultterms,
                                                                presets=presets.codes,
                                                                objectname='abbreviations.db',
                                                                using_database=self.using_database)
                self.default_dict['abbreviations'].console()
                self.dd_changed=True
                self.defaults.backup('abbreviations')
        elif mainterm in ['changemacros']:
            try:            
                self.default_dict['macros'].console()
                self.dd_changed=True
                self.defaults.backup('macros')
            except AttributeError:
                self.default_dict['macros'] = Abbreviate(displayobject=display,
                                                         use_presets=False,
                                                         headings=defaultheadings,
                                                         terms=defaultterms,
                                                         objectname='macros.db',
                                                         using_database=self.using_database)
                self.default_dict['macros'].console()
                self.dd_changed=True
                self.defaults.backup('macros')
        elif mainterm in ['changekeymacros']:
            self.default_dict['keymacros'].console()
            self.dd_changed=True
            self.defaults.backup('keymacros')
        elif mainterm in ['changecommandmacros']:
            try:
                self.default_dict['commands'].console()
                self.dd_changed=True
                self.defaults.backup('commands')
            except AttributeError:
                self.default_dict['commands'] = Abbreviate(displayobject=display,
                                                           use_presets=False,
                                                           headings=defaultheadings,
                                                           terms=defaultterms,
                                                           using_database=self.using_database)
                self.default_dict['commands'].console()
                self.dd_changed=True
                self.defaults.backup('commands')
                

        elif mainterm in ['learn']:
            self.default_dict['knower'].learn(s_input
                                              (queries.LEARN_WHAT,
                                               otherterms[0]),
                                              s_input(queries.IS_WHAT,
                                                      otherterms[1]))
            self.dd_changed=True
            self.defaults.backup('knower')
        elif mainterm in ['forget']:
            self.default_dict['knower'].unlearn(
                s_input(queries.UNLEARN_BEG,
                        otherterms[0]),
                s_input(queries.UNLEARN_END,
                        otherterms[1]))
            self.dd_changed=True
            self.defaults.backup('knower')
        elif mainterm in ['defaultcodes']:
            self.defaults_from_notes(identifying_key='CODES'+s_input(queries.SUFFIX,
                                                                             otherterms[0]),
                                     mark=EQUAL,
                                     obj=self.default_dict['abbreviations'])
            self.dd_changed=True
            self.defaults.backup('abbreviations')
        elif mainterm in ['defaultmacros']:
            self.defaults_from_notes(identifying_key='MACROS'+s_input(queries.SUFFIX,
                                                                             otherterms[0]),
                                     mark=EQUAL,
                                     obj=self.default_dict['macros'])
            self.dd_changed=True
            self.defaults.backup('macros')
        elif mainterm in ['defaultknowledge']:
            self.defaults_from_notes(identifying_key='KNOWLEDGE'+s_input(queries.SUFFIX,
                                                                         otherterms[0]),
                                     mark=SLASH,
                                     mark2=EQUAL,
                                     obj=self.default_dict['knower'])
            self.default_dict['knower'].bore()         
            self.dd_changed=True
            self.defaults.backup('knower')
        elif mainterm in ['defaultkeydefinitions']:
            self.defaults_from_notes(identifying_key='KEYDEFINITIONS'+s_input(queries.SUFFIX,
                                                                              otherterms[0]),
                                     mark=COLON,
                                     obj=self.default_dict['definitions'])
            self.dd_changed=True
            self.defaults.backup('defaultkeydefinitions')


                

    def eliminate_com (self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR):
        if mainterm in ['eliminateblanks']:
            for char in [string.whitespace+BLANK+'   ']:
                self.delete_key(char)
        elif mainterm in ['eliminatekeys']:
            for dk_temp in s_input(queries.KEYS_TO_ELIMINATE,
                                   otherterms[0]).split(COMMA):
                self.delete_key(dk_temp)

    def determ_com (self,mainterm=EMPTYCHAR,
                    otherterms=EMPTYCHAR,
                    predicate=EMPTYCHAR):
            
        if mainterm in ['changedeterminant','changedet']:
            olddet = self.defaults.get('determinant')
            display.noteprint((labels.DETERMINANT,formkeys(DETERMINANTS)))
            self.defaults.set('determinant',s_input(queries.DETERMINANT,
                                                       otherterms[0],
                                                       typeflag='str',
                                                       must_be_in=DETERMINANTS))
            self.dd_changed=True
            if not self.defaults.get('determinant') or \
               self.defaults.get('determinant') not in DETERMINANTS:
                self.defaults.set('determinant','ymd')
                self.dd_changed=True
            display.noteprint((labels.DETERMINANT,self.defaults.get('determinant')))
        elif mainterm in ['showdeterminant','showdet']:
            display.noteprint((labels.DETERMINANT,self.defaults.get('determinant')))
            
        elif mainterm in ['clearpurgekeys']:
            self.default_dict['purge'].clear()
            display.noteprint((labels.PURGE_KEYS,self.default_dict['purge'].show()))
            self.dd_changed=True
        elif mainterm in ['setpurgekeys']:
            e_temp=s_input(queries.SPECS,otherterms[0].strip())
            termset = set()
            spec_temp = EMPTYCHAR
            if e_temp:

                if len(e_temp)<6 and VERTLINE not in e_temp:
                    spec_temp = e_temp
                    e_temp = EMPTYCHAR
                    
                elif len(e_temp)> 2  and  VERTLINE in e_temp:
                    spec_temp = e_temp.split(VERTLINE)[0]
                    e_temp = e_temp.split(VERTLINE)[1]
                
                if e_temp:
                    termset = self.new_search(e_temp,onlyterms=True)
                    self.default_dict['purge'].load(termset)

            self.default_dict['purge'].allcaps(predicate[0] or 'a' in spec_temp)
            self.default_dict['purge'].caps(predicate[1] or 'u' in spec_temp)
            self.default_dict['purge'].lower(predicate[2] or 'l' in spec_temp)
            self.default_dict['purge'].numbers(predicate[3] or 'n' in spec_temp)
            self.default_dict['purge'].sequences(predicate[4] or 's' in spec_temp) 

            display.noteprint((labels.PURGEKEYS,self.default_dict['purge'].show()))
            self.dd_changed=True
        elif mainterm  in ['showpurgekeys']:
            display.noteprint((labels.PURGEKEYS,self.default_dict['purge'].show()))
            
    def spelling_com (self,
                      mainterm=EMPTYCHAR,
                      longphrase=False,
                      otherterms=EMPTYCHAR,
                      predicate=EMPTYCHAR):
        
        if mainterm in ['showspelling']:
            if not longphrase and not predicate[0]\
               and not predicate[1] and not predicate[2] \
               and not predicate[3]:
                self.speller.show_added()
            if longphrase:
                self.speller.show_added(s_input(queries.LANGUAGE,
                                                otherterms[0],
                                                typeflag='str',
                                                must_be_in=['en','de','fr','es']))
            if predicate[0]:
                self.speller.show_added('en')
            if predicate[1]:
                self.speller.show_added('de')
            if predicate[2]:
                self.speller.show_added('fr')
            if predicate[3]:
                self.speller.show_added('es')
 
        elif mainterm in ['defaultspelling']:
            l_temp = 'en'
            if longphrase:
                l_temp = (s_input(queries.LANGUAGE,
                                  otherterms[0],
                                  typeflag='str',
                                  must_be_in=['en','de','fr','es']))
            if predicate[0]:
                l_temp = 'en'
            if predicate[1]:
                l_temp = 'de'
            if predicate[2]:
                l_temp = 'fr'
            if predicate[3]:
                l_temp = 'es'
                
            self.defaults_from_notes(identifying_key='SPELLING'+s_input(queries.LANGUAGE_SUFFIX,
                                                                        otherterms[0]),
                                     mark=EQUAL,
                                     obj=self.speller,
                                     directtext=True,
                                     language=l_temp)


    def flip_com (self,mainterm=EMPTYCHAR,
                  otherterms=EMPTYCHAR,
                  longphrase=False,
                  totalterms=0):

        if mainterm in ['flipbook']:
            if not longphrase:
                self.default_dict['flipbook'] = [Index(i_temp) for i_temp
                                                        in self.indexes()]
                self.dd_changed=True
                self.parent = EMPTYCHAR
                self.show_full_top, self.children_too = self.display_attributes[0],self.display_attributes[1]
            elif totalterms == 1:
                temp_entry = s_input(queries.RANGE_TO_FROM,otherterms[0])

                if SLASH not in temp_entry \
                   and DASH not in temp_entry\
                   and COMMA not in temp_entry \
                   and temp_entry.replace(PERIOD,EMPTYCHAR).isnumeric():
                    self.default_dict['flipbook'] = self.all_descendents(temp_entry)
                    self.dd_changed=True
                    self.parent = temp_entry
                    self.display_attributes = (self.show_full_top,self.children_too)
                    self.show_full_top = False
                    self.children_too = False
                    
                elif temp_entry.replace(BLANK,EMPTYCHAR)\
                     .replace(DASH,EMPTYCHAR)\
                     .replace(LONGDASH,EMPTYCHAR)\
                     .replace(SLASH,EMPTYCHAR)\
                     .replace(COMMA,EMPTYCHAR)\
                     .replace(PERIOD,EMPTYCHAR).isnumeric():
                    
                    self.default_dict['flipbook'] = get_range(temp_entry,many=True)
                    self.dd_changed=True
                    self.parent = EMPTYCHAR
                    self.show_full_top, self.children_too = self.display_attributes[0],self.display_attributes[1]
                else: 
                    self.default_dict['flipbook'] = [Index(x_temp) for x_temp
                                                     in self.show_fields(temp_entry.split(COMMA))
                                                     if Index(x_temp) > Index(0)]
                    self.dd_changed=True
                    self.parent = EMPTYCHAR
                    self.show_full_top, self.children_too = self.display_attributes[0],self.display_attributes[1]

            display.noteprint((alerts.FLIP_CHANGED,
                               rangelist.range_find
                               (self.default_dict['flipbook'],reduce=True)))
            self.set_iterator(self.default_dict['flipbook'],
                              flag=self.defaults.get('setitflag'))
        elif mainterm in ['showflip','showflipbook']:

            self.last_results = rangelist.range_find(self.default_dict['flipbook'])
            
            display.noteprint(('FLIPBOOK',
                               rangelist.range_find(self.default_dict['flipbook'],reduce=True)))

            self.last_results = self.last_results.replace(LONGDASH,SLASH)


    def culkeys_com (self,mainterm=EMPTYCHAR):

        d_temp = {'capkeys':0,
                  'upperkeys':1,
                  'lowerkeys':2}[mainterm]
            

        self.histio = histogram(displayobject=display)
        if not self.using_database:
            self.histio.load_dictionary(entrydictionary=self.key_dict)
        else:
            self.histio.load_dictionary(flag='k')
        self.histio.implode(sort_keyset(self.keys())[d_temp])
        self.histio.show()

    def json_com (self,
              longphrase=False,
              mainterm=EMPTYCHAR,
              otherterms=EMPTYCHAR,
              predicate=EMPTYCHAR,
              totalterms=0):

        if mainterm in ['dumpprojects']:



            datesuffix=str(datetime.datetime.now()).split(' ')[0]
            project = str(transform(self.default_dict['projects'].return_dict()))

            self.dumpprojects()


        if mainterm in ['dumpknowledge','dumpgeneralknowledge']:


            datesuffix=str(datetime.datetime.now()).split(' ')[0]
            knowledge_text = self.default_dict['generalknowledge'].dump()
            if knowledge_text:
                save_file(knowledge_text,
                          filename='GK'+notebookname+datesuffix,
                          folder='/textfiles')

        if mainterm in ['showknowledge']:

            self.text_result = knowledge_text = self.default_dict['generalknowledge'].dump()
            display.noteprint(('GENERAL KNOWLEDGE',knowledge_text))
          
            
        if mainterm in ['loadknowledge','loadgeneralknowledge']:

            filename_temp = get_file_name(file_path=os.altsep + 'textfiles',
                                          file_suffix='.txt',
                                          file_prefix=EMPTYCHAR,
                                          get_filename=otherterms[0])[0].rstrip()
            display.noteprint((alerts.LOADING_FILE,filename_temp))
            knowledge_text = get_text_file(filename_temp)

            for l_temp in knowledge_text.split('\n'):

                if '{{' in l_temp and '}}' in l_temp:
                    l_temp = l_temp.replace('{{','').replace('}}','')
                    self.default_dict['generalknowledge'].text_interpret(l_temp)
                

        if mainterm in ['loadprojects']:

            if self.default_dict['projects'].is_empty():
                filename_temp = get_file_name(file_path=os.altsep + 'textfiles',
                                              file_suffix='.txt',
                                              file_prefix=EMPTYCHAR,
                                              get_filename=otherterms[0])[0].rstrip()
                display.noteprint((alerts.LOADING_FILE,filename_temp))
                project_text = get_text_file(filename_temp)

                self.default_dict['projects'].import_string(project_text)
                if not self.default_dict['projects'].is_empty():
                    display.noteprint((alerts.ATTENTION,'SUCCESSFULLY LOADED'))
                self.dd_changed=True


        if mainterm in ['clearprojects']:
            if input('Are your sure?') in YESTERMS \
               and input('Are you really sure?') in YESTERMS:
                self.default_dict['projects'].clear()
                self.dd_changed=True



    def resize_etc_com (self,
                        longphrase=False,
                        mainterm=EMPTYCHAR,
                        otherterms=EMPTYCHAR,
                        predicate=EMPTYCHAR,
                        totalterms=0):

        global override

        if mainterm in ['test']:

            animals = ['pig','sloth','giraffe','ant','bee','cat','dog','tiger','emu','aardvark','ferkel','mammoth','hippo','rhino']

            test_iterations = int(input('Test iterations>'))

            temp_counter=0
            for x in range(test_iterations):
            
                self.addnew({random.choice(animals)},
                                 random.choice(animals),
                                 show=False,
                                 right_at=False,
                                 as_child=False,
                            ind=Index(str(random.choice(range(1000000)))))


                if temp_counter%20 == 0:
                    db_connection.commit()
                    print(temp_counter, end=' ')
                temp_counter+=1

                

                

        if mainterm in ['cleargeneralknowledge']:
        

            result = self.default_dict['generalknowledge'].clear()

        if mainterm in ['reconstitutegeneralknowledge']:

            if input('DO YOU WANT TO CREATE A NEW GENERAL KNOWLEDGE SHELF??') in ['yes']:

                while True:
                    i_temp = input('(1) GENERAL KNOWLEDGE IN COMMON SHELF (2) GENERAL KNOWLEDGE IN UNIQUE SHELF (3) NO SHELF')
                    if i_temp in ('1','2','3'):
                        break
                if i_temp in ('1','2'):
                    self.default_dict['generalknowledge'] = GeneralizedKnowledge(directoryname=self.directoryname,
                                                                                         filename={2:self.filename,
                                                                                                   1:'GENERALKNOWLEDGE'}[int(i_temp)])

                else:
                    self.default_dict['generalknowledge'] = GeneralizedKnowledge()

                

        if mainterm in ['general','generalknowledge','gk']:

            while True:

                query = s_input('??',otherterms[0])
                result = self.default_dict['generalknowledge'].text_interpret(query)
                
                display.noteprint((result[0],result[1]))
                if not query:
                    break

        if mainterm in ['switchgeneralknowledge']:
            
            while True:
                i_temp = input('(1) GENERAL KNOWLEDGE IN COMMON SHELF (2) GENERAL KNOWLEDGE IN UNIQUE SHELF (3) NO SHELF')
                if i_temp in ('1','2','3'):
                    break
            if i_temp in ('1','2'):
                self.default_dict['generalknowledge'] = GeneralizedKnowledge(directoryname=self.directoryname,
                                                                                     filename={2:self.filename,
                                                                                               1:'GENERALKNOWLEDGE'}[int(i_temp)])

            else:
                self.default_dict['generalknowledge'] = GeneralizedKnowledge()
    

        if mainterm in ['convertdefinitions']:
            for x_temp in ['d','s','e']:
                queries_dic = {'d':'Dividor?',
                               's':'Sequence key mark?',
                               'e':'Entry divisor'}
                defaults = {'d':EOL,
                               's':COLON,
                               'e':COMMA}
                inp_temp = input(queries_dic[x_temp])
                if inp_temp:
                    self.default_dict['convert'][self.defaults.get('convertmode')].change(inp_temp,
                                                                                     x_temp)
                else:
                    self.default_dict['convert'][self.defaults.get('convertmode')].change(defaults[x_temp],
                                                                                      x_temp)
                display.noteprint((self.defaults.get('convertmode'),
                                   '/'.join(self.default_dict['convert'][self.defaults.get('convertmode')].show()).
                                                    replace(EOL,'EOL').
                                                    replace(COMMA,'COMMA').
                                                    replace(COLON,'COLON')))
        if mainterm in ['restoreallprojects']:
            self.restore_projects(query=not predicate[0])

        if mainterm in ['restoreproject']:
            self.restore_project(project=s_input('Name of project?',otherterms[0]),query=not predicate[0])

                
        if mainterm in ['newconvertmode']:
            ex_temp = s_input('New convert mode?',otherterms[0])
            if ex_temp not in self.default_dict['convert']:
                self.default_dict['convert'][ex_temp] = Convert()
            display.noteprint(('/C/ Convert modes',
                               ', '.join(self.default_dict['convert'])))
        if mainterm in ['switchconvertmode']:
            ex_temp = s_input('convert mode?',
                              otherterms[0],
                              typeflag='str',
                              must_be_in=list(self.default_dict['convert']))
            if ex_temp in self.default_dict['convert']:
                self.defaults.set('convertmode',ex_temp)
            display.noteprint((self.defaults.get('convertmode'),
                               '/'.join(self.default_dict['convert'][self.defaults.get('convertmode')].show()).
                                                    replace(EOL,'EOL').
                                                    replace(COMMA,'COMMA').
                                                    replace(COLON,'COLON')))
        if mainterm in ['showallconvertmodes']:
            display.noteprint(('ALL CONVERT MODES',
                               EOL.join([x_temp + ':'
                                         + '/'.join(self.default_dict['convert'][x_temp].show()).
                                                    replace(EOL,'EOL').
                                                    replace(COMMA,'COMMA').
                                                    replace(COLON,'COLON')
                                         for x_temp in self.default_dict['convert'].keys()])))
            

        if mainterm in ['mainsequences']:

            entry_temp = s_input(queries.MAIN_SEQUENCES,otherterms[0])
            if not entry_temp:
                pass
            elif COMMA not in entry_temp and entry_temp.lower() == 'd':
                self.default_dict['main_sequences'] = ['title',
                                                       'author',
                                                       'date',
                                                       'datefrom',
                                                       'dateto',
                                                       'book',
                                                       'page',
                                                       'chapter',
                                                       'section']
            else:
                self.default_dict['main_sequences'] = [x_temp.strip()
                                                       for x_temp in entry_temp.split(COMMA)]
            display.noteprint((alerts.ATTENTION,
                               labels.MAIN_SEQUENCES
                               +', '.join(self.default_dict['main_sequences'])))

        if mainterm in ['seqformone']:
            entry_temp = s_input(queries.SEQ_FORM_ONE,
                                 otherterms[0],
                                 typeflag='str',
                                 must_be_in=['s',
                                             'l',
                                             'c',
                                             'b',
                                             'n'],
                                 returnvalue=self.defaults.get('seqform1'))
            if entry_temp[0].lower() in ['s',
                                         'l',
                                         'c',
                                         'b',
                                         'n']:
                if entry_temp[0].lower() == 's':
                    self.defaults.set('seqform1',BLANK)
                elif entry_temp[0].lower() == 'c':
                    self.defaults.set('seqform1',COMMA + BLANK)
                elif entry_temp[0].lower() == 'l':
                    self.defaults.set('seqform1',EOL)
                elif entry_temp[0].lower() == 'b':
                    self.defaults.set('seqform1',EOL + '/BREAK/')
                elif entry_temp[0].lower() == 'n':
                    self.defaults.set('seqform1',EOL + '/NEW/')
                    
            else:
                
                self.default_dict['seqform1'] = entry_temp
            display.noteprint((labels.SEQ_FORM_ONE,
                               self.defaults.get('seqform1').
                               replace(BLANK,
                                       'BLANK').
                               replace(COMMA+BLANK,
                                       'COMMA + BLANK').
                               replace(EOL,
                                       'EOL').
                               replace('/BREAK/',
                                       'BREAK').
                               replace('/NEW/',
                                       'NEW')))

        if mainterm in ['seqformtwo']:
            
            entry_temp = s_input(queries.SEQ_FORM_TWO,otherterms[0])
            if entry_temp[0].lower() in ['e','l','b','n']:
                if entry_temp[0].lower() == 'e':
                    self.defaults.set('seqform2',EMPTYCHAR)
                elif entry_temp[0].lower() == 'l':
                    self.defaults.set('seqform2',EOL)
                elif entry_temp[0].lower() == 'b':
                    self.defaults.set('seqform2',EOL + '/BREAK/' + EOL)
                elif entry_temp[0].lower() == 'n':
                    elf.defaults.set('seqform2',EOL + '/NEW/'  + EOL) 
            else:
                    elf.defaults.set('seqform2',entry_temp)
            display.noteprint((labels.SEQ_FORM_ONE,self.defaults.get('seqform2').
                               replace(EOL,' EOL ').
                               replace('/BREAK/',' BREAK ').replace('/NEW/',' NEW ')))
        if mainterm in ['dictionaryload']:
            filename_temp = get_file_name(file_path=os.altsep + 'textfiles',
                                    file_suffix='.txt', file_prefix=EMPTYCHAR,
                                    get_filename=otherterms[0])[0].rstrip()
            display.noteprint((alerts.LOADING_FILE,filename_temp))
        
            self.dictionaryload(filename_temp)

        if mainterm in ['language']:
            lang_temp = s_input(queries.LANGUAGE_SELECT,
                                otherterms[0],
                                typeflag='str',
                                must_be_in=['en','es','fr','de'])
            if len(lang_temp) > 1:
                lang_temp = lang_temp[0:2].lower()
            if lang_temp in ['en','es','fr','de']:
                self.speller.set_language(lang_temp)
                

        if mainterm in ['save']:
            text_temp=s_input(queries.TEXT_TO_SAVE,otherterms[0])
            filename = s_input(queries.SAVE_TO_FILE,otherterms[1])
            if totalterms == 3:
                pathname = '/' + s_input(self.FOLDER,otherterms[2])
            else:
                pathname = '/textfiles'
            save_file(text_temp,filename,pathname)

        if mainterm in ['echo']:
            text_temp=s_input(queries.TEXT_TO_PRINT,otherterms[0])
            print(text_temp)

        if mainterm in ['run']:
            program_name = s_input(queries.FUNCTION_NAME,otherterms[0])
            program = get_text_file(program_name,'\programs',suffix='.py')
            print(program)
            text_temp=s_input(queries.TEXT_TO_CONVERT,otherterms[1])
            exec(program)
            exec('self.text_result=generic(text_temp)')

        if mainterm in ['explode']:
            if otherterms[0] in self.indexes():
                self.last_results = otherterms[0]
                self.key_results = ','.join(get_keys_from_note(otherterms[0]))
                self.text_result = self.get_text_from_note(otherterms[0])
                self.last_results_used = False

                
                

        if mainterm in ['load']:

            filename_temp = get_file_name(file_path=os.altsep + 'textfiles',
                                          file_suffix='.txt', file_prefix=EMPTYCHAR,
                                          get_filename=otherterms[0])[0].rstrip()


            self.text_result = get_text_file(filename_temp)

        if mainterm in ['interpret']:
            text_temp=s_input(queries.TEXT_TO_INTERPRET,otherterms[0])
            self.loadtext(text=text_temp)

        if mainterm in ['runinterpret']:
            program_name = s_input(queries.FUNCTION_NAME,otherterms[0])
            program = get_text_file(program_name,'\programs',suffix='.py')
            print(program)
            if not otherterms[1]:
                filename_temp = get_file_name(file_path=os.altsep + 'textfiles',
                                    file_suffix='.txt', file_prefix=EMPTYCHAR,
                                    get_filename=otherterms[1])[0].rstrip()
            else:
                filename_temp = otherterms[1]
            textfile = get_text_file(filename_temp)

            exec(program)
            exec('self.loadtext(text=generic(textfile))')
            
            
            

        if mainterm in ['invert']:
            self.last_results = rangelist.range_find([Index(a_temp)
                                                      for a_temp in self.indexes()
                                                      if Index(a_temp)>Index(0)
                                                      and Index(a_temp)
                                                      not in get_range(s_input(queries.RANGE_TO_FROM,
                                                                               otherterms[0]),
                                        many=True)])
            self.last_results = self.last_results.replace(LONGDASH,SLASH)          
            self.last_results_used = False
            

        elif mainterm in ['setreturnquit','rtq']:
            self.defaults.set('returnquit',int(s_input(queries.RETURN_QUIT,
                                                          otherterms[0],
                                                          typeflag='int',
                                                          conditions=(2,10),
                                                          returnvalue=self.defaults.get('returnquit'))))
            self.dd_changed=True

        elif mainterm in ['resize', 'size', 'sz']:
            self.defaults.set('size',int(s_input(queries.NEW_NOTE_SIZE,
                                                    otherterms[0],
                                                    typeflag='int',
                                                    conditions=(10,300),
                                                    returnvalue=self.defaults.get('size'))))
            self.dd_changed=True
            display.noteprint((labels.SIZE, str(self.defaults.get('size'))))
        elif mainterm in ['flashto','ft']:
            self.side = int(s_input(queries.SIDE,
                                    otherterms[0],
                                    typeflag='int',
                                    conditions=(0,self.sides),
                                    returnvalue=0))
            display.noteprint((labels.SIDE, str(self.side)))

        elif mainterm in ['setsides']:
            while True:
                self.sides = int(s_input(queries.SIDES,
                                        otherterms[0],
                                         typeflag='int',
                                         conditions=(1,10000),
                                         returnvalue=self.sides))
                if self.sides > 0:
                    break
    
            display.noteprint((labels.SIDES, str(self.sides)))

        elif mainterm in ['flexflip']:
            if not self.flexflip:
                self.def_sides = self.sides
                self.flexflip = True
            else:
                self.sides = self.def_sides
                self.flexflip = False
            display.noteprint(('FLEXFLIP',str(self.flexflip)))
        elif mainterm in ['setflipat']:
            while True:
                self.flip_at = int(s_input(queries.FLIP_AT,
                                           otherterms[0],
                                           typeflag='int',
                                           conditions=(0,self.sides+self.flexflip*10-1),
                                           returnvalue=0))
                if self.sides > 0:
                    break
    
            display.noteprint((labels.FLIP_AT, str(self.flip_at)))
                
                


        elif mainterm in ['keytrim']:
            self.defaults.set('keytrim', int(s_input(queries.SET_KEY_TRIM,
                                                       otherterms[0],
                                                       typeflag='int',
                                                       conditions=(0,100),
                                                       returnvalue=self.defaults.get('keytrim'))))
            display.noteprint((labels.KEY_TRIM, str(self.defaults.get('keytrim'))))
            self.dd_changed=True

        elif mainterm in ['texttrim']:
            self.defaults.set('texttrim',int(s_input(queries.SET_TEXT_TRIM,
                                                        otherterms[0],
                                                        typeflag='int',
                                                        conditions=(0,200),
                                                        returnvalue=self.default_dict['texttrim'])))
            display.noteprint((labels.TEXT_TRIM,
                               str(self.defaults.get('texttrim'))))
            self.dd_changed=True


        elif mainterm in ['editnote', 'en']:
            for i_temp in [a_temp for a_temp
                           in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),
                                        many=True)]:
                display.noteprint(self.show(i_temp),
                                  param_width=display.width_needed(self.show(i_temp),
                                                                   self.get_metadata_from_note(i_temp)['size']))
                self.edit(i_temp,{},
                          EMPTYCHAR,
                          changekeys=True,
                          annotate=predicate[0],
                          update_table=True)

        elif mainterm in ['editnotekeys',
                          'enk']:
            for i_temp in [a_temp for a_temp
                           in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),
                                        many=True)]:
                display.noteprint(self.show(i_temp),
                                  param_width=display.width_needed(self.show(i_temp),
                                                                   self.get_metadata_from_note(i_temp)['size']))
                if not self.edit(i_temp,
                                 {},
                                 EMPTYCHAR,
                                 changekeys=True,
                                 changetext=False,
                                 askabort=True,
                                 update_table=True):
                    break
        elif mainterm in ['editnotetext', 'ent']:
            for i_temp in [a_temp for a_temp
                           in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),
                                        many=True)]:
                display.noteprint(self.show(i_temp),
                                  param_width=display.width_needed(self.show(i_temp),
                                                                   self.get_metadata_from_note(i_temp)['size']))
                self.edit(i_temp,{},EMPTYCHAR,annotate=predicate[0],update_table=True)

        elif mainterm in ['link']:
            temp_range = [str(x_temp) for x_temp
                          in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]))]
            
    
            if len(temp_range) > 10:
                display.noteprint((alerts.ATTENTION,
                                   alerts.TOO_LARGE))
            else:
                for x_temp in temp_range:


                    temp_keys = self.get_keys_from_note(x_temp)
                    range_copy = set(temp_range)
                    range_copy.discard(x_temp)
                    temp_keys.update(range_copy)
                    print(temp_keys)
                    self.edit(Index(x_temp),
                              newkeyset=temp_keys,
                              newtext=self.get_text_from_note(x_temp),
                              changekeys=False,
                              changetext=False,
                              update_table=False)

        elif mainterm in ['chain','loop']:
            range_entry = s_input(queries.RANGE_TO_FROM,otherterms[0])
            
            temp_range = [str(x_temp) for x_temp
                          in get_range(range_entry)]

            if len(temp_range) > 1:
                link_from = temp_range[0]
 
                for counter, x_temp in enumerate(temp_range):

                    if counter == 0:
                        temp_keys = self.get_keys_from_note(temp_range[0])
                        temp_keys.add(temp_range[1])
                        self.edit(Index(x_temp),
                                  newkeyset=temp_keys,newtext=self.get_text_from_note(x_temp),
                                  changekeys=False,
                                  changetext=False,
                                  update_table=False)
                    elif counter == len(temp_range)-1:
                        temp_keys = self.get_keys_from_note(temp_range[counter])
                        temp_keys.add(temp_range[counter-1])
                        if mainterm in ['loop']:
                            temp_keys.add(temp_range[0])
                        self.edit(Index(x_temp),
                                  newkeyset=temp_keys,
                                  newtext=self.get_text_from_note(x_temp),
                                  changekeys=False,
                                  changetext=False,
                                  update_table=False)
                    else:
                        temp_keys = self.get_keys_from_note(temp_range[counter])
                        temp_keys.add(temp_range[counter-1])
                        temp_keys.add(temp_range[counter+1])
                        self.edit(Index(x_temp),
                                  newkeyset=temp_keys,
                                  newtext=self.get_text_from_note(x_temp),
                                  changekeys=False,
                                  changetext=False,
                                  update_table=False)


        elif mainterm in ['unlink']:

            range_entry = s_input(queries.RANGE_TO_FROM,otherterms[0])
            temp_range = [str(x_temp) for x_temp
                          in get_range(range_entry)]

            for x_temp in temp_range:
                temp_keys = {k_temp for k_temp
                             in self.get_keys_from_note(x_temp)
                             if not isindex(k_temp)}
                self.edit(Index(x_temp),
                          newkeyset=temp_keys,
                          newtext=self.get_text_from_note(x_temp),
                          changekeys=False,
                          changetext=False,
                          update_table=False)
             

        elif mainterm in ['compress']:
            if longphrase:
                temp_range = [str(a_temp) for a_temp
                            in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),many=True)]
            else:
                temp_range = self.indexes()
                
            self.purge(temp_range)
            self.reduce(temp_range)
        elif mainterm in ['rehome']:
            self.rehome_orphans([str(a_temp) for a_temp
                                 in get_range(s_input(queries.RANGE_TO_FROM,
                                                      otherterms[0]),
                                              many=True)])
        elif mainterm in ['showdel']:
            
            self.last_results = rangelist.range_find([Index(temp_l)
                                                      for temp_l in self.indexes()
                                                      if Index(temp_l) < Index(0)])
            display.noteprint((labels.DELETED,self.last_results))
            self.last_results = self.last_results.replace(LONGDASH,SLASH)



        elif mainterm in ['gc','gocluster']:
            temp_count = int(s_input(queries.CLUSTER,
                                     otherterms[0],
                                     typeflag='int',
                                     conditions=(1,len(self.default_dict['iterators'])),
                                     returnvalue=1)-1)
            if temp_count >= 0 and temp_count < len(self.default_dict['iterators']):
                temp_list = self.default_dict['iterators'][temp_count]
                self.set_iterator(temp_list)

        elif (mainterm in ['permdel']
              and (predicate[0]
                   or (input(queries.SURE) in YESTERMS))):
            temp_counter = 0
            for i_temp in list([Index(n) for n
                                in self.indexes()
                                if Index(n) < Index(0)]):
                temp_counter+=1
                
                self.delete(i_temp)
                print(temp_counter,end=' ')
                
            self.set_iterator(flag=self.defaults.get('setitflag'))
            
        elif mainterm in ['clear'] and (predicate[0]
                                        or (input(queries.SURE)
                                            in YESTERMS)):
            for i_temp in self.indexes():
                self.softdelete(Index(i_temp))
                if input('Go on?') != EMPTYCHAR:
                    break
        elif mainterm in ['undel']:
            if q_input():
                self.undelete()
        elif mainterm in ['addfield']:
            if not predicate[0]:
                self.add_field(s_input(queries.FIELDNAME,otherterms[0]),
                                   [a_temp for a_temp in 
                                    get_range(s_input(queries.RANGE_TO_FROM,otherterms[1]),
                                                 many=True)])
            if predicate[0]:
                fn_temp = s_input(queries.FIELDNAME,otherterms[0])
                temp_range = s_input(queries.STRICT_RANGE_TO_FROM,
                                                 otherterms[1])
                from_temp, to_temp = int(temprange.split(DASH)[0]),int(temprange.split(DASH)[1])
                self.add_field(s_input(queries.FIELDNAME,
                                       otherterms[0]),
                                   [str(a_temp) for a_temp in 
                                    range(from_temp,
                                          to_temp+1)])
                


            self.display_fields()

        elif mainterm in ['fields']:
            self.display_fields()
        elif mainterm in ['deletefield']:
            if not longphrase:
                self.delete_field(s_input(queries.FIELDNAME),
                                  get_range(s_input(queries.RANGE_TO_FROM)))
            elif totalterms == 1:
                self.delete_field(s_input(queries.FIELDNAME,
                                          otherterms[0]))
            elif totalterms == 2:
                self.delete_field(s_input(queries.FIELDNAME,
                                          otherterms[0]),
                                  get_range(s_input(queries.RANGE_TO_FROM,
                                                              otherterms[1])))
            
            self.display_fields()
##            display.noteprint((labels.FIELD,
##                               str(self.show_fields())),
##                              param_is_emb=True)

        elif mainterm in ['undo']:
            if not predicate[0]:
                self.undo()
            else: self.undo_many()


        elif mainterm in ['conflate']:
            inbetween = EMPTYCHAR
            if not (predicate[0]
                    or predicate[1]
                    or predicate[2]
                    or predicate[3]):
                inbetween = {'e':EMPTYCHAR,
                             'b':'|/BREAK/|',
                             'n':'|/NEW/|'}[s_input(queries.EMPTY_BREAK_NEW,
                                                    otherterms[2],
                                                    typeflag='str',
                                                    must_be_in=('e','b','n'))[0].lower()]
            if predicate[1]:
                inbetween += '|/BREAK/|'
            if predicate[2]:
                inbetween += '|/NEW/|'
            if predicate[3]:
                inbetween = s_input(queries.BREAK_MARK,
                                    otherterms[3])
            self.conflate([str(x_temp)
                           for x_temp
                           in get_range(s_input(queries.RANGE_TO_FROM,
                                                otherterms[0]),
                                        many=True)],
                          destinationindex=otherterms[1],
                          inbetween = inbetween)

        elif mainterm in ['cluster']:
            indexlist_temp = [str(x_temp)
                              for x_temp
                              in get_range(s_input(queries.RANGE_TO_FROM,
                                                                          otherterms[0]),many=True)]
            if not indexlist_temp:
                indexlist_temp = None
            if totalterms > 1:
                
                self.cluster(indexlist=indexlist_temp,
                             iterate_over=predicate[0],
                             keycount=int(s_input(queries.KEY_COUNT,
                                                  otherterms[1],
                                                  typeflag='int',
                                                  conditions=(1,30),
                                                  returnvalue=5)),
                             usepurge=predicate[1])
                
            else:
                self.cluster(indexlist=indexlist_temp,
                             iterate_over=predicate[0],
                             usepurge=predicate[1])
            if predicate[0]:
                self.show_iterators()

        elif mainterm in ['descendents']:
            if longphrase:
                temp_entry = s_input(queries.INDEX_OR_RANGE,otherterms[0])
                if DASH not in temp_entry and COMMA not in temp_entry:
                    self.iterate_over_descendents(self.group_into_descendents(self.all_descendents(temp_entry,as_index=False)))
                    self.parent = temp_entry
                    self.display_attributes = (self.show_full_top,
                                               self.children_too)
                    self.show_full_top = False
                    self.children_too = False
                    try:
                        self.set_iterator(nextiterator=True,
                                          flag=self.defaults.get('setitflag'))
                    except AttributeError:
                        display.noteprint((alerts.ATTENTION,
                                           alerts.NOT_YET_CLUSTERED))
                else:
                    temp_range = get_range(temp_entry,many=True)
                    temp_range = [str(x_temp)
                                  for x_temp
                                  in temp_range]
                    self.iterate_over_descendents(self.group_into_descendents(temp_range))
                    self.parent = EMPTYCHAR
                    self.show_full_top,self.children_too = self.display_attributes[0],self.display_attributes[1]
                    
                
            else:
                self.iterate_over_descendents(self.group_into_descendents())
                self.parent = EMPTYCHAR
                self.show_full_top,self.children_too = self.display_attributes[0],self.display_attributes[1]
        elif mainterm in ['cpara']:
            temp_entry = EMPTYCHAR
            if not predicate[0] and not predicate[1] and not predicate[2]:
                if not otherterms[1]:
                    temp_entry = input(queries.WHAT_TO_PURGE).lower()
                else:
                    temp_entry = otherterms[1]
            
            
            self.all_cap_purge = predicate[0] or 'a' in temp_entry
                #  $ to exclude all-cap keywords
            self.first_cap_purge = predicate[1] or 'c' in temp_entry
            self.lower_case_purge = predicate[2] or 'l' in temp_entry

            
                # & to exclude capitalized keywords
            self.purgelist = s_input(queries.OTHERS_TO_PURGE,
                                     otherterms[0]).split(COMMA)

        elif mainterm in [SEMICOLON]:
            try:
                self.set_iterator(nextiterator=True,flag=self.defaults.get('setitflag'))
            except AttributeError:
                display.noteprint((alerts.ATTENTION,
                                   alerts.NOT_YET_CLUSTERED))
        elif mainterm in ['setlongmax']:

            self.longmax  = si_input(prompt=queries.LONG_MAX,
                                                      inputtext=otherterms[0],
                                                      inputrange=range(0,1000),
                                                      alert=(alerts.ATTENTION,
                                                             labels.MUST_BE_BETWEEN+'10'+labels.AND+'1000'))

            display.noteprint((queries.LONG_MAX,
                               str(self.longmax)))
            
        elif mainterm in ['smallsize']:

            self.defaults.set('smallsize',si_input(prompt=queries.SMALL_SIZE,
                                                      inputtext=otherterms[0],
                                                      inputrange=range(0,501),
                                                      alert=(alerts.ATTENTION,
                                                             labels.MUST_BE_BETWEEN+'10'+labels.AND+'500')))
            display.noteprint((labels.SMALL_SIZE,str(self.default_dict['smallsize'])))
            self.dd_changed=True
            
            
                                                      
        elif mainterm in ['showuser']:
            display.noteprint(('USER',
                               self.defaults.get('user')))

        elif mainterm in ['newkeys']:
            
            if not otherterms[0]:
                self.default_dict['keymacros'].show_kd()
            if not predicate[0]:
                self.defaults.set('defaultkeys',list(self.default_dict['keymacros']\
                                                 .get_definition(s_input('Key macro? ',
                                                                         otherterms[0]))))
                self.dd_changed=True
            else:
                self.defaults.set('defaultkeys',self.defaults.get('defaultkeys')+list(self.default_dict['keymacros']\
                                                        .get_definition(s_input('Key macro? ',
                                                                                otherterms[0]))))
                self.dd_changed=True 
        elif mainterm in ['header','footer','leftmargin']:
            
            self.defaults.set(mainterm,min([max([int(s_input(mainterm+QUESTIONMARK,
                                                                otherterms[0],
                                                                typeflag='int',
                                                                conditions=(0,20),
                                                                returnvalue=0)),0]),10]))
            self.dd_changed=True
            
            display.noteprint(('/C/'+mainterm.upper(),
                               str(self.default_dict[mainterm])))
        elif mainterm in ['deeper','shallower']:

            if mainterm == 'deeper':
                self.iterator.deeper()
            else:
                self.iterator.shallower()
            
            display.noteprint((labels.DEPTH,
                               str(self.iterator.level)))            
        elif mainterm in ['updateuser']:
            self.update_user(s_input(queries.OLD_USER,
                                     otherterms[0]),
                             s_input(queries.NEW_USER,
                                     otherterms[1],
                                     typeflag='str',
                                     returnvalue='user'))
        elif mainterm in ['updatesize']:
            sourcerange = get_range(s_input(queries.RANGE_TO_FROM,
                                            otherterms[0]))
            self.update_size(sourcerange, int(s_input(queries.NEW_NOTE_SIZE,
                                                      otherterms[1],
                                                      typeflag='int',
                                                      conditions=(10,300),
                                                      returnvalue=60)))

        elif mainterm in ['testdate']:
            self.find_dates_for_keys_in_indexes(determinant='ymd')
            self.show_date_dictionary(determinant='ymd')

        elif mainterm in ['changeuser']:
            display.noteprint(('USER',
                               self.defaults.get('user')))
            self.defaults.set('user',s_input('User? ',
                                             otherterms[0],
                                             returnvalue=self.defaults.get('user')))
            self.dd_changed=True
            self.configurations = Configuration(self.defaults.get('user'))
            display.noteprint(('USER',
                               self.defaults.get('user')))
 
        elif mainterm in ['formout']:
            if not otherterms[1]:
                get_file_name(file_path=os.altsep + 'textfiles',
                              file_suffix='txt',
                              justshow=True)
            self.format_output(selection=[str(x_temp) for x_temp
                                          in get_range(s_input('RANGE?',
                                                           otherterms[0]),True,
                                                       False,
                                                       sort=True,
                                                       many=True)],
                               saveyes=not predicate[2],
                               filename=(s_input(queries.SAVE_TO,
                                                 otherterms[1])),
                               metashow=(predicate[0]
                                         or s_input(queries.INCLUDE_META,
                                                    otherterms[2],
                                                    typeflag='str',
                                                    must_be_in=YESTERMS+NOTERMS,
                                                    returnvalue='no') in YESTERMS),
                               index_data=(predicate[1]
                                           or s_input(queries.SHOW_INDEXES,
                                                      otherterms[3],
                                                      must_be_in=YESTERMS+NOTERMS,
                                                      returnvalue='no') in YESTERMS),
                               include_project=(predicate[3] or s_input(queries.INCLUDE_PROJECTS,
                                                                        otherterms[4],
                                                                        typeflag='str',
                                                                        must_be_in=YESTERMS+NOTERMS,
                                                                        returnvalue='no' in YESTERMS)))
        elif mainterm in ['findwithin']:
            print(self.find_within(s_input(queries.FROM,
                                           otherterms[0]),
                                   s_input(queries.TO,
                                           otherterms[1]),
                                   orequal=predicate[0]))
        elif mainterm in ['inspect']:
            temp_entry = s_input(queries.INDEX,
                                 otherterms[0],
                                 typeflag='index')
            if self.notebook_contains(temp_entry):
                print()
                print()
                print('****KEYSET****')
                print(str(self.get_keys_from_note(temp_entry)))
                print()
                print('****TEXT****')
                print(self.get_text_from_note(temp_entry).replace(EOL,'|'))
                print()
                print('****META****')
                print(str(self.get_metadata_from_note(temp_entry)))
                print()
                print()
        elif mainterm in ['updatetags']:
            for i_temp in self.indexes():             
                self.add_keys_tags(0,self.get_keys_from_note(i_temp),
                                   addkeys=False)
        elif mainterm in ['showmeta']:
            noteindex = s_input(queries.INDEX,
                                otherterms[0],
                                typeflag='index')
            if noteindex  in self.indexes():              
                display.noteprint((labels.METADATA+str(noteindex),
                                   nformat.format_meta(self.showmeta(Index(noteindex)))),
                                  param_is_emb=True)
        elif mainterm in ['depth']:
            self.iterator.change_level(int(s_input(queries.CHILD_DEPTH,
                                                   otherterms[0],
                                                   typeflag='int',
                                                   conditions=(0,10000),
                                                   returnvalue=0)))
            display.noteprint((labels.DEPTH, str(self.iterator.level)))
        elif mainterm in ['indentmultiplier']:
            while True:
                mult_temp = int(s_input(queries.INDENT_MULTIPLIER,
                                        otherterms[0],
                                        typeflag='int',
                                        conditions=(0,20),
                                        returnvalue=0))
                if 0 <= mult_temp <= 20:
                    break

            self.defaults.set('indentmultiplier',mult_temp)
            self.dd_changed=True
            display.noteprint((labels.INDENT_MULTIPLIER, str(self.default_dict['indentmultiplier'])))
            
        elif mainterm in ['delete', 'del', 'd']:
            todeleterange = get_range(s_input(queries.DELETE_FROM_TO,
                                          otherterms[0]),
                                      True,
                                      False,
                                      sort=True,
                                      many=True)
            temp_counter = 0
            for td_temp in todeleterange:
                temp_counter+=1
                if temp_counter % 20 == 0:
                    print(temp_counter, end=' ')
                
                
                self.softdelete(td_temp, withchildren=True)
        elif mainterm in ['killchild']:
            
            self.softdelete(Index(s_input(queries.CHILD_KILL,
                                          otherterms[0],
                                          typeflag='index')))
        elif mainterm in ['all']:
            if not otherterms[0]:
                l_temp = 0
            else:
                try:
                    l_temp = int(s_input(queries.LEVELS_TO_SHOW,
                                         otherterms[0],
                                         typeflag='int',
                                         conditions=(0,1000),
                                         returnvalue=0))
                except:
                    l_temp = 0
            self.showall(show_date=self.default_dict['showdate'] or predicate[4],
                         quick=not predicate[0],childrentoo=not predicate[1],levels=l_temp,brackets=not predicate[2],
                         shortshow=not predicate[3])

        elif mainterm in [DOLLAR]:
          self.default_dict['display'].present()
        elif mainterm in [DOLLAR+DOLLAR]:
            show_list(allnotebooks[notebookname].default_dict['all'],'INDEXES',0,40,func=dummy,present=True)
        elif mainterm in ['show', 's']:
            
            if not otherterms[1]:
                l_temp = 0
            else:
                try:
                    l_temp = int(s_input(queries.LEVELS_TO_SHOW,
                                         otherterms[1],
                                         typeflag='int',
                                         conditions=(0,500),
                                         returnvalue=0))
                except:
                    l_temp = 0
            self.showall(get_range(s_input(queries.RANGE_TO_FROM,
                                  otherterms[0]),
                         orequal=True,
                         complete=False, 
                         sort=True,
                         many=True),
                show_date=(self.defaults.get('showdate') or predicate[4]),
                childrentoo=not predicate[1],
                levels=l_temp,
                brackets=not predicate[2],
                         shortshow=not predicate[3])
    
        elif mainterm in ['histogram']:

            self.histio = histogram(displayobject=display)

            if predicate[1]:
                if not self.using_database:
                    self.histio.load_dictionary(entrydictionary=self.key_dict)
                else:
                    self.histio.load_dictionary(flag='t'+('n'*predicate[2]))
            
            elif predicate[0]:
                if not self.using_database:
                    self.histio.load_dictionary(entrydictionary=self.key_dict)
                else:
                    self.histio.load_dictionary(flag='k'+('n'*predicate[2]))
            else:                
                if not self.using_database:
                    self.histio.load_dictionary(entrydictionary=self.word_dict)
                else:
                    self.histio.load_dictionary(flag='w'+('n'*predicate[2]))
                
            self.histio.contract([str(x_temp) for x_temp in get_range(s_input('Range from / to',
                                                                              otherterms[0]),many=True)])
            self.histio.show()

        elif mainterm in ['keysfortags']:

            temp_tags = set()
            if longphrase:
                    temp_range = {str(x_temp) for x_temp in get_range(s_input('Range from? ',
                                                                              otherterms[0]),
                                                                              orequal=True,
                                                                              complete=False,
                                                                              sort=True,
                                                                              many=True)}                    
                    temp_keys = {x_temp for x_temp in self.keys() if self.get_indexes_for_key(x_temp).intersection(temp_range)}
                    temp_tags = {x_temp for x_temp in self.tags() if self.get_keys_for_tag(x_temp).intersection(temp_keys)}
            self.histio = histogram(displayobject=display,for_indexes=False)
            if not self.using_database:
                self.histio.load_dictionary(entrydictionary=self.tag_dict)
            else:
                self.histio.load_dictionary(flag='t')
                
            if temp_tags:
                self.histio.implode(temp_tags)
            self.histio.show()
        elif mainterm in ['terms',QUESTIONMARK+QUESTIONMARK+QUESTIONMARK]:
            display.noteprint((EMPTYCHAR,formkeys(self.new_search(s_input(queries.SEARCH_PHRASE,otherterms[0]))[2])))
        elif mainterm in ['indexes',
                          'ind',
                          'i']:            
            if otherterms[0]:
                if predicate[0]:
                    display.noteprint((labels.INDEXES,
                                       nformat.format_keys(sorted([x_temp for x_temp in self.indexes()
                                                                   if x_temp
                                                                   in get_range(s_input(queries.RANGE_TO_FROM,
                                                                                        otherterms[0]),many=True)]))))
                else:
                    display.noteprint((labels.INDEXES,
                                       rangelist.range_find([int(Index(x_temp))
                                                             for x_temp in self.indexes()
                                                             if x_temp in get_range(s_input('Range from / to',
                                                                                            otherterms[0]),
                                                                                    many=True)],reduce=True)))
            else:
                if predicate[0]:
                    display.noteprint((labels.INDEXES,
                                       nformat.format_keys(str(self.default_dict['indexlist']).split(COMMA+BLANK))))
                else:
                    display.noteprint(('TOTAL # of INDEXES',str(len(self.indexes()))))
                    if not predicate[1]:
                        display.noteprint((labels.INDEXES,
                                           rangelist.range_find([int(Index(i_temp))
                                                                 for i_temp in self.indexes()],reduce=True)))

        elif mainterm in ['reform']:
            if longphrase:

                indexrange = get_range(s_input(queries.RANGE_TO_FROM,
                                               otherterms[0]))
                self.reform(indexrange)
            else:
                self.reform()

        elif mainterm in ['override']:
            override = not override
            show_setting('/C/OVERRIDE',override)

        elif mainterm in ['showdepth']:
            display.noteprint((labels.MAX_DEPTH,
                               str(self.deepest(is_string=True))))
            display.noteprint((labels.MAX_DEPTH+' REDUCED',
                               str(self.deepest(is_string=True,abridged=True))))


        elif mainterm in ['refreshfreq']:

            self.constitute_key_freq_dict()
            display.noteprint((labels.CONSTITUTING_KEY_FREQ, EMPTYCHAR))
        elif mainterm in ['cleardatedict']:
            if predicate[0] or predicate[1] or predicate[2] or predicate[3]  or longphrase:
                determinant = EMPTYCHAR
                determinant = predicate[0]*'y' + predicate[1]*'m' + predicate[2]*'d' + predicate[3]*'*h'
                
                if not determinant:
                    determinant = s_input(labels.DETERMINANT,
                                          otherterms[0])
            else:
                determinant = self.default_dict['determinant']
            del self.default_dict['date_dict'][determinant]
            self.dd_changed=True
        elif mainterm in ['multi']:
              # PREDICATE 0 
              # PREDICATE 1
              # PREDICATE 2 VARY 
              # PREDICATE 3 PAUSE
              # PREDICATE 4 SAVE 
              # otherterms[0] INDEX RANGE
              # otherterms[1] DISPLAY STREAM
              # otherterms[2] WIDTH
         

                    
            t_size = 180
            if totalterms >2 and (otherterms[2] == EMPTYCHAR or otherterms[2] or predicate[0]):
                t_size = int(s_input(queries.WIDTH,
                                     otherterms[2],
                                     typeflag='int',
                                     conditions=(40,450),
                                     returnvalue=180))
            if  t_size < 40 or t_size > (450):
                t_size = 180
            display.noteprint((labels.SIZE,str(t_size)))
            if totalterms == 1 or not otherterms[1]:
                display_stream = 'standard'
               
                multi_dict[notebookname][display_stream] = Note_Display(t_size)
            else:
                display_stream = s_input(queries.DISPLAY_STREAM,
                                         otherterms[1])
                if display_stream not in multi_dict[notebookname].keys():
                    if not otherterms[2]:
                        otherterms[2] = '0'
                    multi_dict[notebookname][display_stream] = Note_Display(t_size)
            self.showall(entrylist=get_range(s_input(queries.RANGE_TO_FROM,
                                                     otherterms[0]),
                                             True,
                                             False,
                                             sort=True,
                                             many=True),
                         multi=True,
                         output=multi_dict[notebookname][display_stream],
                         vary=predicate[2],
                         show_date=self.default_dict['showdate'],
                         curtail={True:self.default_dict['smallsize'],
                                  False:0}[predicate[0]])
            save_stream = display_stream
            if otherterms[3]:
                save_stream = otherterms[3]
            self.text_result = multi_dict[notebookname][display_stream].print_all(pause=predicate[3],
                                                 show=not predicate[4],
                                                 save=predicate[4],
                                                 filename=save_stream)


        elif mainterm in ['sheet']:
            t_size = 2000
            if totalterms >2 and (otherterms[2] == EMPTYCHAR or otherterms[2] or predicate[0]):
                t_size = int(s_input(queries.WIDTH,
                                     otherterms[2],
                                     typeflag='int',
                                     conditions=(500,10000),
                                     returnvalue=2000))
            if  t_size < 500 or t_size > (10000):
                t_size = 2000
            display.noteprint((labels.SIZE,str(t_size)))
            if totalterms == 1 or not otherterms[1]:
                display_stream = 'sheet'
               
                multi_dict[notebookname][display_stream] = Note_Display(t_size)
            else:
                display_stream = s_input(queries.DISPLAY_STREAM,
                                         otherterms[1])
                if display_stream not in multi_dict[notebookname].keys():
                    if not otherterms[2]:
                        otherterms[2] = '0'
                    multi_dict[notebookname][display_stream] = Note_Display(t_size)
 
            save_stream = display_stream
            if otherterms[3]:
                save_stream = otherterms[3]


            if predicate[2] and self.sheet_buffer:
                textlist = self.sheet_buffer.split(EOL)
                display.noteprint(('ATTENTION!','RESUMING SHEET'))
            else:
                self.showall(entrylist=get_range(s_input(queries.RANGE_TO_FROM,
                                                 otherterms[0]),
                                         True,
                                         False,
                                         sort=True,
                                         many=True),
                     multi=True,
                     output=multi_dict[notebookname][display_stream],
                     vary=predicate[2],
                     show_date=self.defaults.get('showdate'),
                     curtail={True:self.defaults.get('smallsize'),
                              False:0}[predicate[0]])
                self.text_result = multi_dict[notebookname][display_stream].print_all(pause=predicate[3],
                                     show=False,
                                     save=True,
                                     filename=save_stream)
                self.sheet_buffer = self.text_result
                textlist = self.text_result.split(EOL)

            y_max = self.x_max
            x_max = self.y_max
            if otherterms[4] and '*' in otherterms[4]:
                display.noteprint(('SHEET SIZE',otherterms[4]))
                y_max = otherterms[4].split('*')[0]
                x_max = otherterms[4].split('*')[1]
                try:
                    x_max = int(x_max)
                    y_max = int(y_max)
                    display.noteprint(('','SHEET SIZE = '+str(y_max)+'/'+str(x_max)))
                except:
                    pass
            display.noteprint(('STARTING LOCATION', str(self.y_pos)+'/'+str(self.x_pos)))

            self.window = movingwindow.MovingWindow(self.text_result.split(EOL))
            try:
                self.y_pos,self.x_pos,dummy1,dummy3 = self.window.activate(y_max=y_max,x_max=x_max,y_pos=self.y_pos,x_pos=self.x_pos)
            except:
                self.window.restore()
                

        elif mainterm in ['rsheet','resumesheet']:
            if self.window:
                try:
                    self.y_pos,self.x_pos = self.window.activate()
                except:
                    self.window.restore()
        elif mainterm in ['createworkpad']:
            if otherterms[0] and otherterms[0] not in self.pad_dict:
                padname = otherterms[0]
            else:
                padname = 'default'
                c_temp = 1
                suffix = ''
                while True:
                    if padname+suffix not in self.pad_dict:
                        break
                    suffix = str(c_temp)
                    c_temp += 1
                self.pad_dict[padname+suffix] = emptymovingwindow.EmptyMovingWindow()
                display.noteprint(('NEW PAD CREATED!',padname+suffix))
                display.noteprint(('ALL PADS',', '.join(self.pad_dict.keys())))
                self.currentpad = padname+suffix

        elif mainterm in ['emptypadstack']:

            bufferpad = self.currentpad
            if otherterms[0] and otherterms[0] in self.pad_dict.keys():
                self.currentpad = otherterms[0]
                
            self.pad_dict[self.currentpad].empty_stack()

                
            self.currentpad = bufferpad

        elif mainterm in ['renewpad']:
            
            bufferpad = self.currentpad
            if otherterms[0] and otherterms[0] in self.pad_dict.keys():
                self.currentpad = otherterms[0]

            if input('Are you sure? This will delete all data in pad?') in YESTERMS:
                self.pad_dict[self.currentpad] = emptymovingwindow.EmptyMovingWindow()
               
            self.pad_dict[self.currentpad].empty_stack()

                
            self.currentpad = bufferpad


            
            
            
        
        elif mainterm in ['addtopad','a']:
            bufferpad = self.currentpad
            if otherterms[1] and otherterms[1] in self.pad_dict.keys():
                self.currentpad = otherterms[1]
                
            if otherterms[0]:

                for i_temp in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),many=True):
                    
                    note_temp = display.noteprint(self.show(i_temp),
                                                  np_temp=True)
                    self.pad_dict[self.currentpad].import_note(i_temp,note_temp.split(EOL),full_note=self.get_text_from_note(i_temp),keyset=self.get_keys_from_note(i_temp))
                display.noteprint(('Objects in Stack!',str(self.pad_dict[self.currentpad].objects_in_stack())))
            self.currentpad = bufferpad

        elif mainterm in ['closesheetshelf']:
            del self.sheetshelf
        elif mainterm in ['tosheetshelf']:
            if not self.sheetshelf:
                self.sheetshelf = SheetShelf(self.directoryname,notebookname,display=display)
        
            from_name = otherterms[0]
            if not from_name:
                from_name = self.currentpad
            to_name = otherterms[1]
            if not to_name:
                to_name = self.currentpad
            if not predicate[0]:
                l_temp = list(self.pad_dict[from_name].textlist)
                d_temp = copy.deepcopy(self.pad_dict[from_name].object_dict)
                
                
                
                self.sheetname = self.sheetshelf.add(notebookname=notebookname,
                                                     objectname=to_name,
                                                     textlist = l_temp,
                                                     object_dict = d_temp)
                del l_temp
                del d_temp

        elif mainterm in ['selectsheet']:
            if not self.sheetshelf:
                self.sheetshelf = SheetShelf(self.directoryname,notebookname,display=display)
            to_name = otherterms[0]
            while True:
                
                if not to_name:
                    to_name = 'default'
                if to_name in self.pad_dict:
                    display.noteprint(('ATTENTION!',to_name+' exists'))
                    if input('OK to overwrite') in YESTERMS:
                        break
            temp_obj, self.sheetname = self.sheetshelf.select()

            self.pad_dict[to_name] = emptymovingwindow.EmptyMovingWindow(textlist=temp_obj[0],object_dict=temp_obj[1])
            display.noteprint(('NEW PAD CREATED!',to_name))
            display.noteprint(('ALL PADS',', '.join(self.pad_dict.keys())))
            self.currentpad = to_name
        elif mainterm in ['keyin']:
            size_old = self.defaults.get('size')
            temp_pad = emptymovingwindow.EmptyMovingWindow()
            dummy_y, dummy_x, returned_object, dummy_text = temp_pad.activate(entering=True)
            for obj_identifier in sorted(returned_object.keys()):

                if obj_identifier.startswith('$') and obj_identifier.count('$') == 1:
                    if 'oo' in returned_object[obj_identifier]:
                        newobject_text = '\n'.join(returned_object[obj_identifier]['oo'])
                        if 'l' in returned_object[obj_identifier]:
                            newobject_keyset = returned_object[obj_identifier]['l']
                        obj_identifier = obj_identifier.lstrip('$')
                        if newobject_text:
                            self.defaults.set('size',len(newobject_text[0]))
                        
                        self.enter(ind=Index(obj_identifier),ek=newobject_keyset,et=newobject_text,right_at=True)
            self.defaults.set('size',size_old)
        elif mainterm in ['showpad']:

            def reduce_blanks (x,starting=True):
                if starting:
                    while '  ' in x:
                        x = x.replace('  ',' ')
                    return x
                else:
                    for position, xx in enumerate(x):
                        if xx != ' ':
                            break
                    if len(x) > position:

                        while '  ' in x[position:]:
                            x = x[:position]+x[position:].replace('  ',' ')
                        return x
                return x        
                        
                    

            
            bufferpad = self.currentpad
            if otherterms[0] in self.pad_dict.keys():
                self.currentpad = otherterms[0]
            
            
            if self.pad_dict[self.currentpad]:
                try:
                    display.noteprint(('ACTIVATING',self.currentpad))
                    self.pad_y_pos, self.pad_x_pos,returnedobjects,returnedtextlist, self.text_result = self.pad_dict[self.currentpad].activate(y_pos=self.pad_y_pos,
                                                                                                                                                x_pos=self.pad_x_pos)
                except:
                    self.pad_dict[self.currentpad].restore()

            for obj_identifier in sorted(returnedobjects.keys()):

                

                if obj_identifier.startswith('$$$') and obj_identifier.count('$') == 3:
                    if 'oo' in returnedobjects[obj_identifier]:
                        newobject_text = ''

                        # The following needed to return to original formatting...
                        # Probably should have conceived the text editor differently -- not breaking up into lines 
                        for line in returnedobjects[obj_identifier]['oo']:
                            if line.startswith('  '):
                                newobject_text += '\n' + reduce_blanks(line,starting=False)
                            elif len(line.strip()) == 0:
                                newobject_text += '\n'                          
                            else:
                                newobject_text += reduce_blanks(' ' + line + ' ')

                        if newobject_text.startswith('\n'):
                            newobject_text = nextobject_text[1:].replace('     ','!@#$%').replace('  ',' ').replace('!@#$%','     ')
                            
 
                        if 'l' in returnedobjects[obj_identifier]:
                            newobject_keyset = returnedobjects[obj_identifier]['l']
                        obj_identifier = obj_identifier.lstrip('$$$')
                        self.edit(index=Index(obj_identifier),
                                  newkeyset=newobject_keyset,
                                  newtext=newobject_text,
                                  changekeys=False,
                                  changetext=False)                    

                if obj_identifier.startswith('$') and obj_identifier.count('$') == 1:
                    if 'oo' in returnedobjects[obj_identifier]:
                        newobject_text = '\n'.join(returnedobjects[obj_identifier]['oo'])

                        if 'l' in returnedobjects[obj_identifier]:
                            newobject_keyset = returnedobjects[obj_identifier]['l']
                        obj_identifier = obj_identifier.lstrip('$')
                        self.enter(ind=Index(obj_identifier),ek=newobject_keyset,et=newobject_text,right_at=True)
            if input('Do you want to reclassify uploaded objects?') in YESTERMS:
                
                self.pad_dict[self.currentpad].transform_dictionary(fromprefix='$',toprefix='$$')
                self.pad_dict[self.currentpad].transform_dictionary(fromprefix='$$$',toprefix='$$')
            if input('Do you want to update sheetshelf?') in YESTERMS:
                if not self.sheetshelf:
                    self.sheetshelf = SheetShelf(self.directoryname,notebookname,display=display)
                    if not self.sheetname:
                        self.sheetname = notebookname + self.currentpad
                    
                print(self.sheetname)
                self.sheetshelf.add(notebookname='',
                                    objectname=self.sheetname,
                                    textlist = returnedtextlist,
                                    object_dict = returnedobjects,override=True)

                    
                
                        
                    
            self.currentpad = bufferpad
            display.noteprint(('',self.pad_dict[self.currentpad].show_notes()))
            
        elif mainterm in ['showstream']:
            if not longphrase:
                display_stream = 'standard'
            else:
                display_stream = s_input(queries.DISPLAY_STREAM,
                                         otherterms[0])
            if display_stream in multi_dict[notebookname].keys():
                multi_dict[notebookname][display_stream].print_all(pause=predicate[3])

            

        elif mainterm in ['constdates','constitutedates','makedates']:
            
            
            if predicate[0] or predicate[1] or longphrase:

                determinant = EMPTYCHAR
                if predicate[0]:
                    determinant = 'ym'
                if predicate[1]:
                    determinant = 'ymd'

                if not determinant:
                    display.noteprint((labels.DETERMINANT,formkeys(DETERMINANTS)))
                    determinant = s_input(queries.DETERMINANT2,
                                          otherterms[1])
            else:
                determinant = self.defaults.get('determinant')

            if determinant in self.default_dict['date_dict']:
                self.default_dict['date_dict'][determinant].clear()
                self.dd_changed=True
            flag = 'i' * predicate[2]
            if otherterms[2] or predicate[3]:
                
                flag += s_input(queries.FIRST_NEWEST_ALL,otherterms[2])
            self.find_dates_for_keys_in_indexes(entrylist=[str(x_temp) for x_temp
                                                           in get_range(s_input('Range from / to',
                                                                                otherterms[0]),
                                                                        many=True)],
                                                determinant=determinant,flag=flag)
            self.show_date_dictionary(determinant=determinant)
        elif mainterm in ['showdatedict']:
            determinant = EMPTYCHAR
            if predicate[0] or predicate[1] or predicate[2] or predicate[3] or predicate[4]: 
                if predicate[0]:
                    determinant += 'y'
                if predicate[1]:
                    determinant += 'm'
                if predicate[2]:
                    determinant += 'd'
                if predicate[3]:
                    determinant += '*h'
                    if predicate[4]:
                        determinant+='m'
                
            elif longphrase:
                determinant = s_input(queries.DETERMINANT2,
                                      otherterms[0])
            else:
                determinant = self.defaults.get('determinant')
                
            self.show_date_dictionary(determinant=determinant)
            
        elif mainterm in ['actdet','activedet']:
            display.noteprint((labels.DETERMINANT,
                               formkeys(self.default_dict['date_dict'].keys())))
                    
        elif mainterm in ['showdatedictpurge']:
            
            determinant = EMPTYCHAR
             
            if predicate[3] or otherterms[1]:

                self.default_dict['purge'].clear()
                self.dd_changed=True
                to_purge = s_input(queries.PURGE_WHAT,
                                   otherterms[1]).split(VERTLINE)
                specs = to_purge[0]
                terms = []
                if len(to_purge) > 1:
                    terms = to_purge[1].split(COMMA)
                    
                nprint('SPECS',specs,terms)
                if 'a' in specs:
                    self.default_dict['purge'].allcaps()
                if 'u' in specs:
                   self.default_dict['purge'].caps()
                if 'l' in specs:
                    self.default_dict['purge'].lower()
                if 's' in specs:
                    self.default_dict['purge'].sequences()
                if 'n' in specs:
                    self.default_dict['purge'].numbers()

                if terms:
                    for term in terms:
                        if len(term) > 1:
                            termset = self.new_search(term,onlyterms=True)
                            self.default_dict['purge'].load(termset)


            if predicate[0] or predicate[1] or predicate[2] or longphrase or otherterms[0]:


                if predicate[0]:
                    determinant = 'ym'
                if predicate[1]:
                    determinant = 'ymd'

                if predicate[2]:
                    determinant += '*h'
                
                if not determinant:
                    determinant = s_input(queries.DETERMINANT,
                                          otherterms[0])
                    
            if not determinant:
                determinant = self.defaults.get('determinant')
                self.dd_changed=True


            self.show_date_dictionary(determinant=determinant,func=self.default_dict['purge'].apply)

        elif mainterm in ['grabkeys', 'grabdefaultkeys', 'grabautokeys']:
            grabrange = get_range(s_input(queries.RANGE_FROM+BLANK,
                                          otherterms[0]),
                                  orequal=True,
                                  complete=False,
                                  sort=True,
                                  many=True)
            grabbed = self.grab_keys(grabrange,
                                     all_caps=not predicate[0],
                                     first_caps=not predicate[1])
            display.noteprint((labels.GRABBED_KEYS,
                               formkeys(grabbed)))
            if input(queries.ADD_TO_AUTOKEYS) in YESTERMS:
                self.defaults.set('defaultkeys',self.defaults.get('defaultkeys')+list(grabbed))
                self.dd_changed=True
                if predicate[2]:
                    key_macro_name = input(queries.KEY_MACRO_NAME)
                    self.default_dict['keymacros'].add(key_macro_name,list(grabbed))
                    self.dd_changed=True
                    
            display.noteprint((labels.DEFAULT_KEYS,
                               formkeys(self.defaults.get('defaultkeys'))))
            
        elif mainterm in ['help']:


            if not helploaded:
                for counter, cs_temp in enumerate(commandscript.COMMANDSCRIPT):

                    commandlist[counter] = DisplayList(displayobject=display)
                    nformat.columns(commandscript.COMMANDSCRIPT[counter],
                                    commandlist[counter],
                                    columnwidth=(37,45,60,30,30),
                                    compactwidth=None)

                


            
            
            if longphrase:

                if not otherterms[0].isnumeric():
                    helpdisplay = DisplayList(displayobject=display)
                    i_temp = s_input(queries.WHICH_COMMAND, otherterms[0])
                    if i_temp in commandscript.HELP_DICTIONARY:


                        helptext = (EOL+'/BREAK/'+EOL).join(commandscript.HELP_DICTIONARY[i_temp])
                        display.noteprint(('/C/'+ labels.COMMAND_EQ + i_temp,
                                          helptext))
                                                    

                else:
                    if 0 < int(otherterms[0]) < (len(commandscript.HEADERS) + 1):
                        commandlist[int(otherterms[0])-1].show(header=commandscript.HEADERS[int(otherterms[0])-1],
                                                     centered=True)
                        
            else:
                see_more = True
                counter = 0
                while see_more:
                    which_menu=counter%len(commandscript.HEADERS)
                    commandlist[which_menu].show(header
                                                =commandscript.HEADERS[which_menu],
                                                centered=True)
                    i_temp = input(queries.MENU_ONE)
                    if i_temp in [EMPTYCHAR, RIGHTNOTE]:
                        counter += 1
                    if i_temp == LEFTNOTE:
                        counter -= 1
                    if i_temp in QUITTERMS + (BLANK, SLASH):
                        see_more = False


        elif mainterm in ['showsequences']:
            seqlist= DisplayList(displayobject=display)
            temp_text = []
            for counter, seq in enumerate(self.default_dict['sequences']):
                if seq != '#TYPE#':
                    temp_line = str(counter) + VERTLINE + seq + VERTLINE
                    from_to_temp = abridge(str(self.default_dict['sequences'][seq].ends()[0]),11,overmark=EMPTYCHAR) + DASH + \
                                   abridge(str(self.default_dict['sequences'][seq].ends()[1]),11,overmark=EMPTYCHAR) 

                    from_to_temp += (25 - len(from_to_temp))*BLANK 
                    temp_line += from_to_temp + BLANK + SLASH + BLANK
                    len_temp = str(len(self.default_dict['sequences'][seq])) 
                    temp_line += len_temp + (5 - max([4,len(len_temp)])) * BLANK + BLANK + SLASH
                    temp_line += str(type(self.default_dict['sequences'][seq].ends()[0])) 
                    if predicate[0]:
                        temp_line += self.default_dict['sequences'][seq].convert_to_dates()
                    temp_line += VERTLINE 
                    
                    temp_text.append(temp_line)
                
            nformat.columns(EOL.join(temp_text),listobject=seqlist,columnwidth=(4,10,15))
            seqlist.present()

            if input('CORRECT?') in YESTERMS:
                while True:
                    cor_seq = input('Sequence?')
                    if cor_seq == EMPTYCHAR or cor_seq in self.default_dict['sequences']:
                        break
                if cor_seq:
                    del self.default_dict['sequences'][cor_seq]
                    del self.default_dict['sequences']['#TYPE#'][cor_seq]
                    self.dd_changed=True
                    temp_keys = self.new_search('<'+cor_seq+STAR+'>')
                    print(str(temp_keys))
                

                        
    def reformating_com(self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR,predicate=EMPTYCHAR,longphrase=EMPTYCHAR):
        if mainterm in ['mergemany', 'mm']:
            sourcerange = get_range(s_input(queries.SOURCE_TO_FROM,
                                            otherterms[0]),
                                    True, False, sort=True,many=True)
            if otherterms[1]:
                destination = Index(s_input(queries.DESTINATION, otherterms[1]))
            else:
                destination = Index(-1)
            if not predicate[0] and not predicate[1]:
                manner = s_input(queries.CONFLATE_EMBED , otherterms[2])
            if manner in ['C', 'c', 'conflate'] or predicate[0]:
                self.merge_notes(sourcerange,
                                 destination)
            if manner in ['E', 'e', 'embed'] or predicate[1]:
                self.merge_many(sourcerange, destination)
        elif mainterm in ['columns','col']:
            
            convert_temp=s_input(queries.CHARACTERS_TO_CONVERT,otherterms[1])
            if not convert_temp:
                convert_temp = SEMICOLON

            for i_temp in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),many=True):

                self.columnize(str(i_temp),
                               convert_temp,
                               undo=predicate[0],
                               counters=predicate[1] or predicate[2],
                               only_counter=predicate[2])
        elif mainterm in ['split']:
            columns = EMPTYCHAR
            width = EMPTYCHAR           
            breaker = BLANK
            if otherterms[0]:
                index = s_input(queries.INDEX,otherterms[0])
            if otherterms[1]:
                columns = s_input(queries.COLUMNS,otherterms[1])
            if otherterms[2]:
                width = s_input(queries.WIDTH,otherterms[2])
            if otherterms[3]:
                breaker = s_input(queries.BREAKER,otherterms[3])           
            if columns.isnumeric():
                columns = int(columns)
            else:
                columns = 2
            if width.isnumeric():
                width = int(width)
            else:
                width = 60
            if index in self.indexes() and 1<columns<10 and 10<width<300:
                t_temp = self.get_text_from_note(index).replace(UNDERLINE,'#####')
                newtext = split_into_columns (t_temp,breaker=breaker,width=width,columns=columns)
                self.addnew(self.get_keys_from_note(index),newtext)
        elif mainterm in ['sidenote']:
            textlist = []
            lengthlist = []
            factorlist = []
            widthlist = []
            totallength = 0
            keysets = set()

            entries = get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),many=True)
            totalwidth = int(s_input(queries.WIDTH,
                                     otherterms[1],
                                     typeflag='int',
                                     conditions=(5,200),
                                     returnvalue=10))
            if len(entries) > 15:
                display.noteprint((alerts.ATTENTION,alerts.TOO_MANY_INDEXES))
            else:
                for t_temp in entries:
                    if str(t_temp) in self.indexes():
                        tt_temp = self.get_text_from_note(t_temp)
                        tt_temp = nformat.purgeformatting(tt_temp)
                        tl_temp = len(tt_temp)
                        textlist.append(tt_temp)
                        lengthlist.append(tl_temp)
                        totallength += tl_temp
                        keysets.update(self.get_keys_from_note(t_temp))
                for counter, t_temp in enumerate(lengthlist):
                    factorlist.append(lengthlist[counter]/totallength)
                for t_temp in factorlist:
                    widthlist.append(int(totalwidth*t_temp))
                if predicate[0]:
                    widthlist = [5] + widthlist
                newtext = side_note(textlist,widths=widthlist,counters=predicate[0])
                self.addnew(keysets,newtext)            
        elif mainterm in ['revise', 'rev']:            
            breaker = Note(set(),EMPTYCHAR)
            breakertext = EMPTYCHAR
            if otherterms[2]:
                breakertext = s_input (queries.BREAK_MARK,otherterms[2])
                if breakertext.replace(PERIOD,EMPTYCHAR).isnumeric():
                    if breakertext in self.indexes():
                        breaker = self.get_note(breakertext)
                elif breakertext not in BREAKTERMS + NEWTERMS:
                    breaker = Note(set(),breakertext+EOL)
                
            if breakertext in BREAKTERMS + NEWTERMS or predicate[2] or predicate[3]:                
                if predicate[2] or breaker in BREAKTERMS:
                    if not predicate[0] or predicate[1]:
                        breaker = breaker + BREAKNOTE
                    else:
                        breaker = BREAKNOTE + breaker 
                if predicate[3] or breaker in NEWTERMS:
                    if not predicate[0] or predicate[1]:
                        breaker = breaker + NEWNOTE
                    else:
                        breaker = NEWNOTE + breaker
            oldindex_temp = None
            if otherterms[1]:
                oldindex_temp = Index(s_input(queries.INDEX_TO_MERGE,otherterms[1]))
            for i_temp in [a_temp for a_temp
                           in get_range(s_input(queries.RANGE_TO_FROM,otherterms[0]),
                                        many=True)]:
                display.noteprint(self.show(i_temp),
                                  param_width=display.width_needed(self.show(i_temp),
                                                                   self.get_metadata_from_note(i_temp)['size']))
                self.revise(i_temp,
                            oldindex_temp,
                            infront = not predicate[0] or predicate[1],
                            inback = predicate[0] or predicate[1],
                            breaker=breaker)

        elif mainterm in ['helpall']:

            for com_temp in commandscript.HELP_DICTIONARY:

                display.noteprint((EMPTYCHAR,
                                   side_note((com_temp,
                                              commandscript.HELP_DICTIONARY[com_temp][0]\
                                              +labels.NONE*\
                                              (not commandscript.HELP_DICTIONARY[com_temp][0].strip()),
                                             commandscript.HELP_DICTIONARY[com_temp][1]),
                                             widths=[20,60,30])))
                
        elif mainterm in ['correctkeys']:
            if not longphrase:
                self.menu_correct_keys(keysonly=not predicate[0])
            else:
                self.menu_correct_keys(get_range(s_input(queries.SOURCE_TO_FROM,
                                                         otherterms[0]),
                                                 True, False,
                                                 sort=True,
                                                 many=True),keysonly=not predicate[0])
                
    def copy_move_search_com (self,longphrase=False,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR,predicate=EMPTYCHAR):
        
        if mainterm in ['move','copy']:
                    copy_temp = False
                    if mainterm in ['copy']:
                        copy_temp = True
                    sourcerange = get_range(s_input(queries.RANGE_FROM+BLANK,
                                                    otherterms[0]),
                                            orequal=True,
                                            complete=False,
                                            sort=True,
                                            many=True)
                    destinationrange = get_range(s_input(queries.DESTINATION+BLANK,
                                                         otherterms[1]),
                                                 orequal=True,
                                                 complete=True,
                                                 sort=True)

                    subordinate = False
                    all_children = False
                    makecompact = False

                    action = EMPTYCHAR 

                    if not predicate[0] and not predicate[1] and not predicate[2]:

                        action = (s_input(queries.SUB_OR_MAKE_CHILDREN,
                                          otherterms[2])+BLANK)[0]
                        nprint(action)

                    if action in ['S', 's']  or predicate[0]:
                        subordinate = True
                    if action in ['M', 'm'] or predicate[1]:
                        makecompact = True
                    if action in ['C', 'c'] or predicate[2]:
                        all_children = True
                    if not predicate[3] and not predicate[4]:
                        withchildren =  (s_input(queries.NO_CHILDREN, otherterms[3]) not in YESTERMS)
                    else:
                        withchildren = not predicate[3]

                    self.move_many(sourcerange,
                                   destinationrange,
                                   subordinate=subordinate,
                                   makecompact=makecompact,
                                   all_children=all_children,
                                   withchildren=withchildren,
                                   copy=copy_temp)
        elif mainterm in ['search', QUESTIONMARK]:
            sr_temp = self.new_search(self.default_dict['abbreviations'].undo(s_input(queries.SEARCH_PHRASE,
                                              otherterms[0])))
            display.noteprint(('TOTAL RESULTS!',str(len(sr_temp[1]))))
            if self.flipout:
                self.default_dict['flipbook'] = [Index(a_temp)
                                                     for a_temp in sr_temp[1] if a_temp!=0]
                self.dd_changed=True
                self.set_iterator(self.default_dict['flipbook'],flag=self.defaults.get('setitflag'))

            
            self.last_results = rangelist.range_find([Index(a_temp)
                                                     for a_temp in sr_temp[1] if a_temp!=0]).replace(LONGDASH,SLASH)

            display.noteprint((labels.RESULT_FOR
                               +formkeys(sorted(list(sr_temp[2]))),
                               rangelist.range_find([Index(a_temp)
                                                     for a_temp in sr_temp[1]
                                                     if a_temp!=0],
                                                    reduce=True,
                                                    compact=(len(sr_temp[1])>1000)).replace(LONGDASH,SLASH)))
            #formkeys(sorted(list(sr_temp[2])))

            if predicate[0]:
                self.showall(sr_temp[1], highlight=sr_temp[2],show_date=self.defaults.get('showdate'))
            if predicate[1]:
                
                determinant = self.defaults.get('determinant')
                
                if not predicate[2] and determinant in self.default_dict['date_dict']:
                    self.default_dict['date_dict'][determinant].clear()
                    self.dd_changed=True
                
                self.find_dates_for_keys_in_indexes(entrylist=sr_temp[1],
                                                    determinant=determinant,
                                                    flag='i'*predicate[3])
                self.show_date_dictionary(determinant=determinant,
                                          func=self.default_dict['purge'].apply)

        elif mainterm in ['text']:
            results = []
            temp_range = get_range(s_input(queries.RANGE_FROM,
                                           otherterms[0]),
                                   orequal=True,
                                   complete=False,
                                   sort=True,
                                   many=True)
            temp_words = set()
            first=True
            for t_temp in temp_range:
                if not predicate[0]:
                    temp_words = temp_words.union(get_words(self.get_text_from_note(t_temp)))
                else:
                    if first:
                        temp_words = set(get_words(self.get_text_from_note(t_temp)))
                        first = False
                    else:
                        temp_words = temp_words.intersection(get_words(self.get_text_from_note(t_temp)))

            if predicate[1]:
                results += self.most_common_words(words=temp_words,number=int(s_input('How many words?',
                                                                                      otherterms[1],
                                                                                      typeflag='int',
                                                                                      conditions=(1,1000),
                                                                                      returnvalue=5)))
                
            if predicate[2]:
                results += self.most_common_words(words=temp_words,number=int(s_input('How many words?',
                                                                                      otherterms[1]+otherterms[2],
                                                                                      typeflag='int',
                                                                                      conditions=(1,1000),
                                                                                      returnvalue=5)),
                                                  dictionaryobject=frequency_count(temp_words),
                                                  reverse=True)
            if not predicate[1] and not predicate[2]:
                results = temp_words

            display.noteprint(('WORDS in TEXT',', '.join(results)))
            self.key_results = VERTLINE.join(['<'+x_temp.strip()+'>' for x_temp in results])
            
        elif mainterm in ['keys', 'key','k']:
            if not predicate[0] and not predicate[1] \
               and not predicate[2] and not predicate[3]:
                if longphrase:
                        if otherterms[0].replace(DASH,EMPTYCHAR).replace(PERIOD,EMPTYCHAR).replace(SLASH,EMPTYCHAR).isnumeric():

                            temp_rance = set()

                            temp_range = {str(x_temp) for x_temp in get_range(s_input(queries.RANGE_FROM,
                                                                                              otherterms[0]),
                                                                                      orequal=True,
                                                                                      complete=False,
                                                                                      sort=True,
                                                                                      many=True)}
                        else:

                            enter_keys = {x_temp.strip() for x_temp in otherterms[0].split(',')}
                            temp_range = repeat_function_on_set(enter_keys,self.tagkeyindex)
                            
                        if otherterms[1]:
                            if temp_range:
                                enter_keys = {x_temp.strip() for x_temp in otherterms[1].split(',')}
                                temp_range = temp_range.intersection(repeat_function_on_set(enter_keys,self.tagkeyindex))
                            else:
                                enter_keys = {x_temp.strip() for x_temp in otherterms[0].split(',')}
                                temp_range = repeat_function_on_set(enter_keys,self.tagkeyindex)
                                
                            
                        temp_keys = {str(x_temp)
                                     for x_temp in self.keys()
                                     if self.get_indexes_for_key(x_temp).intersection(temp_range)}
                else:
                    temp_keys = self.keys()


                caps = formkeys(sort_keyset(temp_keys)[0])
                propernames = formkeys(sort_keyset(temp_keys)[1])
                otherkeys = formkeys(sort_keyset(temp_keys)[2])
                
                display.noteprint((labels.CAPKEYS,
                                  caps))
                display.noteprint((labels.PROPER_NAMES,
                                   propernames))
                display.noteprint((labels.OTHER_KEYS,
                                   otherkeys))

                self.key_results = VERTLINE.join(['<'+x_temp.split(SLASH)[0].strip()+'>' for x_temp in (propernames+otherkeys).split(',')])
                display.noteprint(('/C/ KEYS',self.key_results.replace(VERTLINE, BLANK+VERTLINE+BLANK)))
                

                


            elif predicate[1] or predicate[2] or predicate[3]:

                implode_list = []
                if predicate[1]:
                    implode_list += sort_keyset(self.keys())[0]
                if predicate[2]:
                    implode_list += sort_keyset(self.keys())[1]
                if predicate[3]:
                    implode_list += sort_keyset(self.keys())[2]

                self.histio = histogram(displayobject=display)
                if not self.using_database:
                    self.histio.load_dictionary(entrydictionary=self.key_dict)
                else:
                    self.histio.load_dictionary(flag='t')
                self.histio.implode(implode_list)

                if longphrase:
                    
                    self.histio.contract([str(x_temp) for x_temp in get_range(s_input('Range from? ',
                                                                                      otherterms[0]),
                                                                              orequal=True,
                                                                              complete=False,
                                                                              sort=True,
                                                                              many=True)])

                self.histio.show()

            else:
                self.histio = histogram(displayobject=display)
                if not self.using_databse:
                    self.histio.load_dictionary(entrydictionary=self.key_dict)
                else:
                    self.histio.load_dictionary(flag='k')
                if longphrase:
                    self.histio.contract([str(x_temp) for x_temp in get_range(s_input('Range from? ',
                                                                                      otherterms[0]),
                                                                              orequal=True,
                                                                              complete=False,
                                                                              sort=True,
                                                                              many=True)])
                self.histio.show()
        


    def display_function_com(self,uptohere=None):

            #if not console input, displays the next note
##            try:
                if uptohere.is_top():
                    if self.show_full_top:
                        if self.auto_multi:
                            # if automulti function is
                            #selected, and the note top-level

                            if str(uptohere) not in multi_dict[notebookname].keys():
                                # load into note_display if not already loaded
                                multi_dict[notebookname][str(uptohere)] = Note_Display(180)
                                note_with_children = ([uptohere]
                                                      +[Index(a_temp)
                                                        for a_temp
                                                        in self.find_within(int(uptohere),
                                                                            int(uptohere)+1)])
        
                                self.showall(note_with_children, multi=True,
                                             output=multi_dict[notebookname][str(uptohere)],
                                             vary=False,show_date=self.defaults.get('showdate'))

                            multi_dict[notebookname][str(uptohere)].print_all(pause=False)
                                # show content of note_display

                        else:  #if not automulti
                            
                            display.noteprint(self.show(Index(int(uptohere)),
                                                        yestags=self.tagdefault,
                                                        show_date=self.defaults.get('showdate')),
                                              
                                              param_width=display.width_needed(self.show(
                                                  Index(int(uptohere)),
                                                        show_date=self.defaults.get('showdate')),
                                                            self.get_metadata_from_note(str(Index(int(uptohere))))['size'],
                                                            leftmargin=self.defaults.get('leftmargin')),
                                              leftmargin=self.defaults.get('leftmargin'))
                            toshow = self.find_within(int(uptohere), int(uptohere)+1)
                            self.child_show(toshow, not_all=True)

                    else:  # if not full-top, don't show children with top level note
                        display.noteprint(self.show(uptohere,
                                                    yestags=self.tagdefault,
                                                    show_date=self.defaults.get('showdate')),
                                          param_width=display.width_needed(
                                              self.show(uptohere,yestags=self.tagdefault,
                                                        show_date=self.defaults.get('showdate')),
                                              self.get_metadata_from_note(uptohere)['size'],
                                              leftmargin=self.default_dict['leftmargin']),
                                          param_indent=uptohere.level()*self.default_dict['indentmultiplier'],
                                          leftmargin=self.default_dict['leftmargin'])

                elif not self.children_too: #if not a top level note, and children not to be displayed
                    display.noteprint(self.show(uptohere,
                                                yestags=self.tagdefault,
                                                show_date=self.default_dict['showdate']),
                                      param_width=display.width_needed(
                                          self.show(uptohere,
                                                    yestags=self.tagdefault,
                                                    show_date=self.defaults.get('showdate')),
                                          self.get_metadata_from_note(uptohere)['size'],
                                          leftmargin=self.defaults.get('leftmargin')),
                                      param_indent=uptohere.level()*self.defaults.get('indentmultiplier'),
                                      leftmargin=self.defaults.get('leftmargin'))

                else:  #if not a top level note, but children are to be displayed

                    display.noteprint(self.show(Index(str(uptohere)),
                                                yestags=self.tagdefault,
                                                show_date=self.defaults.get('showdate')),
                                      param_width=display.width_needed(
                                          self.show(Index(str(uptohere)),
                                                yestags=self.tagdefault,
                                                show_date=self.defaults.get('showdate')),
                                          self.get_metadata_from_note(str(Index(str(uptohere))))['size'],
                                          leftmargin=self.defaults.get('leftmargin')),
                                      leftmargin=self.defaults.get('leftmargin'))
                    toshow = self.find_within(int(uptohere),
                                              int(uptohere)+1)
                    self.child_show(toshow, not_all=True)
                lastup = uptohere
                return lastup
                       
                
##            except:
##                print('EXCEPTION RAISED')

    def setting_com (self,mainterm=EMPTYCHAR,otherterms=EMPTYCHAR,predicate=EMPTYCHAR):
        
            # general function for all the on-off setting.

            if mainterm in binary_settings:

                exec(binary_settings[mainterm][0]+'= not '+binary_settings[mainterm][0])
                show_setting(binary_settings[mainterm][1],eval(binary_settings[mainterm][0]))

            elif mainterm not in ['allsettings','showsetting']:
                for t_temp in otherterms[0].split(COMMA):

                    if t_temp in binary_settings:

                        if mainterm in ['on']:
                            predicate = True
                        elif mainterm in ['off']:
                            predicate = False
                        elif mainterm in ['toggle']:
                            exec ('predicate = not '+binary_settings[t_temp][0])
                        exec(binary_settings[t_temp][0]+' = predicate')
                        show_setting(binary_settings[t_temp][1],predicate)

            else:
                if mainterm in ['allsettings']:
                    for t_temp in binary_settings:
                    
                        exec ('predicate = '+binary_settings[t_temp][0])
                        show_setting(binary_settings[t_temp][1],predicate)
                else:
                    for t_temp in otherterms[0].split(COMMA):

                        if t_temp in binary_settings:
                            exec ('predicate = '+binary_settings[t_temp][0])
                            show_setting(binary_settings[t_temp][1],predicate)
 

    def enter_com(self,
                  mainterm=EMPTYCHAR,
                  otherterms=EMPTYCHAR,
                  predicate=EMPTYCHAR,
                  longphrase=False,
                  lastup=None,
                  series_enter=EMPTYCHAR):


        index_entered = False
        if predicate[4]:
            key_buffer = self.defaults.get('defaultkeys')
            self.defaults.set('defaultkeys',[])
            self.dd_changed=True
        if mainterm == 'conent':
            mainterm = PLUS
            series_enter = PLUS
        elif mainterm == 'connext':
            mainterm = PLUS + PLUS
            series_enter = PLUS + PLUS
        elif mainterm == 'conchild':
            mainterm = PLUS + PLUS + PLUS
            series_enter = PLUS + PLUS + PLUS
        elif mainterm == 'enternext':
            mainterm = PLUS + PLUS
        elif mainterm == 'enterchild':
            mainterm = PLUS + PLUS + PLUS


        elif mainterm == 'enterback':
            mainterm = DASH
        if ((len(mainterm) < 2 or mainterm[1] != PLUS)
                and (not self.always_next and not self.always_child)):
            if mainterm[0] != DASH:
                right_at = predicate[0] or predicate[1]
                as_child = predicate[1]

            else:
                lastup = lastup.previous()
                right_at = True
                as_child = False

        elif (self.always_child
              or len(mainterm) > 2 and mainterm[2] == PLUS):
            right_at = True
            as_child = True

        else:
            right_at = True
            as_child = False

                    
        if otherterms[0] and otherterms[0].replace(PERIOD+PERIOD,
                                                   PLUS).replace(PERIOD,
                                                                 EMPTYCHAR).replace('^',EMPTYCHAR).isnumeric():
            right_at = True
            lastup=Index(otherterms[0])
            index_entered = True

            otherterms[0], otherterms[1] = otherterms[1],otherterms[2]

            if not otherterms[0] and not otherterms[1]:
                longphrase = False



        if mainterm == 'autoenter':
            lastup = self.enter(ek=(set(otherterms[0].split(COMMA))),
                                show=not predicate[2],
                                right_at=right_at,
                                as_child=as_child,
                                ind=lastup,
                                carrying_keys=(self.carry_keys and not predicate[4]) or predicate[4],
                                usedefaultkeys=self.suspend_default_keys)

            
            

        elif longphrase:
            lastup = self.addnew(set(otherterms[0].split(COMMA)),
                                 otherterms[1].replace(VERTLINE,EOL),
                                 show=not predicate[2],
                                 right_at=right_at,
                                 as_child=as_child,
                                 ind=lastup)

        else:
            lastup = self.enter(show=not predicate[2],
                                right_at=right_at,
                                as_child=as_child,
                                ind=lastup,
                                carrying_keys=(self.carry_keys and not predicate[4]) or predicate[4],
                                usedefaultkeys=self.suspend_default_keys)

        for i_temp in self.find_within(Index(0),
                                       Index(1)):
            self.move(i_temp, Index(i_temp)+lastup)


        next_up = False
        if predicate[4]:
            self.defaults.set('defaultkeys',key_buffer)
            self.dd_changed=True

        return lastup, next_up, series_enter

    def biginputterm_imp (self,lastup,stackobject=None,series_enter=EMPTYCHAR):


        def add_mark (index):

            if str(index) in self.default_dict['marked']:
                return POUND
            return EMPTYCHAR 

        while True:

            if command_stack.size() == 0:
                temp_insert = EMPTYCHAR

                if self.project:
                    temp_insert = SLASH
##                print('<<'+nformat.format_keys(self.default_dict['defaultkeys'])+'>>')
                manyinputterm = input(self.using_shelf*'*'+self.using_database*'DB'+notebookname
                                      +temp_insert
                                      +UNDERLINE.join(self.project)
                                      +COLON+index_reduce(str(lastup))
                                      +BLANK+add_mark(lastup)+
                                      self.parent
                                      +BLANK+{EMPTYCHAR:EMPTYCHAR,
                                              PLUS+PLUS:'[++]',
                                              PLUS+PLUS+PLUS:'[+++]'}[series_enter]+BLANK)
                if self.apply_abr_inp:
                    manyinputterm = self.default_dict['abbreviations'].undo(manyinputterm)
                manyinputterm = self.default_dict['commands'].do(manyinputterm, lchar=EMPTYCHAR)
                print('<'+manyinputterm+'>')
                if STAR + STAR in manyinputterm and manyinputterm.split(STAR+STAR)[1].isnumeric():
                    manyinputterm, mult_temp =  manyinputterm.split(STAR+STAR)[0], int(manyinputterm.split(STAR+STAR)[1])
                    manyinputterm = ((manyinputterm + SLASH + SLASH) * mult_temp)[:-2]

                if manyinputterm[:1] == ATSIGN:  #for a macro

                    manyinputterm = manyinputterm[1:]

                    firstindex = str(self.iterator.first())
                    lastindex = str(self.iterator.last())
                    backupname = self.filename + str(datetime.datetime.now()).split(BLANK)[0]
                                
                    questionlist = extract.extract(manyinputterm,LEFTBRACKET,RIGHTBRACKET)
                    asked = set()
                    for question in questionlist:
                        if question not in asked:
                            answer = input(question)
                            asked.add(question)
                        
                            manyinputterm = manyinputterm.replace(LEFTBRACKET+question+RIGHTBRACKET,answer)
                    manyinputterm = manyinputterm.replace('FIRST',
                                                          firstindex)
                    manyinputterm = manyinputterm.replace('LAST',
                                                          lastindex)
                    manyinputterm = manyinputterm.replace('FILE',
                                                          self.filename)
                    manyinputterm = manyinputterm.replace('BACKUP',
                                                          backupname)
                    manyinputterm = manyinputterm.replace('NOW',
                                                          POUND+str(datetime.datetime.now()).split(BLANK)[0])



                manyinputterm = manyinputterm.split(SLASH+SLASH)  ## split into commands

                rootcommand =  EMPTYCHAR
                afterroot = EMPTYCHAR
                filledinputlist = []
                for t_temp in manyinputterm:
                    if COLON in t_temp:
                        if t_temp.split(COLON)[0]:
                            rootcommand = t_temp.split(COLON)[0]
                        if t_temp.split(COLON)[1]:
                            afterroot = COLON.join(t_temp.split(COLON)[1:])
                        t_temp = rootcommand + COLON + afterroot

                    filledinputlist += [t_temp]


                
                for t_temp in reversed(filledinputlist):

                    command_stack.add(t_temp)
            biginputterm = command_stack.pop()
            if biginputterm == False:
                biginputterm = EMPTYCHAR
                
            if biginputterm in [LEFTBRACKET]:

                self.default_dict['marked'].add(str(lastup))
            elif biginputterm in [RIGHTBRACKET]:
                self.default_dict['marked'].discard(str(lastup))

            else:
                break

        continuelooping = True
        close_notebook = False

        # to retrieve search result

        for rep_temp in range(0,biginputterm.count('{{')):
            if '{{' in biginputterm and '}}' in biginputterm:
                
                for x_temp in range(0,biginputterm.count('{{')):
 
                    
                    n_temp = biginputterm.split('{{')[1].split('}}')[0]




                    if n_temp and n_temp[0] == POUND:
 
                        n_temp = n_temp[1:]

                        temp_list = eval(LEFTBRACKET + n_temp + RIGHTBRACKET)
                        temp_list = [str(x_temp) for x_temp in temp_list]
                        temp_listterm = ','.join(temp_list)

                        if temp_listterm:
                            biginputterm = biginputterm.replace('{{'+POUND+n_temp+'}}',temp_listterm)
                    
                    elif n_temp.isnumeric():
                        biginputterm = biginputterm.replace('{{'+n_temp+'}}',
                                                            rangelist.range_find([Index(a_temp)
                                                                                  for a_temp
                                                                                  in self.searchlog[-(int(n_temp.strip()))][1]
                                                                                  if a_temp!=0]).replace(LONGDASH,SLASH))
                    elif n_temp.isupper() and n_temp in self.variables:

                        biginputterm = biginputterm.replace('{{'+n_temp+'}}',self.variables[n_temp])
##                                                            rangelist.range_find([Index(a_temp)
##                                                                                  for a_temp
##                                                                                  in self.variables[n_temp]]).replace(LONGDASH,SLASH))

                    elif n_temp and n_temp[0] == ATSIGN:
                        n_temp = n_temp[1:]
                        try:
                            textfile = get_text_file(n_temp)
                            biginputterm = biginputterm.replace('{{'+ATSIGN+n_temp+'}}',textfile)
                        except:
                            display.noteprint((alerts.ATTENTION,label.FILE_ERROR))
                        
                        
                        

        # to send result to next command
        if '=>' in biginputterm:


            self.next_term = '=>'.join(biginputterm.split('=>')[1:])
            print(self.next_term)
            biginputterm = biginputterm.split('=>')[0]
            self.last_term = biginputterm

        # to retieve last index
        if '[/]' in biginputterm:
            biginputterm = biginputterm.replace('[/]',
                                                str(lastup))
        # to retrieve marked results
        if '[?]' in biginputterm:
            biginputterm = biginputterm.replace('[?]',
                                                rangelist.range_find([Index(a_temp)
                                                                      for a_temp
                                                                      in self.default_dict['marked']
                                                                      if a_temp in str(a_temp)
                                                                      in self.indexes()]).replace(LONGDASH,SLASH))
        if '[*]' in biginputterm:
            biginputterm = biginputterm.replace('[*]',
                                                rangelist.range_find([a_temp
                                                                      for a_temp
                                                                      in self.default_dict['flipbook']]).replace(LONGDASH,SLASH))

        if '[%' in biginputterm and ']' in biginputterm and '[%]' not in biginputterm:
            projectname = biginputterm.split('[%')[1].split(']')[0]
            print(projectname)
            if projectname in self.default_dict['projects'].get_all_projects():
                biginputterm = biginputterm.replace('[%'+projectname+']', rangelist.range_find([a_temp
                                                                      for a_temp
                                                                      in transpose_keys(self.default_dict['projects'].
                                                                                        get_all_indexes(project=projectname),
                                                                                        surround=False).replace(LONGDASH,SLASH)]))
            

        return biginputterm,continuelooping,close_notebook

    
    def limitlist_cc(self,biginputterm=EMPTYCHAR):
    
        templimit = True
        oldlimit = self.limitlist
        self.set_limit_list('E')


        if PERCENTAGE+PERCENTAGE in biginputterm:

            limit_factor = biginputterm.split(PERCENTAGE+PERCENTAGE)[1]
            biginputterm = biginputterm.split(PERCENTAGE+PERCENTAGE)[0]
            index_limit = None

            self.set_limit_list('R')
            
            for l_temp in limit_factor.split(COMMA):
                if len(l_temp) > 1 and l_temp[0] == PLUS:
                    l_temp = l_temp[1:]
                    intersection_temp = False
                else:
                    intersection_temp = True

                l_temp = l_temp.strip()
                if l_temp in ['FLIPBOOK',EXCLAMATION+EXCLAMATION]:
                    self.set_limit_list('F')

                elif l_temp not in self.show_fields():
                    self.set_limit_list(l_temp,intersection=intersection_temp)
                else:
                    self.set_limit_list(l_temp,
                                        intersection=intersection_temp)



        return biginputterm, oldlimit
                     
## ENTER COMMAND ##


    def enter_command(self,
                      biginputterm=EMPTYCHAR,
                      skipped=False,
                      lastup=1,
                      next_up=True,
                      uptohere=1,
                      notebookname=EMPTYCHAR,
                      series_enter=EMPTYCHAR):

        global override


        """ called from the mainloop of the program to enter commands"""


        

        

        display = Display(self.rectify)
        if self.first_time:
            display.noteprint((alerts.ATTENTION,
                               alerts.ENTER_DOCUMENTATION))
        self.first_time = False
        biginputterm,continuelooping,close_notebook = self.biginputterm_imp(lastup,
                                                                            command_stack,
                                                                            series_enter=series_enter)
        
        if biginputterm and biginputterm[0] == VERTLINE:
            self.suspend_default_keys = False
            biginputterm = biginputterm[1:]
        else:
            self.suspend_default_keys = True 
            
        if biginputterm and self.add_diagnostics:
            diagnostics.addline(biginputterm)
        if biginputterm == EMPTYCHAR:
            biginputterm = series_enter
        if biginputterm == SEMICOLON + SEMICOLON:
            series_enter = EMPTYCHAR 

        self.last_results_used = False

        # if a command has been sent forward
        if not biginputterm  and self.next_term:


            if '=>' in self.next_term: # if refeeding 
                afterterm = '=>'.join(self.next_term.split('=>')[1:])
                biginputterm = self.next_term.split('=>')[0]
            else:
                biginputterm = self.next_term
                
            if self.text_result: #replace with a text result

                biginputterm = biginputterm.replace(QUESTIONMARK+QUESTIONMARK+QUESTIONMARK+QUESTIONMARK,
                                                    self.text_result)

                
            if self.key_results: # replace with key results
                biginputterm = biginputterm.replace(QUESTIONMARK+QUESTIONMARK+QUESTIONMARK,
                                                    self.key_results\
                                                    .replace('<',EMPTYCHAR)\
                                                    .replace('>',EMPTYCHAR)\
                                                    .replace('|',', '))
                biginputterm = biginputterm.replace(QUESTIONMARK+QUESTIONMARK,
                                                    self.key_results)


            if self.last_results: # replace with index results

                biginputterm = biginputterm.replace(SLASH+QUESTIONMARK,'/SLASH#QUEST/')
                biginputterm = biginputterm.replace(QUESTIONMARK,
                                                    self.last_results).replace('/SLASH#QUEST/',
                                                                               SLASH+QUESTIONMARK)
                
                self.last_results_used = True

            if '=>' not in self.next_term:
                self.next_term = EMPTYCHAR
            else:
                self.next_term = afterterm
        if not self.last_results_used:
            self.last_results = EMPTYCHAR 
            
        if self.flipmode: #if using flashcards, then flip the flashcard before going to next index

            self.side += 1
##            nprint('side',str(self.side))
##            nprint('sides',str(self.sides))
##            nprint('flip_at',str(self.flip_at))
            if self.side % self.sides == self.flip_at % self.sides:

                lastup = uptohere
                if self.iteratormode:
                    uptohere = self.iterator.move()
                    if not self.flexflip:
                        self.side = self.flip_at
                else:
                    uptohere = self.hypermove()
                    

        elif next_up and not skipped: #if not using flashcards 

            
##            try:

                lastup = uptohere
                if self.iteratormode:
                    uptohere = self.iterator.move()
                else:
                    uptohere = self.hypermove(lastup)



    
                    
##            except:
##                nprint('Iterator error #1')
        skipped = False

        if self.parent and biginputterm:
        #if a childnote, and BigInT begins with PERIOD, then replace with the parent index
            if biginputterm[0] == PERIOD:
                biginputterm = self.parent + biginputterm
            biginputterm = biginputterm.replace(COLON+PERIOD,
                                                COLON+self.parent+PERIOD).\
                           replace(SEMICOLON+PERIOD,
                                   SEMICOLON+self.parent+PERIOD).\
                           replace(COMMA+PERIOD,
                                   COMMA+self.parent+PERIOD).\
                           replace(DASH+PERIOD,
                                   DASH+self.parent+PERIOD)
            print(biginputterm)
        

        longphrase = False
        predicate = {0: False,
                     1: False,
                     2: False,
                     3: False,
                     4: False}
        otherterms = {0: EMPTYCHAR,
                      1: EMPTYCHAR,
                      2: EMPTYCHAR,
                      3: EMPTYCHAR,
                      4: EMPTYCHAR}
        totalterms = 0
        templimit = False
        
        if not self.using_database and self.indexchanges  == 1 or prefix == 'beta':
            self.counter = 0

            is_con_temp = self.is_consistent()
            
            if not is_con_temp[0]:
                display.noteprint((alerts.IS_INCONSISTENT,
                                   alerts.WAIT))
                self.make_consistent()
                if not is_con_temp[0]:
                    display.noteprint((alerts.STILL_INCONSISTENT,
                                       EMPTYCHAR))

                if self.add_diagnostics:
                    diagnostics.addline('#ISCON - '+str(is_con_temp))
            else:
                if prefix == 'beta':
                    display.noteprint((alerts.IS_CONSISTENT,
                                       EMPTYCHAR))
        self.counter += 1
        if (PERCENTAGE in biginputterm
                or EXCLAMATION in biginputterm
                or EXCLAMATION+EXCLAMATION in biginputterm):
            biginputterm, oldlimit = self.limitlist_cc(biginputterm=biginputterm)

        #Determine the predicates 
        for (a_temp, b_temp) in enumerate(DOLLAR+ANDSIGN+STAR+QUESTIONMARK+EQUAL):
            
            if biginputterm and SLASH+b_temp in biginputterm[1:]:
                predicate[a_temp] = True
                biginputterm = (biginputterm[0]
                                +biginputterm[1:].replace(SLASH+b_temp,
                                                          EMPTYCHAR))
        #determine the otherterms
        if COLON in biginputterm:
            mainterm = biginputterm.split(COLON)[0]
            longphrase = True
            for i_temp, term in enumerate(biginputterm.split(COLON)[1].split(SEMICOLON)):
                otherterms[i_temp] = term
                totalterms += 1
        else:
            # if a list of keywords 
            if biginputterm and len(biginputterm)>4 \
               and not series_enter and ((COMMA in biginputterm
                 and SEMICOLON not in biginputterm
                 and biginputterm.replace(COMMA, EMPTYCHAR)) or
                (COLON not in biginputterm and biginputterm in self.keys())):
                mainterm = 'autoenter'  # 'autoenter' is sent forward as a command 
                otherterms[0] = biginputterm
                longphrase = True
                
            else:
                mainterm = biginputterm

        
        # to assign a variable       
        if len(mainterm) > 2 and mainterm.isupper()\
           and mainterm.isalpha() and COLON not in mainterm:
            if mainterm not in self.variables:
                if self.last_results_used:
                    if self.last_results:
                        self.variables[mainterm] = self.last_results
                        display.noteprint(('/C/'+mainterm,self.variables[mainterm]))
                elif self.key_results:
                     self.variables[mainterm] = self.key_results
                     display.noteprint(('/C/ '+mainterm, self.variables[mainterm]))
                     self.key_results = EMPTYCHAR
                elif self.text_result:
                    self.variables[mainterm] = self.text_result
                    self.text_result = EMPTYCHAR
                    display.noteprint(('/C/ '+mainterm,
                                           self.variables[mainterm]))
                                           
                                          
                        
                    

        if mainterm in ['menu',BLANK]:       #small menu 
            mainterm = self.menu_com()
        elif mainterm in ['bigmenu', BLANK+BLANK]:     #big menu
            mainterm = self.big_menu_com()
        elif mainterm in ['bigmenu?']:
            mainterm = self.big_menu_com() + QUESTIONMARK
        elif mainterm in ['menu?']:
            mainterm = self.menu_com() + QUESTIONMARK

        elif QUESTIONMARK in mainterm and mainterm.replace(QUESTIONMARK,EMPTYCHAR)\
           in commandscript.HELP_DICTIONARY:
            # to display information about a term 
            
            display.noteprint((EMPTYCHAR,
                               side_note((mainterm.replace(QUESTIONMARK,EMPTYCHAR),
                                          commandscript.HELP_DICTIONARY\
                                          [mainterm.replace(QUESTIONMARK,EMPTYCHAR)][0]\
                                          +labels.NONE*(not commandscript.HELP_DICTIONARY\
                                                        [mainterm.replace(QUESTIONMARK,
                                                                          EMPTYCHAR)][0].strip()),
                                         commandscript.HELP_DICTIONARY\
                                          [mainterm.replace(QUESTIONMARK,
                                                            EMPTYCHAR)][1]),
                                         widths=[20,60,30])))
        mainterm = mainterm.strip()
        if mainterm == EMPTYCHAR and str(uptohere) in self.indexes():
            # to display the next note

            lastup = self.display_function_com(uptohere=uptohere)


        elif mainterm and mainterm[0] in [LEFTNOTE, RIGHTNOTE,"'",'"','=']:
            if mainterm and mainterm[1:].isnumeric():
                self.iterator.change_speed(int(mainterm[1:]))
                # changes speed to the number of
                # left or right arrow brackets
            elif mainterm[0] in [LEFTNOTE,RIGHTNOTE] and not mainterm[1:].isnumeric():
                self.iterator.change_speed(len(mainterm))
            if mainterm[0] == LEFTNOTE:
                self.iterator.back()
            elif mainterm[0] == RIGHTNOTE:
                self.iterator.forward()
            elif mainterm[0] == "'":
                self.iterator.change_tilt(1)
            elif mainterm[0] == '"':
                self.iterator.change_tilt(2)
            elif mainterm[0] == '=':
                self.iterator.change_tilt(0)
                
        elif mainterm != EMPTYCHAR and mainterm.replace(PERIOD,
                                                        EMPTYCHAR) == EMPTYCHAR:
            # to skip forward by the number of periods 
            uptohere = self.iterator.skip_forward(len(mainterm))
            lastup = uptohere
            skipped = True
        elif mainterm != EMPTYCHAR and mainterm.replace(COMMA,
                                                        EMPTYCHAR) == EMPTYCHAR:
            # to skip back by the number of commas 
            uptohere = self.iterator.skip_back(len(mainterm))
            lastup = uptohere
            skipped = True
        elif mainterm == SLASH:
            next_up = True 
        # to display a note if index entered as command
        elif index_expand(mainterm) in self.indexes():
            # to display a note that has been entered 
            mainterm = index_expand(mainterm)
            display.noteprint(self.show(Index(mainterm)),
                              param_width=display.width_needed(self.show(Index(mainterm)),
                                                               self.get_metadata_from_note(mainterm)['size']))
        elif mainterm in ["'"]:
            self.always_next = not self.always_next
            self.always_child = False
            show_setting(labels.ALWAYS_NEXT,
                         self.always_next)
            show_setting(labels.ALWAYS_CHILD,
                         self.always_child)
        elif mainterm in ['"']:
            self.always_child = not self.always_child
            show_setting(labels.ALWAYS_CHILD,
                         self.always_child)

        elif mainterm in ['tags', 'tag', 't']:
            is_temp = set()
            if longphrase:
                for tag in self.tags():
                    found_temp = False
                    if self.tag_dict_contains(tag):
                        for key in self.get_keys_for_tag(tag):
                            if {str(x_temp) for x_temp
                                in self.get_indexes_for_key(key+SLASH+tag)}.intersection(
                                {str(x_temp) for x_temp
                                 in get_range(s_input(queries.RANGE_TO_FROM,
                                                      otherterms[0]),
                                              many=True)}):
                                found_temp = True
                        if found_temp:
                            is_temp.add(tag)
                if not predicate[0]:
                    display.noteprint((labels.TAGS,
                                       formkeys(sorted(list(is_temp)))))
                if predicate[0]:
                    mainterm = 'keysfortags'
                            
            else: 
                if not predicate[0]:
                    display.noteprint((labels.TAGS,
                                       formkeys(sorted(list(self.tags())))))
                if predicate[0]:
                    mainterm = 'keysfortags'
            self.key_results = VERTLINE.join(['<'+POUND+x_temp.strip()+'>'
                                              for x_temp in is_temp])
                
        elif mainterm in simple_commands:

            exec(simple_commands[mainterm])
        elif mainterm in binary_settings or mainterm in ['on',
                                                         'off',
                                                         'toggle',
                                                         'allsettings',
                                                         'showsetting']:
            self.setting_com (mainterm=mainterm,
                              otherterms=otherterms,
                              predicate=predicate)  

        elif mainterm in ['startlooping']:
            self.looping = True
            self.linking = True
            self.starting_linking = True
        elif mainterm in ['endlooping','endlinking']:
            self.linking = False
        elif mainterm in ['startlinking']:
            self.linking = True
            self.starting_linking = True

        elif (mainterm in ['ent',
                           'enter',
                           'enternext',
                           'enterchild',
                           'enterback',
                           'autoenter',
                           'conent',
                           'conchild',
                           'connext',
                           PLUS,
                           DASH]
              or (mainterm+BLANK)[0] in [PLUS, DASH]):
            lastup,next_up,series_enter = self.enter_com (mainterm=mainterm,
                                             otherterms=otherterms,
                                             predicate=predicate,
                                             longphrase=longphrase,
                                             lastup=lastup,
                                             series_enter=series_enter)

        elif mainterm in ['first','last']:
            if mainterm == 'first':
                uptohere = self.iterator.first()
            if mainterm == 'last':
                uptohere = self.iterator.last()
            lastup = uptohere
            display.noteprint(self.show(lastup,show_date=self.default_dict['showdate']),
                              param_width=
                              display.width_needed(
                                  self.show(lastup,show_date=self.default_dict['showdate']),
                                  self.get_metadata_from_note(lastup)['size']))

        elif mainterm in [STAR]:
            command_stack.add('keys:'+str(lastup)+' =>search:??')
            

        elif mainterm in ['skip']:
            lastup = Index(s_input('Skip to? ',
                                   otherterms[0]))
            if str(lastup) not in self.indexes():
                lastup = self.find_space(lastup)
            uptohere = self.iterator.go_to(lastup)
            display.noteprint(self.show(lastup,show_date=self.default_dict['showdate']),
                              param_width=
                              display.width_needed(
                                  self.show(lastup,show_date=self.default_dict['showdate']),
                                  self.get_metadata_from_note(lastup)['size']))
        elif mainterm in ['hop']:
            h_temp = s_input(queries.JUMP_AHEAD_BY,
                            otherterms[0])
            if h_temp:
                
                go_back = (h_temp[0] == DASH)
                if h_temp[0] == DASH:
                    h_temp = h_temp[1:]

                if not go_back:
                    uptohere = self.iterator.skip_forward(int(h_temp))
                else:
                    uptohere = self.iterator.skip_back(int(h_temp))
            else:
                uptohere = self.iterator.skip_forward(1)
            lastup = uptohere
            skipped = True


        elif mainterm in ['newproject']:
            
            while True:
                if otherterms[0]:
                    project_name = otherterms[0]
                else:
                    project_name = input(queries.PROJECT_NAME)
                if not project_name or project_name.isalpha():
                    break
                else:
                    otherterms[0] = EMPTYCHAR

            project_name = self.default_dict['projects'].get_new_project_name(project_name)
                        
            if project_name:

                if input(queries.CLEAR_DEFAULT_KEYS) in YESTERMS:
                    self.defaults.set('defaultkeys',[])
                    self.dd_changed=True

                
                    
                uptohere = self.iterator.last()
                nprint('ITERATOR SET TO ',str(uptohere))
                k_temp = get_keys_to_add(self.default_dict['abbreviations'].undo(input(queries.KEYS)).split(COMMA))
                                                    
                self.default_dict['projects'].initiate_project(project_name=project_name,
                                                               defaultkeys=k_temp,
                                                               lastup=lastup,
                                                               uptohere=uptohere,
                                                               mainterm=mainterm,
                                                               series_enter=series_enter,
                                                               date=str(datetime.datetime.now()))
                
                                                
                self.dd_changed=True
                

                self.project.append(project_name)
                allnotebooks_tracking[notebookname]['projectset'].append(project_name)


        elif mainterm in ['saveproject']:
            
            project_name = EMPTYCHAR

            while True:

                if not otherterms[0]:
                    if self.project:
                        project_name = self.project[-1]
                    else:
                        project_name = input(queries.PROJECT_NAME)
                else:
                    project_name = otherterms[0]
                if project_name in self.default_dict['projects'].get_all_projects() or project_name in quit_terms:
                    break
                otherterms[0] = EMPTYCHAR

            if project_name in self.default_dict['projects'].get_all_projects():
                if input('UPDATE KEYS for '+project_name+' ?') in YESTERMS:
                    self.default_dict['projects'].add_default_keys(new_defaultkeys=self.defaults.get('defaultkeys'),
                                                                   project=project_name)
                                                                                 
                    self.defaults.set('defaultkeys',[])
                self.default_dict['projects'].set_position(lastup=lastup,
                                                           uptohere=uptohere,
                                                           project=project_name)
                self.default_dict['projects'].set_going(mainterm=mainterm,
                                                        series_enter=series_enter,
                                                        project=project_name)
                self.default_dict['projects'].add_date(new_date=str(datetime.datetime.now()),
                                                       project=project_name)

                self.default_dict['projects'].set_status_open(status=False,
                                                              project=project_name)
                
                self.default_dict['projects'].add_last_modified(date=str(datetime.datetime.now()),
                                                                project=project_name)
                self.dd_changed=True

        elif mainterm in ['resumeproject','loadproject']:
            project_name = EMPTYCHAR
            
            if self.project and not predicate[0] and COMMA not in otherterms[0]:   # Save the existing project status
                project_name = self.project.pop()
                if project_name in self.default_dict['projects'].get_all_projects():
                    
                    if input('UPDATE KEYS for '+project_name+' ?') in YESTERMS:
                        self.default_dict['projects'].add_default_keys(new_defaultkeys=self.defaults.get('defaultkeys'),
                                                                       project=project_name)
                        self.defaults.set('defaultkeys',[])
                    self.default_dict['projects'].set_position(lastup=lastup,
                                                       uptohere=uptohere,
                                                       project=project_name)
                    self.default_dict['projects'].set_going(mainterm=mainterm,
                                                            series_enter=series_enter,
                                                            project=project_name)
                    self.default_dict['projects'].add_date(new_date=str(datetime.datetime.now()),
                                                   project=project_name)

                    if 'indexes' not in self.default_dict['projects'].get_default_keys(project=project_name):
                        self.default_dict['projects'].clear_indexes(project=project_name)
                    else:
                        if isinstance(self.default_dict['projects'].get_all_indexes(project=project_name),list):
                            self.default_dict['projects'].set_indexes(project=project_name,
                                                                      indexes=OrderedList(sorted(self.default_dict['projects'].get_all_indexes(project=project_name))))
                                                                                                    

                    if 'status' not in self.default_dict['projects'].get_project(project_name):

                        temp_status = {'started':str(datetime.datetime.now()),
                                                'open':True,
                                                'lastmodified':[str(datetime.datetime.now())]}
                        self.default_dict['projects'].set_status(project=project_name,status=temp_status)
                        
 
            if otherterms[0]:  #Get the project title if entered
                project_names = otherterms[0].split(COMMA)

            for project_name in project_names:
                while True:  #If not entered
                    
                    if not project_name:
                        project_name = input(queries.PROJECT_NAME)
                    if not project_name or  project_name in  self.default_dict['projects'].get_all_projects():
                        break
                    else:
                        project_name = EMPTYCHAR

                if project_name:

                    # To load different project
    ##                if input('CARRY OVER DEFAULT KEYS?') not in YESTERMS:
    ##                    self.default_dict['defaultkeys'] = self.default_dict['projects'][project_name]['defaultkeys']
    ##                else:
    ##                    self.default_dict['defaultkeys'] += self.default_dict['projects'][project_name]['defaultkeys']
                    if not predicate[1]:
                        lastup,uptohere = Index(str(self.default_dict['projects'].get_position(project=project_name)[0])),\
                                          Index(str(self.default_dict['projects'].get_position(project=project_name)[1]))
                        mainterm,series_enter = self.default_dict['projects'].get_going(project=project_name)[0],\
                                                self.default_dict['projects'].get_going(project=project_name)[1]
                        
                    self.default_dict['projects'].add_date(project=project_name,
                                                           new_date=str(datetime.datetime.now()))
                                    
        ##            if temp_uptohere in self.indexes(): 
        ##                command_stack.add('skip:'+temp_uptohere)
                    
                    self.project.append(project_name)
                    allnotebooks_tracking[notebookname]['projectset'].append(project_name)
                    self.dd_changed=True


        elif mainterm in ['endproject','quitproject']:
                               
            once_through = False 

            if self.project:
                while self.project and (predicate[0] or  (not predicate[0] and not once_through)):
                    project_name = self.project.pop()
                    if project_name in self.default_dict['projects'].get_all_projects():
                        
                        if input('UPDATE KEYS for '+project_name+' ?') in YESTERMS :
                            self.default_dict['projects'].add_default_keys(project=project_name,new_defaultkeys=self.defaults.get('defaultkeys'))
                            self.defaults.set('defaultkeys',[])
                        self.default_dict['projects'].set_position(project=project_name,
                                                                   lastup=lastup,
                                                                   uptohere=uptohere)

                        self.default_dict['projects'].set_going(project=project_name,
                                                                mainterm=mainterm,
                                                                series_enter=series_enter)

                        
                        self.default_dict['projects'].add_date(project=project_name,
                                                               new_date=str(datetime.datetime.now()))
                        
                        self.default_dict['projects'].set_status_open(project=project_name,
                                                                      status=False)

                        self.default_dict['projects'].add_last_modified(project=project_name,
                                                                        date=str(datetime.datetime.now()))
                        self.dd_changed=True
                        once_through = True 
                                                                    

                

        elif mainterm in ['archiveproject']:

            while True:
                
                project_name = s_input('Project name?',otherterms[0])
                if project_name in self.default_dict['projects'].get_all_projects():
                    break
            if 'archivedprojects' not in self.default_dict:
                self.default_dict['archivedprojects'] = ProjectManager(archive=True)
            if project_name not in self.default_dict['archivedprojects'].get_all_projects():
                self.default_dict['archivedprojects'].set_project(project=project_name,
                                                                  project_dict=copy.deepcopy(self.default_dict['projects'].get_project(project=project_name)))
                if self.default_dict['archivedprojects'].get_project(project=project_name) == self.default_dict['projects'].get_project(project=project_name):
                    self.default_dict['projects'].delete_project(project_name)
                    
                display.noteprint((alerts.ATTENTION,
                                   project_name + ' has been archived'))

        elif mainterm in ['renameproject']:
            while True:
                old_name = s_input('Existing name of project?',otherterms[0])
                if old_name in self.default_dict['projects'].get_all_projects() or not old_name:
                    break
                otherterms[0] = ''
            while True:
                new_name = s_input('Change name of '+old_name+' to?',otherterms[1])
                if new_name not in self.default_dict['projects'].get_all_projects() or not new_name:
                    break
                otherterms[1] = ''
            if old_name and new_name:
                self.default_dict['projects'].set_project(project=new_name,
                                                          project_dict=copy.deepcopy(self.default_dict['projects'].get_project(project=old_name)))
                self.default_dict['projects'].delete_project(project_name=old_name)              
                display.noteprint((alerts.ATTENTION,
                                   old_name+' changed to '+new_name))
                

        elif mainterm in ['deletearchivedproject']:
            while True:
                project_name = s_input('Name of project to delete?',otherterms[0])
                if project_name and project_name in self.default_dict['archivedprojects'].get_all_projects():
                    if input('ARE YOUR SURE?') in YESTERMS:
                        self.default_dict['archivedprojects'].delete_project(project_name=project_name)
                        break
                if not project_name:
                    break
                otherterms[0] = ''
                        
                


        elif mainterm in ['unarchiveproject']:

            if  'archivedprojects' in self.default_dict:

                while True:
                    
                    project_name = s_input('Project name?',otherterms[0])
                    if project_name in self.default_dict['archivedprojects'].get_all_projects():
                        break
                if project_name not in self.default_dict['projects'].get_all_projects():
                    self.default_dict['projects'].set_project(project=project_name,
                                                              project_dict=copy.deepcopy(self.default_dict['archivedprojects'].get_project(project=project_name)))
                    if self.default_dict['projects'].get_project(project=project_name) == self.default_dict['archivedprojects'].get_project(project=project_name):
                        self.default_dict['archivedprojects'].delete_project(project_name)
                    display.noteprint((alerts.ATTENTION,project_name + ' has been unarchived'))

        elif mainterm in ['showprojects']:

            self.show_projects(projectobject=self.default_dict['projects'].return_dict())

        elif mainterm in ['showarchivedprojects']:
            self.show_projects(projectobject=self.default_dict['archivedprojects'].return_dict())


        elif mainterm in ['flipproject']:
            if self.project:
                self.default_dict['flipbook'] = sorted(transpose_keys(self.default_dict['projects'].get_all_indexes(project=self.project[-1]),
                                                                      surround=False),key=lambda x:Index(x))
                self.set_iterator(self.default_dict['flipbook'],
                                  flag=self.defaults.get('setitflag'))
                self.dd_changed=True

        elif mainterm in ['currentproject']:
            if self.project:

                text_temp = self.project[-1] + EOL + EOL \
                            + str(self.default_dict['projects'].get_all_indexes(project=self.project[-1])[0]) \
                            + ':' + str(self.default_dict['projects'].get_all_indexes(project=self.project[-1])[-1])
                

                display.noteprint(('/C/CURRENT PROJECT',text_temp))

        elif mainterm in ['showproject']:

            while True:
                name_temp = s_input('Name of project?',otherterms[0])
                if name_temp in self.default_dict['projects'].get_all_projects() or not name_temp:
                    break
            if name_temp:
                text_temp = 'PROJECTNAME: '+name_temp+EOL+EOL
                text_temp += 'DEFAULTKEYS: '+', '.join(self.default_dict['projects'].get_default_keys(project=name_temp)) + EOL + EOL
                text_temp += 'POSITION:' + str(self.default_dict['projects'].get_position(project=name_temp)[0])+';'\
                             + str(self.default_dict['projects'].get_position(project=name_temp)[1]) + EOL+EOL
                                                       
                text_temp += 'DATES:' + ', '.join(self.default_dict['projects'].get_date(project=name_temp)) + EOL + EOL
                if len(self.default_dict['projects'].get_status_modified(project=name_temp))>0:
                    text_temp += 'LAST MODIDFIED: ' + self.default_dict['projects'].get_status_modified(project=name_temp)[-1] + EOL + EOL
                text_temp += 'INDEXES: ' + ', '.join(transpose_keys(self.default_dict['projects'].get_all_indexes(project=name_temp),
                                                                    surround=False))
                                                  
                display.noteprint(('/C/ PROJECT',text_temp))
        
        elif mainterm in ['showprojectdates']:

            determinant = EMPTYCHAR
            if not predicate[0]:
                determinant = 'ym'
            else:
                determinant = 'ymd'
            if predicate[1]:
                determinant += '*h'
            if predicate[1] and predicate[2]:
                determinant += 'm'

            if not longphrase:
                
                self.show_project_dates(determinant=determinant)
                self.show_date_dictionary(determinant=determinant,prefix='PROJ')

            else:
    
                entrylist_temp = get_range(s_input('Range?',otherterms[0]),many=True)
                if otherterms[1]:
                    determinant = otherterms[1]
     
                self.show_project_dates(entrylist=entrylist_temp,determinant=determinant)
                self.show_date_dictionary(determinant=determinant,prefix='PROJ')
            
        elif (mainterm in ['quit'] and (predicate[0]
                                        or q_input(queries.SURE,command_stack))):

                
            continuelooping = False
            close_notebook = True
            diagnostics.end()

            if self.project:
                project_name = self.project[-1]
                if project_name in self.default_dict['projects'].get_all_projects():
##                    if input('UPDATE KEYS for '+project_name+' ?') in YESTERMS and len(self.project<2):
##                        self.default_dict['projects'][project_name]['defaultkeys'] = self.default_dict['defaultkeys']

                    self.default_dict['projects'].set_position(project=project_name,
                                                               lastup=lastup,
                                                               uptohere=uptohere)
                    self.default_dict['projects'].set_going(project=project_name,
                                                            mainterm=mainterm,
                                                            series_enter=series_enter)
                    
                    self.default_dict['projects'].add_date(project=project_name,
                                                           new_date=str(datetime.datetime.now()))
                self.project = self.project[0:-1]  
        elif mainterm in ['switch']:
            histo_word_dict = None
            histo_key_dict = None
            histo_tag_dict = None
            continuelooping = False
            close_notebook = False
            if longphrase:        
                command_stack.add(otherterms[0])
                    
            
                
            
                

            if self.project:
                while self.project:
                    project_name = self.project[-1]
                    if project_name in self.default_dict['projects'].get_all_projects():
                        if input('UPDATE KEYS for '+project_name+' ?') in YESTERMS:
                            self.default_dict['projects'].add_default_keys(project=project_name,new_defaultkeys=self.defaults.get('defaultkeys'))
                            self.defaults.set('defaultkeys',[])
                                                  
                    self.default_dict['projects'].set_position(project=project_name,
                                                               lastup=lastup,
                                                               uptohere=uptohere)
                    self.default_dict['projects'].set_going(project=project_name,
                                                            mainterm=mainterm,
                                                            series_enter=series_enter)
                    
                    self.default_dict['projects'].add_date(project=project_name,
                                                           new_date=str(datetime.datetime.now()))
                    self.project = self.project[0:-1]
                                                  
                
        else:
            if self.quickenter:
                if not longphrase:
                    self.enter(ek=set(self.defaults.get('defaultkeys')),
                               et=mainterm)
                else:
                    self.enter(ek=set(mainterm.split(COMMA)),
                               et=otherterms[0])



        if templimit:
            self.set_limit_list(oldlimit)

        self.display_buffer.show(header=alerts.ATTENTION[3:],
                                 centered=True,
                                 purge=True)

        if self.changed:
            self.default_save()
            self.changed = False

        if self.dd_changed:
            self.default_save(suffix='d',extra='BACK')
            self.dd_changed = False

        db_connection.commit()

        return continuelooping, \
               skipped, lastup, next_up, \
               uptohere, close_notebook, series_enter

INTROSCRIPT = INTROSCRIPT.replace(PERCENTAGE, BLANK*int((OPENING_WIDTH-150)/2))


display = Display()
register = Registry(displayobject=display)
display.noteprint([INTROSCRIPT],
                  param_is_emb=True,
                  param_indent=0)


betastart = False
reconstitute = False
commandlist = list(range(len(commandscript.COMMANDSCRIPT)))
helploaded=False

while True:
    display.noteprint((labels.SELECT,queries.INITIAL_MENU))
    option = input('?')
    if option == '1' or option == '2':
        compactmode = False
        compactcolumns = None
        helploaded=True

        if option == '2':
             compactmode = True
             compactcolumns = (20,20,20,20,20)
             

            # TO load the help menu in, and also show it on starting.
        for counter, cs_temp in enumerate(commandscript.COMMANDSCRIPT):



                commandlist[counter] = DisplayList(displayobject=display)
                nformat.columns(commandscript.COMMANDSCRIPT[counter],
                                commandlist[counter],
                                columnwidth=(37,45,60,30,30),
                                compactwidth=compactcolumns)
                
                commandlist[counter].show(header=commandscript.HEADERS[counter],
                                          centered=True,indent=0)
                if input():
                    break
                    helploaded=False
        
                      
    if option == '3':
        betastart, reconstitute = True, True
        break
    if option == '4':
        betastart, reconstitute = False, False
        break
    if option == '5':
        betastart, reconstitute = False, True
        break
    if option =='6':
        register.console()
            
        
                      
            
    



successful = False
flagvalue = None
readonly = False

if betastart:
    prefix = 'beta'
else:
    prefix = EMPTYCHAR
if prefix:
    display.noteprint((EMPTYCHAR,'prefix='+prefix))
bigloop = True
allnotebooks = {}
allnotebooks_tracking = {}
add_new_notebook = True

# OPEN DATEBASE CONNECTION


##default_connection = sqlite3.connect('notebooks'+SLASH+'defaults.db')
##default_cursor = default_connection.cursor()
##
##

db_connection = sqlite3.connect('notebooks'+SLASH+'notebook.db')
db_cursor = db_connection.cursor()

# DATA BASE DEFINITION

db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS notebooks (
        notebook TEXT NOT NULL UNIQUE );
        """)
db_cursor.executescript("""

    CREATE TABLE IF NOT EXISTS notes (
        
        notebook TEXT NOT NULL,
        note_index TEXT NOT NULL,
        note_body TEXT DEFAULT '',
        size INTEGER DEFAULT 60,
        user TEXT DEFAULT 'user',
        UNIQUE (notebook, note_index)
        FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
        );""")
            
db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS timestamps (
        notebook TEXT NOT NULL,
        note_index TEXT NOT NULL,
        timestamp DATE NOT NULL,
        UNIQUE (notebook, note_index, timestamp)
        FOREIGN KEY (notebook, note_index) REFERENCES notes (notebook, note_index) ON DELETE CASCADE 
        );""")
                        
db_cursor.executescript("""        
    CREATE TABLE IF NOT EXISTS all_note_keys (
        notebook TEXT NOT NULL,
        note_index TEXT NOT NULL,
        keyword TEXT NOT NULL,
        UNIQUE (notebook, note_index, keyword)
        FOREIGN KEY (notebook, note_index) REFERENCES notes (notebook, note_index) ON DELETE CASCADE
        );""")
db_cursor.executescript("""                        
    CREATE TABLE IF NOT EXISTS all_words (
        notebook TEXT NOT NULL,
        word TEXT NOT NULL,
        UNIQUE (notebook, word)
        );""")
db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS all_keys (
        keyword TEXT NOT NULL,
        notebook TEXT NOT NULL,
        UNIQUE (keyword, notebook)
        );""")

db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS keys_to_indexes (
        notebook TEXT NOT NULL,
        keyword TEXT NOT NULL,
        note_index TEXT NOT NULL,
        UNIQUE (keyword, notebook, note_index)
        FOREIGN KEY (notebook, keyword) REFERENCES all_keys (notebook, keyword) ON DELETE CASCADE
        );""")
db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS tags_to_keys (
        notebook TEXT NOT NULL,
        tag TEXT NOT NULL,
        keyword TEXT NOT NULL,
        UNIQUE (notebook, tag, keyword)
        FOREIGN KEY (notebook, keyword) REFERENCES all_keys (notebook, keyword) ON DELETE CASCADE
        );
    """)
db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS word_to_indexes (
        notebook TEXT NOT NULL,
        word TEXT NOT NULL,
        note_index TEXT NOT NULL,
        UNIQUE (notebook, word, note_index)
        FOREIGN KEY (notebook, word) REFERENCES all_words (notebook, word) ON DELETE CASCADE
        );
    """)

db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS projects (
        notebook TEXT NOT NULL UNIQUE,
        projectfile TEXT,
        FOREIGN KEY (notebook) REFERENCES notebooks (notebook)
        );
        
        """)
db_cursor.executescript("""
    CREATE TABLE IF NOT EXISTS defaults (
        notebook TEXT NOT NULL,
        attribute TEXT NOT NULL,
        content TEXT NOT NULL,
        UNIQUE (notebook, attribute)
        FOREIGN KEY (notebook) REFERENCES notebooks (notebook)
        );
        """)

db_cursor.executescript("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_all_words ON all_words (notebook, word);""")

db_cursor.executescript("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_all_keys ON all_keys (notebook, keyword);""")

db_cursor.executescript("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_notes ON notes (notebook, note_index);""")

        




db_connection.commit()



# TOP-LEVEL LOOP FOR OPENING AND CLOSING NOTEBOOKS.
add_new_notebook = True
succesful = True # if a new notebook is successfully loaded
while bigloop:
    
    flagvalue = None

    dict_temp = EMPTYCHAR 
 
    
    while (add_new_notebook and not isinstance(flagvalue, str)) or  not successful:
            successful = False 


##        try:
            add_new_notebook = True
            notebookname = prefix+'defaultnotebook'
            flagvalue = 'w'
            if command_stack.size() < 1:
                inputterm = stack_input(queries.OPEN_DIFFERENT,command_stack)
            if command_stack.size() > 0 or inputterm not in list(NOTERMS) + list(QUITTERMS):
                if command_stack.size() > 0:
                    notebookname = command_stack.pop()
                    if SLASH in notebookname:
                        flagvalue = notebookname.split(SLASH)[0]
                        notebookname = notebookname.split(SLASH)[1]
                        display.noteprint((alerts.ATTENTION,labels.OPENING + notebookname))
                        display.noteprint((labels.OPEN_FILES,register.show_openfiles))
                       
                            
                    else:
                        flagvalue = 'c'
                else:

                
                    nb_temp = get_file_name(file_path=os.altsep + 'notebooks',
                                            file_suffix='ND.dat',
                                            file_prefix=prefix,
                                            show_notebooks_too=True)
                    notebookname = nb_temp[0]
                    flagvalue = nb_temp[1]
            else:
                if inputterm in ['quit',
                                 'QUIT',
                                 'Quit',
                                 'Q']:
                    bigloop = False
            nprint(notebookname)
            if notebookname in allnotebooks:
                display.noteprint((alerts.ATTENTION,notebookname + alerts.ALREADY_OPEN))
                continuelooping = True
                add_new_notebook = False
                break
            inp_temp = EMPTYCHAR
            if register.is_open(notebookname):
                display.noteprint((alerts.ATTENTION,notebookname +
                                  alerts.NOT_CLOSED))

                while not inp_temp or inp_temp not in ['o','c','s']:
                    display.noteprint((labels.SELECT,queries.REGISTRY))
                    inp_temp = input('?')
                    if inp_temp:
                        inp_temp = inp_temp[0].lower()
                        
                    
                if inp_temp == 's':
                    continuelooping = True
                    add_new_notebook = False
                elif inp_temp == 'c':
                    register.end(notebookname)
                elif inp_temp == 'o':
                    flagvalue = 'r'
                                

            if not register.is_open(notebookname) or inp_temp == 'o':

##                if add_new_notebook:
##                    try:
##                        db_cursor.execute("INSERT INTO notebooks (notebook) VALUES (?);",(notebookname,))
##                        db_connection.commit()
##                    except:
##                        pass

                if bigloop and add_new_notebook:
                    if command_stack.size() > 0:
                        if command_stack.pop() not in YESTERMS or \
                           stack_input(queries.READ_ONLY,command_stack) not in YESTERMS:
                            pass
                        else:
                            flagvalue = 'r'
                            readonly = True

                if bigloop and add_new_notebook:
##                    try:
                    nprint(notebookname, alerts.OPENING, {'c':'new file',
                                                        'r':'read only',
                                                            'w':'read and write'}[flagvalue])
                    nprint('FLAG=',flagvalue)
                    notebook = Console(notebookname, flagvalue)
                    if not notebook.read_only:
                        register.start(notebookname)
                    if register.exists(notebookname):
                            if input(queries.RESUME_FROM_WHERE) not in NOTERMS:
                                dict_temp = register.fetch(notebookname)
                                
                            
##                    except:
##                        if input(queries.OPEN_AS_NEW):
##                            flagvalue = 'c'
##                            nprint(notebookname, alerts.OPENING, {'c':'new file',
##                                                'r':'read only',
##                                                'w':'read and write'}[flagvalue])
##                    print('FLAG=',flagvalue)
####                            notebook = Console(notebookname, flagvalue)
####                            if not notebook.read_only:

                    register.start(notebookname)
                                
                            

                    
                    notebook.configuration.load()

                    notebook.constitute_key_freq_dict()

                    successful = True

                    allnotebooks[notebookname] = notebook
                    if dict_temp and  '{' in dict_temp and '}' in dict_temp:
                            display.noteprint((alerts.ATTENTION,alerts.SUCCESSFULLY_RESUMED))
                            dict_temp = transform(eval(dict_temp))
                            allnotebooks_tracking [notebookname] = copy.deepcopy(dict_temp)
                            if 'projectset' in allnotebooks_tracking[notebookname]:
                                p_temp = sorted(allnotebooks_tracking[notebookname]['projectset'])
                                t_temp =''
                                for counter,x_temp in enumerate(p_temp):
                                    t_temp += str(counter+1)+': ' + x_temp + '\n'
                                                                    
                                display.noteprint((labels.PREVIOUS_PROJECTS,t_temp))

                                yes_temp = input('RESUME PROJECTS? (y)es (no) or list of projects to resume!')
                                if yes_temp in YESTERMS:
                                    q_temp = p_temp
                                else:
                                    q_temp = [p_temp[int(y_temp.strip())-1]
                                              for y_temp in yes_temp.split(',')
                                              if y_temp.isnumeric()
                                              and int(y_temp.strip())>0
                                              and int(y_temp.strip())<=len(p_temp)]
                                
                            allnotebooks_tracking[notebookname]['projectset'] = q_temp
                            display.noteprint(('RESUMED PROJECTS',
                                               ', '.join(allnotebooks_tracking[notebookname]['projectset'])))
                                
                    else:
                        allnotebooks_tracking [notebookname] = {'lastup':1,
                                                                'uptohere':1,
                                                                'next_up':True,
                                                                'skipped':False,
                                                                'readonly':notebook.read_only,
                                                                'projectset':[]}
                    diagnostics = DiagnosticTracking(filename=notebookname)
                    diagnostics.start()

                
                                                    
                

##        except OSError:
##            print('Fail')
##            successful = False
##        except:
##            print('Other Error')

    if bigloop: 

        if add_new_notebook:

            # procedures upon opening a new notebook

            if reconstitute and input(queries.RECON_WORD) in YESTERMS:

                display.noteprint((alerts.CONSTITUTING_WORD_DICT,
                                   alerts.WAIT))
                allnotebooks[notebookname].constitute_word_dict()
##            if not allnotebooks[notebookname].is_consistent():
##                allnotebooks[notebookname].make_consistent()

            allnotebooks[notebookname].set_iterator(children_too=True,
                                                    flag=allnotebooks[notebookname].defaults.get('setitflag'),
                                                    starting=allnotebooks_tracking [notebookname]['uptohere'])
            spelling_was = allnotebooks[notebookname].check_spelling
            allnotebooks[notebookname].check_spelling = False
            if not allnotebooks[notebookname].indexes():
                backup_was = allnotebooks[notebookname].autobackup
                allnotebooks[notebookname].autobackup = False
                allnotebooks[notebookname].enter({labels.WELCOME_HEAD},
                               labels.WELCOME_BODY)
                allnotebooks[notebookname].autobackup = backup_was
            allnotebooks[notebookname].check_spelling = spelling_was
            if reconstitute and input(queries.RECON_KEY) in YESTERMS:

                allnotebooks[notebookname].constitute_key_freq_dict()
                
                display.noteprint((labels.CONSTITUTING_KEY_FREQ,
                                   alerts.WAIT))

            if (input(queries.SHOW_ALL_NOTES) in YESTERMS)\
               and allnotebooks[notebookname].defaults.get('displayonstart'):                
                if not allnotebooks[notebookname].default_dict['display'] \
                   and not allnotebooks[notebookname].default_dict['all']:
                    allnotebooks[notebookname].showall(shortshow=True,quick=True)
                else:
                    if allnotebooks[notebookname].default_dict['all']:
                        show_list(allnotebooks[notebookname].default_dict['all'],
                                  'INDEXES',0,40,
                                  func=dummy,
                                  present=True)
                    else:
                        allnotebooks[notebookname].default_dict['display'].present()




            
        add_new_notebook = False
    

        continuelooping = True
        series_enter = EMPTYCHAR
        multi_dict[notebookname] = {}

        allnotebooks[notebookname].project = list(allnotebooks_tracking[notebookname]['projectset'])

        # TO MOVE SHELF TO DATABASE

        
        if not allnotebooks[notebookname].defaults.get('usedatabase') and \
           input('DO YOU WANT TO MOVE SHELF TO DATABASE?') in YESTERMS:
            if input('ARE YOU SURE?') in YESTERMS:
                try:
                    db_cursor.execute("INSERT INTO notebooks (notebook) VALUES (?);",(notebookname,))
                    db_connection.commit()
                    nprint(notebookname," ADDED TO DATABASE REGISTER")
                except:
                    pass
            
                 
                allnotebooks[notebookname].defaults.set('usedatabase',True)
                allnotebooks[notebookname].using_shelf = False
                allnotebooks[notebookname].using_database = True
                temp_counter = 0
                total_count = '/' + str(len(allnotebooks[notebookname].note_dict))
                display.noteprint(('ATTENTION!','MOVING NOTE DICTIONARY FROM SHELF!'))
                
                for note_index in allnotebooks[notebookname].note_dict:
                    temp_counter+=1
                    if temp_counter % 100 == 0:
                        print(str(temp_counter) + total_count)
                    note = allnotebooks[notebookname].note_dict[note_index]
                    allnotebooks[notebookname].add_note(note_index,
                                                        note=note)
                    

                    
                    db_connection.commit()
                              
                temp_counter = 0
                total_count = '/' + str(len(allnotebooks[notebookname].key_dict))
                display.noteprint(('ATTENTION!','MOVING  KEY DICTIONARY FROM SHELF!'))
                
                    
                for key in allnotebooks[notebookname].key_dict:
                    
                    indexes = allnotebooks[notebookname].key_dict[key]
                    for index in indexes:
                        try:
                            allnotebooks[notebookname].add_key(key,index)
                        except:
                            print('fail')
                            pass
                    temp_counter+=1
                    if temp_counter % 100 == 0:
                        print(str(temp_counter) + total_count)
                    
                    
                    db_connection.commit()
                temp_counter = 0
                total_count = '/' + str(len(allnotebooks[notebookname].tag_dict))
                display.noteprint(('ATTENTION!','MOVING  TAG DICTIONARY FROM SHELF!'))
                for tag in allnotebooks[notebookname].tag_dict:
                    keys = allnotebooks[notebookname].tag_dict[tag]
                    for key in keys:
                        try:
                            allnotebooks[notebookname].add_tag(tag,key)
                        except:
                            print('fail')
                            pass
                    temp_counter+=1
                    if temp_counter % 10 == 0:
                            print(str(temp_counter) + total_count)
                    db_connection.commit()
                temp_counter = 0
                total_count = '/' + str(len(allnotebooks[notebookname].word_dict))
                display.noteprint(('ATTENTION!','MOVING  WORDDICTIONARY FROM SHELF!'))
                for word in allnotebooks[notebookname].word_dict:
                    indexes = allnotebooks[notebookname].word_dict[word]
                    for index in indexes:
                        try:
                            allnotebooks[notebookname].add_word(word,index)
                        except:
                            print('fail')
                            pass
                
                    temp_counter+=1
                    if temp_counter % 1000 == 0:
                            print(str(temp_counter) + total_count)
                    db_connection.commit()

                try:

                    allnotebooks[notebookname].note_dict.close()
                    print('NOTEBOOK CLOSED')
                except:
                    print('NOTEBOOK NOT CLOSED')
                    
                try:
                    allnotebooks[notebookname].key_dict.close()
                    print('KEYDICT CLOSED')
                except:
                    print('KEYDICT NOT CLOSED')
                try:
                    
                    allnotebooks[notebookname].tag_dict.close()
                    print('TAGDICT CLOSED')
                except:
                    print('TAGDICT NOT CLOSED')
                try:
                    allnotebooks[notebookname].word_dict.close()
                    print('WORDDICT CLOSED')
                except:
                    print('WORDDICT NOT CLOSED')

                
                # to migrate the projects 
                allnotebooks[notebookname].default_dict['projects'] = ProjectManager(notebookname=notebookname,
                                                                                     project_dictionary=allnotebooks[notebookname].default_dict['projects'].return_dict(),
                                                                                     connection=db_connection,
                                                                                     cursor=db_cursor)

                

        else:
            if allnotebooks[notebookname].defaults.get('usedatabase') or \
               input('Switch to database mode to use existing database?') in YESTERMS:
                allnotebooks[notebookname].defaults.set('usedatabase',True)
                allnotebooks[notebookname].using_database = True
                allnotebooks[notebookname].using_shelf = False
                
                    
            else:
                allnotebooks[notebookname].using_database = False
                allnotebooks[notebookname].using_shelf = True
        if input("Load projects from database?") in YESTERMS:
                    db_cursor.execute("SELECT projectfile FROM projects WHERE notebook=?;",(notebookname,))
                    
                    text = db_cursor.fetchone()[0]
                    if text:
                        allnotebooks[notebookname].default_dict['projects'].import_string(text)
                        display.noteprint((alerts.ATTENTION,'SUCCESSFULLY LOADED'))
                   
     

        while continuelooping:

            lastup = allnotebooks_tracking[notebookname]['lastup']
            uptohere = allnotebooks_tracking[notebookname]['uptohere']
            next_up = allnotebooks_tracking[notebookname]['next_up']
            skipped = allnotebooks_tracking[notebookname]['skipped']


            if prefix == 'beta' or override:
                continuelooping, skipped, lastup, next_up, uptohere,\
                                 close_notebook,series_enter = \
                                 allnotebooks[notebookname].enter_command(skipped=skipped,
                                                                          lastup=lastup,
                                                                          next_up=next_up,
                                                                          uptohere=uptohere,
                                                                          notebookname=notebookname,
                                                                          series_enter=series_enter)
                

            else:

                try:
                    continuelooping, skipped, lastup, \
                                     next_up, uptohere, \
                                     close_notebook,series_enter=allnotebooks[notebookname].enter_command(
                        skipped=skipped,
                        lastup=lastup,
                        next_up=next_up,
                        uptohere=uptohere,
                        notebookname=notebookname,
                        series_enter=series_enter)

                except KeyError:
                    nprint('KEY ERROR')
                    notebook.usesequence = False
                    notebook.indexchanged = True
                    nprint('RECONSTITING INDEX SEQUENCE')
                    notebook.default_dict['indexlist'] = OrderedList(notebook.indexes(),
                                                                     indexstrings=True)
                    uptohere = Index(notebook.indexes()[-1])
                    lastup = uptohere
                    nprint(str(uptohere))
                except AttributeError:
                    nprint('ATTRIBUTE ERROR')
                except FileNotFoundError:
                    nprint('FILE NOTE FOUND ERROR')
                    
                except IndexError:
                    nprint('INDEX ERROR')
                except TypeError:
                    nprint('TYPE ERROR')
                except NameError:
                    nprint('NAME ERROR')
                except EOFError:
                    nprint('EOF ERROR')
                except RuntimeError:
                    nprint('Runtime Error')
                except UnicodeError:
                    nprint('Unicode Error')
                except PermissionError:
                    nprint('Permission Error')
                except OSError:
                    nprint('OSError')
                except:
                    nprint('OTHER ERROR')
            
            allnotebooks_tracking[notebookname]['lastup'] = lastup
            allnotebooks_tracking[notebookname]['uptohere'] = uptohere
            allnotebooks_tracking[notebookname]['next_up'] = next_up
            allnotebooks_tracking[notebookname]['skipped'] = skipped

        if not continuelooping:

            
            opennotebooks = DisplayList(displayobject=display)
            for counter, nb_temp in enumerate(sorted(allnotebooks.keys())):
                opennotebooks.append(str(counter+1) + ': ' + nb_temp)
            

            if not close_notebook:

                #this is activated when switching 
                
                opennotebooks.present()
                #Displays the notebooks that are already open       
                go_temp = True
                quited_only = False
                while go_temp:
                    old_notebookname = notebookname
                    display.noteprint((queries.SELECT_NOTEBOOK_HEADING,
                                       queries.SELECT_OPEN_NOTEBOOK))
                    if command_stack.size() > 0:
                        notebookname = command_stack.pop()
                    else:
                        notebookname = input(QUESTIONMARK + BLANK)
                    if notebookname in NEWTERMS:
                        add_new_notebook = True
                        go_temp = False
                    elif notebookname in allnotebooks:
                        go_temp = False
                        successful = True 
                        display.noteprint((alerts.SELECTED,notebookname))
                    elif notebookname.isnumeric() and 1 <= int(notebookname) <= len(allnotebooks.keys()):
                        notebookname = sorted(allnotebooks.keys())[int(notebookname)-1]
                        display.noteprint((alerts.SELECTED,notebookname))
                        go_temp = False
                        successful = True 
                    elif notebookname in QUITTERMS:
                        close_notebook = True
                        quited_only = True
                        notebookname = old_notebookname
                        go_temp = False
                    elif notebookname in QUITALLTERMS:
                        close_notebook = True
                        command_stack.add('quitall')
                        go_temp = False
                        notebookname = old_notebookname
                    
                
            if close_notebook and not readonly :

                allnotebooks[notebookname].close()
                display.noteprint((alerts.ATTENTION,notebookname+alerts.IS_CLOSING))
                del allnotebooks[notebookname]
                if not allnotebooks_tracking[notebookname]['readonly']:
                    register.end(notebookname,str(transform(allnotebooks_tracking[notebookname])))
                opennotebooks.clear()
                for counter, nb_temp in enumerate(sorted(allnotebooks.keys())):
                    opennotebooks.append(str(counter+1) + COLON + BLANK + nb_temp)
                opennotebooks.present()
                go_temp = True
                while go_temp:
                    display.noteprint((queries.SELECT_NOTEBOOK_HEADING,
                                       queries.SELECTING_NOTEBOOK))
                        
                    if command_stack.size() > 0:
                        notebookname = command_stack.pop()
                    else:
                        notebookname = input(QUESTIONMARK + BLANK)

                    if notebookname in NEWTERMS:
                        add_new_notebook = True
                        go_temp = False
                    elif notebookname in allnotebooks:
                        go_temp = False
                        display.noteprint((alerts.SELECTED,notebookname))
                    elif notebookname.isnumeric() and 1 <= int(notebookname) <= len(allnotebooks.keys()):
                        notebookname = sorted(allnotebooks.keys())[int(notebookname)-1]
                        display.noteprint((alerts.SELECTED,notebookname))
                        go_temp = False
                    elif notebookname in QUITTERMS + QUITALLTERMS:
                        for notebookname in list(allnotebooks.keys()):
                            allnotebooks[notebookname].close()
                            del allnotebooks[notebookname]
                            display.noteprint((alerts.ATTENTION,notebookname+alerts.IS_CLOSING))
                            if not allnotebooks_tracking[notebookname]['readonly']:
                                register.end(notebookname,str(transform(allnotebooks_tracking[notebookname])))
                        bigloop = False
                        go_temp = False 
                        
                        
                    
            
