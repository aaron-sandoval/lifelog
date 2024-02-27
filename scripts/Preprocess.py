'''
Created on Jan 22, 2018

@author: Aaron
Holds functions used to preprocess timesheet data. 
'''
import csv
import portion
from src import TimesheetGlobals as Global
import numpy as np, pandas as pd
from datetime import datetime, timedelta, time
from functools import reduce
from src.Description import Description
# from src.TimePeriod import TimePeriod
from src.TimesheetDataset import TimesheetDataset
from src.BodyPartsUsage import BodyPartsUsage
from copy import copy


def main(FM_file):
    """
    Main pre-processing function. Imports the CSV, replaces characters, standardizes
    :param FM_file: File path to a csv in the standard FM data standard defined in TimesheetGlobals
    :return: File path to a persistent data file containing the post-PP data
    """
    FM_data = importCSV(FM_file)
    df = Global.getDF([initTask(row) for row in FM_data], 2).sort_index()
    Global.writePersistent(df, 1)  # Writes persistent data type of the FM outputs just for records
    df = trimDeadTasks(df)
    df = trimTaskOverlaps(df)
    df = pd.concat([df, __genSleepTasks(df)]).sort_index()
    tsds = TimesheetDataset(
        __addEmptyCollectibleCols(__addEmptyBodyParts(__genMetaproject(__genEpoch(__genCircad(df))))))
    PP_path = tsds.write(2)
    return PP_path


