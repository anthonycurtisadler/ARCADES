"""
PurgeKeys class
"""
from globalconstants import EOL

class PurgeKeys:

    """class for holding and operating function to purge keysets when showing
    date dictionary
    """

    def __init__(self):

        self.purge_allcaps = False
        self.purge_caps = False
        self.purge_lower = False
        self.purge_numbers = False
        self.purge_sequences = False

        self.keep_set = set()

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
        self.keep_set = set()
        self.keep_set = entryset

    def show (self):
    
        return 'ALL CAPS: ' + str(self.purge_allcaps) + EOL\
               + 'CAPS: ' + str(self.purge_caps) + EOL\
               + 'LOWER:' + str(self.purge_lower) + EOL \
               + 'numbers: ' + str(self.purge_numbers) + EOL \
               + 'sequences: ' + str(self.purge_sequences) + EOL \
               + 'SETS:' + str(len(self.keep_set)) 

    def clear (self):
        self.purge_allcaps = False
        self.purge_caps = False
        self.purge_lower = False
        self.purge_numbers = False
        self.purge_sequences = False

        self.keep_set = set()

    def apply (self,entryset):

        if self.keep_set:
            entryset = {x_temp for x_temp in entryset if x_temp not in self.keep_set}


        if self.purge_allcaps:
            entryset = {x_temp for x_temp in entryset if x_temp != x_temp.upper() or '@' in x_temp or x_temp.isnumeric()}

        if self.purge_lower:
            entryset = {x_temp for x_temp in entryset if x_temp != x_temp.lower() or '@' in x_temp or x_temp.isnumeric()}

        if self.purge_caps:
            entryset = {x_temp for x_temp in entryset if ' '.join([x_temp.capitalize() for x_temp in x_temp.split(' ')]) != x_temp or '@' in x_temp or x_temp.isnumeric()}



        if self.purge_numbers:
            entryset = {x_temp for x_temp in entryset if not x_temp.isnumeric()}
            

        if self.purge_sequences:
            entryset = {x_temp for x_temp in entryset if not '@' in x_temp}

            


        if not entryset:
            entryset = {'VOID'}
        return entryset
    


            


        

        
            
            
            
    

        
