import random
import copy

def xprint(x):
     pass
def dummy (x):

     return [x]

class LoopFinder:

     def __init__ (self,function = dummy):

          self.function = function
          self.element_dictionary = {}
          self.string_list = []

     def reduce_list(self,entrylist):


          for e in entrylist:
               if e:
                    end = e[-1]
                    adjacents = [x for x in self.function(end) if x in self.element_set and x not in e]
                    print('adj',adjacents)
                    for adjacent in adjacents:
                         for ee in entrylist:
                              if  ee and ee != e:
                                        if adjacent == ee[0]:
                                             e += list(ee)
                                             while ee:
                                                  ee.pop()
                                             break
                                        elif len(ee) > 1 and adjacent == ee[-1]:
                                                  e += list(reversed(ee))
                                                  while ee:
                                                       ee.pop()
                                                  break
          entrylist = [x for x in entrylist if x]
          return entrylist

     def find_all_loops (self,elements):
          self.element_set = elements 
          sequences = []
          for node in self.element_set:
               for x in [x for x in self.function(node) if x in self.element_set]:
                    sequences.append([node])
     

          

          while True:
               old_sequences = copy.deepcopy(sequences)
               sequences = self.reduce_list(sequences)

               if sequences == old_sequences:
                    break
          return sequences
     

          
               

               
                         
          
          


def surrounding (c):
     if not isinstance(c,(tuple,list,set)):
          print('x',c)
     returnlist = []
     for x_inc in (-1,0,1):
          for y_inc in (-1,0,1):
               if (abs(x_inc) + abs(y_inc)) == 1:
                    returnlist.append((c[0]+y_inc,c[1]+x_inc))
     return returnlist 
while input('?') == '':
     
     loopfinder = LoopFinder(function=surrounding)

     elements = []
     x = random.choice(range(0,70))
     y = random.choice(range(0,70))
     for i in range(100):
          elements.append((y,x))
          c = surrounding([y,x])
          c = random.choice(c)
          y,x = c[0], c[1]
     elements = tuple(elements)
          

     x = loopfinder.find_all_loops(elements)
     for y in x:
          print(y)
          print()
          



                    
                              
                              
                                  

                    
                    

          

          
