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


     def show (self,phrase):

          keyword = split(phrase)
          if keyword in self.defaultdictionary:
               return self.defaultdictionary[keyword]
          return EMPTYCHAR

     def change (self,phrase,value):
          
          """either add to value, subtracts from value, or replaces it.
          Addition and subtraction for repeated plus or minus signs, according to legnth"""

          
          keyword = split(phrase)
          if value == ' ' and keyword in self.defaultdictionary:
               value = self.defaultdictionary[keyword]
          elif not value:
               return ''
          else:
               if value[0] == '=':
                    value = value[1:]
               elif  self.is_float(keyword):
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
                         
                         
               
          self.defaultdictionary[keyword] = value
          return value 

if __name__ == '__main__':
     test = SequenceDefaultDictionary()
     while True:

          
          print(test.change(input('?'),input('??')))
          print(test.show(input('???')))
          print(test.defaultdictionary)
          print(test.is_float(input('????')))
               
     

          
