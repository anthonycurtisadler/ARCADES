## CLASS FOR MANAGING PROJECTS
## 

from complexobjecttransformindexes import transform
from orderedlist import OrderedList
from indexclass import Index
import datetime

class ProjectManager:

     def __init__ (self,
                   project_dictionary=None,
                   connection=None,
                   cursor=None,
                   notebookname=None,
                   archive=False,
                   db_only=False):

          if connection and cursor:
               self.connection = connection
               self.cursor = cursor
               self.using_database = True


          else:
               self.using_database = False
          if archive:
               self.project_suffix = 'archive'
          else:
               self.project_suffix = ''
          self.notebookname = notebookname
          self.db_only=db_only

          if self.using_database:

               self.cursor.executescript("""
               CREATE TABLE IF NOT EXISTS project_names (

                    notebook TEXT NOT NULL,
                    project TEXT NOT NULL,
                    UNIQUE (notebook, project)
                    FOREIGN KEY (notebook) REFERENCES notebooks (notebook) ON DELETE CASCADE
                    );""")

               self.cursor.executescript("""
               CREATE TABLE IF NOT EXISTS project_keys (

                    notebook TEXT NOT NULL,
                    project TEXT NOT NULL,
                    project_key TEXT NOT NULL,
                    
                    UNIQUE (notebook, project, project_key)
                    FOREIGN KEY (notebook, project) REFERENCES project_names (notebook, project) ON DELETE CASCADE
                    );""")


               self.cursor.executescript("""
               CREATE TABLE IF NOT EXISTS project_indexes (

                    notebook TEXT NOT NULL,
                    project TEXT NOT NULL,
                    project_index TEXT NOT NULL,
                    
                    UNIQUE (notebook, project, project_index)
                    FOREIGN KEY (notebook, project) REFERENCES project_names (notebook, project) ON DELETE CASCADE
                    );""")


               self.cursor.executescript("""
               CREATE TABLE IF NOT EXISTS project_dates (

                    notebook TEXT NOT NULL,
                    project TEXT NOT NULL,
                    project_date TEXT NOT NULL,
                    
                    UNIQUE (notebook, project, project_date)
                    FOREIGN KEY (notebook, project) REFERENCES project_names (notebook, project) ON DELETE CASCADE
                    );""")

               self.cursor.executescript("""
               CREATE TABLE IF NOT EXISTS simple_properties (

                    notebook TEXT NOT NULL,
                    project TEXT NOT NULL,
                    lastup TEXT NOT NULL,
                    uptohere TEXT NOT NULL,
                    mainterm TEXT NOT NULL,
                    series_enter TEXT NOT NULL,
                    opened TEXT NOT NULL,
                                  
                    UNIQUE (notebook, project)
                    FOREIGN KEY (notebook, project) REFERENCES project_names (notebook, project) ON DELETE CASCADE
                    );""")
          if project_dictionary:
               if self.using_database:
                    print('here')
               
                    self.projects = project_dictionary
                    self.current = None
                    self.clear_database()
                    self.load_into_database(all_projects=project_dictionary)
                    print('loaded into database')

          else:
               self.projects = {}
               self.current = None
 

          
               
     
     # methods for accessing the database

     def set_db_only (self,status):

          self.db_only = status 

     def add_new_project_DB (self,project=None):

          value_tuple = (self.notebookname, project+self.project_suffix,)

          self.cursor.execute("INSERT OR REPLACE INTO project_names "
                              +"(notebook, project) VALUES (?,?);",
                              value_tuple)
          self.connection.commit()

     def get_projects_DB (self):

          self.cursor.execute("SELECT project "
                              +"FROM project_names WHERE notebook=?",
                              (self.notebookname,))
          return [x[0] for x in self.cursor.fetchall()]

     def delete_project_DB (self,project=None):
          self.cursor.execute("DELETE FROM project_names "+
                              "WHERE notebook=? AND project=?;",
                              (self.notebookname,project,))
          self.connection.commit()

     def add_index_DB (self,project=None,index=None):

          if index:
               index=str(index)

          value_tuple = (self.notebookname, project+self.project_suffix,index,)
          self.cursor.execute("INSERT OR REPLACE INTO project_indexes "
                              +"(notebook, project, project_index) VALUES (?,?,?);",
                              value_tuple)
          self.connection.commit()

     def delete_index_DB (self,project=None,index=None):

          value_tuple = (self.notebookname, project+self.project_suffix,index,)
          self.cursor.execute("DELETE FROM project_indexes "+
                              "WHERE notebook=? AND project=? and project_index=?;",
                              value_tuple)
          self.connection.commit()

     def delete_key_DB (self,project=None,key=None):

          value_tuple = (self.notebookname, project+self.project_suffix,key,)
          self.cursor.execute("DELETE FROM project_keys "+
                              "WHERE notebook=? AND project=? and project_key=?;",
                              value_tuple)
          self.connection.commit()

     def delete_all_keys_DB (self,project=None):

          keys_temp = self.get_keys_DB(project=project)
          for key_temp in keys_temp:
               self.delete_key_DB(project=project,
                                  key=key_temp)


     def delete_all_indexes_DB (self,project=None):
          
          indexes_temp = self.get_indexes_DB(project=project)
          for ind_temp in indexes_temp:
               self.delete_index_DB(project=project,
                                    index=ind_temp)



     def delete_date_DB (self,project=None,date=None):

          value_tuple = (self.notebookname, project+self.project_suffix,date,)
          self.cursor.execute("DELETE FROM project_dates "+
                              "WHERE notebook=? AND project=? and project_date=?;",
                              value_tuple)
          self.connection.commit()
     

     def get_indexes_DB (self,project=None):

          self.cursor.execute("SELECT project_index FROM project_indexes "
                              +"WHERE notebook=? AND project=?",
                              (self.notebookname,project+self.project_suffix,))
          return [x[0] for x in self.cursor.fetchall()]

     def get_keys_DB (self,project=None):

          self.cursor.execute("SELECT project_key FROM project_keys "
                              +"WHERE notebook=? AND project=?",
                              (self.notebookname,project+self.project_suffix,))
          return [x[0] for x in self.cursor.fetchall()]

     def get_dates_DB (self,project=None):

          self.cursor.execute("SELECT project_date FROM project_dates "
                              +"WHERE notebook=? AND project=?",
                              (self.notebookname,project+self.project_suffix,))
          return [x[0] for x in self.cursor.fetchall()]

     def get_simple_DB (self,project=None,value=None):
          values=['lastup','uptohere','mainterm','series_enter','opened']

          self.cursor.execute("SELECT lastup, uptohere, mainterm, series_enter, opened"
                              +" FROM simple_properties "
                              +"WHERE notebook=? AND project=?",
                              (self.notebookname,project+self.project_suffix,))
          result_temp = self.cursor.fetchone()
          if not value:
               return result_temp
          elif value in values:
               return result_temp[values.index(value)]
          else:
               return ''

     def add_key_DB (self,project=None,key=None):

          value_tuple = (self.notebookname, project+self.project_suffix,key,)
          self.cursor.execute("INSERT OR REPLACE INTO project_keys "
                              +"(notebook, project, project_key) VALUES (?,?,?);",
                              value_tuple)
          self.connection.commit()

     def add_date_DB (self,project=None,date=None):

          value_tuple = (self.notebookname, project+self.project_suffix,date,)
          self.cursor.execute("INSERT OR REPLACE INTO project_dates (notebook, project, project_date) VALUES (?,?,?);",value_tuple)
          self.connection.commit()
          
     def add_simple_DB (self,
                        lastup=None,
                        uptohere=None,
                        mainterm=None,
                        series_enter=None,
                        opened=None,
                        project=None):

          
          if not type(lastup)==type(None) \
             and not type(uptohere)==type(None) \
             and not type(mainterm)==type(None) \
             and not type(series_enter)==type(None) \
             and not type(opened)==type(None):

               lastup = str(lastup)
               uptohere = str(uptohere)
               
               if opened:
                    opened = 'TRUE'
               else:
                    opened = 'FALSE'
               
               value_tuple =(self.notebookname,
                       project+self.project_suffix,
                       lastup,
                       uptohere,
                       mainterm,
                       series_enter,
                       opened,)
               self.cursor.execute("INSERT OR REPLACE INTO simple_properties "
                                   +"(notebook, project, lastup, uptohere, "
                                   +"mainterm, series_enter, opened) VALUES (?,?,?,?,?,?,?);",
                                   value_tuple)
               self.connection.commit()
               self.cursor.execute("SELECT * FROM simple_properties")



          else:


               if not type(lastup)==type(None):
                    lastup = str(lastup)
                    value_tuple = (lastup, self.notebookname, project,)
                    self.cursor.execute("UPDATE simple_properties "+
                                        "SET lastup=? WHERE notebook=? and project=?;",value_tuple)
               if not type(uptohere)==type(None):
                    uptohere = str(uptohere)
                    value_tuple = (uptohere, self.notebookname, project,)
                    self.cursor.execute("UPDATE simple_properties "+
                                        "SET uptohere=? WHERE notebook=? and project=?;",value_tuple)

               if not type(mainterm)==type(None):
                    value_tuple = (mainterm, self.notebookname, project,)
                    self.cursor.execute("UPDATE simple_properties "+
                                        "SET mainterm=? WHERE notebook=? and project=?;",value_tuple)

               if not type(series_enter)==type(None):
                    value_tuple = (series_enter, self.notebookname, project,)
                    self.cursor.execute("UPDATE simple_properties "+
                                        "SET series_enter=? WHERE notebook=? and project=?;",value_tuple)
               if not type(opened)==type(None):
                                   
                    if opened:
                         opened = 'TRUE'
                    else:
                         opened = 'FALSE'
                    value_tuple = (opened, self.notebookname, project,)
                    self.cursor.execute("UPDATE simple_properties "+
                                        "SET opened=? WHERE notebook=? and project=?;",value_tuple)

               self.connection.commit()
               

     # connection management

     def restore_connection (self,
                         connection=None,
                         cursor=None):

        self.cursor = cursor
        self.connection = connection

     def purge_connection (self):
        
        self.cursor = None
        self.connection = None

     # primary methods
     

     def import_string (self,string):
          
          try:
               self.projects = transform(eval(projecttext))
               if self.projects:
                    return True
               else:
                    return False
          except:
               return False

     def return_dict (self):

          if self.using_database:

               project_temp = {}
               for proj in self.get_projects_DB():
                    project_temp[proj] = self.get_project(project=proj)
               return project_temp
          
          if self.projects:

               return self.projects

     def is_empty (self):

          return self.projects=={}
     def clear (self):

          if self.using_database:
               self.cursor.execute("DELETE FROM project_names "+
                                   "WHERE notebook=?;",
                                   (self.notebookname,))
               self.connection.commit()
 
          self.projects = {}
          self.current = None

     def get_all_projects (self):

          if self.using_database:

               return self.get_projects_DB()

          return self.projects.keys()
     

     def get_new_project_name (self,project_name):

          """ to determine in a new project name is the entered name
          is already in use"""

          while project_name in self.projects:

                if project_name.isalpha():
                    project_name  += '1'
                else:
                    suffix = '0'
                    for counter, a in enumerate(project_name):
                        # find the numerical part 
                        if a.isnumeric() and suffix == '0':
                            suffix = project_name[counter:]

  
                    suffix = str(int(suffix)+1) 
                    project_name = project_name[0:counter]+suffix
                    
          return project_name 

     def initiate_project (self,
                           project_name=None,
                           defaultkeys=None,
                           indexes=None,
                           lastup=None,
                           uptohere=None,
                           mainterm=None,
                           series_enter=None,
                           date=None,
                           opened=True):

          if project_name not in self.projects:
               self.projects[project_name] = {}
               self.projects[project_name]['defaultkeys'] = defaultkeys
               self.projects[project_name]['position'] = (lastup,uptohere)
               self.projects[project_name]['going'] = (mainterm,series_enter)
               self.projects[project_name]['date'] = [str(date)]
               self.projects[project_name]['indexes'] = indexes
               self.projects[project_name]['status'] = {'started':str(date),
                                                        'open':opened,
                                                        'lastmodified':[]}
          self.set_current_project(project_name)
          if self.using_database:
               if opened:
                    opened='TRUE'
               else:
                    opened='FALSE'
               self.add_new_project_DB(project=project_name)
               self.add_simple_DB(project=project_name,
                                  lastup=lastup,
                                  uptohere=uptohere,
                                  mainterm=mainterm,
                                  series_enter=series_enter,
                                  opened=opened)
               for key in defaultkeys:
                    self.add_key_DB(project=project_name,
                                    key=key)
               self.add_date_DB(project=project_name,
                                date=str(date))
               self.set_indexes(project=project_name,
                                indexes=indexes)
               

     def clear_indexes (self,
                        project=None,
                        db_only=False):

          if not project:
               project=self.current
          if not db_only and not self.db_only :
               self.projects[project]['indexes'] = OrderedList()

          if self.using_database:
               
               self.delete_all_indexes_DB(project=project)
 
     def get_project (self,
                      project=None):

          if not project:
               project=self.current

          if self.using_database:

               temp_keys = self.get_keys_DB(project=project)
               temp_indexes = sorted(self.get_indexes_DB(project=project),key=lambda x_temp:Index(x_temp))
               temp_dates = sorted(self.get_dates_DB(project=project))
               temp_simple = self.get_simple_DB(project=project)

               
               

               lastup, uptohere, mainterm, series_enter, opened = temp_simple[0], temp_simple[1], temp_simple[2], temp_simple[3], temp_simple[4]

               temp_dict = {}
               temp_dict['defaultkeys'] = temp_keys
               temp_dict['position'] = (lastup,uptohere)
               temp_dict['going'] = (mainterm,series_enter)
               temp_dict['date'] = temp_dates
               temp_dict['indexes'] = OrderedList(temp_indexes)
               temp_dict['status'] = {'started':temp_dates[0],
                                      'open':opened,
                                      'lastmodified':temp_dates}
               return temp_dict 

          if project in self.projects:
               return self.projects[project]

     def set_project (self,
                      project=None,
                      project_dict=None,
                      db_only=False):

          if not project:
               project=self.current
          if project_dict and not db_only:
               self.projects[project] = project_dict

          if project_dict and self.using_database:

               dk_temp = project_dict['defaultkeys']
               indexes_temp = project_dict['indexes']
               position_temp = project_dict['position']
               lastup, uptohere =position_temp[0], position_temp[1]            
               going_temp = project_dict['going']
               mainterm, series_enter = going_temp[0], going_temp[1]
               
               date_temp = project_dict['date']
          
               self.add_new_project_DB(project=project)
               
               self.initiate_project (project_name=project,
                                      defaultkeys=dk_temp,
                                      indexes=indexes_temp,
                                      lastup=lastup,
                                      uptohere=uptohere,
                                      mainterm=mainterm,
                                      series_enter=series_enter,
                                      date=date_temp,
                                      opened=False)                  
         
               
       
          

     def set_indexes (self,
                      project=None,
                      indexes=None,
                      db_only=False):

          if not project:
               project=self.current
               
          if indexes and not db_only:

               self.projects[project]['indexes'] = indexes

          if self.using_database:
               self.clear_indexes(project=project,
                                  db_only=True)
               for index_temp in indexes.list:
                    self.add_index_DB(project=project,
                                      index=index_temp)
          
          
     def delete_project (self,
                         project_name=None,
                         db_only=False):

          if project_name  in self.projects:
               if not db_only and not self.db_only :
                    del self.projects[project_name]

               if self.using_database:
                    self.delete_project_DB(project=project_name)

                    

     def set_default_keys (self,
                           new_defaultkeys,
                           project=None,
                           db_only=False):
          if not project:
               project=self.current

          if isinstance(new_defaultkeys,list):
               if not db_only and not self.db_only :
                    self.projects[project]['defaultkeys'] = new_defaultkeys

               if self.using_database:
                    self.delete_all_keys_DB(project=project)
                    for key_temp in new_defaultkeys:
                         self.add_key_DB(project=project,
                                         key=key_temp)

     def get_default_keys (self,
                           project=None):

          if self.using_database:

               return list(self.get_keys_DB(project=project))
          
          if not project:
               project=self.current
          return self.projects[project]['defaultkeys']
          
     
     def add_default_keys (self,
                           new_defaultkeys=None,
                           project=None,
                           db_only=False):

          if not project:
               project=self.current

          if not isinstance(new_defaultkeys,(set,list)):
               new_defaultkeys = [new_defaultkeys]
          for k_temp in new_defaultkeys:
               if not db_only and not self.db_only :
                    self.projects[project]['defaultkeys'].append(str(k_temp))

          if self.using_database:
               for k_temp in new_defaultkeys:
                    self.add_key_DB(project=project,
                                    key=k_temp)
          
     
     def add_date (self,
                   new_date=None,
                   project=None,
                   db_only=False):

          if not project:
               project=self.current

          if not db_only and not self.db_only :

               self.projects[project]['date'].append(str(new_date))

          if self.using_database:
               self.add_date_DB(project=project,
                                date=str(new_date))
              

     def set_position (self,
                       lastup=None,
                       uptohere=None,
                       project=None,
                       db_only=False):
          
          if not project:
               project=self.current
          if not db_only and not self.db_only :
               self.projects[project]['position'] = (lastup,
                                                         uptohere)
          if self.using_database:
               
               self.add_simple_DB(project=project,
                                  uptohere=uptohere,
                                  lastup=lastup)
          
               

     def set_going (self,
                    mainterm=None,
                    series_enter=None,
                    project=None,
                    db_only=False):

          if not project:
               project=self.current

          if not db_only and not self.db_only :
               self.projects[project]['going'] = (mainterm,
                                                  series_enter)
          if self.using_database:
               self.add_simple_DB(project=project,
                                  mainterm=mainterm,
                                  series_enter=series_enter)
     

     def set_status_open (self,
                          status=None,
                          project=None,
                          db_only=False):
          if not project:
               project=self.current

          if not db_only and not self.db_only :     
               if status:
                    self.projects[project]['status']['open'] = True
               else:
                    self.projects[project]['status']['open'] = False
               
          if self.using_database:
               self.add_simple_DB(project=project,
                                  opened=status)

     def set_current_project (self,
                              project_name,
                              project=None):
          if not project:
               project=self.current
               
          if project_name is self.projects:
               self.current = project_name
               return project_name
          else:
               return False

     def add_last_modified (self,
                            date=None,
                            project=None,
                            db_only=False):
          if not project:
               project=self.current

          if not db_only and not self.db_only :
               
               self.projects[project]['status']['lastmodified'].append(str(date))

     def reset_indexes (self,
                        indexes=None,
                        project=None,
                        db_only=False):


          if not project:
               project=self.current
          if not db_only and not self.db_only :
               if not indexes:
                    self.projects[project]['indexes'] = OrderedList()
               elif isinstance(indexes,list):
                    self.projects[project]['indexes'] = OrderedList(sorted(indexes,
                                                                               key=lambda x_temp:Index(x_temp)))
          if self.using_database:
               self.delete_all_indexes_DB(project=project)
               for temp_index in sorted(indexes,
                                   key=lambda x_temp:Index(x_temp)):
                    self.add_index_DB(project=project,
                                      index=temp_index)                                    

     def add_index (self,
                    index,
                    project=None,
                    db_only=False):
          
          if not project:
               project=self.current
          if not db_only and not self.db_only :
               self.projects[project]['indexes'].add(index)

          if self.using_database:
               self.add_index_DB(project=project,
                                 index=index)

     def delete_index (self,
                       index,
                       project=None,
                       db_only=False):
          
          if not project:
               project=self.current
          if not db_only and not self.db_only :
               self.projects[project]['indexes'].delete(index)
          if self.using_database:
               self.delete_index_DB(project=project,
                                    index=index)

     def set_status (self,
                     project=None,
                     status=None):
          if not project:
               project=self.current
          if project in self.projects and status:

               self.projects[project]['status'] = status


     def get_all_indexes (self,
                          project=None):


          if self.using_database:

               temp_indexes = self.get_indexes_DB(project=project)
               return sorted(temp_indexes,
                             key=lambda x_temp:Index(x_temp))

          if not project:
               project=self.current
          return self.projects[project]['indexes'].list


     def get_position (self,
                       project=None):


          if self.using_database:
               lastup=self.get_simple_DB(project=project,
                                         value='lastup')
               uptohere=self.get_simple_DB(project=project,
                                           value='uptohere')
               return (lastup,uptohere)

          if not project:
               project=self.current
          return self.projects[project]['position']

          

     def get_date (self,
                   project=None):

          if self.using_database:
               dates_temp = self.get_dates_DB(project=project)
               return sorted(dates_temp)
          
          
          if not project:
               project=self.current

          return self.projects[project]['date']
          

     def get_going (self,
                    project=None):

          if self.using_database:
               mainterm=self.get_simple_DB(project=project,
                                         value='mainterm')
               series_enter=self.get_simple_DB(project=project,
                                           value='series_enter')
               return (mainterm,series_enter)

          if not project:
               project=self.current
          return self.projects[project]['going']

     def get_date_list (self,
                        project=None):

          if self.using_database:
               dates_temp = self.get_dates_DB(project=project)
               return sorted(dates_temp)
          

          if not project:
               project=self.current
          return self.projects[project]['date']

     def get_status_open (self,
                          project=None):

          if self.using_database:

               opened = self.get_simple_DB(project=project,
                                           value='opened')
               return opened=='TRUE'
     

          if not project:
               project=self.current
          return self.projects[project]['status']['open']


     def get_status_started (self,
                             project=None):

          if self.using_database:
               dates_temp = self.get_dates_DB(project=project)
               return sorted(dates_temp)[0]
         

          if not project:
               project=self.current
          return self.projects[project]['status']['started']

     def get_status_modified (self,
                              project=None):

          if self.using_database:
               dates_temp = self.get_dates_DB(project=project)
               return sorted(dates_temp)

          if not project:
               project=self.current
          return self.projects[project]['status']['lastmodified']



     # for transfering from dictionary to database

     def load_project_into_DB (self,
                               project=None,
                               all_projects=None):

          try:
               defaultkeys = all_projects[project]['defaultkeys']
          except:
               print(project,':','defaultkeys FAILED')
               defaultkeys = []
          try:
               indexes = all_projects[project]['indexes']
          except:
               print(project,':','index FAILED')
               indexes = OrderedList()
          try:
          
               lastup = all_projects[project]['position'][0]
          except:
               print(project,':','lastup FAILED')
               lastup = Index(2)
               
          try:     
               uptohere = uptohere=all_projects[project]['position'][1]
          except:
               print(project,':','uptohere FAILED')
               uptohere = Index(2)
          try:
               mainterm = mainterm=all_projects[project]['going'][0]
          except:
               print(project,':','mainterm FAILED')
               mainterm = 'quit'

          try:
               
               series_enter = series_enter=all_projects[project]['going'][1]
          except:
               print(project,':','series enter FAILED')
               series_enter = ''
          try:
               date= all_projects[project]['date']
          except:
               date = [str(str(datetime.datetime.now()))]

          self.initiate_project (project_name=project,
                                 defaultkeys=defaultkeys,
                                 lastup=lastup,
                                 indexes=indexes,
                                 uptohere=uptohere,
                                 mainterm=mainterm,
                                 series_enter=series_enter,
                                 date=date,
                                 opened=False)
          
               
              

     def clear_database (self):

          for proj in self.get_projects_DB():
               self.delete_project_DB(project=proj)

     def load_into_database (self,
                             all_projects=None):

          if not isinstance(all_projects,dict):
               all_projects = self.projects

          for proj_temp in all_projects:
               
               self.load_project_into_DB(project=proj_temp,
                                         all_projects=all_projects)
               
               

     

     
          

     
          

          

          

     

     
               

          

          
