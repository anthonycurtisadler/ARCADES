
import datetime
import os


from globalconstants import EMPTYCHAR, COLON, EOL, RIGHTPAREN, LEFTPAREN, BLANK, POUND

class Registry:

     def __init__ (self):

          self.counter = 0
          self.directory = os.getcwd()
          self.openfiles = set()

          self.get_register(getcounter=True)

               
     def get_register(self,getcounter=False):

          try:
               self.alldata = open(self.directory + os.altsep + 'registry' + os.altsep + 'registry' +'.txt','r')
          except:
               self.alldata = open(self.directory + os.altsep + 'registry' + os.altsep + 'registry' +'.txt','x')
          self.register = self.alldata.read()
          if getcounter:
               
               if self.register:
                    try:
                         self.counter=int(self.register.split(EOL)[-2].split(BLANK)[0])             
                    except:
                         print('COUNTER RETRIEVAL FAILED')
                         print(self.register.split(EOL)[-1].split(BLANK)[0])
                         pass
          self.alldata.close()
               

          
     def addline (self,entry):
          
          self.counter += 1
          try:
               self.alldata = open(self.directory + os.altsep + 'registry' + os.altsep + 'registry' +'.txt','a')
          except:
               self.alldata = open(self.directory + os.altsep + 'registry' + os.altsep + 'registry' +'.txt','x')

          prefix = str(self.counter) + (15-len(str(self.counter))) * BLANK\
                   + BLANK + LEFTPAREN + str(datetime.datetime.now())\
                   + RIGHTPAREN + '\t' + COLON + COLON + BLANK
          self.alldata.write(prefix+entry+EOL)
          self.alldata.close()

     def encase (self,entry):

          self.alldata.write('____________'+EOL+entry+EOL+'_____________'+EOL)

     def start (self,filename):
          self.addline(filename+'#OPENED')
          
     def end (self,filename,entry2=EMPTYCHAR):
          if len(filename)<25:
               self.addline(filename+'#CLOSED'+BLANK+(25-len(filename))*BLANK+entry2)
          else:
               self.addline(filename+'#CLOSED'+BLANK+BLANK+entry2)
               

     def findopen (self):

          for line in self.register.split(EOL):
               if line:
                    filename = line.split(COLON+COLON)[1].split(POUND)[0]
                    if filename.strip():
                         if '#OPENED' in line:
                              self.openfiles.add(filename.strip())
                         if '#CLOSED' in line:
                              self.openfiles.discard(filename.strip())

     def is_open (self,filename):
          self.get_register()
          self.findopen()
          return (filename.strip() in self.openfiles)

     def exists (self,filename):
          self.get_register()
          return (BLANK + filename + '#CLOSED') in self.register

     def fetch (self,filename):
          if (BLANK + filename + POUND) in self.register:
               return self.register.split(filename+'#CLOSED')[-1].split(EOL)[0]
          

     def show_openfiles (self):
          self.get_register()
          self.findopen()
          return ', '.join(sorted(self.openfiles))

if __name__ == '__main__':

     register = Registry()
     inputterm = EMPTYCHAR
     while inputterm != 'quit':
          print(register.show_openfiles())
          inputterm = input('OPEN ?')
          register.start(inputterm)
          inputterm = input('CLOSE ?')
          register.end(inputterm)
          inputterm = input('CHECK ?')
          print(register.is_open(inputterm))
          inputterm = input('CHECKEX ?')
          print(register.exists(inputterm))
          inputterm = input('FETCH ?')
          print(register.fetch(inputterm))

     register.close()

     
     
          
     
          

          

     

          

          
          
          
