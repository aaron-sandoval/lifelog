"""
Created on Mar 5, 2023

@author: Aaron
The top-level dataset object created in the project.
"""
import pandas as pd
from typing import Iterable
import portion
import copy
import os
import warnings
# import ruamel.yaml

from src.Catalogs import *
# from src.TimesheetDF import TimesheetDataFrame
import src.TimesheetGlobals as Global
from src.DescriptionSTDLISTS import DC_ONE_OFF_TOKEN_REPLACEMENT_LIST as DC_oneoff


class TimesheetDataset:
    """
    The top-level Timesheet dataset object. Contains a dataframe and Catalog objects.
    """
    COLLECTIBLE_CLASS_MAP = {collxble: CATALOG_SUBCLASS_STRING_MAP[collxble.CATALOG_CLASS()] for collxble in
                             sorted(kiwilib.leafClasses(Collectible), key=lambda x: x.processingPrecedence())}

    def __init__(self,
                 df: Union[pd.DataFrame, TimesheetDataFrame],
                 catalogs: Iterable[Catalog] = None,
                 fileSuffix: str = ''
                 ):
        """
        Initializes self.df to the arg and all other member data to empty instances
        :param df: pd.Dataframe or TimesheetDataFrame object
        """
        self.fileSuffix: str = fileSuffix
        if self.fileSuffix is str or self.fileSuffix != fileSuffix:
            raise TypeError(f'fileSuffix assignment error: {fileSuffix=}, {self.fileSuffix=}')
        if isinstance(df, TimesheetDataFrame):
            self.timesheetdf: TimesheetDataFrame = df
        else:
            self.timesheetdf: TimesheetDataFrame = df.tsdf
        if catalogs and isinstance(catalogs, dict):
            self.cats: dict[str, Catalog] = catalogs
        else:
            self.cats: dict[str, Catalog] = dict()

    def __eq__(self, other):
        if not isinstance(other, TimesheetDataset):
            return False
        return self.timesheetdf == other.timesheetdf and self.cats == other.cats and self.fileSuffix == other.fileSuffix

    def __copy__(self):
        return TimesheetDataset(copy.copy(self.timesheetdf), self.cats)

    @property
    def fileSuffix(self):
        return self._fileSuffix

    @fileSuffix.setter
    def fileSuffix(self, v: str):
        self._fileSuffix = v
        if not hasattr(self, 'cats'):
            return
        for cat in self.cats.values():
            cCls = cat.COLLXBLE_CLASS
            file = os.path.join(Global.rootProjectPath(), 'catalogs', f'Catalog_{cCls.__name__}{v}.yaml')
            cat.CATALOG_FILE = file

    def preCatalogCorrect(self):
        """Make all corrections available before Catalogs and Collectibles are initialized."""
        [self.timesheetdf.df.loc[key, 'description'].initExceptRaw(DC_oneoff[key]) for key in DC_oneoff.keys() if
         key in self.timesheetdf.df.index]  # Targeted Description changes by task ID
        self.timesheetdf.independentTSQY()
        self.timesheetdf = self.timesheetdf.tsqueryFromFile(
            os.path.join(Global.rootProjectPath(), 'tsqparser', 'p1simpleCommand.tsqy'))

    def postCatalogCorrect(self):
        """Make all corrections necessary after loading Catalogs."""
        self.timesheetdf = self.timesheetdf.tsqueryFromFile(
            os.path.join(Global.rootProjectPath(), 'tsqparser', 'p2independent.tsqy'))
        self.timesheetdf = self.timesheetdf.tsqueryFromFile(
            os.path.join(Global.rootProjectPath(), 'tsqparser', 'p1simpleCommand.tsqy'))
        # TODO: Temporarily put complex DC rules here not yet supported by tsquery. Move to p2independent when ready
        self.timesheetdf.df[self.timesheetdf.df.person.apply(
            lambda x: any([any([isinstance(rel, sg.Family)
                                for rel in self.cats['person'].collxn.loc[p, 'relationships']]) for p in x]))]\
            .tsdf.appendToListColumn(Global.Tag.FAMILIA)  # If any people with SocialGroup.Family, add Tag.FAMILIA
        self.timesheetdf.df[self.timesheetdf.df.description.apply(
            lambda desc: any([tok in STDList.SOFTWARE_ALL for tok in desc.tokens])
        )].tsdf.addItem(Global.Tag.ELEC)  # If Software found, add Tag.Electronica. To be replaced by Software Collxble.

    def outerUpdate(self, other):
        """
        Updates self data members with data members of another TsDS instance loosely according to outer update rules.
        Implements functionality similar to not yet implemented pandas.DateFrame.update(join='outer').
        TimesheetDataFrame member is updated per its method.
        :param other: TsDS instance
        :return: N/A, modifies data members in place.
        """
        assert isinstance(other, TimesheetDataset), 'TsDS may only be updated with another TsDS.'
        self.timesheetdf.outerUpdate(other.timesheetdf)

    def write(self, phaseFlag, fileSuffix: str = None, tsdfFile: str = None):
        """
        Writes the TimesheetDataset to persistent storage.
        Uses the writePersistent method for the TimesheetDataFrame.
        Calls the write method of each Catalog.
        """
        if fileSuffix is None:
            fileSuffix = self.fileSuffix
        for cat in self.cats.values():
            # cat.write(file=cat.CATALOG_FILE[:-5] + fileSuffix + '.yaml')
            cat.write()
        return Global.writePersistent(self.timesheetdf.df, phaseFlag, fileSuffix, file=tsdfFile)


    ###############################
    """Catalogs and Collectibles"""
    ###############################

    def loadCatalogs(self, collxbleClasses: Iterable[type] = None, fileSuffix=None):
        """
        Loads catalogs from persistent storage and stores them in self.cats.
        :param fileSuffix: A suffix string in the yaml files.
        Used to specify another set of catalog yamls other than the defaults.
        :param collxbleClasses: list of Collectible classes to load. Defaults to all Collectible leaf classes.
        """
        if fileSuffix is None:
            fileSuffix = self.fileSuffix
        if collxbleClasses is None:
            classMap = self.COLLECTIBLE_CLASS_MAP
        else:
            classMap = {collxble: self.COLLECTIBLE_CLASS_MAP[collxble] for collxble in collxbleClasses}
        for ccCls in classMap:
            # if ccCls is not Food:  # DEBUG
            #     continue
            file = os.path.join(Global.rootProjectPath(), 'catalogs', f'Catalog_{ccCls.__name__}{fileSuffix}.yaml')
            self.cats[ccCls.name()] = classMap[ccCls](ccCls, loadYaml=True, file=file)

    def catalogPopulateDF(self, catalogs: Iterable[Catalog] = None) -> None:
        """
        Populates the tsdf with Collectibles from catalogs according to 2 criteria:
         1. the presence of its name as a token.
         2. catalog.COLLXBLE_CLASS.POPULATION_TSQY(), which filters out some token collisions involving collxble names.
        Also clears collxble name descTokens from the populated rows of tsdf.
        :param catalogs: List of Catalogs. Defaults to all Catalogs in self.cats.
        """
        # TODO: delete and replace calls with direct calls to `catalog.populateDF(self.timesheetdf)`
        if catalogs is None:
            catalogs = self.cats.values()
        for catalog in catalogs:
            catalog.populateDF(self.timesheetdf)  

    def clearInitTokens(self, catalogs: Iterable[Catalog] = None):
        """
        Clears any initialization tokens for the Collectible classes of the Catalog.
        :param catalogs: list of Catalogs whose tokens to clear. Defaults to all Catalogs in self.cats.
        """
        if catalogs is None:
            catalogs = self.cats.values()
        for catalog in catalogs:
            toksToClear = catalog.COLLXBLE_CLASS.INITIALIZATION_TOKENS_TO_CLEAR()
            self.timesheetdf.df[
                self.timesheetdf.df.description.apply(
                    lambda x: any([x.hasToken(tok) and len(x.getChildToks(tok)) == 0 for tok in toksToClear]))
            ].description.apply(lambda desc: desc.removeToken(toksToClear))

    def lookupForeignKeys(self, keys: Iterable[Union[str, tuple]], colName: str) -> List[Collectible]:
        """
        The inverse of Collectible.foreignKey().
        Returns the Collectibles found in a Catalog from the foreign keys.
        :param colName: dfcolumn() of the Collectible class.
        :param keys: List of values returned by calling myCollectible.foreignKey()
        """
        if len(keys) == 0: return []
        if isinstance(keys[0], tuple):  # Subclasses of Media, maybe others
            cat = self.cats[keys[0][0].name()]
            return cat.getObjects(ids=[k[1] for k in keys])
        else:
            cat = self.cats[colName]
            return cat.getObjects(ids=keys)

    def validate(self):
        """ Scalable method to validate the data integrity of a TimesheetDataset. """
        def validateCIDs():
            """Asserts that all foriegn Collxble IDs found in the tsdf are present in the respective Catalog."""
            for cat in self.cats.values():
                cidSer: TimesheetDataFrame = self.timesheetdf.tsquery(f'{cat.COLLXBLE_CLASS.__name__} : ;')
                if len(cidSer) == 0:
                    continue
                if issubclass(cat.COLLXBLE_CLASS, Media):
                    cidSer = cidSer.filterMedia({cat.COLLXBLE_CLASS.name(), })
                cidSer: pd.Series = cidSer.df[cat.COLLXBLE_CLASS.dfcolumn()]  # cidSer now a Series
                if issubclass(cat.COLLXBLE_CLASS, Global.ListColumn):
                    foreignKeys = np.unique(np.fromiter(kiwilib.flatten(cidSer.values, numLevels=1), tuple))
                else:
                    foreignKeys = np.unique(cidSer.values)
                catKeys = set(np.vectorize(cat.COLLXBLE_CLASS.foreignKeyToCatalogKey)(foreignKeys))
                assert len(catKeys & set(cat.collxn.index)) == len(catKeys)\
                    , f'Keys {catKeys - set(cat.collxn.index)} in df["{cat.COLLXBLE_CLASS.name()}"] not found in catalog'

        validateCIDs()

    def autofillPreviousCollectibles(self, cClasses: Iterable[type] = kiwilib.leafClasses(AutofillPrevious)) -> None:
        """
        Fills in a TimesheetDataFrame with the Collectibles in this Catalog.
        Uses Collectible.INITIALIZATION_TOKENS() to filter the TsDF rows to be filled with a Collectible.
        :param cClasses: Types to autofill. Iterable of leaf subclasses of src.Collectibles.AutofillPrevious.
        :return: TsDF with Collectibles filled in
        """
        for cCls in cClasses:
            if not issubclass(cCls, AutofillPrevious):
                raise TypeError(f'{cCls} is not a subclass of AutofillPrevious')
            sourceInds, targetInds = cCls.getAutofillRows(self.timesheetdf)
            startDTs = self.timesheetdf.df.loc[sourceInds, ['start', cCls.dfcolumn()]]
            rowsToFill = self.timesheetdf.df.loc[targetInds, :]
            if len(rowsToFill) == 0:
                return
            # startDTs = self.timesheetdf.df.loc[~self.timesheetdf.isEmpty(
            #     cCls.name()), ['start', cCls.dfcolumn()]]  # Tsdf rows already containing an AutofillPrevious instance
            if issubclass(cCls, Media):
                startDTs = startDTs.tsdf.filterMedia(include={cCls.name()}).df
            # rowsToFill = self.timesheetdf.df[self.timesheetdf.df.description.apply(
            #     lambda x: any([x.hasToken(tok) for tok in cCls.INITIALIZATION_TOKENS()]))]
            if issubclass(cCls, Global.ListColumn):
                collxbles = self.lookupForeignKeys(keys=[a[0] for a in list(startDTs.iloc[:, -1])],
                                                   colName=cCls.name())  # TODO: ensure support for multiple Foods/row
            else:
                collxbles = self.lookupForeignKeys(keys=list(startDTs.iloc[:, -1]), colName=cCls.name())
            for i in range(len(startDTs)-1):  # Iterate over intervals and add the previous collxble to the tsdf
                thisChunk = rowsToFill.loc[startDTs.iloc[i, :].name: startDTs.iloc[i+1, :].name-1, :]
                thisChunk.tsdf.addItem(collxbles[i])
            rowsToFill.loc[startDTs.iloc[-1, :].name:].tsdf.addItem(collxbles[-1])  # Fill chunk after last startDT
            # TODO: maybe fill with collxble with most recent startTaskID? Change where that property is in hierarchy
            cat = self.cats[cCls.name()]
            # Get the most recently-started Collxble ID in the Catalog at the start of self.tsdf
            if any(rowsToFill.head(1).tsdf.isEmpty(cCls.name())):
                # If 1+ task at the start is still unassigned, fill it with the most recent Collxble in the Catalog
                headCollxble = AutofillPrevious.getPreviousID(cat.collxn.startTaskIDs, rowsToFill.index[0])
                rowsToFill.loc[rowsToFill.tsdf.isEmpty(cCls.name())].tsdf.addItem(cat.getObjects(ids=(headCollxble,)))

    def initCatalogs(self, fileSuffix=None):
        """
        High-level method which performs all initialization tasks for the Catalogs and population of the TsDF.
        Initializes and fully populates catalogs with minimally-complete Collectible instances.
        """
        if fileSuffix is None:
            fileSuffix = self.fileSuffix
        self.loadCatalogs(fileSuffix=fileSuffix)
        for catalog in self.cats.values():
            catalog.populateDF(self.timesheetdf)    
        self.clearInitTokens([self.cats['tvshow'], self.cats['movie']])
        for catalog in self.cats.values():
        # for catalog in list(self.cats.values())[3:4]:  # Used when populating only a subset of all catalogs
            oldLen = len(catalog)
            catalog.autoCollect(self.timesheetdf)
            if len(catalog) > oldLen:
                catalog.populateDF(self.timesheetdf)
            if issubclass(catalog.COLLXBLE_CLASS, AutofillPrevious):
                self.autofillPreviousCollectibles([catalog.COLLXBLE_CLASS])
            catalog.updateScalingFields(self.timesheetdf, reset=())
            catalog.headerData['TASK ID RANGE'] = catalog.headerData['TASK ID RANGE'] | \
                portion.closed(int(self.timesheetdf.df.index[0]), int(self.timesheetdf.df.index[-1]))
        self.clearInitTokens()  # TODO: implement __sub__ for Catalogs, reduce clearing cat scope



