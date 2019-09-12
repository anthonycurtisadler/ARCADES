class KeyAuto:

     def __init__(self):

          self.keys = []

     def add(self,key):

          if key not in self.keys:
               self.keys.append(key)

     def search(self,fragment):

          return list(reversed([x for x in self.keys if x.startswith(fragment)]))


     def complete(self,fragment):

          keyword_list = self.search(fragment)
          if not keyword_list:
               return input(fragment+'?')
          returntext = ''
          for counter,keyword in enumerate(keyword_list):
               returntext += '(' + str(counter) + ') ' + keyword + ' ,'
          returntext += ' or RETURN to enter a new key! '

          q_temp = input(returntext)
          if q_temp == ' ':
               return keyword_list[0]
          elif q_temp.isnumeric() and int(q_temp)>=0 \
               and int(q_temp)<len(keyword_list):
               return keyword_list[int(q_temp)]
          else:
               return input(fragment+'?')

if __name__ == "__main__":

     a = KeyAuto()
     while True:
          a.add(input('?'))
          print(a.complete(input('?')))
          
          


          
               
 
               

          
