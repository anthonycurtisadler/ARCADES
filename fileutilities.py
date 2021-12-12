import os
from globalconstants import BLANK, EMPTYCHAR,\
     PERIOD, SLASH, VERTLINE, QUESTIONMARK, YESTERMS
from plainenglish import Queries
from display import Display
from generalutilities import abridge, show_list 

display = Display()
queries = Queries()
dummy = lambda x:x

def nprint(*entries):
    """For printing in a boxed note"""
    
    text = ''
    for entry in entries:
        text += entry + BLANK

    if text.strip:    
        display.noteprint(('',text))
    else:
        print()

class FileAccess:

    def __init__ (self,db_cursor = None):

        self.db_cursor = db_cursor
            

    def get_text_file(self,
                      filename,
                      folder=os.altsep+'textfiles',
                      suffix='.txt'):


        """opens a text file a returns the text"""

        directoryname = os.getcwd()+folder
        if os.altsep+'notebooks'+os.altsep+'textfiles' in directoryname:
            nprint(directoryname)
            directoryname = directoryname.replace(os.altsep + 'notebooks'
                                                  + os.altsep+'textfiles',
                                                  os.altsep+'textfiles')
            nprint(directoryname)
        if  os.altsep+'notebooks'+'/'+'textfiles' in directoryname:
            nprint(directoryname)
            directoryname = directoryname.replace(os.altsep + 'notebooks'
                                                  + '/' + 'textfiles',
                                                  os.altsep+'textfiles')
            nprint(directoryname)
            
        
        with open(directoryname+os.altsep+filename+suffix,'r',
                        encoding='utf-8') as textfile:
            returntext = textfile.read().replace('\ufeff',
                                             EMPTYCHAR)
        return returntext

    def save_file(self,
                  returntext=EMPTYCHAR,
                  filename=EMPTYCHAR,
                  folder=os.altsep+'textfiles'):

        """for saving a file"""
        
                  
        directoryname = os.getcwd()+folder
        nprint(directoryname)
        with open(directoryname+os.altsep
                        +filename+'.txt',
                        'x',
                        encoding='utf-8') as textfile:
            textfile.write(returntext.replace('\ufeff', ' '))

        return 'Saved to ' + directoryname+SLASH+filename+'.txt'

    def get_file_name(self,
                      file_path=EMPTYCHAR,
                      file_suffix=EMPTYCHAR,
                      file_prefix=EMPTYCHAR,
                      get_filename=EMPTYCHAR,
                      justshow=False,
                      show_notebooks_too=False):

        """Lists files in directory asks the user to make a selection.
        returns the name of the file
        """

        def directory ():

            """gets directory"""

                
            allfiles = os.listdir(file_path)

            filelist = [a_temp[0: -len(file_suffix)]
                        for a_temp in allfiles
                        if (a_temp.startswith(file_prefix)
                            and a_temp.endswith(file_suffix))]

            if show_notebooks_too:
                self.db_cursor.execute("SELECT notebook FROM notebooks")
                filelist += list([i[0] for i in self.db_cursor.fetchall()])
            
            dirlist = [a_temp for a_temp in allfiles if PERIOD not in a_temp]
            
            textlist = []
            display_path = abridge(file_path,30,rev=True)

            for temp_counter, filename in enumerate(filelist):
                #Files
                l_temp = filename
                textlist.append((l_temp,file_suffix))

            for temp_counter, filename in enumerate(dirlist):
                #Directories
                l_temp = filename
                textlist.append((l_temp,'DIR'))

            show_list(textlist,display_path+'\n'+\
                      (max([(int(len(file_path)/2))-5,0])*BLANK),0,20,
                      select=True,
                      func=zformat,
                      sfunc=dummy,
                      present=True,
                      display=display)

            return filelist,dirlist
        
        def zformat (x_temp):

            """formating function for columns"""
            
            return x_temp[0] + VERTLINE + x_temp[1] 
        
        def select_file (filelist):

            """selecting function"""
            
            go_on = True
            while go_on:
                newfile = input(queries.SELECT_FILE)
                nprint()

                if newfile in ['b','B','BACK','back']:
                    return 'BACK', EMPTYCHAR
                elif (newfile.isnumeric() and int(newfile) > 0
                        and int(newfile) < len(filelist)+1):
                    newfile = filelist[int(newfile)-1]
                    tag = 'w'
                else:
                    newfile = file_prefix+newfile
                    tag = 'c'
                if input(queries.OPEN_CONFIRM+newfile+QUESTIONMARK+BLANK) in YESTERMS:
                    go_on = False

            return newfile, tag

        """fetches a filename to load"""

        if get_filename != EMPTYCHAR:
            return get_filename, EMPTYCHAR
    ##    if 'simple note' in os.getcwd():
    ##        file_path = os.getcwd() + file_path
    ##    else:
    ##        file_path = os.getcwd()
        file_path = os.getcwd() + file_path
            
        old_file_path = file_path
        added_path = EMPTYCHAR


        filelist,dirlist = directory()



        if not justshow:

            while True:

                selected = select_file(filelist+dirlist)

                if selected[0] != 'BACK' and selected[0] not in dirlist:
                    #to go back to last directory
                    return added_path + selected[0],selected[1]
                else:
                    if selected[0] == 'BACK':
                        file_path = old_file_path
                        added_path = EMPTYCHAR

                    else:
                        file_path += os.altsep + selected[0]
                        added_path += os.altsep + selected[0]
                    os.chdir (file_path)
                        


                    filelist,dirlist = directory()
                    if not filelist and not dirlist:
                        display.noteprint((file_path,'EMPTY'))
                    

        return EMPTYCHAR, EMPTYCHAR

    def make_new_directory (self,
                            directory_name='testnotebook',
                            file_path=EMPTYCHAR,):

        full_path = os.getcwd()+file_path
        allfiles = os.listdir(full_path)
        return_text = ""

        if directory_name not in allfiles:
            try:
                os.mkdir(full_path+os.altsep+directory_name)
                return_text = 'NEW FOLDER CREATED: '+directory_name
            except:
                return_text = 'NEW FOLDER CREATION FAILED'
        else:
            return_text = directory_name + ' ALREADY EXISTS'
        return return_text
       
    def get_all_notebooks ():

        """Returns a list of all the notebooks in the database"""


        self.db_cursor.execute("SELECT * FROM notebooks;")
        temp_list = self.db_cursor.fetchall()
        returnlist = [x[0] for x in temp_list]
        return returnlist 

