import random


def random_d (a,b,c,d):

     if random.choice(range(12)) == 0:
          return False
     else:
          return True

def find_direction (y_pos=0,x_pos=0,y_dim=0,x_dim=0,already=0,function=random_d):

     direction = random.choice(range(8))

     
     dir_table   = {0:(-1,-1),
                    1:(-1,0),
                    2:(-1,1),
                    3:(0,1),
                    4:(1,1),
                    5:(1,0),
                    6:(1,-1),
                    7:(0,-1)}

     while True:
 

          if random.choice(range(2000))<already:
                    lastdirection = direction
                    direction = random.choice(list({0,1,2,3,4,5,6,7}-{direction}))
                    already = 0 


          else:

               already = already + 1


          last_direction = direction
          last_already = already 

          if function(y_pos+dir_table[direction][0],
                      x_pos+dir_table[direction][1],
                      y_dim,
                      x_dim):
               y_pos += dir_table[direction][0]
               x_pos += dir_table[direction][1]
               yield y_pos,x_pos,dir_table[direction][0],dir_table[direction][1], already
          elif function(y_pos+dir_table[last_direction][0],
                      x_pos+dir_table[last_direction][1],
                      y_dim,
                      x_dim):
               y_pos += dir_table[last_direction][0]
               x_pos += dir_table[last_direction][1]
               direction = last_direction
               last_already = already
               yield y_pos,x_pos,dir_table[last_direction][0],dir_table[last_direction][1],already
          else:
               yield y_pos,x_pos,0,0,already

          


y_pos,x_pos, already = 0,0,0
iterator_temp = find_direction()
##while not input('?'):
##     y_pos,x_pos,a,b,already= next(iterator_temp)
##     print(y_pos,x_pos,a,b,already)

     

          
