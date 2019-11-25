import random
import itertools


def random_d (a,b,c,d):

     if random.choice(range(12)) == 0:
          return False
     else:
          return True

class Movement:

     def __init__ (self,movementtype='r',attribute1=None,attribute2=range(100),attribute3=None,y_pos=0,x_pos=0,y_dim=0,x_dim=0):

          #movementtype = 'r' -- moves for random duration in a random direction
          #movementtype = 's' -- moves for a set distance in a sequence of directions

          self.movementtype = movementtype
          self.attribute1 = attribute1
          self.attribute2 = attribute2
          self.attribute3 = attribute3

          if self.movementtype == 'r':
               self.function = self.find_direction_rmode
          if self.movementtype == 's':
               self.function = self.find_direction_smode
          self.y_pos = y_pos
          self.x_pos = x_pos
          self.y_dim = y_dim
          self.x_dim = x_dim
          self.already = 0
          self.iterator = self.function()

          self.dir_table   = {0:(-1,-1),
                              1:(-1,0),
                              2:(-1,1),
                              3:(0,1),
                              4:(1,1),
                              5:(1,0),
                              6:(1,-1),
                              7:(0,-1)}
        
     def find_direction_smode (self):

          already = 0
          if self.attribute1 is None:
               self.attribute1 = 1
          direction_table = {1:[3,7,1,5]}
          directions = direction_table[self.attribute1]
          direction_iterator = itertools.cycle(list(directions))
          while True:

               
               
              

               if already % self.attribute2 == 0:
                    direction = next(direction_iterator)
                    print(direction)
                    
               self.y_pos += self.dir_table[direction][0]
               self.x_pos += self.dir_table[direction][1]
               already += 1

               yield self.y_pos,self.x_pos,self.dir_table[direction][0],self.dir_table[direction][1],already
               
          

          

     def find_direction_rmode (self,function=random_d):
          if self.attribute1 is None:
               self.attribute1 = range(8)
          if isinstance(self.attribute2,int):
               self.attribute2 = range(self.attribute2)
          already = 0
          

          direction = random.choice(self.attribute1)


          while True:
      

               if random.choice(self.attribute2)<already:
                         lastdirection = direction
                         direction = random.choice(list(set(self.attribute1)-{direction}))
                         already = 0 


               else:

                    already = already + 1


               last_direction = direction
               last_already = already


               if function(self.y_pos+self.dir_table[direction][0],
                           self.x_pos+self.dir_table[direction][1],
                           self.y_dim,
                           self.x_dim):
                    self.y_pos += self.dir_table[direction][0]
                    self.x_pos += self.dir_table[direction][1]
                    yield self.y_pos,self.x_pos,self.dir_table[direction][0],self.dir_table[direction][1], already
               elif function(self.y_pos+self.dir_table[last_direction][0],
                           self.x_pos+self.dir_table[last_direction][1],
                           self.y_dim,
                           self.x_dim):
                    self.y_pos += self.dir_table[last_direction][0]
                    self.x_pos += self.dir_table[last_direction][1]
                    direction = last_direction
                    last_already = already
                    yield self.y_pos,self.x_pos,self.dir_table[last_direction][0],self.dir_table[last_direction][1],already
               else:
                    yield self.y_pos,self.x_pos,0,0,already
               

     def move (self):

          return next(self.iterator)

          
                                                  

                                                   
          
          


##y_pos,x_pos, already = 0,0,0
##                                                   
##moving_object= Movement(attribute1=2,attribute2=1,movementtype='s')
##                                                   
##while not input('?'):
##     print (moving_object.move())
##     
##     

          