def importCSV(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        dataList = list(csv.reader(file))
    return dataList


def initTask(FMstdList):
    FMCols = Global.FM_COLUMN_STRINGS
    startEnd = getStartEnd_FM(FMstdList)
    start = startEnd[0]
    end = startEnd[1]
    id = Global.getTaskID(start, end)
    durationStr = FMstdList[FMCols.index('Duration')]
    if durationStr != Global.NULL_FIELD:
        duration = parseDuration(durationStr)
    else:
        duration = end - start
    project = getProject(FMstdList[FMCols.index('Project')])
    tags = getTags(FMstdList[FMCols.index('Tags')])
    try:
        mood = __getMood(FMstdList[FMCols.index('Mood')])
    except(IndexError):
        mood = Global.Mood.Neutral
    desc = Description(FMstdList[FMCols.index('Description')])
    epoch = 0  # Handle this later
    return [id, start, end, duration, project, tags, desc, epoch, mood]


def trimDeadTasks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes tasks whose existence is evaluated to be in error.
    """
    def dfToInterval(df) -> portion.Interval:
        return reduce(lambda x, row: x | portion.closedopen(row.start, row.end), df)

    dead = df.tsdf.tsquery('duration < timedelta(minutes=2) & ! description : ;').df
    # TODO: Default length is 1 hr for manually-added task in timesheet.io. These are sometimes extraneous.
    # hourTasks = df.loc[df.duration == timedelta(hours=1)]
    # iv = hourTasks.apply(lambda row: df.shift(-1).loc[(row.index.values[0]):].head(10))
    return df.drop(dead.index)


def trimTaskOverlaps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trims the end time of a task if it is greater than the start time of the next task.
    Reduces the duration per above, and also reduces anomalous durations which exceed end-start to end-start.
    Deletes tasks whose duration is now <= 0.
    """
    # df.sort_index(inplace=True)

    # Tasks whose time interval encapsulates the time interval of the next task
    containsNext =  df[df.end >= df.shift(-1).end]

    # Clean erroneous raw logs whose duration is 12 hours too long due to user AM/PM selection error
    # TODO: check if it makes more sense to trim the starting or ending 12 hours. Currently always trimming the end.
    over12Hrs = df[df.duration > timedelta(hours=12)]
    # Indices of tasks whose logging likely contains an error in the end time's AM/PM attribute
    ampmError = list(set(over12Hrs.index).intersection(set(containsNext.index)))
    df.loc[ampmError, 'duration'] -= timedelta(hours=12)
    df.loc[ampmError, 'end'] -= timedelta(hours=12)

    # Clean erroneous raw logs where a task time interval contains the interval of the next task
    containsNext = df[df.end >= df.shift(-1).end]
    nextTasks = df.shift(-1).loc[containsNext.index]
    # Bool mask, true if the longer task should have its start trimmed, false if it should have its end trimmed
    trimStart = (containsNext.end - nextTasks.end) > (nextTasks.start - containsNext.start)
    trimEndIDs = trimStart[~trimStart].index
    shiftTimeDelta = df.loc[trimEndIDs, 'end'] - df.shift(-1).start.loc[trimEndIDs]
    df.loc[trimEndIDs, 'end'] -= shiftTimeDelta
    df.loc[trimEndIDs, 'duration'] -= shiftTimeDelta

    trimStartIDs = trimStart[trimStart].index
    allTrimStartIDs = copy(trimStartIDs)
    i = 1
    while len(trimStartIDs) > 0:
        # TODO: breaks when updated ID collides with existing. Fix
        shiftTimeDelta = df.shift(-i).end.loc[trimStartIDs] - df.loc[trimStartIDs, 'start']
        df.loc[trimStartIDs, 'start'] += shiftTimeDelta
        df.loc[trimStartIDs, 'duration'] -= shiftTimeDelta
        i += 1
        trimStart = df.loc[trimStartIDs].end > df.shift(-i).loc[trimStartIDs].end
        trimStartIDs = trimStart[trimStart].index
    newIDs = [Global.getTaskID(df.loc[j, 'start'], df.loc[j, 'end']) for j in allTrimStartIDs]
    df.rename(index=dict(zip(allTrimStartIDs, newIDs)), inplace=True)

    # Clean common errors of small overlaps between time periods of adjacent tasks. Start is preserved, end is updated.
    df.sort_index(inplace=True)
    newEnd = np.minimum(df.start.shift(-1).head(-1), df.end.head(-1))
    df.loc[:df.index[-2], 'duration'] -= df.end.head(-1) - newEnd
    df.loc[:, 'duration'] = np.minimum(df.duration, df.end-df.start)  # Duration must be <= end-start
    df.loc[:df.index[-2], 'end'] = newEnd
    return df.loc[df.duration > timedelta(minutes=0), :]


def getStartEnd_FM(FMstdList):
    FMCols = Global.FM_COLUMN_STRINGS
    dateStr = FMstdList[FMCols.index('Date')] 
    startStr = FMstdList[FMCols.index('Start time')] 
    endStr = FMstdList[FMCols.index('End time')]
    return getDateTime(dateStr, startStr, endStr)

    
def parseDuration(durStr):
    try:
        return datetime.strptime(durStr, '%H:%M:%S') - datetime(1900,1,1)
    except:
        x = [int(piece) for piece in durStr.split(':')]
        return timedelta(hours=x[0], minutes=x[1], seconds=x[2])


def getProject(enumString: str):
    """
    Takes a string representation of a project and returns a corresponding enum Project instance.
    Supports obsolete string representations potentially found in FM datasets
    :param enumString:
    :return: Global.Project
    """
    def projectNameUpdate(oldEnumString: str) -> str:
        """
        Replaces old project names with current standard names, or short-lived projects into their larger parent project
        Passing valid project names returns an error, for some reason
        :param oldEnumString: String representing an old project naming convention
        """
        projectMap = {
            'RECREO_EN_COMPUTADORA': 'RECREO_ELECTRÓNICO',
            'MAE_5160': 'CLASES_EXTRAS',
            'OPIR_GSE_SSA': 'OPIR_GSE_AI_T',
            'BOWIE_GXS': 'CARRERA_OPIR',
            'ROBOCHEF': 'ACADÉMICO',
            'CARRERA_ENTRENAMIENTO_MANDATARIO': 'CARRERA_ENTRENAMIENTO_MANDATORIO',
        }
        if oldEnumString in projectMap.keys():
            return projectMap[oldEnumString]
        else:
            raise KeyError('Project enum string \'' + oldEnumString + '\' not recognized.')

    if enumString is None or enumString is Global.NULL_FIELD: return None
    enumString = processEnumString(enumString)
    try:
        projectEnum = Global.Project[enumString]
    except:
        enumString = projectNameUpdate(enumString)
        projectEnum = Global.Project[enumString]
    return projectEnum


def getTags(tagStrings: str):
    """
    Takes a single comma-separated string and
    :param tagStrings:
    :return:
    """
    if tagStrings is None or tagStrings == Global.NULL_FIELD:
        return []
    enumStrings = tagStrings.split(',')
    tags = [0]*len(enumStrings)
    for i, enumString in enumerate(enumStrings):
        enumString = enumString.strip()
        enumString = processEnumString(enumString)
        # tagEnum = Global.Tag[enumString].value
        tagEnum = Global.Tag[enumString]
        tags[i] = tagEnum
    return tags


def __getMood(raw):
    return Global.Mood.idMap()[Global.MOOD_RAW_STRINGS[raw]]


def __genSleepTasks(df):
    # Minimum interval [minutes] for which a sleep task is generated
    td = timedelta(minutes=120)
    startOffset = timedelta(minutes=0);
    endOffset = timedelta(minutes=0);

    start = df['start']
    end = df['end']
    start = start.shift(-1)
    df1 = pd.DataFrame({'start': start, 'end': end})
    isGap = df1[df1.end < (df1.start - td)]
    PPlist = [0] * len(isGap)
    for i, row in enumerate(isGap.iterrows()):
        startI = to_datetime_MANUAL(row[1].end + startOffset)
        endI = to_datetime_MANUAL(row[1].start + endOffset)
        idI = Global.getTaskID(startI, endI)
        if endI - startI > timedelta(hours=2) and time(hour=18) > startI.time() > time(hour=10):
            projectI = Global.Project.SIN_DATOS
            metaprojectI = -1
        else:
            projectI = Global.Project.DORMIR
            metaprojectI = 0
        # moodI = __getMood('-')
        # descriptionI = Description('')
        # tagsI = []
        PPlist[i] = [idI, startI, endI, endI - startI, projectI, [], Description(''), metaprojectI, Global.Mood.Neutral]
    retDF = pd.DataFrame(PPlist, columns=Global.PP_COLUMN_STRINGS[:Global.IND_mood + 2])
    # +2 because +1 needed since id is still a regular column, and +1 for slice end index convention
    retDF.set_index('id', inplace=True, drop=True)
    return retDF


def __genCircad(df):
    """
    Creates a field to store the circadian day of a task.
    That is the day of the start of the first task after the most recent primary sleep task
    :param df:
    :return:
    """
    def startDate(df1):
        return df1.start.apply(datetime.date).iat[0]

    colName = Global.PP_COLUMN_STRINGS[Global.IND_circad+1]
    newSeries = pd.Series(np.zeros(len(df)), index=df.index, name = colName)
    newSeries = pd.to_datetime(newSeries)
    df = pd.concat([df, newSeries], axis=1)
    # TODO: Refine criteria for detecting overnight sleep tasks
    sleepTasks = df[(df.project == Global.Project.DORMIR) & (df.duration > timedelta(hours=2))]
    prevID = 0
    for sleepTask in sleepTasks.iterrows():
        curID = sleepTask[0]
        if prevID == 0:
            circad_i = startDate(df.head(1))
        else:
            circad_i = startDate(df[df.index > prevID].head(1))
#         nextID = sleepTasks[sleepTasks.index>curID].head(1)
        df.loc[(df.index <= curID) & (df.index > prevID), colName] = circad_i
        prevID = curID
    circadLast = startDate(df[df.index > (sleepTasks.tail(1).index[0])])
    df.loc[(df.index > (sleepTasks.tail(1).index[0])), colName] = circadLast
    return df


def __genEpoch(df):
    """
    Populates epoch field for all tasks in df
    :param df: Dataframe to which the epoch column is to be populated
    :return:
    """
    sorted_epochs = Global.Epoch.sortedIter()
    for i, cur_epoch in enumerate(sorted_epochs[:-1]):
        #  Slices for tasks that start after current epoch and before next epoch, sets epoch field to the current enum
        df.loc[(df.start >= cur_epoch.dt()) & (df.start < sorted_epochs[i+1].dt()), 'epoch'] = cur_epoch
    # df.epoch.dtype = Global.Epoch  # This didn't work, pd doesn't recognize enum Epoch as a valid dtype
    return df


def __genMetaproject(df) -> pd.DataFrame:
    """
    Adds a new column and populates the metaproject based on Project.default_metaproject
    :param df:
    :return: augmented df
    """
    metaproject = pd.Series([Global.Metaproject(p.default_metaproject) for p in df.loc[:, 'project']],
                            index=df.index, name='metaproject')
    return pd.concat([df, metaproject], axis=1)


def __addEmptyBodyParts(df) -> pd.DataFrame:
    """
    Adds a new column and populates with emptyobject list
    :param df:
    :return: augmented df
    """
    bodyparts = pd.Series(np.empty(len(df), dtype=object), index=df.index, name='bodyparts')
    return pd.concat([df, bodyparts], axis=1)


def __addEmptyCollectibleCols(df) -> pd.DataFrame:
    """
    Adds the rest of the columns in Global.PP_COLUMN_STRINGS, populating them with empty lists.
    Population of the lists is done in the DC module
    :param df:
    """
    g = Global.PP_COLUMN_STRINGS
    newCols = g[g.index('location') : g.index('media')+1]
    dfCols = np.empty((len(df), len(newCols)), dtype=object)
    for i in np.ndindex(dfCols.shape): dfCols[i] = []
    # for col in newCols:
    df = pd.concat([df, pd.DataFrame(dfCols, index=df.index, columns=tuple(newCols))], axis=1)
    return df


def to_datetime_MANUAL(ts):
    return datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)  


