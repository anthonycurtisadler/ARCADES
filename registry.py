
import datetime
import os
from displaylist import DisplayList
import nformat
from display import Display


from globalconstants import EMPTYCHAR, COLON, EOL, \
     RIGHTPAREN, LEFTPAREN, BLANK, POUND, LEFTNOTE,\
     RIGHTNOTE, DASH, PERIOD, UNDERLINE, VERTLINE

def is_date(entry,isbefore=False):

     if not entry:
          return EMPTYCHAR

     if not isbefore:
          supplements = (0,1,1,0,0,0,0,0,0)
     else:
          supplements = (0,12,31,23,59,59,0,0)
          
               

     entry = entry.replace(DASH,BLANK).replace(COLON,BLANK).replace(PERIOD,BLANK).replace(BLANK+BLANK,BLANK)
     returnentry = []
     for counter,x in enumerate((entry.split(BLANK)+['x','x','x','x','x','x'])[0:8]):
          if x != 'x':
               returnentry.append(int(x))
          else:
               returnentry.append(supplements[counter])
     return returnentry

class Registry:

     def __init__ (self,displayobject=None):

          self.counter = 0
          self.directory = os.getcwd()
          self.openfiles = set()
          if displayobject:
               self.displayobject = displayobject
          else:
               self.displayobject  = Display()
          

          self.get_register(getcounter=True)

     def get_date (self,entry):

          if LEFTPAREN in entry and RIGHTPAREN in entry:
               date = is_date(entry.split(LEFTPAREN)[1].split(RIGHTPAREN)[0])
               if date:
                    return date
          return False

               
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

     def convert (self,entrylist):
          returnlist = []
          for line in entrylist:
               firsthalf = line.split(COLON+COLON)[0]
               if COLON+COLON in line:
                    secondhalf = line.split(COLON+COLON)[1]
               else:
                    secondhalf = BLANK

          
               counter = firsthalf.split(LEFTPAREN)[0].strip()
               if LEFTPAREN in firsthalf:
                    date = firsthalf.split(LEFTPAREN)[1].split(RIGHTPAREN)[0]
               else:
                    date = BLANK
               filename = secondhalf.split(POUND)[0]
               if POUND in secondhalf:
                    status = secondhalf.split(POUND)[1].split(BLANK)[0]
               else:
                    status = BLANK
               if "'projectset':" in secondhalf:
                    term_temp = secondhalf.split("'projectset':")[1]
                    if '{' in term_temp and '}' and term_temp:
                         projects = term_temp.split('{')[1].split('}')[0].replace("'",EMPTYCHAR)
               else:
                    projects = BLANK
               returnlist.append(counter+BLANK+VERTLINE+BLANK+
                                 date+BLANK+VERTLINE+BLANK+
                                 filename+LEFTPAREN+status+RIGHTPAREN+VERTLINE+BLANK+
                                 projects)
          return returnlist 
                                 
               

     def fetchall (self,entry1=EMPTYCHAR,entry2=EMPTYCHAR,entry3=EMPTYCHAR,entry4=EMPTYCHAR,d_aft=EMPTYCHAR,d_bef=EMPTYCHAR):
          self.get_register()
          if  isinstance(d_aft,str):
               d_aft = is_date(d_aft)
          if  isinstance(d_bef,str):
               d_bef = is_date(d_bef,isbefore=True)
          print(d_aft)
          print(d_bef)
          returnlist = []
          for line in self.register.split(EOL):
               d_com = self.get_date(line)
               

     
               if ((entry1 and entry1 in line) or not entry1) \
                  and ((entry2 and entry2 in line) or not entry2)\
                  and ((entry3 and entry3 in line) or not entry3) \
                  and ((entry4 and entry4 in line) or not entry4) \
                  and ((d_com and d_bef and d_com<=d_bef) or not d_bef) \
                  and ((d_com and d_aft and d_com>=d_aft) or not d_aft):
                    returnlist.append(line)
          return returnlist 

     def present (self,entryterms=EMPTYCHAR,dates=EMPTYCHAR):

          

          notelist = DisplayList(displayobject=self.displayobject)
          if entryterms:
               if UNDERLINE in entryterms:
                    entryterms = entryterms.split(UNDERLINE)
                    if len(entryterms) == 2:
                         entry1, entry2, entry3 = entryterms[0], entryterms[1], EMPTYCHAR
                    else:
                         entry1, entry2, entry3 = entryterms[0], entryterms[1], entryterms[2]
               else:
                    entry1, entry2, entry3 = entryterms, EMPTYCHAR, EMPTYCHAR
          else:
               entry1, entry2, entry3 = EMPTYCHAR, EMPTYCHAR, EMPTYCHAR
          if dates:
               if UNDERLINE in dates:
                    dates = dates.split(UNDERLINE)
                    d_aft, d_bef= dates[0],dates[1]
               else:
                    d_aft, d_aft = EMPTYCHAR, EMPTYCHAR
          else:
               d_aft, d_bef = EMPTYCHAR, EMPTYCHAR
          nformat.columns(EOL.join(self.convert(self.fetchall(entry1=entry1,
                                                              entry2=entry2,
                                                              entry3=entry3,
                                                              d_bef=d_bef,
                                                              d_aft=d_aft))),
                                                listobject=notelist,
                                                columnwidth = (10,30,40,60))
          notelist.present()
                    
        

     def console (self):

          
          menu = "(1) Show the entire registry \n"+\
                 "(2) Show registry for a notebook \n"+\
                 "(3) Search \n" +\
                 "(4) Quit "
          
          inputterm = EMPTYCHAR
          while inputterm != '4':
               self.displayobject.noteprint(('',menu))
               inputterm = input('?')
               if inputterm == '1':
                    self.present()
               if inputterm == '2':
                    self.present(entryterms=input('PROJECT NAME?'))
               if inputterm == '3':
                    term1 = input('NOTEBOOK NAME?')
                    term2 = input('(c)losed or (o)open')
                    if term2:
                         term2 = {'c':'CLOSED',
                                  'o':'OPENED'}[term2[0].lower()]
                    term3 = input('PROJECT NAME?')
                    dateafter = input('DATE AFTER?')
                    datebefore = input('DATE BEFORE?')
                    self.present(term1+UNDERLINE+term2+UNDERLINE+term3,dateafter+UNDERLINE+datebefore)
                    
                    
          

     def show_openfiles (self):
          self.get_register()
          self.findopen()
          return ', '.join(sorted(self.openfiles))

if __name__ == '__main__':

     register = Registry()
     inputterm = EMPTYCHAR
     register.console()
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
          dateafter = input('DATEaft?')
          datebefore = input('DATEbef?)')
          print(EOL.join(register.fetchall(inputterm,d_aft=is_date(dateafter),d_bef=is_date(datebefore,isbefore=True))))

     register.close()

     
     
          
     
          

          

     

          

          
          
          
