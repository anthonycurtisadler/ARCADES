###Class for purging keywords when displaying notes###

class KeyPurge:

    def __init__ (self):

        self.permanent = set()
        self.temporary = set()
        

    def purge(self,keywords,projects=None):
        topurge = self.permanent.union(self.temporary)
        if not projects:
            projects = set()
        else:
            projects = set(projects)
            
            
        sequences = {x for x in topurge if x.endswith('@')}

        is_all_caps = lambda x: ('#ALLCAPS#' in topurge) and (x==x.upper()) and (x not in projects)
        is_caps = lambda x:('#CAPS#' in topurge) and (x[0]==x[0].upper()) and not (x==x.upper()) and (x not in projects)
        is_any_sequence = lambda x:  ('#ALLSEQ#' in topurge) and ('@' in x)
        is_non_project = lambda x: ('#NONPS#' in topurge) and ('@' in x) and (x.split('@')[0] not in projects) 
        is_project = lambda x: ('#PROJ#' in topurge) and x.split('@')[0] in projects

        
        return {x for x in keywords if not is_all_caps(x)
                and not is_caps(x)
                and not is_any_sequence(x)
                and not is_non_project(x)
                and not is_project(x)
                and not x in topurge}


if __name__ == "__main__":

    kp = KeyPurge()
    kp.temporary = {'frog','toad', '#CAPS#'}

    proj = {'Aristotle','Plato','PRIMARY'}

    

    while True:

        print(kp.purge(set(input('?').split(',')),proj))
        
        

            
            
