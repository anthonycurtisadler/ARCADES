""" Module containing the Display class, which is used to display formatted notes
pylint rated 9.20/10 
"""


from globalconstants import BOX_CHAR, MARGINFACTOR,\
     DASH, BLANK, EOL, EMPTYCHAR, COLON, UNDERLINE, POUND, \
     LEFTBRACKET, RIGHTBRACKET, SLASH
from generalutilities import side_note, split_into_columns  
from nformat import columns, purgeformatting 
from displaylist import DisplayList

    
## CLASSES

class Display:


    """ The fundamental class for displaying formatted notes
    Noteprint is called externally to print a note, while
    width needed is called externally to establish the
    needed width of a note, given its stated width and content.
    Lineprint is only called from within noteprint function
    of display class, and prints individual lines."""

    def __init__(self,rectify=False):
        
        self.rectify = rectify

    def lineprint(self,
                  line,
                  showsize=60,
                  maxsize=65,
                  printyes=True,
                  bracket=True,
                  splitchar=BLANK,
                  is_embedded=False,
                  p_indent=0,
                  leftmargin=0):

        """prints out individual lines of note.
        showsize = basic size for note.
        Maxsize = maximum size for note.
        printyet = True is note should be printed.
        splitchar - used to split line into elements
        is_embedded - true if note is contained in another note
        indent - Identation to be added to the note."""


        def splitnumber(integer):
            if integer % 2 == 0:
                return (int(integer/2),int(integer/2))
            if integer % 2 == 1:
                return (int((integer-1)/2),int((integer-1)/2+1))
        
        def embedded(t_temp):

            """ tests to see if there is a note embedded within the note """

            for a_temp in [BOX_CHAR['v'],
                           BOX_CHAR['lu'],
                           BOX_CHAR['lm'],
                           BOX_CHAR['h']]:

                if a_temp in t_temp:
                    return True

            return False

        if showsize > maxsize:
            maxsize = showsize
        linelist = []
        nextline = EMPTYCHAR
        returntext = EMPTYCHAR
        center = False
        leftalign = False
        


        if line not in ['H', 'M', 'F']:
            # If the note had another note embedded in it
            if embedded(line) or is_embedded:

                for l_temp in line.split(EOL):
                    linelist.append(BOX_CHAR['v']*bracket+leftmargin*BLANK+l_temp
                                    +((maxsize-leftmargin-1-len(l_temp))*BLANK)
                                    +BOX_CHAR['v']*bracket)

            else:
                if line.startswith('/C/'):
                    line = line.replace('/C/',EMPTYCHAR)
                    center = True
                if line.startswith('/R/'):
                    line = line.replace('/R/',EMPTYCHAR)
                    leftalign = True


                
                #if the note does not have an embedded note in it
                for word in line.split(splitchar):
                    word = word.replace('_',BLANK)

                    nextline += str(word)+splitchar
                    if len(nextline) > showsize-int(showsize/MARGINFACTOR):
                        nextline = nextline.replace(EOL, BLANK)

                        if not center and not leftalign:
                            middlestuff = leftmargin*BLANK+nextline+((maxsize-leftmargin-1-len(nextline))*BLANK)
                        elif center:
                            margins = splitnumber((maxsize-leftmargin-1-len(nextline)))
                            middlestuff = leftmargin*BLANK+(BLANK*margins[0])+nextline+(BLANK*margins[1])
                        else:
                            middlestuff = leftmargin*BLANK+((maxsize-leftmargin-1-len(nextline))*BLANK)+nextline
                            
                            
                        linelist.append(BOX_CHAR['v']*bracket+middlestuff
                                        +BOX_CHAR['v']*bracket)
                        nextline = EMPTYCHAR
                    elif EOL in nextline:
                        nextline = nextline.replace(EOL, BLANK)
                        
                        if not center and not leftalign:
                            middlestuff = leftmargin*BLANK+nextline+((maxsize-leftmargin-1-len(nextline))*BLANK)
                        elif center:
                            margins = splitnumber((maxsize-leftmargin-1-len(nextline)))
                            middlestuff = leftmargin*BLANK+(BLANK*margins[0])+nextline+(BLANK*margins[1])
                        else:
                            middlestuff = leftmargin*BLANK+((maxsize-leftmargin-1-len(nextline))*BLANK)+nextline

                        linelist.append(BOX_CHAR['v']*bracket+middlestuff+BOX_CHAR['v']*bracket)
                        nextline = EMPTYCHAR
                        linelist.append(BOX_CHAR['v']
                                        *bracket+leftmargin*BLANK+nextline
                                        +((maxsize-leftmargin-1-len(nextline))*BLANK)
                                        +BOX_CHAR['v']*bracket)
                if nextline != EMPTYCHAR:
                    if not center and not leftalign:
                        middlestuff = leftmargin*BLANK+nextline+((maxsize-leftmargin-1-len(nextline))*BLANK)
                    elif center:
                        margins = splitnumber((maxsize-leftmargin-1-len(nextline)))
                        middlestuff = leftmargin*BLANK+(BLANK*margins[0])+nextline+(BLANK*margins[1])
                    else:
                        middlestuff = leftmargin*BLANK+((maxsize-leftmargin-1-len(nextline))*BLANK)+nextline


                    linelist.append(BOX_CHAR['v']*bracket+middlestuff
                                    +BOX_CHAR['v']*bracket)

        else:
            if bracket:
                if line == 'H':
                    linelist = [BOX_CHAR['lu']
                                +(BOX_CHAR['h']*(maxsize-1))
                                +BOX_CHAR['ru']]
                elif line == 'M':
                    linelist = [BOX_CHAR['lm']
                                +(BOX_CHAR['h']*(maxsize-1))
                                +BOX_CHAR['rm']]
                elif line == 'F':
                    linelist = [BOX_CHAR['ll']
                                +(BOX_CHAR['h']*(maxsize-1))
                                +BOX_CHAR['rl']]
            else:
                linelist = [DASH*(maxsize+2)]
        if printyes:
            leftstuff = (int(p_indent/50))*']'+(p_indent % 50)*BLANK
            for l_temp in linelist:
                print(leftstuff+l_temp)
                
                returntext += leftstuff+l_temp+EOL    
        else:

            for l_temp in linelist:
                returntext += l_temp+EOL
        return returntext

    def noteprint(self,
                  textlist,
                  notenumber=0,
                  brackets=True,
                  param_width=60,
                  np_temp=False,
                  param_is_emb=False,
                  param_indent=0,
                  param_spacing=0,
                  leftmargin=0,
                  rectify=None,
                  override=False):

        """ prints the note.
        notenumber == index position of note.
        param_width = width of note
        np_temp = False if printing, True if not printing.
        param_indent --- indicates indentation of note
        param_spacing --- indicated spacing of note """

        def box_or_nothing(char):
            if char not in [BOX_CHAR['h'],BOX_CHAR['rm']]:
                return BLANK
            else:
                return char

        npp_temp = np_temp
        np_temp = True

        if not rectify:
            rectify = self.rectify
        modified = False  ## to keep track of whether different widths introd.


        maximum = self.width_needed(textlist, p_width=param_width,leftmargin=0)
        param_width_def = param_width
        maximum_def = maximum 
        #the maximum width of the lines in the note
        if len(textlist) == 1:
            returntext = textlist[0]
            if not np_temp:
                print(textlist[0])
        #if the note is embedded in another note
        elif BOX_CHAR['lu'] in textlist[1]:

            head = textlist[0]    #head are the keywords
            body = textlist[1].replace('[BREAK]',
                                       '/BREAK/').replace('[NEW]',
                                                          '/NEW/') #to deal with different
                                                                                     #coding from before 
            #body is the text
            

            
                
            
            returntext = EMPTYCHAR

            returntext += self.lineprint('H',
                                         showsize=param_width,
                                         maxsize=maximum,
                                         printyes=not np_temp,
                                         p_indent=param_indent,
                                         leftmargin=leftmargin,
                                         bracket=brackets)
                                         # prints the top of the box
            if notenumber > 0:
                returntext += self.lineprint(POUND+str(notenumber),
                                             showsize=param_width,
                                             maxsize=maximum,
                                             printyes=not np_temp,
                                             p_indent=param_indent,
                                             leftmargin=leftmargin,
                                             bracket=brackets)
                                             #print the number of the note
            returntext += self.lineprint(head,
                                         showsize=param_width,
                                         maxsize=maximum,
                                         printyes=not np_temp,
                                         p_indent=param_indent,
                                         leftmargin=leftmargin,
                                         bracket=brackets)
                                        # print the keywords
            returntext += self.lineprint('M',
                                         showsize=param_width,
                                         maxsize=maximum,
                                         printyes=not np_temp,
                                         p_indent=param_indent,
                                         leftmargin=leftmargin,
                                         bracket=brackets)
            # print the divider between box heading and box body
            for line in body.split(EOL):
                #split the main body into lines
                if (param_spacing > 0 or line.strip() != EMPTYCHAR):

                    if not override and  '/BREAK/' in line or '/NEW/' in line:
                        if '/BREAK/' in line:
                            breaker = ['M']
                        else:
                            breaker = ['F','H']

                        for temp_x in breaker:
                            returntext += self.lineprint(temp_x,
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)
                    else:

                        returntext += self.lineprint(line,
                                                     showsize=param_width,
                                                     maxsize=maximum,
                                                     printyes=not np_temp,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)
                                                      #add a new line
            returntext += self.lineprint('F',
                                         showsize=param_width,
                                         maxsize=maximum,
                                         printyes=not np_temp,
                                         p_indent=param_indent,
                                         leftmargin=leftmargin,
                                         bracket=brackets)
            returntext += (EOL*param_spacing)

        else:            # For a non-embedded note 
            head = textlist[0]
            body = textlist[1].replace('[BREAK]',
                                       '/BREAK/').replace('[NEW]','/NEW/')
            if rectify and ('/COL/' in body
                            or '/NEW/' in body
                            or '/BREAK/' in body
                            or LEFTBRACKET + SLASH in body):
                np_temp = True 
            if '/ENDCOL/' in body and '/COL/' not in body:
                body = body.replace('/ENDCOL/',EMPTYCHAR)
            returntext = EMPTYCHAR

            if head:

                # Print header
                returntext += self.lineprint('H',  
                                             showsize=param_width,
                                             maxsize=maximum,
                                             printyes=not np_temp,
                                             is_embedded=param_is_emb,
                                             p_indent=param_indent,
                                             leftmargin=leftmargin,
                                             bracket=brackets)
                # Print note number
                if notenumber > 0:
                    returntext += self.lineprint(POUND+str(notenumber), 
                                                 showsize=param_width,
                                                 maxsize=maximum,
                                                 printyes=not np_temp,
                                                 is_embedded=param_is_emb,
                                                 p_indent=param_indent,
                                                 leftmargin=leftmargin,
                                                 bracket=brackets)
                # Keys
                returntext += self.lineprint(head,                  
                                             showsize=param_width,
                                             maxsize=maximum,
                                             printyes=not np_temp,
                                             is_embedded=param_is_emb,
                                             p_indent=param_indent,
                                             leftmargin=leftmargin,
                                             bracket=brackets)
                # divider between keys and main body
            else:
                returntext += self.lineprint('H',  
                                             showsize=param_width,
                                             maxsize=maximum,
                                             printyes=not np_temp,
                                             is_embedded=param_is_emb,
                                             p_indent=param_indent,
                                             leftmargin=leftmargin,
                                             bracket=brackets)


            columnate = False
            columns_done = False
            columnlist = DisplayList()
            columntextlist = []
            splitting = False
            starting = True
            

            
            if not override and '/COL/' in body:
                if (len(body.split('/COL/')[0])) < 5:
                    
                    body = '/COL/'.join(body.split('/COL/'))[1:]
            if not override and ('/DEF/' in body or LEFTBRACKET + SLASH in body):
                rectify = False

            if body.replace(BLANK,EMPTYCHAR).replace(EOL,EMPTYCHAR):

                for line in body.split(EOL):

                    if columns_done:
                        columnate = False
                        columns_done = True

                    # Initiate columns.

                    if starting:
                        if '/COL/' not in line and head:
                            returntext += self.lineprint('M',                 
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         is_embedded=param_is_emb,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)
                        elif head:


                            returntext += self.lineprint('F',                 
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         is_embedded=param_is_emb,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)
                    starting = False
                        
                    
                    if not override and line.startswith('/COL/') and not splitting:
                        modified = True
    ##                    returntext += self.lineprint('F',
    ##                                                 showsize=param_width,
    ##                                                 maxsize=maximum,
    ##                                                 printyes=not np_temp,
    ##                                                 is_embedded=param_is_emb,
    ##                                                 p_indent=param_indent,
    ##                                                 leftmargin=leftmargin)
     
                        first_line = True
                        line = line[5:]
                        columnate = True
                        if line:
                            columntextlist.append(line)

                    elif not override and splitting and '/M/' in line:
                        column_count += 1
                        line = line.split('/M/')
                        if line[0]:
                            columntextlist.append(line[0])
                        columntextlist.append('/M/')
                        if line[1]:
                            columntextlist.append(line[1])
                        
                        
                    elif (not override
                          and line.startswith('/SPLIT/')
                          and not columnate):
                        modified = True
                        first_line = True
                        line = line[7:]
                        splitting = True
                        column_count = 1
                        if line:
                            columntextlist.append(line)

                    # For the middle of the columsn.
                    elif (not override
                          and ((columnate and '/ENDCOL/' not in line)
                               or (splitting and '/ENDSPLIT/' not in line))):                                                
                        columntextlist.append(line)

                    # for the end of the columns 
                    elif not override and ((columnate and '/ENDCOL/' in line) or (splitting and '/ENDSPLIT/' in line)):
                        line = line.replace('/ENDCOL/',EMPTYCHAR).replace('/ENDSPLIT/',EMPTYCHAR)
                        if line:
                            columntextlist.append(line)

                        if splitting:
                            splittextlist = BLANK.join(columntextlist).split('/M/')
 
                            splittext = side_note(splittextlist)

                            columns(splittext,
                                    columnlist,
                                    middle=UNDERLINE,
                                    encased=True,
                                    leftmargin=leftmargin)
                            
                            
                        else:     
                                
                            columns(EOL.join(columntextlist),
                                    columnlist,
                                    middle=UNDERLINE,
                                    encased=True,
                                    leftmargin=leftmargin)
                        c_temp = columnlist.show(returntext=True)
                        if not c_temp:
                            c_temp = EMPTYCHAR

                        #determine width of the columned note
                        param_width_def = param_width 
                        maximum_def = maximum
                        param_width =  max([len(x_temp) for x_temp in c_temp.split(EOL)])-1
                        maximum = param_width

                        c_temp = EOL.join([x_temp[0:-1]+(param_width-len(x_temp)+1)*BLANK+x_temp[-1]
                                           for x_temp
                                           in c_temp.split(EOL)
                                           if x_temp])
                        ## add spaces at the end of the lines so then match.
                            

                        # Print the top of the columned note 
                        returntext += self.lineprint('H',
                                                     showsize=param_width,
                                                     maxsize=maximum,
                                                     printyes=not np_temp,
                                                     is_embedded=param_is_emb,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)

                        # Determine the body of the columned note.
                        returntext += c_temp + EOL
                        if not np_temp:
                            print(c_temp)
                            
                        # print the bottom of the columned note
                        returntext += self.lineprint('F',
                                                     showsize=param_width,
                                                     maxsize=maximum,
                                                     printyes=not np_temp,
                                                     is_embedded=param_is_emb,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)


     
                        
                        param_width = param_width_def
                        maximum = maximum_def

                        # print the head of non-columned note.
                        
    ##                    returntext += self.lineprint('H',
    ##                             showsize=param_width,
    ##                             maxsize=maximum,
    ##                             printyes=not np_temp,
    ##                             is_embedded=param_is_emb,
    ##                             p_indent=param_indent,
    ##                             leftmargin=leftmargin)


                        
                        columns_done = True
                        columnlist.clear()
                        columntextlist = []
                        columnate = False
                        splitting = False
                    
                        
                    elif (LEFTBRACKET + SLASH in line
                          and SLASH + RIGHTBRACKET in line
                          and line.split(LEFTBRACKET + SLASH)[1].split(SLASH + RIGHTBRACKET)[0].isnumeric()):
                        modified = True
                        param_width_def = param_width
                        maximum_def = maximum
                        param_width = int(line.split(LEFTBRACKET + SLASH)[1].split(SLASH + RIGHTBRACKET)[0])
                        maximum = param_width
                        returntext += self.lineprint('F',
                                                     showsize=param_width_def,
                                                     maxsize=maximum_def,
                                                     printyes=not np_temp,
                                                     is_embedded=param_is_emb,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)
                        returntext += self.lineprint('H',
                                                     showsize=param_width,
                                                     maxsize=maximum,
                                                     printyes=not np_temp,
                                                     is_embedded=param_is_emb,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)

                        
                        
                    elif not override and '/DEF/' in line:
                        returntext += self.lineprint('F',
                                                     showsize=param_width,
                                                     maxsize=maximum,
                                                     printyes=not np_temp,
                                                     is_embedded=param_is_emb,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)
                        param_width = param_width_def
                        maximum = maximum_def
                        returntext += self.lineprint('H',
                                                     showsize=param_width,
                                                     maxsize=maximum,
                                                     printyes=not np_temp,
                                                     is_embedded=param_is_emb,
                                                     p_indent=param_indent,
                                                     leftmargin=leftmargin,
                                                     bracket=brackets)
                    elif not override and ('/BREAK/' in line or '/NEW/' in line):
                        if '/BREAK/' in line:
                            returntext += self.lineprint('M',
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         is_embedded=param_is_emb,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)
                        else:
                            returntext += self.lineprint('F',
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         is_embedded=param_is_emb,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)
                            returntext += self.lineprint('H',
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         is_embedded=param_is_emb,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)

                    else:

                        if not columns_done or not columns:

                            # adds ordinary line of columntext    
                            returntext += self.lineprint(line,
                                                         showsize=param_width,
                                                         maxsize=maximum,
                                                         printyes=not np_temp,
                                                         is_embedded=param_is_emb,
                                                         p_indent=param_indent,
                                                         leftmargin=leftmargin,
                                                         bracket=brackets)

            if not columns_done or not columns: 
                returntext += self.lineprint('F',
                                             showsize=param_width,
                                             maxsize=maximum,
                                             printyes=not np_temp,
                                             is_embedded=param_is_emb,
                                             p_indent=param_indent,
                                             leftmargin=leftmargin,
                                             bracket=brackets)
            returntext += (EOL*param_spacing)

        line_length_list = [len(l_temp) for l_temp in returntext.split(EOL)]
        max_len = max(line_length_list)
        min_len = min(line_length_list)
        leftstuff = (int(param_indent/50))*']'+(param_indent % 50)*BLANK
        if min_len != max_len:
            returntext = EOL.join([leftstuff+l_temp[0:-1]
                                   +box_or_nothing(l_temp[-2])*(max_len-len(l_temp))
                                   +l_temp[-1]
                                   for l_temp
                                   in returntext.split(EOL)
                                   if l_temp])
        else:
            returntext = EOL.join([leftstuff+l_temp
                                   for l_temp
                                   in returntext.split(EOL)])
        if not npp_temp:
            print(returntext)
            
            


        if npp_temp:
            modified = True
            if modified:
                returnlist = returntext.split(EOL)
                maxwidth = 0
                new_returnlist = []
                for l_temp in returnlist:
                    maxwidth = max([maxwidth,len(l_temp)])
                
                for l_temp in returnlist:
                    if rectify:
                        if len(l_temp) > 1:
                            if l_temp[-2] != BOX_CHAR['h']:
                                l_temp = l_temp[0:-1] + (maxwidth - len(l_temp))\
                                         * BLANK + l_temp[-1] 
                            else:
                                l_temp = l_temp[0:-1] + (maxwidth - len(l_temp))\
                                         * BOX_CHAR['h'] + l_temp[-1] 
                                
                        else:
                             l_temp += (maxwidth - len(l_temp)) * BLANK  
                             
                    else:
                        l_temp += (maxwidth - len(l_temp)) * BLANK 
                    new_returnlist.append(l_temp)
                    
                returntext = EOL.join(new_returnlist)
            
            return returntext

        if len(textlist) == 1:
            pass
        return returntext


    def width_needed(self,
                     textlist,
                     p_width=60,
                     splitchar=BLANK,
                     p_is_emb=False,
                     leftmargin=0):

        """calculates width needed for the actual note
        given the width of the line of text
        """

##        if (len(textlist) > 1 and (BOX_CHAR['lu'] in textlist[1]
##                                   or p_is_emb)):
##
##            maxwidth = p_width + leftmargin
##            for line in textlist[1].split(EOL):
##                if len(line) + leftmargin > maxwidth:
##                    maxwidth = len(line) + leftmargin
##            return max([len(textlist[0].split(BLANK)[0])+2,maxwidth+2])

        if (len(textlist) > 1 and (BOX_CHAR['lu'] in textlist[1]
                                    or p_is_emb)):

            return max([len(temp_x)
                        for temp_x
                        in textlist[1].split(EOL)]+[p_width+leftmargin+2])
        
        

        maxwidth = p_width + leftmargin
        for line in textlist:

            nextline = EMPTYCHAR

            for word in line.split(splitchar):
                nextline += word+splitchar
                if (len(nextline) > (p_width-int(p_width/MARGINFACTOR))
                        or EOL in nextline):
                    if len(nextline) + leftmargin > maxwidth:
                        maxwidth = len(nextline) + leftmargin
                    nextline = EMPTYCHAR
        return max([len(textlist[0].split(BLANK)[0])+2,maxwidth+2])
