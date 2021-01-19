###CLASS FOR DISPLAY MULTIPLE COLUMNS OF TEXT###



def overflow_text (text,splitting=' ',maximum=60):

        """Formats text into a column of given width
        Column may be longer if a single word is longer than MAXIMUM"""
        

        
        returnlines = []
        newline = ''
        for l in text.split('\n'):    

            for w in l.split(splitting):

                if len(newline + w)>maximum:
                    
                    returnlines.append(newline)
                    newline = w+splitting
                else:
                    newline += w+splitting
            returnlines.append(newline)
            newline=''
        returnlines.append(newline)
        return returnlines


class IndexDisplay:

    """CORE COLUMN DISPLAY CLASS FOR INDEX"""

    def __init__ (self,columns=2,automatic=True,column_size=None,default_barrier='|',barriers=None):

        #column size 2-TUPLE MIN,MAX  0 for AUTOMATIC

        self.columns = columns
        self.automatic = automatic
        if column_size:
            self.column_size = column_size
        else:
            self.column_size = []
        self.column_dict = {}
        self.default_barrier = default_barrier
        self.barriers = barriers
        self.column_widths = {}
        self.multi_column_dict = {}
        self.multi_column_Count = None

        def get_size(column):

            if self.column_size and column < len(self.column_size):
                return self.column_size[column]
            else:
                return 0
            
        for column in range(self.columns):
            self.column_dict[column] = []
            self.column_widths[column] = (0,0)
            

    def load (self,text,column_at=0):

        """To load TEXT into the given COLUMN.
        TEXT added if COLUMN ALREADY EXISTS.
        IF COLUMN is BEYOND FURTHEST, THEN WILL
        ADD NEXT"""

        if column_at not in self.column_dict:
            column_at = max(self.column_dict.keys()) + 1
        

        returnlist = []

        def form_or_not_form_text (x):

            if self.automatic or (column_at < len(self.column_size) and self.column_size[column_at][1] == 0) or column_at > len(self.column_size):
                
                returnlist = text.split('\n')
            else:
                returnlist = overflow_text(x,maximum=self.column_size[column_at][1])
            return returnlist

        x = form_or_not_form_text(text)
        
        
        if column_at in self.column_dict:
            self.column_dict[column_at] += x
        else:
            self.column_dict[column_at] = x
        max_len = max([len(r) for r in x])
        min_len = min([len(r) for r in x])
        if column_at not in self.column_widths:
            self.column_widths[column_at] = (min_len,max_len)
        else:
            self.column_widths[column_at] = (min([min_len,self.column_widths[column_at][0]]),max([max_len,self.column_widths[column_at][1]]))
        

    

    def get_line (self,line_no):

        """Gets single line of colums"""

        def get_barrier(column):

            """Determines whether the barrier for a given column is the
               default or the preset"""

            if column < len(self.column_dict.keys())-1:
                
                if self.barriers and column<len(self.barriers) and self.barriers[column]:
                    return self.barriers[column]
                return self.default_barrier
            return ''

        def form_line_for_column (column):

            """Gets the line for a single column"""

            if line_no < len(self.column_dict[column]):
                text = self.column_dict[column][line_no]
            else:
                text = ''
            

            text += (max([self.column_widths[column][1],self.column_widths[column][0]])-len(text))*' '
            if '_' in text and not text.replace(' ','').replace('_','').replace('|',''):
                text = text.replace(' ','_')
            return text 
        line = ''
        for c in self.column_dict:
            line += form_line_for_column(c) + get_barrier(c)
        return line

    def show (self,from_here=0,to_there=1000000):

        """Displays all the columns"""

        returnlist = []
        
        max_rows = max([len(self.column_dict[x]) for x in range(len(self.column_dict.keys()))])

        if to_there > max_rows:
            to_there = max_rows

        for r in range(from_here, to_there):
            returnlist.append(self.get_line(r))
        return '\n'.join(returnlist)


    def load_multiple_columns (self,entry_list = None,multi_column_count=None,barrier=True):

            

        if not self.multi_column_dict:
                row = 1
                if multi_column_count:
                    self.multi_column_count = multi_column_count
                else:
                    self.multi_column_count = len(entry_list)
        else:
            row = len(self.multi_column_dict.keys())+1

        if len(entry_list) < self.multi_column_count:
            entry_list += [',']*(self.multi_column_count-len(entry_list))
        elif self.multi_column_count > len(entry_list):
            etnry_list = entry_list[0:self.multi_column_count]
            
        line_list = []
        for counter, el in enumerate(entry_list) :

            line_list.append(overflow_text(el,maximum=self.column_size[counter][1]))

        max_length = max([len(x) for x in line_list])
        for index in range(len(line_list)):

            line_list[index] = line_list[index]+['']*(max_length-len(line_list[index]))+barrier*['_'*max([len(l) for l in line_list[index]])]
            
        self.multi_column_dict[row] = line_list

    def load_multi (self):

        for row in range(1,len(self.multi_column_dict.keys())+1):
            for column, column_text in enumerate(self.multi_column_dict[row]):
                self.load('\n'.join(column_text),column)
    

        

            

            
                    
                    

            
        
        
            
            
        


        

            

        
                                           

                                    
            

    
                                        

        

        
