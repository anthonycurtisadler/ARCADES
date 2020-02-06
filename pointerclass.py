"""Module for the pointer class, which is
used to iterate over a list of indexes
pylint rated 9.62/10
Only problems involve use of variable for for loop
"""

from indexclass import Index
import random

class Pointer:

    """Class used to iterate over a list of indexes"""

    def __init__(self, entrylist):

        self.all = entrylist
        self.all_backup = list(entrylist)
        self.current = 0
        self.direction = 1 # 1 =forward, -1 = back
        self.speed = 1
        self.length = len(entrylist)
        self.level = 0 #if 0, then gets all children. Otherwise, only indexes with length=level
        self.random = False
        self.tilt = 0 # if 0, then change main level; if 1, then go to next; if 2, then go to child
        self.running_up = 0


    def defaults(self):

        """Shows default settings."""

        print('current', self.current)
        print('direction', self.direction)
        print('speed', self.speed)
        print('level', self.level)

    def first(self):

        return self.all[0]

    def last(self):

        return self.all[-1]


    def add(self, index, onlypositive=True):

        """Adds an index to list"""

        if isinstance(index, str):
            index = Index(index)
        if index >= Index(0) or not onlypositive:
            self.all.append(index)
            self.length = len(self.all)

    def delete(self, index):

        """Deletes an index from the list."""

        if isinstance(index, str):
            index = Index(index)
        if index in self.all:
            self.all.remove(index)
            self.length = len(self.all)
            


    def return_point(self):

        """Returns pointer location."""

        
        l_temp = self.length
        if l_temp == 0:
            l_temp = 1
        self.current = self.current % l_temp
        return self.all[self.current]


    def get(self):

        """Get next pointer location"""

        if self.level != 0:
            notfound = True
            while notfound:
                self.current += self.direction
                here = self.return_point()
                if here.level() <= self.level:
                    notfound = False
            return here

        self.current += self.direction
        here = self.return_point()
        return here



    def change_direction(self):

        """Changes direction of the pointer"""

        self.direction = self.direction*(-1)

    def move(self):

        """Advance forward according to the speed"""

        if not self.all:
            return Index(1)


        if not self.random:
            if self.tilt == 0:              
                for a_temp in range(self.speed):
                    here = self.get()

                return here
            here = self.return_point()

            was_here = here
            for x_temp in range(10):
                if self.direction == 1:
                    if self.tilt == 1:
                        here = here.next()
                    if self.tilt == 2:
                        here = here.child()
                elif self.direction == -1:
                    if self.tilt == 1:
                        here = here.previous()
                    if self.tilt == 2:
                        here = here.parent()
                if here in self.all:
                    self.current = self.all.index(here)

                    return here

            if self.running_up > 2:
                if self.tilt == 2:
                    self.tilt = 0
                if self.tilt == 1:
                    self.tilt = 2
                self.running_up = 0
            self.running_up +=1     
            return was_here
                    

        if not self.all:
            self.all = list(self.all_backup)

        random_point = random.randint(0,len(self.all)-1)
        i_temp = self.all.pop(random_point)

        return i_temp 



    def change_tilt(self, tilting):
        self.tilt = tilting
        print(self.tilt)

    def random_on(self):

        """ turn on random mode"""
        
        self.random = True
        self.all_backup = list(self.all)
        self.all = [x_temp for x_temp in self.all if self.level==0 or x_temp.level()<=self.level]


        
    def random_off(self):

        """turn off random mode"""
        
        self.random = False
        self.all = list(self.all_backup)

    def change_speed(self, speed):

        """Change the speed"""

        self.speed = speed

    def skip_forward(self, count):

        """Skip forward to a new location"""

        td_temp = self.direction
        self.direction = 1
        for a_temp in range(count):
            here = self.get()
        self.direction = td_temp
        return here

    def skip_back(self, count):

        """Skip backward to a new location"""


        td_temp = self.direction
        self.direction = -1
        for a_temp in range(count):
            here = self.get()
        self.direction = td_temp
        return here

    def change_level(self, level):

        """Change the maximum level of index that the
        pointer ranges over
        """

        self.level = level

    def forward(self):

        """Set direction to forward."""

        self.direction = 1

    def back(self):

        """Set direction to backwards"""

        self.direction = -1

    def go_to(self, index_to):

        """Go a certain pointer location"""

        if index_to in self.all:
            self.current = self.all.index(index_to)
            return self.current
        return index_to

    def deeper(self):

        """Increase the levels ranged over by one"""

        self.level += 1

    def shallower(self):

        """Decrease by one."""

        self.level -= 1
        if self.level < 1:
            self.level = 1
