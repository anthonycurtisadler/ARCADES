"""Module with general functions for formatting text
pylint rated 9.61/10
"""

import extract
from globalconstants import VERTLINE, EOL, BLANK, EMPTYCHAR,\
     COMMA, COLON, LEFTNOTE, RIGHTNOTE,PERIOD, BOX_CHAR, LEFTPAREN, RIGHTPAREN
from indexutilities import index_reduce, index_expand, index_is_reduced


def columns(text,
            listobject,
            buffer=3,
            not_centered=None,
            middle=VERTLINE,
            displaymiddle=VERTLINE,
            columnwidth=None,
            compactwidth=None,
            encased=False,
            leftmargin=0,
            allcapscenter=False):


    """#used to format text passed through listobject
    into an arbitrary number of evenly spaced columns.
    Verticle slash "|" used to divide columns in each line.
    "||" skips a row. For blank columns, make
    sure to separate verticle slashes with a space.
    Add -1 to not_centered to void centered along y axis 
    columnwidth and compactwidth for preset-widths.
    """

    def matchsize (phrase,
                   length):

        if len(phrase) > length:
            phrase = phrase[0:length]
        if len(phrase) < length:
            phrase += (length - len(phrase))*BLANK
        return phrase
            
    if not columnwidth:
        columnwidth = (0,0)*20
    if not compactwidth:
        compactwidth = (0,0)*20
    columnwidth += (0,0)*20
    compactwidth += (0,0)*20


    if not_centered is None:
        not_centered = set()
    horizontal_not_centered = {a_temp for a_temp in not_centered if a_temp > -1}
    vertical_not_centered = {abs(a_temp) for a_temp in not_centered if a_temp < 0}
    max_width_dict = {}
    for line in text.split(EOL):

        if middle*2 in line:
            pass
        elif middle in line:
            phrases = line.split(middle)

            for counter, phrase in enumerate(phrases):
                phrase = phrase.strip()
                if counter in max_width_dict:
                    if len(phrase) > max_width_dict[counter]:
                        max_width_dict[counter] = len(phrase)
                else:
                    max_width_dict[counter] = len(phrase)
    column_count = len(max_width_dict)
    for y_count, line in enumerate(text.split(EOL)):
        newline = EMPTYCHAR
        e_mark = encased * BOX_CHAR['v']

        if middle*2 in line:
            listobject.append(EMPTYCHAR)
                #This skips a line.
        elif middle in line:
            phrases = line.split(middle)

            for counter, phrase in enumerate(phrases):
                if counter < len(columnwidth):
                        # iterates over the separate columns in the line
                    phrase = phrase.strip()
                    phrase_length = max_width_dict[counter]+buffer

                    
                    if columnwidth[counter] > 0 and columnwidth[counter] > phrase_length:
                        phrase_length = columnwidth[counter]
                    if compactwidth[counter] > 0:
                        phrase_length = compactwidth[counter]

                    

                    if  (allcapscenter and phrase == phrase.upper()) and (counter not in horizontal_not_centered
                                                     and y_count not in vertical_not_centered):
                        if '/C/' in phrase:
                            phrase = phrase.replace('/C/',BLANK*3)
                        newline += (matchsize(center(phrase,
                                            phrase_length),phrase_length)
                                    +(displaymiddle*{True: 1,
                                              False: 0}[counter
                                                        in range(0,
                                                                 column_count-1)]))
                        # IF ALLCAPS then CENTER, as for column headings

                    
                    else:
                        newline += (matchsize(phrase,phrase_length)
                                    +(displaymiddle*{True:1,
                                              False:0}[counter
                                                       in range(0,
                                                                column_count-1)]))
            listobject.append(leftmargin*BLANK+e_mark+newline+e_mark)
    return sum(max_width_dict.values())



def encase(text,
           termset,
           surround=False):


    """surrounds words in the text with double arrow brackets.
    Surround = True if word is to be surrounded by spaces.
    """

    if termset == set():
        return text
    termlist = list(termset)
    termlist.sort()
    termlist.sort(key=len)

    for term in termlist:
        if surround:
            term = BLANK + term + BLANK
        text = text.replace(term, LEFTNOTE+LEFTNOTE+term+RIGHTNOTE+RIGHTNOTE)
    return text

def center(text,
           width,
           char=BLANK):

    


    """centers text. Width= total width of the segment
    in which the text will be centered. Char is used for the
    character surrounding the centered text
    """

    

    before_after = max([0, int((width-len(text))/2)])
    return (char*before_after)+text+(char*before_after)

def right_justify(text,
         width,
         char=BLANK):

    """ right justify text. Width= total width of the segment
    in which the text will be centered. Char is used for the
    character surrounding the centered text
    """

    before_after = max([0, int((width-len(text)))])
    return (char*before_after)+text
    


    

def remove_between(entrytext,
                   lchar,
                   rchar):


    """ removes str between lchar and rchar """
    for a_temp in extract.extract(entrytext, lchar, rchar):
        entrytext = entrytext.replace(lchar+a_temp+rchar, EMPTYCHAR)
    return entrytext

def format_keys(keyset,maxlegnth=0):


    """returns a string with a formatted list of keys"""

    returntext = EMPTYCHAR
    for k_temp in sorted(list(keyset)):
        
        if maxlegnth > 0 and len(k_temp) > maxlegnth:
            k_temp = k_temp[0:maxlegnth]+PERIOD*3
        returntext += index_reduce(str(k_temp)) + COMMA + BLANK
    return returntext[:-2]


def format_meta(metadictionary):


    """returns a string showing metadata"""

    returntext = EMPTYCHAR
    returntext += 'SIZE' + BLANK + COLON + BLANK + str(metadictionary['size'])+EOL
    returntext += 'USER' + BLANK + COLON + BLANK + str(metadictionary['user'])+EOL
    returntext += 'DATE' + BLANK + COLON + BLANK +format_keys(metadictionary['date'])+EOL
    return returntext

def reduce_blanks(text):


    """Reduces all multiple blanks to single blanks."""

    while  BLANK + BLANK in text:
        text = text.replace(BLANK + BLANK, BLANK)
    return text

def purgeformatting(text,flag='nbcedlr'):

    purgelist = []
    for f_temp,m_temp in [('n','/NEW/'),
                          ('b','/BREAK/'),
                          ('c','/COL/'),
                          ('e','/ENDCOL/'),
                          ('d','/DEF/'),
                          ('s','/SPLIT/'),
                          ('x','/ENDSPLIT/'),
                          ('y','/M/'),
                          ('l','[/'),
                          ('r','/]')]:
        if f_temp in flag:
            purgelist.append(m_temp)


    for x_temp in purgelist:
        text = text.replace(x_temp,BLANK)
    return text 

def purgesets(keysetlist,
              noallcap=False,
              nofirstcap=False,
              nolowercase=False,
              purgelist=None):


    """Eliminates from the keysets alls keys that are either
    in all caps, or first cap, according to parameteres
    """
    if purgelist is None:
        purgelist = []

    for ks_temp in keysetlist:

        for k_temp in list(ks_temp):
            if ((noallcap and k_temp.upper().replace('ß', 'ss') == k_temp.replace('ß', 'ss')) 
                 or (nofirstcap and k_temp.capitalize().replace('ß', 'ss') == k_temp.replace('ß', 'ss'))
                 or (nolowercase and k_temp.lower() == k_temp)
                 or k_temp in purgelist):
                ks_temp.remove(k_temp)
    return [k_temp for k_temp in keysetlist if k_temp != set()]
