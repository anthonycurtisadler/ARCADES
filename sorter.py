import datetime
from sequences import is_date
from indexclass import Index

enclosed = lambda x:x[0]+x[-1]
parenthetic = lambda x:enclosed(x)=='()'
extract = lambda x:x[1:-1]
strip_all = lambda x:[y.strip() for y in x]


    

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
                    
                    if specifier not in ['K','KW','T','TC','TW','TCW']:
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
                if self.sequenceobject.query(term1=val, action='in'):
                    temp_value_type = self.sequenceobject.query(term1='#TYPE#',
                                                               term2=val,
                                                               action='get')
                    self.full_sort_schema.append((val,temp_value_type))
                elif val not in ['DATE','USER','SIZE','KEYCOUNT','TEXTLENGTH']:
                    self.full_sort_schema.append(('INDEX','INDEX'))
                else:
                    self.full_sort_schema.append((val,val))
                
      

    def fetch_value (self,
                     index):
        return_list = []

        temp_note = self.fetchfunction(index)
        temp_sequence_dict = {}
        for keyword in temp_note.keyset:
            if '@#' in keyword:
                head, value = keyword.split('@#')
                temp_sequence_dict[head] = is_date(value)
            elif '@_' in keyword:
                head, value = keyword.split('@_')
                temp_sequence_dict[head] = Index(value)
            elif '@' in keyword:
                head, value = keyword.split('@')
                if head in self.sequenceobject.query(action='get'):
                    value_type = self.sequenceobject.query(term1='#TYPE#',
                                                           term2=head,
                                                           action='get')
                if value_type in [float,int]:
                    
                    temp_sequence_dict[head] = float(value)
                elif value_type  == str:
                    temp_sequence_dict[head] = value
                    
                
        for v in self.full_sort_schema:

            
            val = v[0]
            spec = v[1]

            if spec in [int,float,str,type(datetime.date(1972,3,13))]:
                
                if val in temp_sequence_dict:   
                    return_list.append(temp_sequence_dict[val])
                else:
                    
                    if spec in [float,int]:
                        return_list.append(-10000000000000)
                    elif spec == str:
                        return_list.append('')
                    elif spec == type(datetime.date(1972,3,13)):
                        return_list.append(datetime.date(-100000000,1,1))
            elif spec in ['DATE','USER','SIZE','KEYCOUNT','INDEX','TEXTLENGTH']:

                if spec in ['DATE','USER','SIZE'] and spec.lower() in temp_note.meta:
                    return_list.append(temp_note.meta[spec.lower()])
                elif spec == 'KEYCOUNT':
                    return_list.append(len(temp_note.keyset))
                elif spec == 'TEXTLENGTH':
                    return_list.append(len(temp_note.text))
                else:
                    return_list.append(index)

            elif val in ['K','KW','T','TC','TW','TCW']:

                total_weighted_value = 0
                if isinstance(spec,dict):

                    for k in spec:
                        if 'K' in val:
                            total_weighted_value += (k in temp_note.keyset)*spec[k]
                        elif 'TC' in val:
                            total_weighted_value += (k in temp_note.text)*spec[k]
                        elif 'T' in val:
                            total_weighted_value += temp_note.text.count(k)*spec[k]
                return_list.append(total_weighted_value)
            else:
                return_list.append(index)
                
                        
                        
    
        return_list = tuple(return_list)

        return tuple(return_list)

    def generate_dict (self):

        self.result_dict = {}

        for temp_index in self.index_list:
            temp_value = self.fetch_value(temp_index)
            self.result_dict[temp_index] = self.fetch_value(temp_index)

    def get_sort (self):
        
        self.analyze_schema()
        self.generate_dict()
        
        return sorted(self.index_list,key=lambda x:self.result_dict[x])
    
            
        
            
                    
                    
            
            
                     

        
        
