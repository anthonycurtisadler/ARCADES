from globalconstants import BOX_CHAR, UNDERLINE, ATSIGN, \
     EMPTYCHAR, BLANK, PERIOD, COMMA, COLON, EOL, \
     POUND, STAR, DASH, PLUS, TAB, SLASH, VERTLINE, LEFTNOTE, RIGHTNOTE, \
     EQUAL, CARET, PERCENTAGE, LEFTBRACKET, RIGHTBRACKET, DOLLAR 
import nformat
from itertools import product
import datetime
from displaylist import DisplayList
from rangelist import range_find
from indexorderer  import index_orderer
from indexclass import Index 
from indexutilities import index_expand
import string





ind_ord = index_orderer()


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

def reduce_tupples(entrylist):


    """provides a list of tupples giving the 'moves'
    needed to reduce a NoteBook"""

    #Create a list of top-level (non-child) indexes.
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


def get_range(entryterm,
              orequal=True,
              complete=False,
              sort=True,
              many=False,
              indexes=True,
              notebook=None):

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

def dummy(x_temp):


    """#dummy function to be passed as argument"""

    return x_temp

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


def stack_input(query,stack_object):

    """if the stack is not empty, pulls from the stack.
    otherwise, queries use
    """

    if stack_object.size() > 0:
        return stack_object.pop()
    else:
        return input (query)


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

def combine_sequence_values (keylist):

    """combines sequence keys into ranges.
       used with const_dict
       
    """

    from indexclass import Index

    sequence_key_dict = {}
    other_key_set = set()
    returnlist = []
    
    def all_numeric (l):
        for x in l:
            if not x.isnumeric():
                return False
        else:
            return True

    def all_float (l):
        for x in l:
            if not x.replace('.','').isnumeric() or x.count('.')>1:
                return False
        else:
            return True 
            
        

    for key in keylist:
        if ATSIGN in key:

            if ATSIGN+UNDERLINE in key:
                value = key.split(ATSIGN+UNDERLINE)[1]
            elif ATSIGN+POUND in key:
                value = key.split(ATSIGN+POUND)[1]
            elif ATSIGN in key:
                value = key.split(ATSIGN)[1]
            if value:
                
                head = key.split(value)[0]
            else:
                head = key
                value = ''
            if value.endswith('.0'):
                value = value[:-2]

            if value:
                if head not in sequence_key_dict:
                    sequence_key_dict[head] = {value}
                else:
                    sequence_key_dict[head].add(value)
        else:
            other_key_set.add(key)

    for head in sequence_key_dict:
        if UNDERLINE not in head and POUND not in head and all_numeric(sequence_key_dict[head]):
            
            all_values = range_find(list(sequence_key_dict[head]), breaker=';')
            returnlist.append(head+all_values)
        elif UNDERLINE not in head and POUND not in head and all_float(sequence_key_dict[head]):
            ordered_indexes = ind_ord.format([Index(x) for x in sequence_key_dict[head]])
            returnlist.append(head+ordered_indexes)
        elif UNDERLINE in head:            
            ordered_indexes = ind_ord.format([Index(x) for x in sequence_key_dict[head]])
            returnlist.append(head+ordered_indexes)
        elif POUND in head:
##            ordered_dates = ind_ord.format([datetime.datetime([int(y) for y in x.split('-')]) for x in sequence_key_dict[head]])
##            returnlist.append(head+ordered_indexes)
            pass
            
    returnlist += list(other_key_set)
    return sorted(returnlist) 
    

def select_func (entrylist):

    """ passed-in function to select form menu """

    to_keep = input('ENTER KEYWORDS')
    to_keep = rangelist.range_set(to_keep)
    return [entrylist[a_temp]
            for a_temp in to_keep
            if a_temp in range(len(entrylist))]


def format_text_output (text):

    return text.replace('//','~!SEP!~').replace(':','~!COLON!~').replace(';','~!SEMICOLON!~').replace('\n','~!EOL!~')

def unformat_text_output (text):

    return text.replace('~!SEP!~','//',).replace('~!COLON!~',':').replace('~!SEMICOLON!~',';').replace('~!EOL!~','\n')
    

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

def concatenate(lista,
                listb,
                infix=EMPTYCHAR):


    """Concatenates the strings from two lists,
    joining them with index
    """

    return [a_temp+(infix*max([len(b_temp), 1]))
            +b_temp for a_temp,
            b_temp in product(lista, listb)]


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

def is_date(entry,returndate=False,maxlen=0):



    """tests if a string constitutes a date, returning either
    a boolean value or a converted date """

    if type(entry) == datetime.date:
        if not returndate:
            return True
        
        return entry

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
            entry+=[1,1]
            return datetime.date(entry[0],
                                 entry[1],
                                 entry[2])
        elif len(entry) == 5 or maxlen <= 5:
            entry+=[1,1,1,1]
            return datetime.datetime(entry[0],
                                     entry[1],
                                     entry[2],
                                     entry[3],
                                     entry[4])
        elif len(entry) == 7:
            entry+=[1,1,1,1,1,1]
            return datetime.datetime(entry[0],
                                     entry[1],
                                     entry[2],
                                     entry[3],
                                     entry[4],
                                     entry[5],
                                     entry[6])
    
    return True 


def repeat_function_on_set(enterset,function=None):

    if function is None:
        function = dummy

    returnset = set()
    for x_temp in enterset:
        returnset.update(function(x_temp))
    return returnset 

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

def side_note(texts,
              widths=[30]+[20]*10,
              counters=False,
              columnchar=UNDERLINE):

    """Joins texts together into columns
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
              compactwidth=None,
              display=None):

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


