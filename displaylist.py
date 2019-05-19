"""Module containing class used to display lists
pylint rated 9.6/10
"""

import nformat
from ninput import i_input
from globalconstants import EMPTYCHAR, EOL, BLANK,\
     PERIOD, COMMA, LEFTNOTE, RIGHTNOTE, SLASH, COLON, DASH

def get_simple_range (entry):

    returnset = set()
    ranges = entry.split(COMMA)
    for r_temp in ranges:
        if DASH in r_temp:
            returnset.update(str(x_temp) for x_temp in range(int(r_temp.split(DASH)[0]),int(r_temp.split(DASH)[1])+1))
        else:
            returnset.update({r_temp})
    return returnset
            
            

class DisplayList:


    """General function for loading, displaying,
    and selecting lines of text"""

    def __init__(self,
                 entrylist=None,
                 displayobject=None):

        self.displayobject = displayobject
        if entrylist is None:
            entrylist = []
        self.dis_list = []
        self.maxwidth = 0
            # This is the maximum width of a line of text fed into the object
        self.padding = 4
            # This is Additional padding added to
            #maxwidth when it is displayed as a note.
        self.counter = 0
            # Keeps track of the current line being added
        self.how_many = 50
            # This shows how many notes should be displayed at once
        self.group = 1
            # This is the total number of groups of lines being displayed

        if entrylist != []:
            for label in entrylist:
                self.append(label)
            self.show()

    def __len__(self):

        """ returns the number of lines of text that have been loaded"""
        return len(self.dis_list)

    def dump(self):

        """returns all the lines as unformatted text"""

        return EMPTYCHAR.join(self.dis_list)
##        for line in self.dis_list:
##            text += line
##        return text

    def append(self,
               item):

        """adds a new line"""

