##Shelf for keeping workpads and sheets##

import shelve
from globalconstants import SLASH


def openshelf(path_and_name,shelfobject=None,createnew=False):
     
     flag = 'w'
     try:
          if createnew:
               print(1+'g') #create an exception
          shelfobject = shelve.open(path_and_name, flag)
          return 'w'
                    
               

     except:
          try:
               flag = 'c'
               shelfobject = shelve.open(path_and_name, flag)
               return 'c'
          except:
               return 'f'


class SheetShelf:

     def __init__ (self,directoryname=None,notebookname=None,display=None):

          try:
               flag = 'w'

               self.sheetshelf = shelve.open(directoryname+SLASH+'SHEETSHELVE',flag)
               self.display = display
          except:
               flag = 'c'
               self.sheetshelf = shelve.open(directoryname+SLASH+'SHEETSHELVE',flag)
               self.notebookname = notebookname

     def add (self,
              notebookname=None,
              objectname=None,
              textlist=None,
              object_dict=None,
              y_pos=0,
              x_pos=0,
              override=False):

          if notebookname is None:
               notebookname = self.notebookname

          if not override:

               while objectname and notebookname+objectname in self.sheetshelf:

                    self.display.noteprint(('',notebookname + objectname + 'already exists!'))
                    newobjectname = input('New name or numerical suffix!')
                    if newobjectname.isnumeric():
                         objectname = objectname + str(newobjectname)
                    else:
                         objectname = newobjectname
          self.sheetshelf[notebookname+objectname] = (textlist,object_dict,(y_pos,x_pos))
          print(self.sheetshelf.keys)
          return notebookname+objectname 
          

     def return_object (self,fullobjectname):

       if fullobjectname and fullobjectname in self.sheetshelf:

            return self.sheetshelf[fullobjectname]

     def select (self):
          print('start')
          objectnames = sorted(self.sheetshelf.keys())
          for counter, obj in enumerate(objectnames):

               print (str(counter)+':'+obj)
          while True:
               
               imp_temp = input('?')
               if imp_temp.isnumeric():
                    return self.return_object (objectnames[int(imp_temp)]), objectnames[int(imp_temp)]
               elif imp_temp in self.sheetshelf:
                    return self.return_object (imp_temp), imp_temp
               elif not imp_temp:
                    break
               else:
                    print('Failed!')

     
               
               


     
            
                    

          
          

          

     
