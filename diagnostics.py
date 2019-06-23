
import datetime
import os


from globalconstants import EMPTYCHAR, COLON, EOL, RIGHTPAREN, LEFTPAREN, BLANK

class DiagnosticTracking:

     def __init__ (self,filename):

          self.counter = 1
          directory = os.getcwd()
          try:
               self.alldata = open(directory + os.altsep + 'diagnostics' + os.altsep + filename +'DIAG.txt','a')
          except:
               self.alldata = open(directory + os.altsep + 'diagnostics' + os.altsep + filename +'DIAG.txt','x')
               

     def addline (self,entry):

          prefix = str(self.counter) + (10-len(str(self.counter))) * BLANK\
                   + BLANK + LEFTPAREN + str(datetime.datetime.now())\
                   + RIGHTPAREN + '\t' + COLON + COLON + BLANK
          self.alldata.write(prefix+entry+EOL)
          self.counter += 1

     def encase (self,entry):

          self.alldata.write('____________'+EOL+entry+EOL+'_____________'+EOL)

     def start (self):
          self.encase('INITIALIZE')
     def end (self):
          self.encase('TERMINATE')
          self.alldata.close()


          

if __name__ == '__main__':

     diagnostics = DiagnosticTracking('TEST')
     diagnostics.start()
     inputterm = EMPTYCHAR
     while inputterm != 'quit':
          inputterm = input('?')
          diagnostics.addline(inputterm)

     diagnostics.end()

     
     
          
     
          

          

     

          

          
          
          
