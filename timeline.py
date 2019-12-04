from orderedlist import OrderedList
from datetimetimeline import TimeLineDateTime

class TimeLine:

     def __init__ (self):

          self.dates = OrderedList()
          self.index_to_dates = {}
          self.dates_to_index = {}
          self.index_to_event = {}

     def add_event (self,date,event,index):

          newdate = TimeLineDateTime(date)
          if newdate.exists:
               self.dates.add(newdate)
          self.index_to_dates[index] = date
          self.dates_to_index[date] = index
          self.index_to_event[index] = event

tl = TimeLine()

while True:

     date=input('date')
     index=input('index')
     event=input('event')
     tl.add_event(date,event,index)
     

     print(tl.dates.list)
     

          

          
