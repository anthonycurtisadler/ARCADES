# For keeping track of the default values of sequences


from globalconstants import ATSIGN,EMPTYCHAR 

def split(phrase):
     return phrase.split(ATSIGN)[0]

def isonly(phrase,char):

     if char in phrase and phrase.count(char)==len(phrase):
          return True
     return False


class SequenceDefaultDictionary:

     def __init__(self):

          self.defaultdictionary = {}

     def is_numeric(self,keyword):

          if keyword in self.defaultdictionary and self.defaultdictionary[keyword].isnumeric():
               return True
          return False

     def is_float(self,keyword):
          if keyword in self.defaultdictionary:
               try:
                    float(self.defaultdictionary[keyword])
                    return True
               except:
                    return False
          return False

     def is_index(self,keyword):
          if keyword in self.defaultdictionary:

               val = self.defaultdictionary[keyword]
               if val[0] !='.' and val[-1] != '.' and '.' in val and val.replace('.','').isnumeric():
                    return True
                    
          return False



     def show (self,phrase):

          keyword = split(phrase)
          if keyword in self.defaultdictionary:
               return self.defaultdictionary[keyword]
          return EMPTYCHAR

     def change (self,phrase,value):
          
          """either add to value, subtracts from value, or replaces it.
          Addition and subtraction for repeated plus or minus signs, according to legnth"""

          if value == '/':
               return value
          keyword = split(phrase)
          if value == ' ' and keyword in self.defaultdictionary:
               value = self.defaultdictionary[keyword]
          elif not value:
               return ''
          else:
               if value[0] == '=':
                    value = value[1:]
               elif  self.is_float(keyword) and value and not value[0]=='.':
                    if isonly(value,'+') and self.is_float(keyword):
                         value = str(float(self.defaultdictionary[keyword])+len(value))
                    elif isonly(value,'-') and self.is_float(keyword):
                         value = str(float(self.defaultdictionary[keyword])-len(value))
                    elif value[0]=='+' and len(value)>1:
                         try:
                              value = str(float(self.defaultdictionary[keyword])+float(value[1:]))
                         except:
                              pass
                    elif value[0]=='-' and len(value)>1:
                         try:
                              value = str(float(self.defaultdictionary[keyword])-float(value[1:]))
                         except:
                              pass
                    if self.is_numeric(keyword):
                         value = str(int(float(value)))
               elif self.is_index(keyword):
                    if len(value) > 1 and value[0]=='.' and value.count('.')<=self.defaultdictionary[keyword].count('.'):
                         index_values = self.defaultdictionary[keyword].split('.')
                         new_values = value[1:].split('.')
                         value = '.'.join(index_values[0:-len(new_values)]+new_values)
                    
                         
                         
                         
               
          self.defaultdictionary[keyword] = value
          return value 

if __name__ == '__main__':
     test = SequenceDefaultDictionary()
     while True:

          
          print(test.change(input('?'),input('??')))
          print(test.show(input('???')))
          print(test.defaultdictionary)
          print(test.is_float(input('????')))
               
     

          
