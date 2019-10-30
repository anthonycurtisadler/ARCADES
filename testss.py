import random
from math import sin,cos


starting = True
new_direction = False
x_coord = y_coord = 15
y_total = x_total = 2000
y_max = x_max = 200

float_y = float(y_coord) 
float_x = float(x_coord) 
key_pressed = -1
while key_pressed == -1:
     if starting:
          direction = random.choice(range(360))
          going_for = 0
          starting = False
     going_for += 1
     if float_y  < 10:
          float_y  = 10.0
          new_direction = True                                  
     elif float_y  > y_total - y_max -10:
         float_y  = float(y_total - y_max - 10)
         new_direction = True 
     if float_x < 10:
          float_x = 10.0
          new_direction = True                                       
     elif float_x > float_x - x_max - 10:
          float_x = float(x_total - x_max - 10)
          new_direction = True
     if new_direction:
          direction = random.choice(range(360))
          new_direction = False

     float_y += sin(direction) 
     float_x += cos(direction)
     print('direction',direction)
     print('sin',sin(direction))
     print('cos',cos(direction))
     print('fy',float_y)
     print('fx',float_x)

     if abs(y_coord-int(float_y)) + abs(x_coord-int(float_x)) >= 1:
            y_coord = int(float_y)
            x_coord = int(float_x)
     print(y_coord,x_coord)
     input('?')
