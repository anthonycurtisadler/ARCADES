from globalconstants import UNDERLINE, EMPTYCHAR, BLANK, PERIOD, COLON, EOL, POUND
from nformat import purgeformatting

def split_into_columns (t_temp,
                        breaker=BLANK,
                        width=80,
                        columns=3):

    """ splits text into columns.
    """

    t_temp = purgeformatting(t_temp)
    
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
