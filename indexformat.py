# For displaying the index


from numbertools  import format_range as fr, rom_to_int, int_to_roman,\
     abbreviate_range,convert_range
import string
SUBHEAD_WORDS = ['and','of','as','vs.','for','a','the','into']
DELETE_CHARS = (string.punctuation+string.whitespace).replace(',','').replace('(','').replace(')','')

def format_range(x):
    return convert_range(fr(x),join_phrase=',')

def truncate_small(x,words=SUBHEAD_WORDS):

    while x:
        found = False
        for w in words:
            if x.startswith(w+' '):
                x = x[len(w+' '):]
                found = True
        if not found:
            break 
    return x


def get_if(x,left=None,right=None):

    if left and right:
        if left in x and right in x:
            return x.split(left)[1].split(right)[0].strip(),\
                   x.split(left)[0]+x.split(right)[1].strip()
        
        return '',x.strip()
def get_comma (x):

    if ',' in x:
        return x.split(',')[0].strip(),x.split(',')[1].strip()
    return x.strip(),''

def get_right (x,div_char=';;'):

    if div_char in x:
        return x.split(div_char)[1].strip(), x.split(div_char)[0].strip()
    else:
        return '',x.strip()

def sort_function (x):

    #FOLLOWING CMS 16 'LETER by LETTER'

    
    x = truncate_small(x)
    x = x.replace('(',',(')
    
    for c in DELETE_CHARS:
            x = x.replace(c,'')
    x = x.lower()
    return tuple(x.split(','))


class Entry:

    def __init__ (self,entry):

        pages,entry = get_if(entry,'{','}')
        

        self.ref_full_name, entry = get_if(entry,'<','>')
        if self.ref_full_name:
            self.ref_full_name = self.ref_full_name.split(';;')[0].strip()
            
            self.ref_last_name, self.ref_first_name = get_comma(self.ref_full_name)
        else:
            self.ref_last_name = ''
            self.ref_first_name = ''
        self.search_phrase, entry = get_right(entry)
        self.see_also, self.head_phrase = get_if(entry,'[',']')
        self.sub_head, self.main_head = get_right(self.head_phrase,div_char='_')
        self.descriptor, self.main_head = get_if(self.main_head,'(',')')
        
    
    def __str__ (self):
        to_return = ''

        if self.ref_full_name:
            to_return += 'REF_FULL_NAME='+self.ref_full_name+';'
        if self.ref_last_name:
            to_return += 'REF_LAST_NAME='+self.ref_last_name+';'
        if self.ref_first_name:
            to_return += 'REF_FIRST_NAME='+self.ref_first_name+';'
        if self.search_phrase:
            to_return += 'SEARCH_PHRASE='+self.search_phrase+';'
        if self.see_also:
            to_return += 'SEE_ALSO='+self.see_also+';'
        if self.main_head:
            to_return += 'MAIN_HEAD='+self.main_head+';'
        if self.sub_head:
            to_return += 'SUB_HEAD='+self.sub_head
        if self.descriptor:
            to_return += 'DESCRIPTOR='+self.descriptor
        return to_return         
    
            

