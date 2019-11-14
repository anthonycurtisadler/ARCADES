from coordlinkedlist import CoordLinkedList
import random

def surrounding (c):
     if not isinstance(c,(tuple,list,set)):
          c=tuple(c)
     returnlist = []
     for x_inc in (-1,0,1):
          for y_inc in (-1,0,1):
               if (abs(x_inc) + abs(y_inc)) == 1:
                    returnlist.append((c[0]+y_inc,c[1]+x_inc))
     return returnlist

class LoopFinder:

     def __init__ (self,function=surrounding,elements=None):

           self.function = function
           self.elements = elements
           self.all_nodes = {}

           for e in self.elements:

                self.all_nodes[e] = CoordLinkedList(node=e)
                self.all_nodes[e].receive([x for x in self.function(e) if x in self.elements])
               
     
     def find_cycle (self,node=None):

          starting_node = node
          seed_nodes = set(self.all_nodes[node].send())
          if not seed_nodes:
               return {node}


          done_nodes = seed_nodes
          counter = 0

          while True:
               
               seed_nodes_copy = set(seed_nodes)
               counter += 1
               for s_n in list(seed_nodes):
                    new_nodes = set(self.all_nodes[s_n].send())                    
                    for n_n in new_nodes-set(done_nodes):
                              done_nodes.add(n_n)
                              seed_nodes.update(set(self.all_nodes[n_n].send()))

               if not len(seed_nodes_copy) < len(seed_nodes):
                    break

          return sorted(done_nodes)

     def find_all_loops (self):

          done_nodes = set()
          self.cycles = {}
          counter = 0
          for n in self.all_nodes:
               if n not in done_nodes:
                    found_nodes = self.find_cycle(n)
                    done_nodes.update(found_nodes)
                    self.cycles[counter] = found_nodes
                    counter+=1
          return self.cycles
          
                    
               

               

          
if __name__ == '__main__':


     while input('?') == '':
          


          elements = []
          for k in range(10):
               x = random.choice(range(0,200))
               y = random.choice(range(0,200))
               for i in range(5):
                    elements.append((y,x))
                    c = surrounding([y,x])
                    c = random.choice(c)
                    y,x = c[0], c[1]

     ##          elements = []
     ##          for i in range(300):
     ##               x = random.choice(range(0,60))
     ##               y = random.choice(range(0,60))
     ##               
     ##               elements.append((y,x))

                    
          loopfinder = LoopFinder(function=surrounding,elements=elements)

          x = loopfinder.find_all_loops()
          counter=0
          for y in x:
               print(counter)
               print(','.join([str(zz) for zz in sorted([z for z in x[y]])]))
               print()
               counter+=1
               
                    


     

          



                    
                              
                              
                                  

                    
                    

          

          
