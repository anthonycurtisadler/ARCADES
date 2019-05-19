"""Module containing class to display multiple notes in parallel
pylint rated at 9.60/10
"""

import codecs
import os
from globalconstants import EOL, BLANK, EMPTYCHAR, POUND, SLASH

class Note_Display: #displays multiple columns of notes

    """This class handles the display of
    multiple columns of notes
    """

    def __init__(self,
                 totalwidth=300):

        self.display_dict = {}
            # Theictionary which contains the text of the notes.
            #Key is an integer
        self.size_dict = {}
            # The dictionary containing information
            #about the size of each note. Key is an integer
        self.output = []
            # The containing the data for displaying
            #each line of parallel notes. Each member of this list
            #is itself a list (henceforth referred to as 'format list'):
            #[noteindex, starting position, length of note, y coordinate]
        self.width = totalwidth
            # The width of the display. Defaults to 180.
        self.already_shown = set()
            # keeps track of notes that have already been displayed

    def load(self,
             text):

        """loads the text of a note into
        the Note_Display object and records its dimensions
        """

        linelist = text.split(EOL)
        xsize = max([len(line) for line in linelist])
        ysize = len(linelist)
        index = max([1, max([a_temp for a_temp in self.display_dict]+[0])+1])
        self.display_dict[index] = linelist

        self.size_dict[index] = (xsize, ysize)


    def get_next(self,
                 smaller_than=0):

        """Gets the lowest-indexed note fitting
        into an available width
        """

        if smaller_than == 0:
            if (len(self.display_dict.keys())
                    == len(self.already_shown)):
                return False
##            r_temp = min(self.display_dict.keys()
##                    -self.already_shown)
####                self.already_shown.add(r_temp)
            return min(self.display_dict.keys()-self.already_shown)
        for a_temp in sorted(list(self.display_dict.keys()
                                  -self.already_shown)):
            if self.size_dict[a_temp][0] <= smaller_than:
##                self.already_shown.add(a)
                return a_temp
        return False

    def get_first_group(self):

        """Packs the first group of notes.
        Returns a format:
            list=[noteindex,
                starting position,
                length of note,
                y coordinate]
                """

        self.already_shown = set()

        returnlist = []
        first = self.get_next(self.width)

        width_left = self.width

        position = 0
        if not first:
            return []
        returnlist.append((first,
                           0,
                           self.size_dict[first][0],
                           self.size_dict[first][1]))
        width_left -= self.size_dict[first][0]
        position += self.size_dict[first][0]+1

        self.already_shown.add(first)
        can_go_on = True

        while can_go_on:
            new = self.get_next(width_left)

            if not new:
                can_go_on = False
            else:
                returnlist.append((new,
                                   position,
                                   self.size_dict[new][0],
                                   self.size_dict[new][1]))
                width_left -= self.size_dict[new][0]
                position += self.size_dict[new][0]+1
                self.already_shown.add(new)

        return returnlist

    def nextline(self,
                 out_line=None):

        """analyzes the inputed format list and
        returns the next format list.
        """

        if out_line is None:
            return self.get_first_group()
                #initializes a sequence of lines
        next_line = []
        for t_temp in out_line:
                #reads a format list
            tt_temp = (t_temp[0],
                       t_temp[1],
                       t_temp[2],
                       t_temp[3]-1)
                #subtracts from y coordinates (order reversed!)
                #to get format list for next line
            if tt_temp[3] > 0:
                next_line.append(tt_temp)
                #adds format list to next line
                #if the indexed note is not yet depleted

        next_copy = list(next_line)
            #makes a copy of line list to work with
        next_copy.append((0, self.width, 0, 0))
            # a 'dummy' format list marking the end of the line

        position = 0
        added = 0
            #keeps track of the number of previous format list insertions;
        for x_temp, t_temp in enumerate(next_copy):


            if t_temp[1]-position > 0:
                # if space left in line, continues
                can_go_on = True

                width_left = t_temp[1]-position
                position_within = position

                while can_go_on:
                    new = self.get_next(width_left)
                        # gets a note index for the
                        #note that fits into the available space

                    if new:
                            # checks to see if a note index
                            #is returned, and then inserts
                            #format list at the appropriate
                            #position in the line list
                        next_line.insert(x_temp+added,
                                         (new,
                                          position_within,
                                          self.size_dict[new][0],
                                          self.size_dict[new][1]))
                        added += 1
                        position_within += self.size_dict[new][0]
                        width_left -= self.size_dict[new][0]-1
                        self.already_shown.add(new)
                    else: can_go_on = False
                        # don't continue if a note isn't returned
            position = t_temp[1]+t_temp[2]
                # updates position
        return next_line

    def generate_lines(self):

        """Generates a list of line lists with
        formatting information
        """

        not_yet_done = True
        return_list = [[]]
        while (len(self.already_shown) < len(self.display_dict.keys()) or not_yet_done) and not_yet_done:
            nl_temp = self.nextline(return_list[-1])
            return_list.append(nl_temp)

            if len(nl_temp) == 0 or (len(nl_temp) == 1 and len(nl_temp[0]) == 0):
                
                not_yet_done = False

        return return_list

    def print_to_output(self):

        """prints to output"""

        self.output = self.generate_lines()

    def print_init(self):

        """initializes printing by generating a line list
        and producing an iteration object"""

        self.print_to_output()
        self.line_to_show = iter(range(0, len(self.output)))

    def print_line(self):

        """prints the next line"""


        row = next(self.line_to_show, POUND + POUND + POUND)

        if row == POUND + POUND + POUND:
            return BLANK + BLANK
        line_to_print = EMPTYCHAR
        for column in self.output[row]:
            line_to_print += (column[1]-len(line_to_print))*BLANK
##            line_to_print+=self.display_dict[column[0]].pop(0)
            line_to_print += self.display_dict[column[0]][self.size_dict[column[0]][1]-column[3]]


        return line_to_print

    def print_all(self,
                  pause=True,
                  show=True,
                  save=False,
                  back=False,
                  filename='textdefault'):

        """ prints all the notes"""

        # back = return the text to be shown.


        if back:
            save = True
        self.print_init()
        self.already_shown = set()
        go_on = True
        savetext = EMPTYCHAR
        showtext = EMPTYCHAR

        while go_on:

            pl_temp = self.print_line()

            if not pause:
                if show:
                    print(pl_temp)
                    showtext += pl_temp + EOL
                if save:
                    savetext += pl_temp+EOL


            if (pause and input(pl_temp) != EMPTYCHAR) or pl_temp == BLANK + BLANK:
                go_on = False

            if pl_temp == BLANK + BLANK and pause:
                go_on = True
                self.print_init()
                self.already_shown = set()

        if save and back:
            return savetext

        if save and not back:


            directoryname = os.getcwd()+'/textfiles'
            textfile = open(directoryname
                            +SLASH+filename
                            +'.txt', 'ab')
            for line in savetext.split(EOL):
                textfile.write(codecs.encode(line+'\r\n',
                                             encoding='utf-8',
                                             errors='ignore'))
            textfile.close
            return savetext

        else:
            return showtext
