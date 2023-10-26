'''
Created on Jan 16, 2018

@author: Aaron

Standard object for a Timesheet-style task. Implements TimePeriod to represent 
timekeeping aspect. Not suitable for tasks longer than 24 hours.
'''

import src.TimesheetGlobals as Global
# import TimesheetGlobals as Global
from datetime import datetime, timedelta
from src.TimePeriod import TimePeriod
from src.Description import Description
from utils.Preprocess import processEnumString, getDateTime, getProject


class Task(TimePeriod):
    '''
    classdocs
    '''
    # TODO: Task is deprecated, move still useful procedures to other modules
    
    def __init__(self, *stdList, **kwargs):
        '''
        Constructor
        '''
        from src.TimesheetGlobals import FM_COLUMN_STRINGS as FMCols
        if ((not kwargs) & (stdList is not None)): # Used for initial CSV read
            stdList = stdList[0]
            dateStr = stdList[FMCols.index('Date')] 
            startStr = stdList[FMCols.index('Start time')] 
            endStr = stdList[FMCols.index('End time')] 
            startEnd = getDateTime(dateStr, startStr, endStr)
            TimePeriod.__init__(self, startEnd[0], startEnd[1])
            self.project = getProject(stdList[FMCols.index('Project')].upper())
            self.tags = getTags(stdList[FMCols.index('Tags')].upper())
            self.description = Description(stdList[FMCols.index('Description')].upper())
            
        elif(kwargs): # Used to build and add tasks individually post-CSV read
            if 'start' in kwargs:     self.start = kwargs.get('start')
            else:                     print('Error: no start datetime given.')
            if 'end' in kwargs:       self.end = kwargs.get('end') 
            else:                     print('Error: no end datetime given.')
            if 'project' in kwargs:   self.project = getProject(kwargs.get('project')) 
            else:                     print('Error: no project given.')
            if 'tags' in kwargs:      self.tags = getTags(kwargs.get('tags')) 
            else:                     self.tags = []
            if 'description' in kwargs:
                self.description = Description(kwargs.get('description')) 
            else:
                self.description = Description(Global.NULL_FIELD)
            
#             self.project = getProject(kwargs.get('project'))
#             self.tags = getTags(kwargs.get('tags'))
#             self.description = Description(kwargs.get('description'))
        else:
            print('Error: Unexpected task construction args.\n')
            
        # self.serial = -1 #May or may not keep this. We'll see how it goes.
        self.ID = Global.getTaskID(self.start, self.end)
        self.duration = stdList[FMCols.index('Duration')]
#         self.epoch = (self.start)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # def getDuration(self):
    #     return self.duration
#         return self.end - self.start 


#     def getTaskID(self):
#         """
#         Generates an ID for a task based on its start time and duration, which really should be robustly unique
#         Should be updated if the start or duration of the Task ever change
#         :return: int unique ID
#         """
# #         return int(self.start.strftime('%y%m%d%H%M')+self.end.strftime('%M'))
#         td = self.start - Global.TASK_ID_EPOCH
#         minEpoch = int(td.total_seconds()/60)
#         tdDuration = self.end - self.start
#         minDur = int(tdDuration.total_seconds()/60)
#         return "{0}{num:04d}".format(minEpoch,num=minDur)


# def getProject(enumString):
#     enumString = processEnumString(enumString)
#     try:
#         projectEnum = Global.Project[enumString]
#     except:
#         enumString = Global.projectNameUpdate(enumString)
#         projectEnum = Global.Project[enumString]
#     return projectEnum


def getTags(tagStrings):
    if tagStrings == Global.NULL_FIELD:
        return []
    enumStrings = tagStrings.split(',')
    tags = [0]*len(enumStrings)
    for i, enumString in enumerate(enumStrings):
        enumString = enumString.strip()
        enumString = processEnumString(enumString)
        tagEnum = Global.Tag[enumString]
        tags[i] = tagEnum
    return tags


# Returns an Epoch enum for the most recent epoch in TimesheetGlobals
# def setEpoch(datetime):
#     for i, epoch in enumerate(Global.Epoch):
#         if(i == 0):
#             prevEpoch = epoch
#             continue
#         elif(datetime < epoch.value):
#             return prevEpoch
#         elif(i >= (len(Global.Epoch) - 1)):
#             return epoch
#         prevEpoch = epoch
                    
        
