def get_range (string):

    return_set = set()
    
    for x in string.split(','):
        x = x.strip()

        if '-' not in x and x.isnumeric():
            return_set.add(int(x))
        elif x.count('-')==1:
            from_here, to_here = x.split('-')[0].strip(), x.split('-')[1].strip()
            if from_here.isnumeric() and to_here.isnumeric() and int(from_here)<int(to_here):
                for y in range(int(from_here),int(to_here)+1):
                    return_set.add(y)
    return return_set

def search (location='',entry_list=None,less_than=None):

    minimum = 0
    maximum = len(entry_list)
    if less_than is None:
        less_than = lambda x,y:x<y
    
    while True:
        position = int((minimum+maximum)/2)
        if position == minimum or position == maximum:
            break
        elif entry_list[position] == location:
            break
        elif 0<position<len(entry_list)-1:
            if less_than(entry_list[position-1], location) and less_than(location, entry_list[position+1]):
                break
            elif less_than(location,entry_list[position]):
                maximum = position
            else:
                minimum = position
        else:
            break 
    return position 


class Select:

    def __init__ (self,entryset=None,sort_function=None):

        if entryset:

            self.entries = entryset
            
        self.to_delete = set()
        self.purged = set()
        if sort_function is None:
            sort_function = lambda x:x 
        self.sort_function = sort_function


    def load (self,entryset):

        self.entries = entryset
        if isinstance(self.entries,list):
            self.entries = set(self.entries)

    def show (self,showlist,start=0):

        for counter, x in enumerate(showlist):

            print(counter+start,':',x)

    def scroll_through (self,entry_list):


        def less_than (x,y):

            if x == y:
                return False
            elif sorted([x,y],key = lambda x:self.sort_function(x))[0] == x:
                return True
            return False


        if entry_list:
            
            scroll_list = sorted(entry_list,key=lambda x:self.sort_function(x))
        else:
            scroll_list = []
        
        starting = 0
        showing = 20
        
        go_on = True

        while go_on:

            sort = False
            last = ''
            relocate = False
            

            print()
            self.show (scroll_list [starting:min([starting+showing,len(scroll_list)])],start=starting)

            while True:
                
                inp = input('\n\n[ < > ] D(elete); U(ndelete); C(hange); Q(uit); \nR(eform); I(nvert); c(L)ear); A(dd)\n Add (M)any;  S(sort); (F)ind \n')
                if inp  in ['[',']','<','>','D','C','Q','U','R','I','A','F','S','L','M']:
                    break
            if inp == '[':
                starting = 0
            elif inp == ']':
                staring = len(scroll_list)
            elif inp == '<':
                starting -= showing
            elif inp == '>':
                starting += showing
            elif inp == 'C':
                new = input('SHOW HOW MANY> ?')
                if new.isnumeric():
                    new = int(new)
                    if 0 < new < 101:
                        showing = new
            elif inp == 'Q':
                go_on = False
            elif inp in ['D','U']:
                to_delete = input('?')
                for x in get_range(to_delete):

                    if 0 <= x < len(scroll_list):
                        if inp == 'D':
                            scroll_list [x] = '_'+scroll_list[x]
                        elif inp == 'U' and scroll_list [x].startswith('_'):
                            scroll_list [x] = scroll_list [x][1:]
            elif inp == 'R':
                new_list = []
                for x in scroll_list:
                    if not x.startswith ('_'):
                        new_list.append(x)
                    else:
                        self.purged.add(x[1:])
                scroll_list = new_list
            elif inp in ['I']:
                for x in range(len(scroll_list)):
                    if scroll_list[x].startswith('_'):
                        scroll_list[x] = scroll_list[x][1:]
                    else:
                        scroll_list [x] = '_' + scroll_list[x]
            elif inp == 'L':
                for x in range(len(scroll_list)):
                    if scroll_list[x].startswith('_'):
                        scroll_list[x] = scroll_list[x][1:]

            elif inp == 'A':
                new = input('ADD>   ?')
                scroll_list.append(new.strip())
                sort = True
                last = new.strip()
                relocate = True 
                position = search(new.strip(),entry_list=scroll_list,less_than=less_than)

            elif inp == 'M':
                 new = input('ADD> W1,W2,W3... ?')
                 for x in new.split(','):
                     scroll_list.append(x.strip())
                 last = x.strip()
                 relocate = True 
                 sort = True
                 

            elif inp == 'S':
                sort = True

            elif inp == 'F':
                last = (input('FIND>   ?'))
                relocate = True 

            if sort:
                scroll_list = sorted(scroll_list,key=lambda x:self.sort_function(x))
            if relocate and last:
                position = search(last,entry_list=scroll_list,less_than=less_than)
                starting = position - int(showing/2)

            if starting < 0:
                starting = 0
            elif starting > len(entry_list)-1:
                starting = len(entry_list)-1
    
           
        self.entries = set(scroll_list)
        return [x for x in scroll_list if not x.startswith('_')]

    def finish (self):

        return self.entries

if __name__ == '__main__':

   
    sel = Select(sort_function=lambda x:int(x))
    sel.scroll_through({str(x) for x in range(100000)})
            
        

            


                    
                
            
                
            

            
        

        

        
