### Orders a list of words in groups of "derivative" words
### for example: catty is a derivative of cat.
### Excludes words of length less than MINIMUM

MINUMUM = 3




from genericorderer import generic_orderer

def word_child (x,y):

    return y.startswith(x)

def apply_all_funcs (value_tuple, funclist):

    """Returns True is any one of the functions
    in funclist returns True when applies to x and y
    """
    temp_val = value_tuple[0][-1] # gets last entry
    
    y = value_tuple[1]
    for x in [z for z in temp_val if len(z)>=MINUMUM]:
        
        for f in funclist:
            if f(x,y):
                return True
    return False


class text_orderer (generic_orderer):


    
    def __init__ (self,orderfuncs=(word_child,),sortfunc=lambda x:x.upper()):

        if orderfuncs and isinstance(orderfuncs,(list,tuple,set)):
            self.orderfuncs = orderfuncs
        elif orderfuncs:
            self.orderfuncs = (orderfuncs,)
        self.sortfunc = sortfunc
        
        self.resultlist = []
        self.entrylist = []

    def order (self,entrylist=None):

        if entrylist:
            self.resultlist=[]
            self.entrylist = entrylist
        if not self.is_sorted():
            self.entrylist = sorted(self.entrylist,key=lambda x:self.sortfunc(x))
        

        for x in self.entrylist:
            if not self.resultlist:
                self.resultlist = [[x]]
            elif apply_all_funcs((self.resultlist,x),self.orderfuncs):
                self.resultlist[-1].append(x)
            else:
                self.resultlist.append([x])
        return self.resultlist
    
    def format (self,entrylist=None,breaker='; '):

        if entrylist:
            self.resultlist=[]
            self.order(entrylist)

        formattedlist = []
        for x in self.resultlist:
            formattedlist.append(','.join(sorted(x)))
        
        return breaker.join(formattedlist)
        
    
