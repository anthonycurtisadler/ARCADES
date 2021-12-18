from globalconstants import EOL, VERTLINE, BLANK, EMPTYCHAR,\
     UNDERLINE, DOLLAR, SLASH, DASH, PLUS, CARET, POUND, COMMA 

from plainenglish import Queries, Alerts
from display import Display
from displaylist import DisplayList
from indexclass import Index
import nformat
from notebookutilities import transpose_keys
from generalutilities import get_range

display = Display()
queries = Queries()
alerts = Alerts()

def formkeys(entry_temp,notebook=None):

    """ combines format key and transpose keys """

    return nformat.format_keys(transpose_keys(entry_temp,
                                              notebook=notebook))


def textedit_new(text,
                 size=60,
                 splitchar=BLANK,
                 annotate=False,
                 notebookobject=None):

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
                                                              indexes=False,
                                                              notebook=notebookobject)]
                     else:

                         keyobject = [listcopy[int(a_temp)] for a_temp in get_range(i_temp,
                                                                                     orequal=True,
                                                                                     complete=False,
                                                                                     many=True,
                                                                                     indexes=False,
                                                                                    notebook=notebookobject)
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
                           formkeys(keyobject,notebook=notebookobject)))

    if addkeys:

        in_temp = notebookobject.default_dict['abbreviations'].undo(input(queries.KEYS))
        if in_temp:
                
            keyobject += in_temp.split(COMMA)

        
    return keyobject

