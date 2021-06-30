import datetime
from sequences import is_date
from indexclass import Index

enclosed = lambda x:x[0]+x[-1]
parenthetic = lambda x:enclosed(x)=='()'
extract = lambda x:x[1:-1]
strip_all = lambda x:[y.strip() for y in x]


class upper_str(str):

    def __init__(self, string):

        self.self = string.upper()
    def __repr__(self):
        return self.self

class Sort:

    """
    For sorting the indexes from a search research.
    index string = indexes separated by commas
    sort string = the sort instruction;
                    Criterion1_Criterion2_etc.

                    A Criterion:
                        (1) a sequence keyword
                        (2) 'DATE','USER','SIZE','KEYCOUNT','INDEX','TEXTLENGTH'
                        (3) a parenthetical phrase:

                                SPECIFIER#val1,val2,val3,val4..

                                val = WORD*WEIGHT

                                    WORD = a simple search word
                                    WEIGHT = a floating point number
                                    
                                SPECIFIER = K, KW, T, TC, TW, TCW
                                            K = KEYWORD
                                            KW = KEYWORD WEIGHTED
                                            T = TEXTWORD
                                            TC = TEXTWORD  COUNT
                                            TW = TEXTWORD WEIGHTED
                                            TCW = TEXTWORD COUNT WEIGHTED
                    USE ~ to REVERSE ordering of element
                    USE $ to make a text ordering not case sensitive

                                
    """

    def __init__ (self,
                  indexstring,
                  sortstring,
                  fetchfunction,
                  sequenceobject):
        self.fetchfunction = fetchfunction
        self.sequenceobject=sequenceobject
        strip = lambda x:x.replace(' ','')

        self.index_list = strip_all(indexstring.split(','))
        self.sort_schema =  strip_all(sortstring.split('_'))
        self.full_sort_schema = []

    def analyze_schema (self):
        #Analyzes the sortstring into the schema that can then be appplied
        #during the search

        for val in self.sort_schema:

            if len(val)>2 and parenthetic(val):
                #For a complex instruction

                val = extract(val)
                if '#' not in val:
                    specifier = 'P'
                    members = strip_all(val.split(','))
                else:
                    specifier = val.split('#')[0]
                    members = strip_all(val.split('#')[1].split(','))
                    
                    if specifier not in ['K','KW','T','TC','TW','TCW','~K','~KW','~T','~TC','~TW','~TCW']:
                        # Keyword, KeywordRanked, Text, TextCount, TextWeighted
                        specifier = 'P'
                weight_dict = {}
                #Make weighting dictionary 
                if 'W' in specifier:
                    
                    for m in members:
                        if '*' in m:
                            m, weight = m.split('*')
                            try:
                                weight = float(weight)
                            except:
                                weight = 1
                            
                        else:
                            weight = 1
                        weight_dict[m] = weight
                else:
                    for m in members:
                        weight_dict[m] = 1
                self.full_sort_schema.append((specifier,weight_dict))
                
                
               
                        

            else:
                non_case_sensitive = False
                reverse_order = ''
                            
                
                if val.startswith('~'):
                    val = val[1:]
                    reverse_order = '~'
                if val.startswith('$'):
                    #For non case sensitive search
                    val = val[1:]
                    non_case_sensitive = True
                    
                if self.sequenceobject.query(term1=val, action='in'):
                    temp_value_type = self.sequenceobject.query(term1='#TYPE#',
                                                               term2=val,
                                                               action='get')
                    if temp_value_type == str and non_case_sensitive:
                        temp_value_type = type(upper_str('f'))
                    self.full_sort_schema.append((reverse_order+val,temp_value_type))
                elif val not in ['DATE','USER','SIZE','KEYCOUNT','TEXTLENGTH','~SIZE','~KEYCOUNT','~TEXTLEGNTH']:
                    self.full_sort_schema.append((reverse_order+'INDEX',reverse_order+'INDEX'))
                else:
                    self.full_sort_schema.append((reverse_order+val,reverse_order+val))   
      

    def fetch_value (self,
                     index):

        #Fetches the appropriate information from the note in the notebase
        #corresponding to the given index.
        
        return_list = []

        temp_note = self.fetchfunction(index)
        temp_sequence_dict = {}
    
        for keyword in temp_note.keyset:
            #Extracts values for sequence keywords in the keyset of note
            
            if '@#' in keyword: #For a date sequence keyword
                head, value = keyword.split('@#')
                temp_sequence_dict[head] = is_date(value)
            elif '@_' in keyword: #For an index sequence keyword
                head, value = keyword.split('@_')
                temp_sequence_dict[head] = Index(value)
            elif '@' in keyword: #For others, in which case the type has to be
                                 #determined from the sequence register
                head, value = keyword.split('@')
                if head in self.sequenceobject.query(action='get'):
                    value_type = self.sequenceobject.query(term1='#TYPE#',
                                                           term2=head,
                                                           action='get')
                #TO convert into types
            
                if value_type in [float,int]:
                    
                    temp_sequence_dict[head] = float(value)
                elif value_type  == str:
                    temp_sequence_dict[head] = value
                elif value_type == type(upper_str('f')):
                    temp_sequence_dict[head] = upper_str(value)

                
        for v in self.full_sort_schema:
            # Applies the sort schema to the given note 

            
            val = v[0]
            spec = v[1]
            reverse = 1
            if type(val) == str and val.startswith('~'):
                val = val[1:]
                reverse = -1
            if type(spec) == str and spec.startswith('~'):
                spec = spec[1:]
                reverse = -1

            if spec in [int,float,str,type(datetime.date(1972,3,13)),type(upper_str('f')),type(Index('1'))]:
                #IF the sorting criterion is a sequence keyword 
                
                if val in temp_sequence_dict:
                    if spec in [int,float]:
                        return_list.append(temp_sequence_dict[val]*reverse)
                    elif spec in [str,type(upper_str('f'))]:
                        temp_result = temp_sequence_dict[val]
                        if spec == type(upper_str('f')):
                            temp_result = temp_result.upper() #Class not really so useful. Oh well!
                        temp_result = tuple([ord(x)*reverse for x in temp_result])
                        return_list.append(temp_result)
                    elif spec in [type(Index('1'))]:
                        return_list.append(temp_sequence_dict[val]*reverse) #NOTE no reverse yet for date or indextype
                    else:
                        #For a date sequence 
                        return_list.append((temp_sequence_dict[val].year*reverse,temp_sequence_dict[val].month*reverse,temp_sequence_dict[val].day*reverse))
                    
                else:
                    #For there is no sequence keyword corresponding to the criterion 
                    
                    if spec in [float,int]:
                        return_list.append(-10000000000000*reverse)
                    elif spec in [type(Index('1'))]:
                        return_list.append(Index('0'))
                    elif spec in [str,type(upper_str('f'))]:
                        return_list.append(tuple([0]))
                    elif spec == type(datetime.date(1972,3,13)):
                        return_list.append((-100000000*reverse,1*reverse,1*reverse))
            elif spec in ['DATE','USER','SIZE','KEYCOUNT','INDEX','TEXTLENGTH']:
                #For general sorting criterion

                if spec in ['DATE','USER','SIZE'] and spec.lower() in temp_note.meta:
                    return_list.append(temp_note.meta[spec.lower()])
                elif spec == 'KEYCOUNT':
                    return_list.append(len(temp_note.keyset)*reverse)
                elif spec == 'TEXTLENGTH':
                    return_list.append(len(temp_note.text)*reverse)
                else:
                    return_list.append(index*reverse)

            elif val in ['K','KW','T','TC','TW','TCW']:
                #To sort by the number of found elements in keywordset or text

                total_weighted_value = 0
                if isinstance(spec,dict):

                    for k in spec:
                        if 'K' in val:
                            total_weighted_value += (k in temp_note.keyset)*spec[k]
                        elif 'TC' in val:
                            total_weighted_value += (k in temp_note.text)*spec[k]
                        elif 'T' in val:
                            total_weighted_value += temp_note.text.count(k)*spec[k]
                return_list.append(total_weighted_value*reverse)
            else:
                return_list.append(index)
                
                        
                        
    
        return_list = tuple(return_list)

        return tuple(return_list)

    def generate_dict (self):

        #Generates a coversion dictionary to be applied during the sort lambda
        #Each index is assigned a tuple.

        self.result_dict = {}

        for temp_index in self.index_list:
            temp_value = self.fetch_value(temp_index)
            self.result_dict[temp_index] = self.fetch_value(temp_index)

    def get_sort (self):
        
        self.analyze_schema()
        self.generate_dict()
##        for l in sorted(self.index_list,key=lambda x:self.result_dict[x]):
##            print(self.result_dict[l])
##            for e in self.result_dict[l]:
##                if e and type(e) == tuple:
##                    print(e)
##                    try:
##                        print(''.join(chr(abs(x)) for x in e))
##                    except:
##                        pass
        
        return sorted(self.index_list,key=lambda x:self.result_dict[x])
    
            
        
            
                    
                    
            
            
                     

        
        
