'''
Created on Jan 10, 2018
@author: Aaron Sandoval

Holds functions used to manage raw timesheet data files. 
'''
import csv
import os
# import unidecode
from src import TimesheetGlobals as Global
# import TimePeriod as TP
from src.Task import Task
from src.TimePeriod import TimePeriod


def main(dataFiles: list) -> str: # todo: rename descriptive name for all mainFuncs
    """
    Cleans and merges raw source data exported from the Timesheet app
    :param dataFiles: List of CSV file(s) containing timesheet data
    :return: Single, merged CSV file in standard format
    """
    stdColDatasets = [0] * len(dataFiles)
    for i, file in enumerate(dataFiles):
        data = importCSV(file)
        # data = replaceSpecialChars(data)
        data = standardizeColumns(data)
        stdColDatasets[i] = data
    data = mergeDatasets(stdColDatasets)
    FM_filePath = writeFMCSV(data)
    #     for task in data: print(task) #DEBUG
    return FM_filePath


def importCSV(fileName: str) -> list:
    """
    Imports a CSV and reads it into a Python list of lists
    :param fileName: Single CSV filename
    :return: List of lists containing the CSV data
    """
    def getRawCSVPath(fileName: str) -> str:
        """
        Gets path of the given CSV file name. Must be changed in event of directory reorganization or for use with other projects
        :param fileName: Name of file (no path)
        :return: FUll file path. Assumes internal folder structure
        """
        return os.path.join(Global.rootProjectPath(), 'Raw_CSVs', fileName)

    filePath = getRawCSVPath(fileName)
    with open(filePath, 'r', encoding='utf-8') as file:
        dataList = list(csv.reader(file))
    return dataList


def writeFMCSV(list_list: list) -> str:
    """
    Writes a FM list of lists dataset to a CSV file
    :param list_list: 
    :return: File path of output CSV
    """
    def getFMFileName(list_list):
        startTask = Task(list_list[0])
        endTask = Task(list_list[-1])
        return Global.getFileNameByTasks(startTask, endTask, 1) + '.csv'

    def getFMCSVPath(fileName: str) -> str:
        """
        Gets path including the CSV file name in the FM_CSVs directory. Must be changed in event of directory reorganization or for use with other projects
        :param fileName: Name of file (no path)
        :return: FUll file path. Assumes internal folder structure
        """
        filePath = os.path.join(Global.rootProjectPath(), 'FM_CSVs', fileName)
        #     print(filePath) #DEBUG
        return filePath

    fileName = getFMFileName(list_list)
    filePath = getFMCSVPath(fileName)
    with open(filePath, 'w', encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(list_list)
    # file.close()
    return filePath


# def replaceSpecialChars(data):
#     """
#     Performs a series of character find/replace operations
#     :param data: String or iterable object containing strings or other iterables.
#     :return: Data structured same as input
#     """
#     #TODO: Change this to preserve special chars, maybe change encoding to read from CSV instead
#     if isinstance(data, str):
#         #         print('String') #DEBUG
#         output = unidecode.unidecode(data)
#     else:
#         try:
#             iter(data)
#         except TypeError:
#             print(data, 'is not iterable')
#         #         print('iterable') #DEBUG
#         output = []
#         for item in data:
#             output.append(replaceSpecialChars(item))
#     return output


def standardizeColumns(list_list) -> list:
    """
    Rearranges the "columns" of the list to fit with the standard
    :param list_list: List of lists. 1st row is column titles
    :return: List of lists with columns rearranged in the standard order per Global.RAW_COLUMN_STRINGS
    """
    colTitles = list_list.pop(0)  # First row of list_list is the column titles
    colMap = [[i, j] for i, title in enumerate(colTitles) for
              j, searches in enumerate(Global.RAW_COLUMN_STRINGS) if title in searches]
    if colMap.__len__() == 0:
        colMap = [[i, j] for i, title in enumerate(colTitles) for
              j, searches in enumerate(Global.RAW_COLUMN_STRINGS_2) if title in searches]
    colMapTranspose = [i[1] for i in colMap]
    newData = [Global.NULL_FIELD] * len(list_list)
    for i, task in enumerate(list_list):
        taskStd = [Global.NULL_FIELD] * (max(colMapTranspose) + 1)
        for mapping in colMap:
            if (task[mapping[0]]):
                taskStd[mapping[1]] = task[mapping[0]]
        newData[i] = taskStd
    #     for task in newData: print(task) #DEBUG
    return newData


def mergeDatasets(datasets: list) -> list:
    """
    Detects dataset overlaps and returns a single, unified list of tasks
    :param datasets: List of lists of lists (tasks) in std columns, no column titles
    :return: List of lists (tasks), not task objects
    """

    def deleteOverlap(setRef, setMut):
        """
        Finds any overlapping time periods and deletes tasks from overlap from setMut.
        Guaranteed not to delete tasks entirely only for datasets with no internally overlapping tasks.
        Assumes that both inputs are chronologically sorted
        :param setRef: Reference set. All tasks should be preserved in the output
        :param setMut: Mutable set. Deletion of overlaps takes place on this set
        :return:
        """
        refTP = TimePeriod.spanningTimePeriod(Task(setRef[0]), Task(setRef[-1]))
        mutTP = TimePeriod.spanningTimePeriod(Task(setMut[0]), Task(setMut[-1]))
        overlapTP = TimePeriod.overlap(refTP, mutTP)
        if not overlapTP: return setMut
        # Else if there is an overlap, pop tasks from setMut until no overlap
        if not mutTP.compare(overlapTP, 1):
            popIndex = 0
        elif not mutTP.compare(overlapTP, 2):
            popIndex = -1
        else:
            exit('overlapTP should coincide with an end of mutTP.')
        while overlapTP:
            setMut.pop(popIndex)
            if len(setMut) == 0: return None
            mutTP = TimePeriod.spanningTimePeriod(Task(setMut[0]), Task(setMut[-1]))
            overlapTP = TimePeriod.overlap(refTP, mutTP)
        return setMut

    numSets = len(datasets)
    trimmedSets = []
    for i in range(numSets - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            datasets[i] = deleteOverlap(datasets[j], datasets[i])  # Prefer the data from datasets further down the list
        if datasets[i]: trimmedSets.append(datasets[i])
    trimmedSets.reverse()
    mergedData = [j for i in trimmedSets for j in i]
    return mergedData
