

def successor (x,y):
    try:
        return y-x == 1
    except:
        return False

successor = (successor,)

def apply_all_funcs (x,y,funclist):

    for f in funclist:
        if f(x,y):
            return True
    return False

class generic_orderer:


    def __init__ (self,orderfuncs=successor,sortfunc=lambda x:x):

        if orderfuncs and isinstance(orderfuncs,(list,tuple,set)):
            self.orderfuncs = orderfuncs
        elif orderfuncs:
            self.orderfuncs = (orderfuncs,)
        self.sortfunc = sortfunc
        
        self.resultlist = []
        self.entrylist = []
        

    def is_sorted (self):

        if not isinstance(self.entrylist,(list,tuple)):
            self.entrylist = list(self.entrylist)
        for x in range(len(self.entrylist)-1):
            if not self.entrylist[x]<self.entrylist[x+1]:
                return False
        return True

    def order (self,entrylist=None):

        if entrylist:
            self.resultlist=[]
            self.entrylist = entrylist
        if not self.is_sorted():
            self.entrylist = sorted(self.entrylist,key=lambda x:self.sortfunc(x))
        

        for x in self.entrylist:
            if not self.resultlist:
                self.resultlist = [[x]]
            elif apply_all_funcs(self.resultlist[-1][-1],x,self.orderfuncs):
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
            if len(x)==1:
                formattedlist.append(str(x[0]))
            else:
                formattedlist.append(str(x[0])+'-'+str(x[-1]))
        
        return breaker.join(formattedlist)
        
    
        
            
    
        
        
