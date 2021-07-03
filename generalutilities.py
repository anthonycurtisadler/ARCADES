from globalconstants import UNDERLINE, EMPTYCHAR, BLANK, PERIOD, COMMA, COLON, EOL, POUND, STAR, DASH, PLUS
import nformat
from itertools import product
import datetime
from displaylist import DisplayList

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



def dummy(x_temp):


    """#dummy function to be passed as argument"""

    return x_temp


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


