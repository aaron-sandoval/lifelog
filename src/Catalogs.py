import typing
import numpy as np
import yaml
import os.path
import warnings
from functools import reduce

from src.Collectibles import *


class Catalog(abc.ABC):
    _METADATA_HEADER_DEFAULT = {'HEADER': {
        'FILE TYPE': 'Catalog',
        'DATE WRITTEN': None,
        'TASK ID RANGE': portion.empty(),
        'COLLECTIBLE TYPE': '',
        'CATALOG COUNT': 0,
    }}

    def __init__(self, COLLXBLE: typing.Type[Collectible], loadYaml=True, file=None):
        """
        :param COLLXBLE: The type of data in this Catalog. A leaf class of Collectible.
        :param loadYaml: Should the catalog initialize by loading data from file or initialize an empty Catalog?
        :param file: yaml file for r/w persistent storage. If no arg provided, uses the default.
        """
        self.COLLXBLE_CLASS: typing.Type[Collectible] = COLLXBLE  # Tells what Collectible is being stored.
        if not file:
            self.CATALOG_FILE = os.path.join(Global.rootProjectPath(), 'catalogs', f'Catalog_{COLLXBLE.__name__}.yaml')
        else:
            self.CATALOG_FILE = file
        self.collxn = self.getEmptyCollxn()
        self.headerData = self._METADATA_HEADER_DEFAULT[next(iter(self._METADATA_HEADER_DEFAULT))].copy()
        self.headerData['COLLECTIBLE TYPE'] = self.COLLXBLE_CLASS.name()
        if loadYaml:
            self.read(file=file)

    def __repr__(self):
        return f'{type(self).__name__}: {self.COLLXBLE_CLASS.__name__} at {hex(id(self))}'

    def __len__(self):
        return len(self.collxn)

    def __eq__(self, other):
        if not isinstance(other, Catalog):
            return False
        return self.collxn.equals(other.collxn) or (self.collxn.isna().equals(other.collxn.isna()) and
                                                    self.collxn.fillna(0).equals(other.collxn.fillna(0)))

    @property
    def collxn(self):
        return self._collxn

    @collxn.setter
    def collxn(self, val):
        self._collxn = val

    def collect(self, collxbles: Union[dict, Iterable[dict], Collectible, Iterable[Collectible]]) -> None:
        """
        Adds a set of Collectibles to self.collxn if not already present. If already present, the collxble is skipped.
        Presence determined by Catalog.hasCollectible(collxble).
        :param collxbles: Objects or dictionaries as produced by collxble.toCatalogDict().
        """
        # TODO: add support for specifying overwrite behavior
        if isinstance(collxbles, self.COLLXBLE_CLASS):
            self.collect((collxbles,))
            return
        if collxbles is None or len(collxbles) == 0:
            return
        if not isinstance(collxbles[0], dict):  # collxbles are Iterable[Collectible]
            if any([not isinstance(c, self.COLLXBLE_CLASS) for c in collxbles]):
                raise TypeError(f'Cannot collect types other than {self.COLLXBLE_CLASS}.')
            collxbles = [item.toCatalogDict() for item in collxbles if not self.hasCollectible(item)]
        if not collxbles or len(collxbles) == 0:
            return
        if 'id' not in collxbles[0].keys():
            for item in collxbles:
                item['id'] = self.COLLXBLE_CLASS.generateID(**item)
        self.collxn = pd.concat((self.collxn, pd.DataFrame(collxbles).set_index('id')))

    def hasCollectible(self, collxble: Collectible) -> bool:
        return collxble.id in self.collxn.index

    def autoCollect(self, timesheetdf: TimesheetDataFrame, *args):
        """
        Leaf class methods.
        Processes a TsDF and finds if there is an instance of that collectible. If so, adds to collection.
        :param overwrite: str/bool parameter which determines behavior when a Collectible with an identical ID is found.
        overwrite=True: the existing Collectible is overwritten with the newly-collected instance.
        overwrite=False: the newly-collected instance is discarded
        overwrite='ask': query the user at runtime for desired behavior
        :param timesheetdf: tsdf in which to search for Collectibles
        """
        # TODO: add support for overwrite behavior
        objs = self.COLLXBLE_CLASS.constructObjects(timesheetdf, args)
        # Task ID range update eliminated b/c it interferes w/ updateScalingFields(). Task ID range updated afterwards.
        self.collect(objs)

    def getObjects(self, collxn=None, ids: Iterable[str] = None) -> List[Collectible]:
        """
        If no args, constructs and returns a list of Collectibles encoded in the Catalog.
        :param collxn: Data structure of the same type as self.collxn. If passed, uses that instead of self.collxn.
        :param ids: If passed, only constructs the Collectible whose id is in the list
        """
        if collxn is None:
            collxn = self.collxn
        if ids is not None:
            collxn = collxn[collxn.index.isin(set(ids))]
            objDict = {id: self.COLLXBLE_CLASS(**d) for d, id in zip(collxn.to_dict('records'), collxn.index)}
            return [objDict[id] for id in ids]
        else:
            return [self.COLLXBLE_CLASS(**d) for d in collxn.to_dict('records')]

    def _getYamlable(self) -> typing.List[typing.Dict]:
        """
        Also converts any datetime or timedelta dtype columns to object dtype.
        Overwrites all pd.NaT with np.nan to avoid yaml read errors on pd.NaT.
        :return:
        """
        dts = self.collxn.select_dtypes(include=('datetime', 'timedelta')).astype(object).where(lambda x: ~pd.isna(x))
        self.collxn[dts.columns] = dts
        if issubclass(self.COLLXBLE_CLASS, IncompletePersistent):
            return [{next(iter(self._METADATA_HEADER_DEFAULT)): self.headerData}] + \
               self.collxn[[c for c in self.collxn.columns if c not in self.COLLXBLE_CLASS.colsNotCataloged()]] \
                   .reset_index().to_dict('records')
        else:
            return [{next(iter(self._METADATA_HEADER_DEFAULT)): self.headerData}] + \
                   self.collxn.reset_index().to_dict('records')

    # @abc.abstractmethod
    def write(self, file=None):
        # Maybe not abstract, depends on if tree can be yaml'd easily
        self.updateHeaderData()
        data = self._getYamlable()
        if not file:
            if len(data) > 1 and set(data[1].keys()) - set(self.COLLXBLE_CLASS.CATALOG_FIELDS()) != set():
                raise KeyError(f'When writing to the default catalog file, fields:\n'
                               f'{set(data[1].keys()) - set(self.COLLXBLE_CLASS.CATALOG_FIELDS())}\nare not allowed')
            file = self.CATALOG_FILE
        with open(file, 'w') as yamlfile:
            yaml.dump(data, yamlfile, sort_keys=False)

    def _readYaml(self, file: str = None) -> dict:
        """
        Helper function to implement common functionality of file reading.
        :param file: Optional file path. Defaults to self.CATALOG_FILE.
        :return: None: No yaml data available, and construction of self.collxn is complete.
         not None: data read from yaml file. Subclass read() methods use this data to construct self.collxn.
        """
        if not file: file = self.CATALOG_FILE
        if not os.path.isfile(file):
            self.collxn = self.getEmptyCollxn()
            return None
        with open(file, 'r') as yamlfile:
            yamlData = yaml.load(yamlfile.read(), Loader=yaml.SafeLoader)
        if not yamlData:
            self.collxn = self.getEmptyCollxn()
            self.headerData = next(iter(self._METADATA_HEADER_DEFAULT.values()))
            return None
        elif next(iter(yamlData[0])) == next(iter(self._METADATA_HEADER_DEFAULT)):
            self.headerData = yamlData[0][next(iter(self._METADATA_HEADER_DEFAULT))]
            return yamlData[1:]
        else:
            self.headerData = next(iter(self._METADATA_HEADER_DEFAULT.values())).copy()
            return yamlData

    @abc.abstractmethod
    def read(self, file: str = None) -> None:
        """
        Common partial implementation of Catalog load sequence from file.
        :param file: Optional file path. Defaults to self.CATALOG_FILE.
        :return: None: No yaml data available, and construction of self.collxn is complete.
         not None: data read from yaml file. Subclass read() methods use this data to construct self.collxn.
        """
        self._readYaml(file)

    def updateFields(self) -> None:
        """ Corrects the columns in self.collxn to match self.COLLXBLE_CLASS.CATALOG_FIELDS(), if necessary. """
        if ['id']+list(self.collxn.columns) != self.COLLXBLE_CLASS.CATALOG_FIELDS():
            existing = [col for col in self.COLLXBLE_CLASS.CATALOG_FIELDS() if col in self.collxn.columns]
            new = [col for col in self.COLLXBLE_CLASS.CATALOG_FIELDS() if col not in ['id'] + list(self.collxn.columns)]
            self.collxn = self.collxn[existing]
            for c in new:
                if c in self.COLLXBLE_CLASS.DEFAULT_MEMBERS():
                    if isinstance(self.COLLXBLE_CLASS.DEFAULT_MEMBERS()[c], typing.Hashable):
                        self.collxn.loc[:, c] = [self.COLLXBLE_CLASS.DEFAULT_MEMBERS()[c] for _ in
                                                 range(len(self.collxn))]
                    else:  # Need to copy objects to create independent instances and avoid overwriting class variable.
                        self.collxn.loc[:, c] = [self.COLLXBLE_CLASS.DEFAULT_MEMBERS()[c].copy() for _ in
                                                 range(len(self.collxn))]
            # newdf = pd.DataFrame().from_dict({k: [v] * len(self.collxn) for k, v in self.COLLXBLE_CLASS.
            #                                  DEFAULT_MEMBERS().items() if k in new})
            # self.collxn = pd.concat([self.collxn, newdf], axis=1)[self.COLLXBLE_CLASS.CATALOG_FIELDS()[1:]]
            # self.collxn.set_index('id', inplace=True)

    # @abc.abstractmethod
    def updateHeaderData(self):
        """Updates self.headerData to reflect the current state of the Catalog."""
        self.headerData['FILE TYPE'] = self.__class__.__name__
        self.headerData['DATE WRITTEN'] = pd.Timestamp.now().date()
        # self.headerData['TASK ID RANGE'] = portion.closed(self.collxn.firstTask)
        self.headerData['COLLECTIBLE TYPE'] = self.COLLXBLE_CLASS.name()
        self.headerData['CATALOG COUNT'] = len(self)

    def getEmptyCollxn(self)-> pd.DataFrame:
        """Returns an empty Catalog instance of the appropriate type for the Collectible class."""
        return pd.DataFrame(columns=self.COLLXBLE_CLASS.CATALOG_FIELDS()).set_index('id')

    @abc.abstractmethod
    def diff(self, other):
        """
        Prints the difference between two catalogs.
        Used to show how a catalog would be updated before writing it to disk.
        :param other:
        :return:
        """
        raise NotImplementedError('Abstract method not implemented in child class')

    @abc.abstractmethod
    def removeIDs(self, ids: Iterable[int]) -> None:
        """
        Removes Collectibles with the given ids from the Catalog. If an id is not present in the Catalog, it is ignored.
        """
        pass

    # def getMostRecent(self, dt: datetime.datetime) -> Collectible:
    #     if is_list_like(dt):
    #         return kiwilib.mapOverListLike(lambda x: self.getMostRecent(x), dt)
    #     byFirst = self.collxn.sort_values('firstTime')
    #     if dt < kiwilib.dt64_2_dt(byFirst.head(1)['firstTime'].values[0]):
    #         return None
    #     else:
    #         ind = byFirst['firstTime'].searchsorted(dt, side='right')
    #         return self.getObjects(byFirst.iloc[[ind - 1]])[0]

    def updateScalingFields(self, timesheetdf: TimesheetDataFrame, reset=tuple()) -> None:
        """
        Updates the set of Catalog fields which may change as new instances of Collectibles are found in the dataset
        over time.
        Updates timesheetdf in-place when extracting Reviewable Review enums from the 'mood' field.
        Collectible fields: lastTaskID, lastTime, timeSpent, taskCount
        Collectible subclass fields: numReruns
        :param reset: Collxble class names whose scaling fields should be reset to the defaults. Use 'all' to reset all.
        Only true when starting over with collection of scaling fields after, e.g., new previous data cleaning is added.
        :param timesheetdf: Data from which the updates to the Catalog data are retrieved.
        """
        # TODO: migrate ops dependent on issubclass() calls to Collectible methods
        if self.COLLXBLE_CLASS.name() in reset or 'all' in reset:
            self.headerData['TASK ID RANGE'] = portion.empty()
            for fld in self.COLLXBLE_CLASS.SCALABLE_FIELDS():
                self.collxn.loc[:, fld] = self.COLLXBLE_CLASS.DEFAULT_MEMBERS()[fld]
        if issubclass(self.COLLXBLE_CLASS, Media):
            hasCollxble = timesheetdf.df[~timesheetdf.isEmpty(self.COLLXBLE_CLASS.name())].tsdf.\
                filterMedia(self.COLLXBLE_CLASS.name()).df
        else:
            hasCollxble = timesheetdf.df[~timesheetdf.isEmpty(self.COLLXBLE_CLASS.name())]
        cids = np.unique([self.COLLXBLE_CLASS.foreignKeyToCatalogKey(a) for a in
                         kiwilib.flatten(hasCollxble[self.COLLXBLE_CLASS.dfcolumn()], numLevels=1)])
        if self.COLLXBLE_CLASS.NULL_INSTANCE().id in cids:
            raise KeyError(f'Null instance of {self.COLLXBLE_CLASS} found in the tsdf.')
        for cid in cids: # Loop over the collectible IDs contained in timesheetdf
            # if cid in ['FIRST BREAK ALL THE RULES_00994', 'SECOND FOUNDATION_00473']:
            #     a = 1
            if cid not in self.collxn.index:
                raise KeyError(f'{cid} not found in the catalog.')
            catRow = self.collxn.loc[cid, :]  # Can't assign to catRow since it's a copy, but useful for conditionals
            if issubclass(self.COLLXBLE_CLASS, Global.ListColumn):
                tsdfRows = hasCollxble.loc[hasCollxble.tsdf.isinListColumn(self.getObjects(ids=(cid,))[0]), :]
            elif issubclass(self.COLLXBLE_CLASS, Global.SingleInstanceColumn):
                raise NotImplementedError('SingleInstanceColumns yet to be implemented')
            else:
                raise TypeError(f'{self.COLLXBLE_CLASS} should inherit from ListColumn or SingleInstanceColumn')
            if tsdfRows.head(1).index < catRow.firstTaskID:  # Rare, if a Collxble instance before its firstTaskID found
                changedID = False
                if catRow.name != catRow['name']:  # If not BareNameID, also need to update the ID in tsdf
                    changedID = True
                    tsdfRows.tsdf.deleteItem(self.getObjects(ids=(cid,)))
                firstFields = self.COLLXBLE_CLASS.getFirstFieldDicts(tsdfRows.head(1).tsdf)[0]
                warnings.warn(f"Found an instance of {self.COLLXBLE_CLASS.__name__} {oldCid} "
                              f"older than the cataloged earliest instance.\n"
                              f"Cataloged first time: {self.collxn.at[cid, 'firstTime']}\n"
                              f"New first time: {firstFields['firstTime']}")
                for fld in set(firstFields.keys()).intersection(self.collxn.columns):
                    self.collxn.at[cid, fld] = firstFields[fld]
                if changedID:
                    oldCid = cid
                    collxble = self.getObjects(ids=(cid,))[0]
                    cid = collxble.id
                    self.collxn.rename(index={oldCid: cid}, inplace=True)
                    tsdfRows.tsdf.addItem(collxble)
            if pd.isna(catRow.lastTaskID) or tsdfRows.index[-1] > catRow.lastTaskID:
                self.collxn.at[cid, 'lastTaskID'] = tsdfRows.index[-1]
                self.collxn.at[cid, 'lastTime'] = tsdfRows.end.iloc[-1]
            if pd.isna(catRow.timeSpent):
                self.collxn.at[cid, 'timeSpent'] = tsdfRows.duration.sum()
                self.collxn.at[cid, 'taskCount'] = len(tsdfRows)
            else:
                unlogged = \
                    tsdfRows.loc[np.vectorize(lambda x: x not in self.headerData['TASK ID RANGE'])(tsdfRows.index)]
                self.collxn.at[cid, 'timeSpent'] += unlogged.duration.sum()
                self.collxn.at[cid, 'taskCount'] += len(unlogged)
            if issubclass(self.COLLXBLE_CLASS, Reviewable) and not issubclass(self.COLLXBLE_CLASS, ManuallyReviewable) \
                    and pd.isna(catRow.review) and tsdfRows.index[0] == catRow.firstTaskID:
                # Clear review-initing mood from timesheetdf and assign the Review to the Catalog entry
                self.collxn.at[cid, 'review'] = \
                    self.COLLXBLE_CLASS.getFirstFieldDicts(timesheetdf.df.loc[[tsdfRows.index[0]]].tsdf)[0]['review']
                timesheetdf.df.at[tsdfRows.index[0], 'mood'] = Global.Mood.NEUTRAL
            if issubclass(self.COLLXBLE_CLASS, MonolithicMedia) and \
                    portion.closed(*tsdfRows.iloc[[0, -1], :].index) not in self.headerData['TASK ID RANGE']:
                if self.collxn.at[cid, 'firstTaskID'] not in catRow.startTaskIDs:
                    startIDs = sorted([min(catRow.startTaskIDs)] + list(tsdfRows.index))
                else:
                    startIDs = sorted([max(catRow.startTaskIDs)] + list(tsdfRows.index))
                # Include the last already-selfed taskID and all taskIDs in the current TsDF
                # TODO: The above line isn't robust for instances which take on the order of rerunMinInterval()
                #  to complete consumption. numReruns may be logged too high in that case. Update if needed.
                startInterval = reduce(lambda x, y: x | y, [portion.closedopen(tid, tid + 10) for tid in startIDs])
                # Assemble a non-atomic interval. +10 assumes a duration of 1 minute for each task
                consolidated = kiwilib.consolidateInterval(startInterval, Global.timedelta2taskID(
                    self.COLLXBLE_CLASS.rerunMinInterval()))
                self.collxn.at[cid, 'numReruns'] += len(consolidated) - 1
                if self.collxn.at[cid, 'firstTaskID'] not in catRow.startTaskIDs:  # If just found an earlier firstTask
                    if len(consolidated) == 1:  # Earlier tasks are part of same rerun as was logged.
                        self.collxn.at[cid, 'startTaskIDs'].remove(min(catRow.startTaskIDs))  # Delete old rerun taskID
                    self.collxn.at[cid, 'startTaskIDs'].update([a.lower for a in consolidated])
                else:
                    self.collxn.at[cid, 'startTaskIDs'].update([a.lower for a in consolidated[1:]])
            if issubclass(self.COLLXBLE_CLASS, Food) and \
                    portion.closed(*tsdfRows.iloc[[0, -1], :].index) not in self.headerData['TASK ID RANGE']:
                cookIDs, _ = self.COLLXBLE_CLASS.getAutofillRows(tsdfRows.tsdf)
                if len(cookIDs) > 0:
                    startInterval = reduce(lambda x, y: x | y, [portion.closedopen(tid, tid + 10) for tid in cookIDs])
                    consolidated = kiwilib.consolidateInterval(startInterval, Global.timedelta2taskID(
                        self.COLLXBLE_CLASS.rerunMinInterval()))
                    self.collxn.at[cid, 'startTaskIDs'].update([a.lower for a in consolidated])
            if issubclass(self.COLLXBLE_CLASS, Person) and \
                    portion.closed(*tsdfRows.iloc[[0, -1], :].index) not in self.headerData['TASK ID RANGE']:
                circads = tsdfRows.circad.unique()
                self.collxn.at[cid, 'whenWith'] |= \
                    reduce(lambda x, y: x | y, (portion.closedopen(c, c+datetime.timedelta(days=1)) for c in circads))


