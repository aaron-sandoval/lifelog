"""
Created on Mar 5, 2023

@author: Aaron
Defines a class implementing a custom accessor for pandas dataframes.
Adds functionality specific to the Timesheet project directly callable on a Dataframe object
"""
import os
from datetime import datetime, date, timedelta
import pickle
from typing import Union, Iterable, List, Tuple, Set
from collections import Counter

import pandas as pd
from pandas.core.dtypes.inference import is_list_like
from src.TimesheetGlobals import *
from antlr4 import *
from tsqparser.TimesheetQueryLexer import TimesheetQueryLexer
from tsqparser.TimesheetQueryParser import TimesheetQueryParser
import kiwilib

@pd.api.extensions.register_dataframe_accessor("tsdf")
class TimesheetDataFrame:
    isEmptyColumnMap = {
        'id': lambda x: x is None,
        'start': lambda x: not isinstance(x, datetime),
        'end': lambda x: not isinstance(x, datetime),
        'duration': lambda x: not isinstance(x, timedelta),
        'project': lambda x: not isinstance(x, Project),
        'tags': lambda x: x is None or len(x) == 0,
        'description': lambda x: x is None or x.isEmpty(),
        'epoch': lambda x: not isinstance(x, Epoch),
        'mood': lambda x: not isinstance(x, Mood),
        'circad': lambda x: not isinstance(x, date),
        'metaproject': lambda x: not isinstance(x, Metaproject),
        'bodyparts': lambda x: True,  # TODO: implement the rest of isEmpty when built
        'location': lambda x: True,
        'person': lambda x: x is None or len(x) == 0,
        'food': lambda x: x is None or len(x) == 0,
        'media': lambda x: x is None or len(x) == 0,
        'audiobook': lambda x: x is None or len(x) == 0 or not any([y[0].name() == 'audiobook' for y in x]),
        'podcast': lambda x: x is None or len(x) == 0 or not any([y[0].name() == 'podcast' for y in x]),
        'tvshow': lambda x: x is None or len(x) == 0 or not any([y[0].name() == 'tvshow' for y in x]),
        'movie': lambda x: x is None or len(x) == 0 or not any([y[0].name() == 'movie' for y in x]),
    }
    extraColumnNameMap = {
        'audiobook': 'media',
        'podcast': 'media',
        'movie': 'media',
        'tvshow': 'media',
        'software': 'media',
        'videogame': 'media',
        'tabletopgame': 'media',
    }

    def __init__(self, df):
        self.df = df

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, obj):
        self.validate(obj)
        self._df = obj

    @staticmethod
    def validate(obj):
        # verify that it's a dataframe
        if obj.__class__ != pd.DataFrame:
            raise AttributeError(f"TimesheetDataFrame must be passed a pandas DataFrame, not a {obj.__class__}")

    @staticmethod
    def _validateStartEnd(obj):
        # verify that it's a dataframe or series
        if 'start' not in obj.columns or 'end' not in obj.columns:
            raise AttributeError("This TimesheetDataFrame must have 'start' and 'end' columns")

    def __eq__(self, other):
        if not isinstance(other, TimesheetDataFrame):
            return False
        return self.df.equals(other.df)

    def __copy__(self):
        return TimesheetDataFrame(self.df.copy(deep=False))

    def __deepcopy__(self, memodict={}):
        return TimesheetDataFrame(pickle.loads(pickle.dumps(self.df)))

    def __len__(self):
        return len(self.df)

    def __str__(self):
        return '\n'.join('TSDF:', str(self.df), '</TSDF>')

    def isEmpty(self, cols: Union[Iterable[str], str] = None) -> Union[pd.Series, pd.DataFrame]:
        """
        Returns boolean DataFrame/Series showing if each data entry is empty.
        The definition of empty changes depending on the column as defined in class static variable isEmptyColumnMap.
        :param cols: Single or iterable of string column names
        :return: boolean mask with # of columns
        """
        if isinstance(cols, str): return self.isEmpty((cols,))
        if not cols:
            cols = tuple(self.df.columns)
        else:
            cols = tuple([c.lower() for c in cols])
        out = pd.DataFrame(index=self.df.index, columns=cols)
        # else:
        #     out = pd.Series(index=self.df.index, name=cols[0])

        for col in cols:
            if col not in self.df.columns:
                if col not in self.isEmptyColumnMap:
                    raise KeyError(f'{col} column either not present or is not a standard TSDF column name.')
                else:  # col is special key from extraColumnNameMap
                    out[col] = self.df[self.extraColumnNameMap[col]].apply(self.isEmptyColumnMap[col])
            else:  # col is Standard TSDF column name
                out[col] = self.df[col].apply(self.isEmptyColumnMap[col])
        if out.isna().values.any():
            raise NotImplementedError(f'Some data not processed')
        if len(cols) == 1:
            out = out.squeeze('columns')
        return out

    def isinListColumn(self, val: Union[Iterable[ListColumn], ListColumn], column=None) -> pd.Series:
        """
        Returns boolean Series showing if val is in column.
        If val is an iterable of ListColumns, a given row returns True iff all items in val are present
        :param val: Singular or iterable ListColumn.
        :param column:
        :return:
        """
        if column is None: column = ListColumn.getColumnClassDict()[type(val)]
        if column not in self.df.columns:
            raise KeyError(f'Column {column} does not exist in TimesheetDataFrame')
        if is_list_like(val):
            val0 = val[0]
            if len(val) == 1:
                return self.isinListColumn(val0, column)
            return self.isinListColumn(val0, column) & self.isinListColumn(val[1:], column)
        ser = self.df[column]
        if hasattr(val, 'foreignKey'):
            val = val.foreignKey()
        return ser.apply(lambda row: val in row)

    def appendToListColumn(self, val: Union[ListColumn, Iterable[ListColumn]], column: str = None):
        """
        Appends values to a ListColumn, disallowing duplicates.
        :param val: Value or list_like of values to append. Must be of a ListColumn subclass.
        :param column: String representing column name to append to.
        """
        if len(self.df) == 0: return
        if not column: column = ListColumn.getColumnClassDict()[type(val)]
        elif column not in ListColumn.getColumnClassDict().values():
            raise KeyError(f'Column {column} is not a ListColumn')
        if is_list_like(val):
            val0 = val[0]
            self.appendToListColumn(val0, column)
            if len(val) > 1:
                self.appendToListColumn(val[1:], column)
            return
        elif type(val) not in ListColumn.getColumnClassDict():
            raise TypeError(f'Object of type {val.__class__} cannot be appended to TSDF column {column}')
        rowsToAppend = ~self.isinListColumn(val, column)
        # notYetInListCol = self.df[column].apply(lambda row: val in row)
        if hasattr(val, 'foreignKey'):
            self.df.loc[rowsToAppend, column].apply(lambda row: row.append(val.foreignKey()))
        else:
            self.df.loc[rowsToAppend, column].apply(lambda row: row.append(val))

    def deleteFromListColumn(self, val: Union[Iterable[ListColumn], ListColumn], column: str) -> None:
        """
        Deletes value(s) from a ListColumn.
        If val is not present in the column, no action taken.
        :param val: Value or list_like of values to delete. Must be of a ListColumn subclass.
        :param column: String representing column name to delete from.
        :return: TimesheetDataFrame with values deleted
        """
        if len(self.df) == 0: return
        if not column: column = ListColumn.getColumnClassDict()[type(val)]
        if column not in ListColumn.getColumnClassDict().values():
            raise KeyError(f'Column {column} is not a ListColumn')
        if is_list_like(val):
            val0 = val[0]
            self.deleteFromListColumn(val0, column)
            if len(val) > 1:
                self.deleteFromListColumn(val[1:], column)
            return
        elif type(val) not in ListColumn.getColumnClassDict():
            raise TypeError(f'Object of type {val.__class__} cannot be found in TSDF column {column}')
        rowsToDelete = self.isinListColumn(val, column)
        # notYetInListCol = self.df[column].apply(lambda row: val in row)
        if hasattr(val, 'foreignKey'):
            self.df.loc[rowsToDelete, column].apply(lambda row: row.remove(val.foreignKey()))
        else:
            self.df.loc[rowsToDelete, column].apply(lambda row: row.remove(val))

    def deleteItem(self, item: Union[ColumnEnum, Iterable[ColumnEnum]]) -> None:
        """Removes an object from all rows of the tsdf. ListColumn and SingleInstanceColumn supported."""
        if len(self.df) == 0: return
        if isinstance(item, ColumnEnum):
            itemClass = type(item)
            col = item.dfcolumn()
        else:
            itemClass = type(item[0])
            col = item[0].dfcolumn()
        if issubclass(itemClass, ListColumn):
            self.deleteFromListColumn(item, col)
        elif issubclass(itemClass, SingleInstanceColumn):
            self.df.loc[:, col] = None

    def addItem(self, item: Union[ColumnEnum, str, Iterable]) -> None:
        """
        Adds the item to the TSDF in the appropriate column and with the appropriate behavior depending on the column.
        For a ListColumn, appends the item to the list.
        For a SingleInstanceColumn, overwrites the existing value.
        :param item: Single of Iterable of items to add.
        """
        if len(self) == 0:
            return
        if is_list_like(item):
            for i in item:
                self.addItem(i)
        elif isinstance(item, ListColumn):
            self.appendToListColumn(item)
        elif isinstance(item, SingleInstanceColumn):
            self.df[item.dfcolumn()] = item
        elif isinstance(item, str):
            self.df.description.apply(lambda desc: desc.addToken(item))
        else:
            raise TypeError(f'Cannot add item {item} of type {item.__class__} to TimesheetDataFrame')

    def getDescTokenChildren(self, descToken: str) -> pd.Series:
        """
        Returns a Series of lists of descToken's children in the Description.
        If descToken is not present, that entry is NaN.
        If descToken has no children, that entry is an empty list.
        :param descToken: Singluar token to search for
        :return: 
        """
        return self.df.description.apply(lambda x: x.getChildToks(descToken))

    def filterMedia(self, include: Set[str] = None, exclude: Set[str] = None):
        """
        Returns a copy of self with some items in the 'media' column filtered out.
        Filter either by a list of types to include or exclude, but not both.
        :param include: Media lowercase leaf class names
        :param exclude:
        :return:
        """
        def deleteMedia(mList):
            i = 0
            while i < len(mList):
                if include is not None and mList[i][0].name() not in include:
                    del mList[i]
                elif exclude is not None and mList[i][0].name() in exclude:
                    del mList[i]
                else:
                    i += 1
        if include is not None and exclude is not None:
            raise LookupError('Can either specify include or exclude, but not both.')
        out = self.df.copy(deep=False)
        filtered = pickle.loads(pickle.dumps(out.media))
        out.media = filtered
        out.media.loc[~out.tsdf.isEmpty('media')].apply(deleteMedia)
        return out.tsdf

    def outerUpdate(self, other):
        """
        Implements functionality similar to not yet implemented pandas.DateFrame.update(join='outer')
        Merges on index.
        For rows in the intersection of indices, overwrites self.df with other.
        For rows exclusive to self.df, no change.
        For rows exclusive to other, appends those rows to self.df.
        For rows in other whose values are filled with NA, delete that row from self.df.
        This is used, for instance, when splitting a task when both new task IDs are different from the original ID.
        Columns of self.df and other must be identical. Handling of different sets of columns not implemented.
        :param other: Other TimesheetDataFrame or DataFrame.
        :return: None, modifies self.df in-place
        """
        if isinstance(other, TimesheetDataFrame):
            other = other.df
        if not all(other.columns == self.df.columns):
            raise NotImplementedError('Support for different sets of columns not yet implemented.')
        self.df.update(other)  # Overwrite rows with shared IDs
        self.df = pd.concat((self.df, other.loc[~other.index.isin(self.df.index)]), axis=0)
        # self.df.append(other.loc[~other.index.isin(self.df.index)])  # Append any rows with new IDs
        self.df.dropna(how='all', inplace=True)  # Deletes and rows which are filled with NA

    def generateIDs(self):
        """
        Generates task IDs using the Global function and sets the index of the df to those IDs
        """
        # TODO: finish generateIDs when it's needed
        from src.TimesheetGlobals import getTaskID
        self._validateStartEnd()
        self._df[:, 'newid'] = 0
        for row in self._df:
            row['newid'] = getTaskID(row['start'].values[0], row['end'].values[0])
        self._df.set_index('newid', inplace=True, drop=True)
        return self._df # TODO: Don't know if this is needed, depends on if pass by reference

    def tokenCounter(self) -> pd.Series:
        """
        :return: A counter Series object of all the tokens in all Description objects contained in the TsDF.
        """
        return pd.Series(i18n.kiwilib.flatten(self.df.description.apply(lambda x: x.tokens).values))\
            .value_counts()

    ##########################
    # TimesheetQuery Methods #
    ##########################
    # independentTSQYRules = os.path.join(rootProjectPath(),'tsqparser', 'testQueries_1.txt')
    independentTSQYRules = os.path.join(rootProjectPath(),'tsqparser', 'independent.tsqy')

    def independentTSQY(self):
        PRIVATE_FILENAME = Path(os.path.abspath(self.independentTSQYRules))\
                               .parent / f'{os.path.splitext(self.independentTSQYRules)[0]}_PRIVATE.tsqy'
        if os.path.isfile(PRIVATE_FILENAME):
            self.df = self.tsqueryFromFile(PRIVATE_FILENAME).df
        self.df = self.tsqueryFromFile(self.independentTSQYRules).df

    def tsqueryFromFile(self, filePath):
        """
        Applies TimesheetQuery commands from a file
        :param filePath: File in TimesheetQuery language
        """
        with open(filePath, 'r', encoding='utf-8') as rulesList:
            text = rulesList.read()
        return self.tsquery(text)

    def tsquery(self, rulesText: str):
        """
        Applies a set of TimesheetQuery commands to the TsDF in-place
        :param rulesText: String in TimesheetQuery language representing a set of queries and/or updates to the TsDF
        """
        from tsqparser.MyTimesheetQueryListener import MyTimesheetQueryListener
        lexer = TimesheetQueryLexer(InputStream(rulesText))
        stream = CommonTokenStream(lexer)
        parser = TimesheetQueryParser(stream)
        tree = parser.ruleList()
        listener = MyTimesheetQueryListener(self)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return tree.data.timesheetdf

    @classmethod
    def mergeTSDFs(cls, tsdfs: List) -> 'TimesheetDataFrame':
        """
        Merges tsdfs into a single TimesheetDataFrame.
        Precedence for overlaps is given to the later tsdf.
        A tsdf is later if its last 'start' value is later. The first 'start' value is the tiebreaker.
        :param tsdfs: List of TimesheetDataFrame objects to merge.
        :return:
        """
        dfs = sorted([o.df.sort_index() for o in tsdfs], key=lambda x: 2*x.index[-1]+x.index[0])
        trimmed = [df.loc[:dfs[i + 1].index[0] - 1, :] for i, df in enumerate(dfs[:-1])]
        trimmed.append(dfs[-1])
        return pd.concat(trimmed, axis=0).tsdf