def getDateTime(date: str, time1: str, time2: str) -> list:
    """
    Takes a date string and two time strings and returns 2 datetime objects.
    The date for datetime1 always matches the input.
    For datetime2 it matches the input if time1 < time2. Assumes all TimePeriods <24 hours.
    :param date: String representation of date, various formats supported
    :param time1: String representation of time, various formats supported
    :param time2: String representation of time, various formats supported
    :return: List of 2 datetime objects
    """
    dt1 = date + ' ' + time1
    dt2 = date + ' ' + time2
    if time1[-4:] in {'. m.', '.\xa0m.'}:
        dt1 = dt1[:-4] + 'm'
        dt2 = dt2[:-4] + 'm'
    if date[-5:-2] != '/20' and date[0:2] == '20':
        datetime1 = datetime.strptime(dt1, '%Y-%m-%d %I:%M %p')
        datetime2 = datetime.strptime(dt2, '%Y-%m-%d %I:%M %p')
    elif any([k in date for k in ['201', '202', '203', '204']]):
        datetime1 = datetime.strptime(dt1, '%m/%d/%Y %I:%M %p')
        datetime2 = datetime.strptime(dt2, '%m/%d/%Y %I:%M %p')
    elif time1[-1] in 'Mm.':
        datetime1 = datetime.strptime(dt1, '%m/%d/%y %I:%M %p')
        datetime2 = datetime.strptime(dt2, '%m/%d/%y %I:%M %p')
    else:
        datetime1 = datetime.strptime(dt1, '%m/%d/%y %H:%M')
        datetime2 = datetime.strptime(dt2, '%m/%d/%y %H:%M')
    if(datetime1 > datetime2): #Tasks spanning midnight, set end to next day
        datetime2 = datetime2 + timedelta(days=1)
    return [datetime1, datetime2]


def processEnumString(enumString):
    return enumString.replace(' ', '_').replace('/', '_').replace('&', '_').replace(',', '').replace(':', '').upper()
