
## Expanded version of the  knowledgebase
##

import shelve
from globalconstants import SLASH
from printcomplexobject import print_complex_object 

def listprint(x):
     returntext = ''
     for item in x:
          returntext+=str(item) + '\n'
     return returntext

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

class GeneralizedKnowledge:

     def __init__ (self,find_paths=False,directoryname=None,filename=None):

          if (directoryname and filename):

               self.shelf = {}

               self.shelf['knowledge'] = None
               self.shelf['relations'] = None 
               self.shelf['converses'] = None

               try:
                    flag = 'w'
                              
                    self.shelf['knowledge'] = shelve.open(directoryname+SLASH+filename +'GKK',flag)
                    self.shelf['relations'] = shelve.open(directoryname+SLASH+filename +'GKR',flag)
                    self.shelf['converses'] = shelve.open(directoryname+SLASH+filename +'GKC',flag)
                    print(flag)
                    print(self.shelf['knowledge'])

               except:

                    flag = 'c'
                    
                    self.shelf['knowledge'] = shelve.open(directoryname+SLASH+filename +'GKK',flag)
                    self.shelf['relations'] = shelve.open(directoryname+SLASH+filename +'GKR',flag)
                    self.shelf['converses'] = shelve.open(directoryname+SLASH+filename +'GKC',flag)
                    print(flag)
                    print(self.shelf['knowledge'])

               

               
               self.knowledge = self.shelf['knowledge']
               self.relations = self.shelf['relations']
               self.converses = self.shelf['converses']

               self.is_shelf = True
               
               
          else:    
               
               self.knowledge = {}
               self.relations = {}
               self.converses = {}
               self.is_shelf = False
          
          self.find_paths = find_paths

     def clear (self):

          def empty_shelf(shelfobject):

               for key in list(shelfobject.keys()):
                    del shelfobject[key]

          if input('DO YOU REALLY WANT TO CLEAR THE ENTIRE KNOWLEDGE SHELF?? Type "yes" to continue!') == 'yes':
               empty_shelf(self.knowledge)
               empty_shelf(self.relations)
               empty_shelf(self.converses)

          print('DELETED')

     def node_exists (self,node):

          return node in self.knowledge
     
     def relation_exists (self,relation):

          return relation in self.relations

     def restart (self,directoryname=None,filename=None):

          if self.is_shelf and directoryname and filename:

               
               flag = 'w'
                         
               self.shelf['knowledge'] = shelve.open(directoryname+SLASH+filename +'GKK',flag)
               self.shelf['relations'] = shelve.open(directoryname+SLASH+filename +'GKR',flag)
               self.shelf['converses'] = shelve.open(directoryname+SLASH+filename +'GKC',flag)
               print('REOPENING '+ directoryname+SLASH+filename +'GK')


     def add_relation (self,relation,typeof=0,converse=None):

          """ 0 for DIRECTED
          1 for non-DIRECTED
          2 for attribute
          3 for reciprocal
          4 for complex"""

          if not typeof in (0,1,2,3,4) or relation in self.relations:
               return False
          
          else:
               if typeof in (0,1,2):
                    self.relations[relation] = typeof
               elif typeof==3:
                    if converse not in self.relations:
                         self.relations[relation] = typeof
                         self.relations[converse] = typeof
                         self.converses[relation] = converse
                         self.converses[converse] = relation
               else:
                    self.relations[relation] = typeof
                    self.converses[relation] = converse
                         
               

     def delete_relation (self,relation):

          if relation in self.relations:
               del self.relations[relation]
          if relation in self.converses:
               con_relation = self.converses[relation]
               if con_relation in self.converses:
                    del self.converses[relation]
                    del self.converses[con_relation]
                    if con_relation in self.relations:
                         del self.relations[con_relation]

     def show_relations (self,typeof=None):
          
          returnlist = []
          for relation in self.relations:

               if typeof is None or self.relations[relation] == typeof:
                    returnlist.append(relation + ' = ' + {0:'DIRECTED',
                                                          1:'NONDIRECTED',
                                                          2:'ATTRIBUTE',
                                                          3:'RECIPROCAL',
                                                          4:'COMPLEX'}[self.relations[relation]])
          return returnlist
     
     def add_attribute (self,node,relation,content):

          if node in self.knowledge and relation.strip() and content.strip():
               if relation not in self.knowledge[node]:
                    self.knowledge[node][relation] = [content]
                    return True
               else:
                    x = self.knowledge[node][relation]
                    x.append(content)
                    self.knowledge[node][relation] = x
                    return True
          return False

     def delete_attribute (self,node,relation,content):

          if node in self.knowledge and relation.strip() and content.strip():
               if relation in self.knowledge[node]:
                    x = self.knowledge[node][relation]
                    x.pop(x.index(content))
                    self.knowledge[node][relation] = x
                    

     def add_definition (self,node,content):

          if 'DEFINITION' not in self.relations:
               self.add_relation(relation='DEFINITION',typeof=2)
          self.add_attribute(node=node,relation='DEFINITION',content=content)
          

     def add_node (self,node):

          if node not in self.knowledge:

               self.knowledge[node] = {}

     def delete_node (self, node):

          if node in self.knowledge:

               del self.knowledge[node]

          for n_temp in self.knowledge:

               for relation in list(self.knowledge[n_temp].keys()):

                    if node in self.knowledge[n_temp][relation]:
                         self.delete_directed_edge (relation,n_temp,node)

     def add_directed_edge (self,relation,nodefrom,nodeto):

          if nodefrom in self.knowledge and nodeto in self.knowledge:

               if relation in self.knowledge[nodefrom]:
                    x = self.knowledge[nodefrom][relation]

                    x.add(nodeto)

                    self.knowledge[nodefrom][relation] = x

                    
               else:
                    x = self.knowledge[nodefrom]
                    x[relation] = {nodeto}
                    self.knowledge[nodefrom] = x

     def add_edge (self,relation,nodeone,nodetwo):

          self.add_directed_edge (relation,nodeone,nodetwo)
          self.add_directed_edge (relation,nodetwo,nodeone)

     def delete_directed_edge (self,relation,nodefrom,nodeto):

          if nodefrom in self.knowledge:

               if relation in self.knowledge[nodefrom]:
                    if nodeto in self.knowledge[nodefrom][relation]:

                         self.knowledge[nodefrom][relation].remove(nodeto)
                         
                         if not self.knowledge[nodefrom][relation]:
                              del self.knowledge[nodefrom][relation]
                         return True
          return False

     def delete_edge (self,relation,nodeone,nodetwo):
     
          if self.delete_directed_edge (relation,nodeone,nodetwo) and self.delete_directed_edge (relation,nodetwo,nodeone):
               return True

     def find_nodes_with_attributes (self,relation,content,findin=True):

          
          if relation not in self.relations:
               return set()
          returnset = set()

          for node in self.knowledge:

               if relation in self.knowledge[node]:

                    if not findin:

                         if content  in self.knowledge[node][relation]:

                              returnset.add(node)
                    else:

                         for phrase in self.knowledge[node][relation]:
                              if content in phrase:
                                   returnset.add(node)
          return returnset 

     def find_nodes (self,relation,nodeset=None,resultlist=None,pathlist=None,searched_nodes=None):

          last_paths = []
          if resultlist == None:
               resultlist = []

          if searched_nodes == None:
               searched_nodes = set()

          if pathlist == None and self.find_paths:
               pathlist == []
               
          found_nodes = set()
          new_paths = [] 
          for node in nodeset:
               if pathlist:
                    last_paths = [path[0:path.index(node)+1] for path in pathlist if path and node in path]

               if node not in self.knowledge or relation not in self.knowledge[node]:
                    pass
               else:
                    found_nodes.update(self.knowledge[node][relation])
                    searched_nodes.add(node)
                    for related_node  in  self.knowledge[node][relation]:
                         resultlist.append(str(related_node)+' is the '+str(relation)+' of ' + str(node))
                         if last_paths:
                              for path in last_paths:
                                   path_to_add = path+[related_node]
                                   
                                   new_paths.append(path_to_add)
          if pathlist:
               for path in new_paths:
                    if path not in pathlist:
                         pathlist.append(path)
         
          return found_nodes

     def unpack_complex_relation (self,enterstring):

          def unpack(enterstring):

               last = enterstring.count('>')

               while True:
                    for r in enterstring.split('>'):

                         if r in self.relations:
                              if self.relations[r] == 4:
                                   if r in self.converses:
                                        enterstring = enterstring.replace(r,self.converses[r])
                    if enterstring.count('>') == last:
                         break
                    last = enterstring.count('>')
               return enterstring 

          returnlist = []
          for seg in enterstring.split(','):
               returnlist += reversed(unpack(seg).split('>'))

          return returnlist 
                               

     def find_all_relations (self,relation,node):

          many = False 

          if not isinstance(relation,list):
               relations = [relation]
          else:
               relations = relation
               many = True
          results = []


          

          last_nodes = set()

          last_found_nodes = set() #for the nodes found with the last relation
                                   # and hence the results of the search
          
          starting_nodes = set()

          for count, relation in enumerate(relations):
                    


               find_all = True
               if (not many and '/' not in relation) or relation.endswith('*'):
                    if relation.endswith('*'):
                         relation = relation[0:-1]
                    find_all = True
                    how_many = 1000
               elif '/' in relation:
                    try:
                         how_many = int(relation.split('/')[1])
                         find_all = False
                    except:

                         how_many = 1
               else:
                    how_many = 1
                    find_all = False


          
               searched_nodes = set()

               while True:
                    if not starting_nodes:
                         starting_nodes = self.find_nodes (relations[0].split('/')[0].split('*')[0],{node},results)
                         temp_result = starting_nodes
                         found_nodes = set(starting_nodes)
                         paths = [[node,result] for result in starting_nodes]
                         if not starting_nodes:
                              return [],[],[]

                         
                    else:
                         temp_result = self.find_nodes (relation,found_nodes-searched_nodes,resultlist=results,pathlist=paths,searched_nodes=searched_nodes)
                         found_nodes.update(temp_result)
                    if count == len(relations)-1:
                         last_found_nodes.update(temp_result)

                    how_many -=1
                    if not found_nodes > last_nodes or (not find_all and how_many<1):
                         break
                    last_nodes = set(found_nodes)


          return last_found_nodes,results,paths

     def dump (self):

          def wrap(x):
               return '{{' + x + '}}'
               

          nodelist = []
          knowledgelist = []
          relationlist = []

          for key in self.knowledge:

               nodelist.append(wrap(key))
               for relation in self.knowledge[key]:

                    other_nodes = self.knowledge[key][relation]
                    knowledgelist.append(wrap(key+':'+relation+';'+','.join(other_nodes)))
          for key in self.relations:
               complement = ''

               relation_type = {0:'DIRECTED',
                                1:'NONDIRECTED',
                                2:'ATTRIBUTE',
                                3:'RECIPROCAL',
                                4:'COMPLEX'}[self.relations[key]]

               if self.relations[key] in (3,4) and key in self.converses:

                    complement = ';'+self.converses[key]

               relationlist.append(wrap(key+':'+relation_type+complement))

          return '\n'.join(nodelist)+'\n'+'\n'.join(relationlist)+'\n'+'\n'.join(knowledgelist)
               

     def text_interpret (self,command):

          ## "are nodes"
          ## "is a RELATION of"
          ## " and "
          ## " is a directed relation"
          ## " is a nondirected relation"
          ## " is a reciprocal relation with"

          def reduce_blanks (command):
               while '  ' in command:
                    command = command.replace('  ',' ')
               return command

          if ':' in command:
               return(self.interpret(command,reverse_order=False))
               
          
          ARE_NODES = ' are nodes'
          IS_A_NODE = ' is a node'
          IS_A = ' is a '
          OF = ' of '
          AND = ' and '
          IS_A_DIRECTED_RELATION = ' is a directed relation'
          IS_A_NONDIRECTED_ELATION = ' is a nondirected relation'
          IS_A_RECIPROCAL_RELATION = ' is a reciprocal relation with'
          IS_A_COMPLEX_RELATION = ' is a complex relation meaning the'
          SHOW_NODES = 'Show nodes'
          SHOW_RELATIONS = 'Show relations'
          SHOW_ALL = 'Show everything'
          WHAT_ARE = 'Show '
          APOSTROPHE = "'s "
          APOSTROPHE2 = "'"
          IS_AN = ' is an '
          IS_A = ' is a '
          IS = ' is '
          IS_THE = ' is the '
          ARE_THE = ' are the '
          reverse_order = False


          table = {ARE_NODES:':;',
                   IS_A_NODE:':;',
                   IS_A_DIRECTED_RELATION:':DIRECTED',
                   IS_A_NONDIRECTED_ELATION:':NONDIRECTED;',
                   IS_A_RECIPROCAL_RELATION:':RECIPROCAL;',
                   IS_A_COMPLEX_RELATION:':COMPLEX;',
                   SHOW_NODES:'$',
                   SHOW_RELATIONS:'$$$',
                   SHOW_ALL:'$$$',
                   APOSTROPHE:':'}

          command = reduce_blanks(command)
          command = command.strip()

          
          if IS_AN in command:
               command = command.replace(IS_AN,IS_A)
          if (' is ' in command or ' are ' in command) and (' relation' not in command) and ('Show ' not in command) and ('nodes' not in command):
               reverse_order = True 
          for t in table:
               command = command.replace(t,table[t])
          if command.startswith('show'):
               command = 'Show' + command[4:]
          command = command.replace(WHAT_ARE,'$$')
          command = command.replace(IS_A,':')
          command = command.replace(OF,';')
          command = command.replace(OF,';')
          command = command.replace(APOSTROPHE2,':')
          command = command.replace(AND,',')
          command = command.replace(IS,';')
          command = command.replace(IS_THE,' is a ')
          command = command.replace(ARE_THE,' are a ')
          all_true = ' all ' in command
          command = command.replace(' all ',' ')

          command_beginning = command.split(':')[0]
          command_middle, command_end = '',''
          if ':' in command:
               command_middle = command.split(':')[1].split(';')[0]
               if ';' in command:
                    command_end = command.split(':')[1].split(';')[1]
          command_end = command_end.replace(' from ','>').replace(' from ','>')
          if 'self' in command_end or 'self' in command_end:
               command_end = command_beginning
          if all_true:
               command_middle_list = command_middle.split(',')
               new_command_list = []
               for cml in command_middle_list:
                    if cml.endswith('s') and cml[0:-1] in self.relations:
                         new_command_list.append(cml[0:-1]+'*')
                    else:
                         new_command_list.append(cml+'*')
               command_middle = ','.join(new_command_list)

          command = command_beginning + ':' + command_middle + ';' + command_end
               
           
          return(self.interpret(command,reverse_order=reverse_order))
          

     def interpret (self,command,reverse_order):

          """Accepts commands and interprets them to control the
          knowledgebase class.

          node1,node2,node3 ... (a list of nodes) = CREATES NEW NODES
          node:DEFINITION;DEFINITION_CONTENT1,DEFCONT2,DEFCONT2 = DEFINES A NODE
          relation:DIRECTED/NONDIRECTED/ATTRIBUTE = DEFINES A RELATION
          fromnode:relation;tonode1,tonode2,tonode3... = establishes a relation between fromnode and tonode

          $ = shows all the nodes 
          $node:; = shows all the relations of the node
          $$node:relation; =  finds all the related nodes for the given relation
          $$$ = shows all the relations
          
 
          """          

          def splitcommand(command,reverse_order=None):

               node = [x.strip() for x in command.split(':')[0].split(',')]
               relation = [x.strip() for x in command.split(':')[1].split(';')[0].split(',')]
               content_string = command.split(':')[1].split(';')[1]
               contents = [x.strip() for x in content_string.split(',')]
               
               if reverse_order:
                    node, contents = contents, node
               
                    
               return node,relation,contents

          returntext = ''
          header = ''
          
          if ':' not in command:
                    command += ':'
          if ';' not in command.split(':')[1]:
                    command += ';'     
          # THE SHOW COMMANDS

          if command.startswith('$$$$') or command.startswith('????'):

               header = 'ALL SHELVES'
               returntext += 'RELATIONS \n'
               returntext += print_complex_object(self.relations)
               returntext += '\n KNOWLEDGE \n'
               returntext += print_complex_object(self.knowledge)
               returntext += '\n CONVERSES \n'
               returntext += print_complex_object(self.converses)
               returntext += '\n'
               return header, returntext
          
          elif command.startswith('$$$') or command.startswith('???'):
               # to show all the defined relations
               header = 'ALL RELATIONS '

               returntext += listprint(self.show_relations())
               returntext += '\n'
               return header, returntext
          
          elif command.startswith('$$') or command.startswith('??'):
               
               # to show all the relatives of a node 

               nodes,all_relations,contents = splitcommand(command[2:],reverse_order)
               found_nodes = set()

               if nodes[0] in self.relations and self.relations[nodes[0]] == 2:
                    attribute_search = True
                    all_relations, contents = nodes,all_relations
               else:
                    attribute_search = False
                    

          

               for relation in all_relations:

                    if relation in self.relations and self.relations[relation]==2:

                         header = 'ATTRIBUTE'
                         if not attribute_search:
                              for node in nodes:

                                   returntext += '// \n'

                                   if node in self.knowledge and relation in self.knowledge[node]:
                                        returntext += node + ' is ' + ', '.join(self.knowledge[node][relation]) + '\n'
                         else:
                              for content in contents:
                                        found_nodes.update(self.find_nodes_with_attributes(relation,content))
               if attribute_search:

                    returntext += ','.join(sorted(found_nodes)) + '// \n'
                    
                                   
                                   

                              

 

               relation = self.unpack_complex_relation(','.join(all_relations))
               if not relation:
                    pass
                
               for node in nodes:
                    header = str(relation) + '(s) of '+node+ ''
                    results = self.find_all_relations(relation,node)
                    returntext += ','.join(results[0])
                    returntext += '// \n'
                    returntext += listprint(list(set(results[1])))
                    returntext += '\n'
                    listprint(results[2])
                    returntext += '\n'
               return header, returntext



          elif command.startswith('$') or command.startswith('?'):
               # to show the immediate relations of a node

               all_nodes,all_relations,contents = splitcommand(command[1:])
               for relation in all_relations:
                    for node in all_nodes:
                         header = 'IMMEDIATE RELATIONS of ' + node + ''
                         if not node:
                              returntext += ', '.join(sorted(list(self.knowledge))) + '\n'
                         elif not relation:
                              if node in self.knowledge:
                                   returntext += node + ': ' + '\n\n'

                                   for relation in self.knowledge[node]:
                                        returntext +='  ' + relation + '\n'
                                        
                                        for item in self.knowledge[node][relation]:
                                             returntext += '     ' + item + '\n'                   
                                   
                         elif node in self.knowledge and relation in self.knowledge[node]:

                         
                              returntext += ', '.join(sorted(list(self.knowledge[node][relation]))) + '\n'
               return header, returntext
          # THE ENTRY COMMANDS 
          else:
               if command.startswith('-'):
 
                    deleting = True
                    command = command[1:]
               else:
                    deleting = False
               
               all_nodes,all_relations,contents = splitcommand(command,reverse_order)



               if not all_relations:
                    all_relations = [None]
               for relation in all_relations:
                    for node in all_nodes:

                         if node:

                              if ((deleting and node in self.knowledge) or (not deleting and node not in self.knowledge)) and (relation not in ('DIRECTED','NONDIRECTED','ATTRIBUTE','RECIPROCAL','COMPLEX')):
                                   # To add a single node or nodes
                                   if not relation:

                                        main_function = self.add_node
                                        if deleting:
                                             main_function = self.delete_node
                                        header = 'NEW NODES'
                                        main_function(node)
                                        returntext += node + ', '

                              else:
                                   if relation == 'DEFINITION':
                                        # to define a node
                                        header = 'DEFINITION of ' + node 
                                        returntext += node + ':'
                                        for content in contents:
                                             self.add_definition(node,content)
                                             returntext += content + ', '
                                        returntext = returntext.rstrip(', ')
                                        returntext += '\n'

                                   
                                   else:
                                        if not deleting and node not in self.relations and relation in ('DIRECTED','NONDIRECTED','ATTRIBUTE','RECIPROCAL','COMPLEX'):
                                             # to define a definition
                                             header = 'NEW RELATION  '

                                             if not contents:
                                                  contents = ['none']
                                             for content in contents:
                                                  
                                                  if relation in ('DIRECTED','NONDIRECTED','ATTRIBUTE','RECIPROCAL','COMPLEX') \
                                                     and not ((relation in ('RECIPROCAL' or 'COMPLEX'))
                                                              and content == 'none'):
                                                       
                                                       self.add_relation(node,{'DIRECTED':0,
                                                                               'NONDIRECTED':1,
                                                                               'ATTRIBUTE':2,
                                                                               'RECIPROCAL':3,
                                                                               'COMPLEX':4}[relation],content)
                                                       if relation == 'RECIPROCAL':
                                                            returntext += node + ': ' + relation + '; reciprocal with '+content
                                                       else:
                                                            returntext += node + ': ' + relation
                                                       returntext += '\n'
                                                       
                                            
                                        elif deleting and node in self.relations:
                                             self.delete_relation(node)
                                             
                                        elif relation in self.relations:

                                             
                                             for content in contents:

                                                  if (len(contents)<2 and len(all_nodes)<2) or node!=content:

                                                       if deleting:

                                                            func_one = self.delete_directed_edge
                                                            func_two = self.delete_edge
                                                            func_three = self.delete_attribute

                                                       else:
                                                            func_one = self.add_directed_edge
                                                            func_two = self.add_edge
                                                            func_three = self.add_attribute 


                                                       header = 'NEW ATTRIBUTE  '
                                                       
                                                       if self.relations[relation] == 0:
                                                            func_one(relation,node,content)
                                                            returntext += node + ' - ' + relation + '\ ' + content + '\n'
                                                       elif self.relations[relation] == 1:
                                                            func_two(relation,node,content)
                                                            returntext += node + ' ' + relation + '-\ ' + content + '\n'
                                                       elif self.relations[relation] == 2:
                                                            func_three(node,relation,content)
                                                            returntext += node + ' =' + relation + '= ' + content  + '\n'
                                                       elif self.relations[relation] == 3:
                                                            func_one(relation,node,content)
                                                            func_one(self.converses[relation],content,node)
                                                            returntext += node + ' - ' + relation + '\ ' + content + '\n'
                                                            returntext += content + ' - ' + self.converses[relation] + '\ ' + node + '\n'
                                             
               return header, returntext.rstrip(', ').rstrip(',')
          return '',''

          
                                   
                                   

if __name__ == '__main__':


     b = GeneralizedKnowledge(find_paths=True)

     while True:
          x= input('?')
          print(listprint(b.text_interpret(x)))
 

          if not x:
               break

          if x=='?':
               while True:
                    
                    y = input('???')
                    if '/' in y:
                         print(b.find_nodes_with_attributes(y.split('/')[0],y.split('/')[1]))

                    if not y:
                         break
                    
                    
          
     
               
               

               
               
     
     
               
               

     
          

          