##        if EOL in item:
##            print('YES')
        self.dis_list.append(item)
        if len(item) > self.maxwidth:
            self.maxwidth = len(item)


    def clear(self):

        """empties the list of all lines"""

        self.dis_list = []
        self.maxwidth = 0
        self.padding = 4
        self.counter = 0

    def show(self,
             line_from=0,
             line_to=0,
             header=EMPTYCHAR,
             reverse=False,
             centered=False,
             purge=False,
             indent=0,
             markset=None,
             returntext=False):

        """ displays  line_from to line_to as as formatted note
        header = the label put at top of the note.
        reverse -- True if lines to be displayed in reverse order
        centered --- True if label is to be centered
        purge --- True if object is to be emptied after showing
        If indent is greater than 50, it will indent to center according to indent.
        """
        if not markset:
            markset = set()

        if indent > 50:
            indent = int((indent-self.maxwidth)/2)
        if not self.dis_list:
            return
        if line_from != 0 and line_to == 0:
            line_to = line_from+1
        if line_to > len(self.dis_list):
            line_to = len(self.dis_list)
        if line_to == 0:
            line_to = len(self.dis_list)
        if centered:
            header = nformat.center(header, self.maxwidth+self.padding)
        if reverse:
            if returntext:
                return EOL.join(reversed(self.dis_list[line_from: line_to]))
            else:
                self.displayobject.noteprint((header,
                                              EOL.join(reversed(self.dis_list[line_from: line_to]))),
                                             param_width=self.maxwidth+self.padding,
                                             param_is_emb=True,
                                             param_indent=indent)
        else:
            temp_list = []
            for counter,x_temp in enumerate(self.dis_list[line_from: line_to]):
                marked = False

                for m_temp in markset:
                    if x_temp.startswith(str(m_temp)+COLON):
                        marked = True

                if marked:
                    temp_list.append('#'+x_temp)
                else:
                    temp_list.append(' '*(markset!=set())+x_temp)
            
                
            if returntext:
                            
                if purge:
                    self.clear()
                return  EOL.join(temp_list)
            else:
                
                r_temp = self.displayobject.noteprint((header,
                                              EOL.join(temp_list)),
                                              param_width=self.maxwidth+self.padding,
                                              param_is_emb=True,
                                              param_indent=indent)
                            
                if purge:
                    self.clear()
                return r_temp


    def present(self,
                header=EMPTYCHAR,
                centered=False,
                accumulate=False,
                dump=False):

        """ presents all the lines in the object in such
        a way that one can examine them page by page
        """

        s_temp = EMPTYCHAR
        accumulate_set = set()
        if not self.dis_list:
            return False
        total_groups = int(len(self.dis_list)/self.how_many)+1
        if total_groups == 1 and not accumulate:
            s_temp = self.show(0, len(self.dis_list), header=header
                               +('From 0 to '+str(len(self.dis_list)))*(header==EMPTYCHAR),
                               centered=centered)
        else:

            if self.group > total_groups:
                self.group = 1

            go_on = True
            while go_on:
                start_at = (self.group-1)*self.how_many
                end_at = (self.group)*self.how_many
                self.show(start_at, end_at, header=header+' From '
                          +str(start_at)
                          +' to '+str(end_at),
                          centered=centered,
                          markset=accumulate_set)
                prompt = LEFTNOTE+LEFTNOTE+BLANK+LEFTNOTE
                if total_groups+1 < 20:
                    for a_temp in range(1, total_groups+1):
                        prompt += str(a_temp)+BLANK
                if total_groups+1 > 20:
                    prompt += '1 2 3 4 5 6 7 8 9 10 ... '+str(total_groups)
                prompt += RIGHTNOTE + BLANK + RIGHTNOTE + \
                          RIGHTNOTE + BLANK+' [A]ll [C]hange entries shown [Q]uit menu ' + '[S]elect] or U[nselect]' * accumulate
                q_temp = input(prompt)
                if q_temp in [LEFTNOTE, COMMA] and self.group > 1:
                    self.group -= 1
                elif q_temp in [RIGHTNOTE, PERIOD, BLANK, EMPTYCHAR]:
                    if self.group < total_groups:
                        self.group += 1
                    else: go_on = False
                elif q_temp == RIGHTNOTE + RIGHTNOTE:
                    self.group = total_groups
                elif q_temp == LEFTNOTE + LEFTNOTE:
                    self.group = 1
                elif (q_temp.isnumeric() and
                      int(q_temp) > 0 and
                      int(q_temp) < total_groups+1):
                    self.group = int(q_temp)
                elif q_temp[0] in ['A', 'a']:
                    self.show(0, len(self.dis_list), header=header
                              +'From 0 to '
                              +str(len(self.dis_list)),
                              centered=centered)
                elif q_temp[0] in ['Q', 'q', SLASH]:
                    go_on = False
                elif q_temp[0] in ['C', 'c']:
                    self.how_many = i_input('Show how many items? ')
                    go_on = self.present(header=header, centered=centered)
                elif q_temp[0] in ['S', 's', 'U', 'u'] and accumulate:
                    if len(q_temp) > 1 and q_temp[1].isnumeric():
                        to_add=q_temp[1:]
                    else:
                        print()
                        if q_temp[0] in ['S','s']:
                            p_temp = 'Ranges to select? '
                        else:
                            p_temp = 'Ranges to unselect? '
                        to_add = input(p_temp)
                    for s_temp in get_simple_range(to_add):
                        if s_temp.isnumeric():
                            if q_temp[0] in ['S','s']:
                                accumulate_set.add(s_temp)
                            else:
                                accumulate_set.discard(s_temp)
            
                    
                    
        if accumulate:
            return accumulate_set
        if dump:
            if not s_temp:
                return self.show(returntext=True)
            else:
                return s_temp
            
        return False    # Returns false to quit loop with recursive function calls

    def enter(self,
              entrylist):

        """enters in an entire list"""

        self.dis_list = list(entrylist)

    def next(self):

        """ show the next line"""
        self.show(self.counter)
        self.counter += 1
        if self.counter > len(self.dis_list):
            self.counter = 0

    def previous(self):

        """show the previous line"""
        self.counter -= 1
        self.show(self.counter)
        if self.counter == 0:
            self.counter = len(self.dis_list)

##displaylist.py:70:4: R0913: Too many arguments (7/5) (too-many-arguments)
##displaylist.py:88:12: W0104: Statement seems to have no effect (pointless-statement)
##displaylist.py:108:4: R0912: Too many branches (18/12) (too-many-branches)
