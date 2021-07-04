from genericorderer import generic_orderer


def suc_one (x,y):

    return (ord(y.upper())-ord(x.upper())) == 1




class text_orderer (generic_orderer):

    def __init__ (self,orderfuncs=(suc_one,),sortfunc=lambda x:x.upper()):

        if orderfuncs and isinstance(orderfuncs,(list,tuple,set)):
            self.orderfuncs = orderfuncs
        elif orderfuncs:
            self.orderfuncs = (orderfuncs,)
        
        self.resultlist = []