class LinearCatalog(Catalog):
    # def collect(self, collxbles: Union[dict, Iterable[dict], Collectible, Iterable[Collectible]]) -> None:
    #     # TODO: add support for specifying overwrite behavior
    #     if isinstance(collxbles, self.COLLXBLE_CLASS):
    #         self.collect((collxbles,))
    #         return
    #     if collxbles is None or len(collxbles) == 0:
    #         return
    #     if not isinstance(collxbles[0], dict):  # collxbles must be Iterable[Collectible]
    #         collxbles = [item.toCatalogDict() for item in collxbles if not self.hasCollectible(item)]
    #     if not collxbles or len(collxbles) == 0:
    #         return
    #     if 'id' not in collxbles[0].keys():
    #         for item in collxbles:
    #             item['id'] = self.COLLXBLE_CLASS.generateID(**item)
    #     self.collxn = pd.concat((self.collxn, pd.DataFrame(collxbles).set_index('id')))

    # def getNewlyAdded(self) -> List[Collectible]:
    #     return self.getObjects(self.collxn[self.collxn.firstTaskID.apply(lambda x: x in
    #                                                                                self.headerData['TASK ID RANGE'])])

    def read(self, file: str=None) -> None:
        yamlData = self._readYaml(file)
        if not yamlData:
            return
        # if issubclass(self.COLLXBLE_CLASS, IncompletePersistent):
        self.collxn = self.getEmptyCollxn()
        self.updateFields()
        self.collect([self.COLLXBLE_CLASS(**d) for d in yamlData])
        # else:
        #     self.collxn = pd.DataFrame.from_records(yamlData)
        #     self.collxn.set_index('id', inplace=True)

    def diff(self, other):
        pass # TODO: Catalog diff

    def removeIDs(self, ids: Iterable[int]) -> None:
        self.collxn.drop(ids, axis=0)


