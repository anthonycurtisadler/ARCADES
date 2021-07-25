###Class for purging keywords when displaying notes###

from globalconstants import EOL

class KeyPurge:

    def __init__ (self):

        self.permanent = set()
        self.temporary = set()
        self.purge_allcaps = False
        self.purge_caps = False
        self.purge_lower = False
        self.purge_numbers = False
        self.purge_sequences = False
        self.inverted = False 

    def allcaps (self, boolentry=True):

        self.purge_allcaps = boolentry

    def caps (self, boolentry=True):
        self.purge_caps = boolentry

    def lower (self, boolentry=True):
        self.purge_lower = boolentry

    def numbers (self, boolentry=True):
        self.purge_numbers = boolentry

    def sequences (self, boolentry=True):
        self.purge_sequences = boolentry


    def load (self, entryset):
        if isinstance(entryset,(set,list)):
            for x in entryset:
                self.permanent.add(x)
        else:
            self.permanent.add(str(x))

    def invert(self,boolentry=True):
        self.inverted = boolentry
            
            

    def show (self):
    
        return 'INVERTED'*self.inverted + EOL + 'ALL CAPS: ' + str(self.purge_allcaps
                                  or '#ALLCAPS#'
                                  in self.permanent.union(self.temporary)) + EOL\
               + 'CAPS: ' + str(self.purge_caps
                                or '#CAPS#'
                                  in self.permanent.union(self.temporary)) + EOL\
               + 'LOWER:' + str(self.purge_lower
                                or '#LOWER#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'numeric sequences: ' + str(self.purge_numbers
                                   or '#NUMSEQ#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'all sequences: ' + str(self.purge_sequences
                                     or '#ALLSEQ#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'non-project sequences: ' + str('#NONPS#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'projects: ' + str('#PROJ#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'index sequences: ' + str('#INDSEQ#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'string sequences: ' + str('#STRSEQ#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'date sequences: ' + str('#DATSEQ#'
                                  in self.permanent.union(self.temporary)) + EOL \
               + 'SETS:' + str(', '.join(self.temporary.union(self.permanent)))
    
    

    def purge(self,keywords,projects=None):
        topurge = self.permanent.union(self.temporary)
        if not projects:
            projects = set()
        else:
            projects = set(projects)
            
            
        sequences = {x for x in topurge if x.endswith('@')}

        is_lower = lambda x: (('#LOWER#' in topurge or self.purge_lower)
                              and ('@' not in x)
                              and (x==x.lower()))

        is_hyper = lambda x:(('#HYP#' in topurge)
                             and x.replace('.','').isnumeric())

        is_all_caps = lambda x: (('#ALLCAPS#' in topurge or self.purge_allcaps)
                                 and ('@' not in x)
                                 and (x==x.upper()))
        is_caps = lambda x:(('#CAPS#' in topurge or self.purge_caps)
                            and x 
                            and (x[0]==x[0].upper())
                            and ('@' not in x) and not (x==x.upper()))
        is_any_sequence = lambda x:  (('#ALLSEQ#' in topurge or self.purge_sequences)
                                      and ('@' in x))
        is_non_project = lambda x: (('#NONPS#' in topurge)
                                    and ('@' in x)
                                    and (x.split('@')[0] not in projects))
        is_project = lambda x: (('#PROJ#' in topurge)
                                and x.split('@')[0] in projects)
        is_floaty = lambda x: x.replace('.','').replace('-','').isnumeric()
        is_numeric_sequence = lambda x: (('#NUMSEQ#' in topurge or self.purge_numbers)
                                         and ('@' in x)
                                         and ('@_' not in x)
                                         and (x.split('@')[0] not in projects)
                                         and  is_floaty(x.split('@')[1]))
        is_index_sequence = lambda x: (('#INDSEQ#' in topurge)
                                         and ('@_' in x)
                                         and (x.split('@')[0] not in projects))
        is_string_sequence = lambda x: (('#STRSEQ#' in topurge)
                                         and ('@' in x)
                                         and ('@_' not in x)
                                         and (x.split('@')[0] not in projects)
                                         and  not is_floaty(x.split('@')[1]))
        is_date_sequence = lambda x: (('#DATSEQ#' in topurge)
                                         and ('@#' in x)
                                         and (x.split('@')[0] not in projects))
        
        

        
        returnvalue = {x for x in keywords if not is_all_caps(x)
                and not is_numeric_sequence(x)
                and not is_index_sequence(x)
                and not is_string_sequence(x)
                and not is_caps(x)
                and not is_any_sequence(x)
                and not is_non_project(x)
                and not is_project(x)
                and not is_date_sequence(x)
                and not is_lower(x)
                and not x in topurge
                and not is_hyper(x)}

        if self.inverted:
            returnvalue = keywords - returnvalue

        if not returnvalue:
            returnvalue = {'VOID'}
        return returnvalue

    def clear (self):
        self.purge_allcaps = False
        self.purge_caps = False
        self.purge_lower = False
        self.purge_numbers = False
        self.purge_sequences = False

        self.permanent = set()
        self.temporary = set()
        self.inverted = False

    def apply(self,keys,projects=None):

        return(self.purge(keys,projects))
                                          



if __name__ == "__main__":

    kp = KeyPurge()
    kp.temporary = {'#HYP#'}
    kp.purge_numbers = True 

    proj = {'Aristotle','Plato','PRIMARY'}

    

    while True:

        print(kp.apply(set(input('?').split(',')),proj))
        print(kp.show())
        
        
        

            
            
