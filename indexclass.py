"""Module for the index class. The index is the data
type that is used to organize notes in the notebase.
An index is of the form sign N1.N2.N3 ...
1.1 is the child of 1
1.1.1 is the child of 1.1
1.2 is the next note to 1.1
2 is the next note to 1

pylint rated 10.0/10
"""

from globalconstants import PERIOD, EMPTYCHAR, LEFTPAREN, RIGHTPAREN

import random
from indexutilities import index_is_reduced, index_reduce, index_expand



class Index:

    """The class for the index data type."""

    def __init__(self, data):

        if not isinstance(data,(int,str,tuple,list,float)):
            data = str(data)
            
            
        if isinstance(data, int):
            self.self = tuple([data])
        if isinstance(data, str):
            if '^' in data:
                data = index_expand(data)

            self.self = tuple([int(a_temp) for a_temp in data.split(PERIOD)])
        if isinstance(data, (tuple, list)):
            self.self = tuple(data)


    def __str__(self):

        """converts an index into a string"""

        t_temp = EMPTYCHAR
        for a_temp in self.self:
            t_temp += str(a_temp)+PERIOD
        return t_temp[:-1]

    def conv(self,this):
        if isinstance(this,(str,int)):
            return Index(this)
        return this


    def __add__(self, other):

        """Operator overload. Adds two indexes together"""
        other = self.conv(other)

        templist = []
        if isinstance(other, int):
            other = Index(other)


        for i_temp in range(max([len(self.self), len(other.self)])):
            if i_temp >= len(self.self):
                a_temp = 0
            else:
                a_temp = self.self[i_temp]
            if i_temp >= len(other.self):
                b_temp = 0
            else:
                b_temp = other.self[i_temp]
            templist.append(a_temp+b_temp)
        return Index(templist)

    def __sub__(self, other):

        """Operator overload.Subtracts one index from another."""

        other = self.conv(other)

        templist = []
        if isinstance(other, int):
            other = Index(other)

        for i_temp in range(max([len(self.self), len(other.self)])):
            if i_temp >= len(self.self):
                a_temp = 0
            else:
                a_temp = self.self[i_temp]
            if i_temp >= len(other.self):
                b_temp = 0
            else:
                b_temp = other.self[i_temp]
            templist.append(a_temp-b_temp)
        return Index(templist)

    def __eq__(self, other):

        other = self.conv(other)

        """Operator overload. Equality."""
        if isinstance(other, (str, int)):
            other = Index (other)
        if len(self.self) != len(other.self):
            return False
        for i_temp in range(len(self.self)):
            if self.self[i_temp] != other.self[i_temp]:
                return False
        return True

    def __ne__(self, other):

        other = self.conv(other)

        """Operator overload. Indequality."""

        return not self == other

    def __lt__(self, other):

        other = self.conv(other)

        """Operator overload. Less than."""

        for i_temp in range(min([len(self.self), len(other.self)])):
            if  self.self[i_temp] < other.self[i_temp]:
                return True
            if  self.self[i_temp] > other.self[i_temp]:
                return False
        if len(self.self) >= len(other.self):
            return False
        return True

    def __gt__(self, other):

        other = self.conv(other)

        """Operator overload. Greater than."""

        return not self == other and not self < other

    def __le__(self, other):


        """Less than equal."""

        other = self.conv(other)

        return self < other or self == other

    def __ge__(self, other):

        """Greater than equal."""

        other = self.conv(other)

        return self > other or self == other

    def __neg__ (self):

        """Inverts index"""
        tl_temp = list(self.self)
        return Index(tuple([-x for x in tl_temp]))

    def __mul__ (self,mult_by):
        """Multiplies index"""
        tl_temp = list(self.self)
        return Index(tuple([x*mult_by for x in tl_temp]))

    def child(self):

        """Gets the child note  e.g. 1-> 1.1"""

        return Index(str(self) + '.1')

    def previous(self):

        """Gets the previous note."""


        tl_temp = list(self.self)
        if len(tl_temp) > 1:
            tl_temp = tl_temp[:-1]
        return Index(tuple(tl_temp))

    def next(self):

        """Gets the next note."""

        tl_temp = list(self.self)
        tl_temp[len(tl_temp)-1] = tl_temp[len(tl_temp)-1]+1
        return Index(tuple(tl_temp))

    def __int__(self):

        """Converts an index to the integer of the top level."""

        return int(self.self[0])

    def __abs__(self):

        """Operator overload. Returns the absolute value of an Index."""

        tl_temp = list(self.self)
        tl_temp[0] = abs(tl_temp[0])
        return Index(tuple(tl_temp))

    def is_top(self):

        """Test if the index is top-level."""

        if len(self.self) == 1:
            return True
        return False

    def is_descendent(self, other):

        """Tests if self is a descendent of other."""

        other = self.conv(other)

        la_temp = tuple(self.self)
        lb_temp = tuple(other.self)
        if len(la_temp) <= len(lb_temp):
            return False
        if la_temp[0: len(lb_temp)] == lb_temp:
            return True
        return False

    def is_first_descendent(self, other):

        """Tests if one index is the immediate descendent of another."""

        other = self.conv(other)

        if not self.is_descendent(other):
            return False

        la_temp = tuple(self.self)
        lb_temp = tuple(other.self)
        if len(la_temp) == len(lb_temp)+1:
            return True
        return False

    def level(self):

        """Returns the level or 'depth' of an Index."""

        return len(tuple(self.self))

    def within(self,limit=(),not_less=False,not_more=False,must_have=True):

        """For checking whether elements of index are above or below given values"""

        if must_have:
            # rejects if any element fails to meet a given condition for all elements given in the slice

            for position in range(len(limit)):
                if position < len(tuple(self.self)):
                    
                    if not_less and limit[position] and tuple(self.self)[position] < limit[position]:
                        return False
                    if not_more and limit[position] and tuple(self.self)[position] > limit[position]:
                        return False
                else:
                    return False
            return True 
        # only rejects
        for position in range(min([len(limit),len(tuple(self.self))])):
                if position < len(tuple(self.self)):
                    
                    if not_less and limit[position] and tuple(self.self)[position] < limit[position]:
                        return False
                    if not_more and limit[position] and tuple(self.self)[position] > limit[position]:
                        return False
        return True 
            
        

        

    def parent(self):

        """Returns the parent of an index."""

        if not self.is_top():
            return Index(list(self.self)[:-1])
        return self

    def subordinate(self, other):

        other = self.conv(other)

        """Subordinates one index to another."""
        # NOT SURE ###

        other = self.conv(other)

        la_temp = tuple(self.self)
        lb_temp = tuple(other.self)
        return Index(la_temp+lb_temp)

    def all_parents(self):

        la_temp = tuple(self.self)
        returnlist = []
        for x_temp in range(len(la_temp)):
            returnlist.append(Index(la_temp[0:x_temp+1]))
        return returnlist

    def short(self):
        return index_reduce(str(self.self))


##for count in range(0,1000):
##    
##    length = random.randint(1,1000)
##    print(count,'=length=',length)
##    a = '.'.join([random.choice(['1','11']) for a_temp in range(0,100)])
##    print(a)
##    print(index_reduce(a))
##    print()
##    print()
##    print('_______________________________')
##    
    



    