class DAGCatalog(Catalog):
    """
    Directional acyclic graph. Used for cataloging hierarchical Collectibles.
    Graph edges defining the hierarchy point from child>>parent, or specific>>general.
    collxbleClass: Location, Food, SubjectMatter
    """

    def __init__(self, COLLXBLE: type, loadYaml=True, file=None):
        if not issubclass(COLLXBLE, DAGCollectible):
            raise TypeError(
                f'{type(self).__name__} cannot use type {COLLXBLE}. Type must be a subclass of DAGCollectible.')
        super().__init__(COLLXBLE, loadYaml, file)
        if not hasattr(self, 'dag'):
            self.dag: nx.DiGraph = self.COLLXBLE_CLASS.emptyDAG()

    def __eq__(self, other):
        return super().__eq__(other) and isinstance(other, type(self)) and \
               other.dag.nodes() == self.dag.nodes() and nx.is_isomorphic(self.dag, other.dag)
        # nx.utils.graphs_equal(self, other)  # This didn't have the desired behavior

    def _getYamlable(self) -> List[Iterable]:
        return [super()._getYamlable(), {'adj': self.dag.adj._atlas}]

    def write(self, file=None):
        # Maybe not abstract, depends on if tree can be yaml'd easily
        self.updateHeaderData()
        data = self._getYamlable()
        if file is None:
            if len(data[0]) > 1 and set(data[0][1].keys()) - set(self.COLLXBLE_CLASS.CATALOG_FIELDS()) != set():
                raise KeyError(f'When writing to the default catalog file, fields:\n'
                               f'{set(data[1].keys()) - set(self.COLLXBLE_CLASS.CATALOG_FIELDS())}\nare not allowed')
            file = self.CATALOG_FILE
        with open(file, 'w') as yamlfile:
            yaml.dump_all(data, yamlfile, sort_keys=False)

    def _readYaml(self, file: str = None) -> dict:
        """
        Helper function to implement common functionality of file reading.
        :param file: Optional file path. Defaults to self.CATALOG_FILE.
        :return: None: No yaml data available, and construction of self.collxn is complete.
         not None: data read from yaml file. Subclass read() methods use this data to construct self.collxn.
         For DAGCatalog, len(yamlData) should always be 2, since yaml files should contain 2 documents.
         Doc 1: list=Same as LinearCatalog. Header, then list entry for each Collectible.
         Doc 2: dict=Adjacency list
        """
        if not file: file = self.CATALOG_FILE
        if not os.path.isfile(file):
            self.collxn = self.getEmptyCollxn()
            self.dag = self.COLLXBLE_CLASS.emptyDAG()
            return None
        with open(file, 'r') as yamlfile:
            yamlData = [a for a in yaml.safe_load_all(yamlfile)]
        if not yamlData:
            self.collxn = self.getEmptyCollxn()
            self.dag = self.COLLXBLE_CLASS.emptyDAG()
            self.headerData = next(iter(self._METADATA_HEADER_DEFAULT.values()))
            return None
        elif not (isinstance(yamlData[0], list) and len(yamlData) == 2 and isinstance(yamlData[1], dict)):
            raise TypeError(f'Yaml structure is not correct {type(self)} format.')
        elif next(iter(yamlData[0][0])) == next(iter(self._METADATA_HEADER_DEFAULT)):  # [0][0] entry is file header
            self.headerData = yamlData[0][0][next(iter(self._METADATA_HEADER_DEFAULT))]
            return [yamlData[0][1:], yamlData[1]]
        else:  # No header present in file
            self.headerData = next(iter(self._METADATA_HEADER_DEFAULT.values())).copy()
            return yamlData

    def read(self, file: str=None) -> None:
        yamlData = self._readYaml(file)
        if yamlData is None:
            return
        # if issubclass(self.COLLXBLE_CLASS, IncompletePersistent):
        if len(yamlData[0]) == 0:  # If an empty DAGCatalog was read
            self.collxn = self.getEmptyCollxn()
            self.dag = self.COLLXBLE_CLASS.emptyDAG()
        elif 'adj' in yamlData[1] and len(yamlData[1]['adj']) > 0:  # If there is some data in yaml adj
            self.collxn = pd.DataFrame.from_records(yamlData[0])
            self.collxn.set_index('id', inplace=True)
            self.dag = nx.DiGraph(yamlData[1]['adj'])
        else:
            self.dag = self.COLLXBLE_CLASS.emptyDAG()
            self.collect([self.COLLXBLE_CLASS(**d) for d in yamlData[0]])
        self.updateFields()
        self.validate()
        # TODO: validate dag read from yaml

    def collect(self, collxbles: Union[dict, Iterable[dict], Collectible, Iterable[Collectible]]) -> None:
        super().collect(collxbles)
        # if isinstance(collxbles, Collectible):
        verts = self.collxn.loc[~self.collxn.index.isin(self.dag.nodes), :].index
        self.dag.add_edges_from([(v, self.COLLXBLE_CLASS.undefinedVertex(), {'p': 0}) for v in verts])
        # else:
        #     self.dag.add_nodes_from([c.id for c in collxbles])

    def diff(self, other):
        raise NotImplementedError

    def removeIDs(self, ids: Iterable[int]) -> None:
        raise NotImplementedError

    def children(self, cid: str, deep=False) -> List[str]:
        """
        Returns the children of a given vertex.
        'Children' is defined in the sense of the hierarchy, not the abstracted graph edge directionality.
        TODO: implement explicit sequencing of the output list. Probably sort on edge weights.
        :param cid: Collxble id as produced by collxble.generateID().
        :param deep: If True, returns all descendants in the DAG until leaf vertices found.
        If False, returns only the immediate descendants of the given id.
        """
        if deep:
            return list(nx.ancestors(self.dag, cid))
        else:
            return sorted(list(self.dag.pred[cid]), key=lambda x: self.dag.pred[cid][x]['p'])

    def parents(self, cid: str, deep: bool = False, sort: bool = False, primary: bool = False) -> List[str]:
        """
        Same as children(), except in the opposite direction.
        :param cid: Collxble id as produced by collxble.generateID().
        :param deep: If True, returns all parents in the DAG up to and including the root vertex.
        :param sort: If True and deep==False, the list is sorted by edge weight.
        If deep==True, the ancestry list is sorted by nx.bfs_successors, each sublayer sorted by edge weight.
        :param primary: If True and deep=False, returns a length-1 list with the parent with the smallest edge weight.
        If True and deep=True does this iteratively up the DAG until the root vertex.
        """
        def sortedGenerator(cid1: str) -> typing.Generator:
            for vertex in sorted(list(self.dag.adj[cid1].keys()), key=lambda x: self.dag.adj[cid1][x]['p']):
                yield vertex

        if primary:
            # TODO: implement primary=True. Used for pseudo-mro, primary parental path.
            raise NotImplementedError
        if deep and not sort:
            # out = self.parents(cid, deep=False)
            # nx.bfs self.dag
            return list(nx.descendants(self.dag, cid))
        elif deep and sort:
            return list(kiwilib.flatten(
                (a[1] for a in nx.bfs_successors(self.dag, cid, sort_neighbors=sortedGenerator(cid)))))
        elif not deep and not sort:
            return list(self.dag.adj[cid].keys())
        elif not deep and sort:
            return sorted(self.parents(cid, deep=False, sort=False, primary=primary),
                          key=lambda x: self.dag.adj[cid][x]['p'])

    def validate(self) -> None:
        """
        Checks for consistency between the contents of self.collxn, self.dag,
        and the default DAG contents defined in self.COLLXBLE_CLASS.emptyDAG().
        """
        assert set(self.collxn.index).union(self.COLLXBLE_CLASS.emptyDAG().nodes) == set(self.dag.nodes), \
            f'Inconsistent DAG vertices and collxn ids: ' \
            f'{set(self.collxn.index).union(self.COLLXBLE_CLASS.emptyDAG().nodes) ^ set(self.dag.nodes)} ' \
            f'in one set but not the other.'
        # Check that the set of catalog entries is consistent between self.collxn and self.dag
        assert nx.is_directed_acyclic_graph(self.dag), f'Not a DAG; cycle(s): {[c for c in nx.simple_cycles(self.dag)]}'
        # Check that all vertices are children of root vertex.
        assert len(self.children(self.COLLXBLE_CLASS.rootVertex(), deep=True)) == len(self.dag)-1


CATALOG_SUBCLASS_STRING_MAP = {cls.__name__: cls for cls in kiwilib.getAllSubclasses(Catalog, includeSelf=False)}
