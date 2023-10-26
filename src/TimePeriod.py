'''
Created on Jan 17, 2018

@author: Aaron

Represents a period of time. Contains datetime objects.
'''
from sys import exit
import datetime as dt
from pandas import Series


class TimePeriod:
    """
    High-level class for a period of time as defined by 2 datetime objects.
    TODO: TimePeriod is deprecated. Substitute with portion library.
    """

    def __init__(self, start: dt.datetime, end: dt.datetime):
        self.start = start
        self.end = end

    # def __init__(self, ser: Series):
    #     self.start = ser.head(1)
    #     self.end = ser.tail(1)
    
    def getDuration(self):
        return self.end - self.start
    
    def compare(self, TP, flag) -> int:
        '''
        Compares the TimePeriod to another using a method determined by flag
        :param TP: TimePeriod to compare to
        :param flag:
        flag = 0: Compare using durations
        flag = 1: Compare using start
        flag = 2: Compare using end
        :return: = [-1, 0, 1]:[self<TP, self=TP, self>TP]
        '''
        if(flag == 0 or flag == 'duration'):
            f1 = self.getDuration()
            f2 = TP.getDuration()
        elif(flag == 1 or flag == 'start'):
            f1 = self.start
            f2 = TP.start
        elif(flag == 2 or flag == 'end'):
            f1 = self.end
            f2 = TP.end
        else:
            exit('args[1]: flag must be contained in range(0:3)')
        if(f1 > f2):    return 1
        elif(f2 < f1):  return -1
        else:           return 0
    
    def withinCalendarDay(self) -> bool:
        # return: The TimePeriod is contained within a single calendar day
        sameDay = self.start.day == self.end.day
        sameMonth = self.start.month == self.end.month
        sameYear = self.start.year == self.end.year
        return sameDay & sameMonth & sameYear
    
    def overlap(self, TP) :
        """
        Finds the TimePeriod of overlap with a second TP
        :param TP: Other TimePeriod
        :return: TimePeriod of overlap
        """
        #TODO: not robust, rewrite overlap to account for all possibilities
        if((self.start < TP.end) & (self.end > TP.start)):
            if(self.start < TP.start):
                return TimePeriod(TP.start, self.end)
            else:
                return TimePeriod(self.start, TP.end)
        else: return None

    def spanningTimePeriod(self, TP):
        """
        Returns a TimePeriod spanning the interval of self and another TimePeriod
        :param TP: Other TimePeriod
        :return:
        """
        if self.start > TP.start:
            if self.end > TP.end:   return TimePeriod(TP.start, self.end)
            else:                   return TimePeriod(TP.start, TP.end)
        else:
            if self.end > TP.end:   return TimePeriod(self.start, self.end)
            else:                   return TimePeriod(self.start, TP.end)
    
    def __str__(self):
        return self.start.__str__() + ' - ' + self.end.__str__()