class FormatIndex:

    def __init__ (self,index_object=None):

        self.index_object = index_object
        self.headings = {}
        self.names = {} #For keeping track of common last names

        self.comma_before_single_quotes = True
        self.comma_before_double_quotes = True
        self.single_quote = '’'
        self.double_quote = '”'

    
    def generate_dictionary (self):

        for mode, dict_obj in enumerate([self.index_object['names'],self.index_object['concepts']]):
            for name in dict_obj:

                name_inf = Entry(name)
                
                if not name_inf.sub_head:
                    if name_inf.main_head not in self.headings:
                        self.headings[name_inf.main_head] = {'descriptor':name_inf.descriptor,
                                                             'pages':dict_obj[name],
                                                             'works':{},
                                                             'pages_in_titles':set(),
                                                             'subheadings':{},
                                                             'pages_in_subheadings':set(),
                                                             'type':'HEADNAME'}
                        if mode == 0:
                            last_name, first_name = get_comma (name_inf.main_head)
                            
                            if last_name not in self.names:
                                self.names[last_name] = set()
                            self.names[last_name].add(name_inf.main_head)
            for name in dict_obj:
                name_inf = Entry(name)

                if name_inf.sub_head:
                    if name_inf.main_head in self.headings:
                        self.headings[name_inf.main_head]['subheadings'][name_inf.sub_head] = {'pages':dict_obj[name]}
                        self.headings[name_inf.main_head]['pages_in_subheadings'].update(dict_obj[name])
                    else:
                        self.headings[name_inf.main_head] = {'descriptor':name_inf.descriptor,
                                                             'pages':self.index_object['names'][name],
                                                             'works':{},
                                                             'pages_in_titles':set(),
                                                             'subheadings':{},
                                                             'pages_in_subheadings':set(),
                                                             'type':'HEADNAME'}
                        self.headings[name_inf.main_head]['subheadings'][name_inf.sub_head] = {'pages':dict_obj[name]}
                        self.headings[name_inf.main_head]['pages_in_subheadings'] = dict_obj[name]

            
        for title in self.index_object['titles']:
            title_inf = Entry(title)

            

            if not title_inf.ref_full_name:
                if title_inf.main_head not in self.headings:
                    self.headings[title_inf.main_head] = {'descriptor':name_inf.descriptor,
                                                         'pages':self.index_object['titles'][title],
                                                         'works':{},
                                                         'pages_in_titles':set(),
                                                         'subheadings':{},
                                                         'pages_in_subheadings':set(),
                                                         'type':'SOLOTITLE'}

            else:
                
                if title_inf.ref_last_name in self.names:
                    if len(self.names[title_inf.ref_last_name]) == 1:
                        name = list(self.names[title_inf.ref_last_name])[0]

                    else:
                        name = [x for x in self.names[title_inf.ref_last_name] if title_inf.ref_last_name in x and title_inf.ref_first_name in x]
                        if name:
                            name = name[0]
                        else:
                            print('NAME NOT FOUND')
                            name = ''

                if name and name in self.headings:

                    self.headings[name]['works'][title_inf.main_head] = {'pages':self.index_object['titles'][title]}
                    self.headings[name]['pages_in_titles'].update(self.index_object['titles'][title])


    def print_dictionary (self):

        all_heads = sorted(self.headings.keys(),key=lambda x:sort_function(x))
        returnlist = []
        last_letter = ''

        

        for x in all_heads:
            

            linetext = ''
            if last_letter.lower() != x[0].lower():
                returnlist.append('')
            last_letter = x[0]
            skip_empty = True
            
            def some_numeric(x):
                return 'see ' in x or len(set(y for y in x if y.isnumeric()))>0

            def correct (x):

                if  self.comma_before_single_quotes and self.comma_before_double_quotes:
                    x = x.replace(self.single_quote+self.double_quote+',',','+self.single_quote+self.double_quote)
                if self.comma_before_single_quotes:
                    x = x.replace(self.single_quote+',',','+self.single_quote)
                if self.comma_before_double_quotes:
                    x = x.replace(self.double_quote+',',','+self.double_quote)
                return x
            


            for mode in [0,1]:

                if mode == 0 or (mode == 1 and self.headings[x]['works']):

                    # mode=0 for the MAIN HEADING of CONCEPTS, NAMES
                    # mode=1 for the WORKS listed under AUTHORS 
                    
                    
                    
                        
                    if mode == 0:

                        

                        if self.headings[x]['pages']-self.headings[x]['pages_in_titles']-self.headings[x]['pages_in_subheadings']:
                            linetext += x
                            if self.headings[x]['descriptor']:
                                linetext += '('+self.headings[x]['descriptor']+')'
                            linetext += ', '
                            linetext += format_range(self.headings[x]['pages']-self.headings[x]['pages_in_titles']-self.headings[x]['pages_in_subheadings']).replace(',',', ')
                            linetext += '; '
                        else:
                            linetext += x
                            linetext += '; '
                        if self.headings[x]['subheadings']:

                            for sub_head in sorted(self.headings[x]['subheadings'],key=lambda x:sort_function(x)):
                                linetext += sub_head
                                linetext += ', '
                                linetext += format_range(self.headings[x]['subheadings'][sub_head]['pages']).replace(',',', ')
                                linetext += '; '
                        if linetext.endswith('; '):
                            linetext = linetext[:-2]        
                        if linetext and some_numeric(linetext):
                            returnlist.append(correct(linetext))
                        else:
                            print('SKIPPED ',linetext)
                        linetext = ''

                    else:
                        
                        linetext += x
                        if self.headings[x]['descriptor']:
                            linetext += '('+self.headings[x]['descriptor']+')'
                        linetext += ', works by: '
                        for work in sorted(self.headings[x]['works'],key=lambda x:sort_function(x)):
                            linetext += work
                            linetext += ', '
                            linetext += format_range(self.headings[x]['works'][work]['pages']).replace(',',', ')
                            linetext += '; '
                        if linetext.endswith('; '):
                            linetext = linetext[:-2]
                        if linetext:
                            returnlist.append(correct(linetext))
                        linetext = ''
            

        return '\n'.join(returnlist)
    
                

            

            


        

                


        
