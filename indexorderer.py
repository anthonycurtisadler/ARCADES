from genericorderer import generic_orderer
from indexclass import Index


def suc_one (x,y):

    return y.is_child (x)

def suc_two (x,y):

    return y.is_next(x)

successor = (suc_one,suc_two,)


class index_orderer (generic_orderer):

    def __init__ (self,orderfuncs=(suc_one,suc_two,),sortfunc=lambda x:Index(x)):

        if orderfuncs and isinstance(orderfuncs,(list,tuple,set)):
            self.orderfuncs = orderfuncs
        elif orderfuncs:
            self.orderfuncs = (orderfuncs,)
        self.sortfunc = sortfunc
        
        
        self.resultlist = []
