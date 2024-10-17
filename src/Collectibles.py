import abc
import datetime
import anytree
import pandas as pd
from yamlable import YamlAble, yaml_info
import portion
import networkx as nx
from typing import Union, Iterable, List, Tuple, Set, Sequence

from src.TimesheetDF import TimesheetDataFrame
import src.TimesheetGlobals as Global
import src.DescriptionSTDLISTS as STDList
import catalogs.SocialGroups as sg
import catalogs.Genres as genres
from external_modules import kiwilib


class Collectible(abc.ABC):
    """
    Leaf classes: Person Audiobook TVShow Movie Podcast Software VideoGame TabletopGame Location Food
    Abstract class of unique items which are collected and cataloged to a file.
    """
    # _INITIALIZATION_FILTER: str
    _CATALOG_FIELDS: list
    _NULL_INSTANCE = None
    # COLS_NOT_CATALOGED = set()  # Set of columns to be excluded when a Catalog of this Collectible class is serialized
    # Fields in COLS_NOT_CATALOGED should be populated in the constructor.

    @staticmethod
    @abc.abstractmethod
    def DEFAULT_MEMBERS() -> dict:
        """
        Holds default values for data members not required at instantiation.
        If data members in the class definition are added between writing and reading a catalog,
        this is referenced to determine the empty values with which to populate the new Catalog columns.
        The order of keys in this dict determines the order of columns in the Catalog.
        """
        return {
            'timeSpent': pd.NA,  # Sum of task durations containing this collectible.
            'taskCount': pd.NA,  # qty of tasks with this Collxble. Same caveats as timeSpent
            'lastTaskID': pd.NA,  # timesheetdf ID when the Collectible last appeared
            'lastTime': pd.NA  # datetime when the Collectible last appeared in the complete dataset
        }

    @classmethod
    @abc.abstractmethod
    def CATALOG_FIELDS(cls) -> list:
        """
        Contains the comprehensive list of fields to be stored in Catalogs of this Collectible subclass.
        The order of keys in this list determines the order of columns in the Catalog.
        firstTaskID: timesheetdf ID where the Collectible first appeared
        firstTime: datetime when the Collectible first appeared
        firstCircad: circad when the Collectible first appeared
        """
        if not hasattr(cls, '_CATALOG_FIELDS') or len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = ['id', 'name', 'firstTaskID', 'firstTime', 'firstCircad'] + \
                                  list(cls.DEFAULT_MEMBERS().keys())
        return cls._CATALOG_FIELDS

    @classmethod
    def SCALABLE_FIELDS(cls) -> list:
        """
        Subset of catalog fields which accumulate/scale/otherwise change as more tsdf data is processed.
        Excludes fields that don't need to be reset to default values for a fresh update, e.g., Person.whenWith.
        """
        return ['timeSpent', 'taskCount']

    def __init__(self, **kwargs):
        """
        Initializes a Collectible or subclass instance based on the provided kwargs.
        The elements in CATALOG_FIELDS and not in DEFAULT_MEMBERS are required to be passed in kwargs.
        kwargs may contain keys in DEFAULT_MEMBERS, which will override the defined default values.
        All other keys in kwargs are ignored.
        :param kwargs: Dictionary containing values for at least the minimal set of initialization parameters.
        """
        requiredKeys = set(self.CATALOG_FIELDS())-set(self.DEFAULT_MEMBERS())
        if len(requiredKeys-set(kwargs.keys())-{'id'}) > 0:
            raise KeyError(f'Missing required initialization parameters: {requiredKeys-set(kwargs.keys())}')
        for key in set(kwargs.keys()).intersection(self.CATALOG_FIELDS()[1:]):  # Exclude 'id' field
            if key in self.DEFAULT_MEMBERS() and not any(pd.isna([self.DEFAULT_MEMBERS()[key], kwargs[key]])) and\
                type(self.DEFAULT_MEMBERS()[key]) != type(kwargs[key]):
                # Cast the value read from kwargs to the type in self.DEFAULT_MEMBERS()
                self.__setattr__(key, type(self.DEFAULT_MEMBERS()[key])(kwargs[key]))
            else:
                self.__setattr__(key, kwargs[key])
        self.id = self.generateID(**kwargs)
        for key in set(self.DEFAULT_MEMBERS().keys())-set(kwargs.keys()):
            self.__setattr__(key, self.DEFAULT_MEMBERS()[key])  # Could cause issues with not copying object types

        """
        The sequence of defining data members matters for CATALOG_FIELDS.
        A specific order is desired for the members of CATALOG_FIELDS in Collectible and in each subclass.
        Since dictionaries preserve insertion order, CATALOG_FIELDS will reflect that insertion order. 
        """

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        if self.name == other.name:
            return self.firstTime < other.firstTime
        else: return self.name < other.name

    def __le__(self, other):
        if self.name == other.name:
            return self.firstTime <= other.firstTime
        else: return self.name <= other.name

    def __gt__(self, other):
        if self.name == other.name:
            return self.firstTime > other.firstTime
        else: return self.name > other.name

    def __ge__(self, other):
        if self.name == other.name:
            return self.firstTime >= other.firstTime
        else: return self.name >= other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{str(type(self)).split(".")[-1][:-2]}: {self.id}'

    @classmethod
    def dfcolumn(cls):
        return cls.__name__.lower()

    @classmethod
    def name(cls):
        """ Should never be overridden in subclasses"""
        return cls.__name__.lower()

    @classmethod
    def tempInitToken(cls):
        """
        A token added to the Description to indicate a Collectible instance when no other is already present.
        The token is added in PP and removed near the end of DC initCatalogs.
        """
        return '$' + cls.__name__.upper()

    @classmethod
    @abc.abstractmethod
    def INITIALIZATION_TSQY(cls) -> str:
        """TimesheetQuery string to filter a df down to only initializable rows for that class"""
        pass

    @classmethod
    @abc.abstractmethod
    def INITIALIZATION_TOKENS(cls) -> Tuple[str]:
        """Usually just all tokens that appear in `INITIALIZATION_TSQY`, but in a tuple."""
        pass

    @classmethod
    def INITIALIZATION_TOKENS_TO_CLEAR(cls) -> Tuple[str]:
        """Subset of `INITIALIZATION_TOKENS` which should be cleared after populating the tsdf with a Collectible."""
        return cls.INITIALIZATION_TOKENS()

    @classmethod
    @abc.abstractmethod
    def POPULATION_TSQY(cls):
        """
        A tsqy to detect instances of a Collxble in a tsdf after the Collxble has been initialized.
        Used in TimesheetDataset.catalogPopulateDF().
        """
        return ' : ;'

    @staticmethod
    @abc.abstractmethod
    def CATALOG_CLASS() -> str:
        """
        String representation of the Catalog subclass for this Collectible subclass.
        The mapping of strings to classes is defined in Catalog.
        """
        pass

    @classmethod
    def NULL_INSTANCE(cls):
        """
        Defines an instance representing a null Collectible.
        A placeholder for null values like pd.NA, except that the particular Collectible subclass is known.
        """
        # TODO: do leaf classes each need their own _NULL_INSTANCE in the class definition?
        if cls._NULL_INSTANCE is None:
            cls._NULL_INSTANCE = cls(name=cls.name()+'_NULL', firstTaskID=0, firstTime=Global.TASK_ID_EPOCH,
                                     firstCircad=Global.TASK_ID_EPOCH.date())
        return cls._NULL_INSTANCE


    @staticmethod
    def generateID(**kwargs):
        return f'{kwargs["name"]}_{(kwargs["firstCircad"]-Global.TASK_ID_EPOCH.date()).days:05}'

    @classmethod
    def getFirstFieldDicts(cls, timesheetdf: TimesheetDataFrame):
        return timesheetdf.df[['start', 'circad']].reset_index().rename(columns={
            'id': 'firstTaskID', 'start': 'firstTime', 'circad': 'firstCircad'}).to_dict(orient='records')

    @classmethod
    @abc.abstractmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> list:
        """
        Processes a TsDF and returns a list of all the Collectibles found.
        Uses detection criteria to filter the DataFrame rows to only those containing/initiating new Collectibles.
        Scrapes data from each initiating row to instantiate a Collectible instance.
        :param timesheetdf: df to process
        :return: List of Collectible objects
        """
        # def detectUnpopulated() -> TimesheetDataFrame:
        return timesheetdf.tsquery(cls.INITIALIZATION_TSQY())
        # timesheetdf = detectUnpopulated()

    @classmethod
    def tsdfPopulationFilter(cls, timesheetdf: TimesheetDataFrame, collxs: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """
        Filters a set of proposed Collxble instance populations encoded in `collxs` using the data in `timesheetdf`.
        This method should be overridden in subclasses only when `cls.POPULATION_TSQY` is insufficiently precise/powerful.
        This method is only called in `Catalog.populateDF`. It may be assumed that `cls.POPULATION_TSQY` has already been applied when `collxs` was constructed.
        Arguments are not mutated.
        :param collxs: pd.Series[int, Iterable(str)] An encoding of potential Collxble instances to be later populated in `timesheetdf`.
        Each row in `collxs` indicates a set of collxbles with names corresponding to those tokens should be added to the row in `timesheetdf` that shares that index.
        :return: [0]: pd.Series[int, str] = A subset of `collxs` where each token appears exactly once in the task description in `timesheetdf`.
        [1]: pd.Series[int, anytree.Node] = Covers rare cases when the token in `collxs` appears >1 time in the task description in `timesheetdf`.
        In those instances, an entry is created in this series with similar data format as `return[0]`, 
        except that the token is represented by its `anytree.Node` object rather than simply a string, to differentiate it from duplicate tokens.
        """
        return collxs, pd.Series([], dtype="object")

    @classmethod
    @abc.abstractmethod
    def processingPrecedence(cls) -> int:
        """
        Int to set the sequence of processing of Collectible leaf classes in the TimesheetDataset.cats field.
        Smaller numbers are processed first. Range is approximately range(0,50)
        """
        pass

    def foreignKey(self):
        """
        Returns the foreign key to be stored in the TimesheetDataFrame to represent the Collectible.
        Default behavior is to return the Collectible's id. Some subclasses override this behavior.
        """
        return self.id

    @staticmethod
    def foreignKeyToCatalogKey(key):
        """
        Extracts the catalog key from a given foreign key, somewhat like an inverse of foreignKey().
        Update this procedure if foreignKey() is updated.
        """
        return key

    def toCatalogDict(self):
        catDict = self.__dict__
        keysToPop = set(self.CATALOG_FIELDS()) - set(catDict.keys())
        for key in keysToPop:
            catDict.pop(key)
        return catDict


class DAGCollectible(Collectible, abc.ABC):
    """
    All Collectibles which are stored in a DAGCatalog.
    """
    @staticmethod
    def CATALOG_CLASS() -> str:
        return 'DAGCatalog'

    @classmethod
    def rootVertex(cls) -> str:
        """Name of the root vertex in DAGCatalog.dag, the ultimate successor of all vertices."""
        return f'${cls.name().upper()}'

    @classmethod
    def undefinedVertex(cls) -> str:
        """
        Name of the vertex in DAGCatalog.dag used to mark instances whose location in the DAG is yet unprocessed.
        By default, new vertices will be added with this vertex as successor by DAGCatalog.collect().
        """
        return f'{cls.rootVertex()}_UNDEFINED'

    @classmethod
    def _emptyDAG(cls) -> nx.DiGraph:
        """
        Helper method to emptyDAG(). Should be called by subclasses
        """
        p = {'p': 0}
        return nx.DiGraph({
            cls.rootVertex(): {},
            cls.undefinedVertex(): {cls.rootVertex(): p},
        })

    @classmethod
    def emptyDAG(cls) -> nx.DiGraph:
        """
        The DAG template instantiated by the DAGCatalog constructor.
        Should include all vertices and edges not contained in the source data.
        Subclasses overriding this method should extend the graph returned by cls._emptyDAG(), not modify that portion.
        Conventions:
        Vertices starting with a '$' are not members of the dataset, but are rather used for metadata classifiers.
        If an analysis using a given vertex would be classifying as a metadata analysis rather than data analysis,
        then that vertex should probably be labeled using '$'.
        See Food.emptyDAG() for an example of the division between metadata classifiers and dataset members.
        """
        return cls._emptyDAG()


class Media(Collectible, Global.ListColumn):
    """
    Leaf classes: Audiobook, TV, movie, podcast, video games, software, tabletop games
    """
    _DEFAULT_MEMBERS = {}  # Populated in classmethod
    _CATALOG_FIELDS = []  # Populated in classmethod
    _EXTERNAL_DATA_SOURCE: str  # Used at some point in pullExternalData

    @classmethod
    @abc.abstractmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = {**super(Media, cls).DEFAULT_MEMBERS(), **{
                'creator': pd.NA,
                'creationTime': pd.NA,
                'genres': {genres.GenreUndefined(), },
                # 'durationConsumed': pd.NaT,
            }}
        return cls._DEFAULT_MEMBERS

    @classmethod
    @abc.abstractmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(super(Media, cls).CATALOG_FIELDS() +
                                                     list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    @staticmethod
    def CATALOG_CLASS() -> str:
        return 'LinearCatalog'

    def foreignKey(self) -> tuple:
        """
        Returns the foreign key to be stored in the TimesheetDataFrame to represent the Collectible.
        :return: Tuple containing the class name and the Collectible's id
        """
        return type(self), self.id

    @staticmethod
    def foreignKeyToCatalogKey(key) -> str:
        """
        Extracts the catalog key from a given foreign key, somewhat like an inverse of foreignKey().
        Update this procedure if foreignKey() is updated.
        """
        return key[1]

    def isGenre(self, genre: genres.Genre) -> bool:
        """
        Returns true if any member of self.genres are an instance or subclass of the given genre
        :param genre: A subclass of genres.Genre
        """
        return any([isinstance(g, genre) for g in self.genres])

    @classmethod
    @abc.abstractmethod
    def isActive(cls) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def EXTERNAL_DATA_SOURCE(cls) -> str:
        return cls._EXTERNAL_DATA_SOURCE

    @abc.abstractmethod
    def pullExternalData(self):
        pass

    @classmethod
    def dfcolumn(cls):
        return 'media'


class ConsumptionMedia(Media, abc.ABC):
    """Audiobook, Podcast, TV, Movie.
    Any passive media which has a well-defined start and end, which may be fully consumed by traversing the full span.
    """
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    @classmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = {**super(ConsumptionMedia, cls).DEFAULT_MEMBERS(), **{
                'subjectMatters': set(),
            }}
        return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(super(ConsumptionMedia, cls).CATALOG_FIELDS() +
                                                     list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    @classmethod
    def isActive(cls) -> bool:
        return False


class StartIDsCataloged(Collectible, abc.ABC):
    """
    Movie, Audiobook, Location.
    startTaskIDs: Set of taskIDs indicating the start of time intervals when that Collxble instance is active.
    Used by AutofillPrevious to find the current active Collxble to fill unmarked instances at the start of data files.
    """
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    @classmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = {**super(StartIDsCataloged, cls).DEFAULT_MEMBERS(), **{
                'startTaskIDs': set()  # Default value in __init__
            }}
        return cls._DEFAULT_MEMBERS

    # @classmethod
    # def CATALOG_FIELDS(cls):
    #     if len(cls._CATALOG_FIELDS) == 0:
    #         cls._CATALOG_FIELDS = list(dict.fromkeys(super(StartIDsCataloged, cls).CATALOG_FIELDS() +
    #                                                  list(cls.DEFAULT_MEMBERS().keys())))
    #     return cls._CATALOG_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.startTaskIDs) == 0:
            self.startTaskIDs = {self.firstTaskID, }

    @classmethod
    @abc.abstractmethod
    def rerunMinInterval(cls) -> datetime.timedelta:
        """
        :return: Timedelta above which 2 instances of an object in a TsDF are considered as reruns rather than a
        continuation of a single consumption run.
        """


class MonolithicMedia(ConsumptionMedia, StartIDsCataloged, abc.ABC):
    """
    Movie, Audiobook. Media which is contained in a single, contiguous unit.
    numReruns supports manual editing in yaml to account for consumption instances outside the data collection period.
    """
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    @classmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = {**super(MonolithicMedia, cls).DEFAULT_MEMBERS(), **{
                'duration': pd.NaT,
                'numReruns': 1,  # How many times has this been watched/read/consumed?
            }}
        return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(super(MonolithicMedia, cls).CATALOG_FIELDS() +
                                                     list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    @classmethod
    def SCALABLE_FIELDS(cls) -> list:
        return super(MonolithicMedia, cls).SCALABLE_FIELDS() + ['numReruns']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if pd.isna(self.numReruns):
            self.numReruns = self.DEFAULT_MEMBERS()['numReruns']


class Reviewable(Media):
    """
    Leaf classes: BOok, Podcast, TVShow, Movie, VideoGame
    Any Collectible which can be reviewed.
    """
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    @classmethod
    @abc.abstractmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = {**super(Reviewable, cls).DEFAULT_MEMBERS(), **{
                'review': pd.NA,
                'externalReview': pd.NA,
            }}
        return cls._DEFAULT_MEMBERS

    @classmethod
    @abc.abstractmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(super(Reviewable, cls).CATALOG_FIELDS() + list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    @classmethod
    def getFirstFieldDicts(cls, timesheetdf: TimesheetDataFrame):
        # timesheetdf.df.loc[:, 'review'] = timesheetdf.df['mood'].apply(sg.Review.moodMap)
        timesheetdf.df['review'] = timesheetdf.df['mood'].apply(sg.Review.moodMap)
        return timesheetdf.df.loc[:, ['start', 'circad', 'review']].reset_index().rename(columns={
            'id': 'firstTaskID', 'start': 'firstTime', 'circad': 'firstCircad'
            }).to_dict(orient='records')

    # def pullReview(self, timesheetdf: TimesheetDataFrame) -> int:
    #     """
    #     Assigns the pre-filtered dataframe mood field to the Reviewable review field.
    #     The review will be pulled from the first row in timesheetdf which contains self.foreignKey()
    #     """
    #     # TODO: pullReview
    #     # {review = df.mood; df.mood = 0}
    #     # Don't know if thie can work, may have to do manually outside or figure something with pointers
    #     # Don't know if clearing out of the tsdf mood field should be done here or by the caller
    #     raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def EXTERNAL_REVIEW_SOURCE() -> str:
        pass

    @abc.abstractmethod
    def pullExternalReview(self):
        """Pull data from an external source (the web) to populate externalReview field."""
        # TODO: add common step to access the external review data source class attribute
        raise NotImplementedError


class ManuallyReviewable(Reviewable, abc.ABC):
    """ Reviewable types whose reviews are not present in the dataset. Must be entered manually in the Catalog yaml. """
    @classmethod
    def getFirstFieldDicts(cls, timesheetdf: TimesheetDataFrame):
        return Collectible.getFirstFieldDicts(timesheetdf)


class AutofillPrevious(StartIDsCataloged, abc.ABC):
    """
    For collectibles for which the chronologically previous instance should be autofilled into all future instances
    until a different instance is explicitly specified in the DataFrame.
    Leaf classes: Audiobook, Food, Location
    """

    @classmethod
    @abc.abstractmethod
    def getAutofillRows(cls, timesheetdf: TimesheetDataFrame) -> Tuple[pd.Index, pd.Index]:
        """
        Returns the indices of a given tsdf necessary for TimesheetDataset.autofillPreviousCollectibles().
        :return:
            [0]: sources: Indices of already populated rows defining the source of the autofill operation.
            [1]: targets: Indices of the rows to be autofilled with the Collectible instances in return[0].
        """
        return timesheetdf.df.loc[~timesheetdf.isEmpty(cls.name())].index, \
            timesheetdf.df[timesheetdf.df.description.apply(
                               lambda x: any([x.hasToken(tok) for tok in cls.INITIALIZATION_TOKENS()]))].index

    @staticmethod
    def getPreviousID(startTaskIDs: pd.Series, target: int) -> str:
        """
        Finds the Collxble ID containing the most recent startTaskID before target.
        :param startTaskIDs: pd.Series[Set[int]]
        The 'startTaskIDs' column from a Catalog containing AutofillPrevious Collxbles.
        :param target: Task ID from which the previous ID is to be found.
        :return: Collxble ID
        """
        maxID, prevCID = 0, ''
        # Reverse for efficiency gains by triggering assignment in loop less frequently
        for cid, IDset in startTaskIDs[::-1].items():
            moreRecent = {x for x in IDset if maxID < x <= target}
            if len(moreRecent) > 0:
                prevCID, maxID = cid, max(moreRecent)
        if prevCID == '':
            raise KeyError(f'No collectibles found before {target}')
        return prevCID


class IncompletePersistent(abc.ABC):
    """
    Classes which contain at least 1 data member which is not written to Catalog persistent data.
    """
    @classmethod
    @abc.abstractmethod
    def solveFields(cls):
        """
        Use populated fields to solve for and fill as many unpopulated fields as possible.
        Implementation will be different for every subclass with different field relationships.
        May solve for additional fields beyond those in colsNotCataloged().
        Example: Use a 'birthday' field and the current date to solve for an 'age' field.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def colsNotCataloged(cls) -> Set[str]:
        """
        Returns a set of field names which are not written to Catalog persistent data.
        These fields should be solved for using solveFields() after reading in the Catalog from disk.
        """
        pass


class BareNameID(Collectible, abc.ABC):
    """For Collectibles whose IDs are identical to their names."""
    @staticmethod
    def generateID(**kwargs):
        return kwargs['name']


class Audiobook(MonolithicMedia, Reviewable, AutofillPrevious):
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    # @classmethod
    # def DEFAULT_MEMBERS(cls):
    #     if len(cls._DEFAULT_MEMBERS) == 0:
    #         cls._DEFAULT_MEMBERS = {**super(Audiobook, cls).DEFAULT_MEMBERS(), **{
    #             'audioLength': pd.NaT
    #         }}
    #     return cls._DEFAULT_MEMBERS

    # @classmethod
    # def CATALOG_FIELDS(cls):
    #     if len(cls._CATALOG_FIELDS) == 0:
    #         cls._CATALOG_FIELDS = list(dict.fromkeys(super(Audiobook, cls).CATALOG_FIELDS() + list(cls.DEFAULT_MEMBERS().keys())))
    #     return cls._CATALOG_FIELDS

    def pullReview(self, timesheetdf: TimesheetDataFrame):
        raise NotImplementedError

    @staticmethod
    def EXTERNAL_REVIEW_SOURCE(cls) -> str:
        raise NotImplementedError

    def pullExternalReview(self):
        raise NotImplementedError

    @classmethod
    def EXTERNAL_DATA_SOURCE(cls) -> str:
        raise NotImplementedError

    def pullExternalData(self):
        raise NotImplementedError

    @classmethod
    def INITIALIZATION_TSQY(cls):
        return '"Audiolibro," | "' + cls.tempInitToken() + '" :;'

    @classmethod
    def INITIALIZATION_TOKENS(cls):
        return 'AUDIOLIBRO', cls.tempInitToken()

    @classmethod
    def POPULATION_TSQY(cls):
        return f'"LEER" | "AUDIOLIBRO" | "{cls.tempInitToken()}" | Tag.Lectura | Project.RECREO_LEER : ;'

    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> List[Collectible]:
        # initingRows = Collectible.constructObjects(timesheetdf)  # Rows which each initialize a new instance
        initingRows = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())
        initTokDFs = [initingRows.getDescTokenChildren(prefix).dropna() for prefix in cls.INITIALIZATION_TOKENS()]
        initingIDs = pd.concat(initTokDFs).sort_index().drop_duplicates(keep='first')
        initingIDs.drop(initingIDs.index[initingIDs.apply(lambda x: len(x) == 0)], inplace=True)
        initingRows = initingRows.df.loc[list(initingIDs.index), :].tsdf
        if len(initingRows) == 0: return []
        titles = [{'name': title} for title in initingRows.df.description.apply(
            lambda x: x.tokens[x.tokens.index('AUDIOLIBRO')+1])]  # Get the token after 'audiolibro'
        initFields = cls.getFirstFieldDicts(initingRows)
        initFields = [{**titles[i], **initFields[i]} for i in range(len(titles))]
        return [Audiobook(**bookDict) for bookDict in initFields]

    @classmethod
    def processingPrecedence(cls) -> int:
        return 5  # Relatively early

    @classmethod
    def _getAutofillDF(cls, timesheetdf: TimesheetDataFrame) -> TimesheetDataFrame:
        pass

    @classmethod
    def getAutofillRows(cls, timesheetdf: TimesheetDataFrame) -> Tuple[pd.Index, pd.Index]:
        return super().getAutofillRows(timesheetdf)

    @classmethod
    def rerunMinInterval(cls) -> datetime.timedelta:
        return datetime.timedelta(days=180)


class Podcast(ConsumptionMedia, ManuallyReviewable):
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    # @classmethod
    # def DEFAULT_MEMBERS(cls):
    #     if len(cls._DEFAULT_MEMBERS) == 0:
    #         cls._DEFAULT_MEMBERS = {**super(Podcast, cls).DEFAULT_MEMBERS(), **{
    #             #  Add default members here, if any arise
    #         }}
    #     return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(
                dict.fromkeys(super(Podcast, cls).CATALOG_FIELDS() + list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    # def pullReview(self, timesheetdf: TimesheetDataFrame):
    #     raise NotImplementedError

    @staticmethod
    def EXTERNAL_REVIEW_SOURCE(cls) -> str:
        raise NotImplementedError

    def pullExternalReview(self):
        raise NotImplementedError

    @classmethod
    def EXTERNAL_DATA_SOURCE(cls) -> str:
        raise NotImplementedError

    def pullExternalData(self):
        raise NotImplementedError

    @classmethod
    def INITIALIZATION_TSQY(cls):
        return '"Podcast," | "' + cls.tempInitToken() + ',":;'

    @classmethod
    def INITIALIZATION_TOKENS(cls):
        return 'PODCAST', cls.tempInitToken()

    @classmethod
    def POPULATION_TSQY(cls):
        return Collectible.POPULATION_TSQY()

    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> list:
        initingRows = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())
        initTokDFs = [initingRows.getDescTokenChildren(prefix).dropna() for prefix in cls.INITIALIZATION_TOKENS()]
        initingIDs = pd.concat(initTokDFs).sort_index().drop_duplicates(keep='first')
        initingIDs.drop(initingIDs.index[initingIDs.apply(lambda x: len(x) == 0)], inplace=True)
        initingRows = initingRows.df.loc[list(initingIDs.index), :].tsdf
        if len(initingRows) == 0: return []
        titles = initingRows.df.description.apply(lambda x: [x.getChildToks(tok) if tok in x.tokens else
                                                             None for tok in cls.INITIALIZATION_TOKENS()])
        # Get all child tokens of INITIALIZATION_TOKENS()
        titles = titles.apply(lambda x: [titl for titl in kiwilib.flatten(x) if titl])
        multiple = titles[titles.apply(lambda x: len(x) > 1)]
        titles = titles.apply(lambda x: x[0] if len(x) == 1 else x)
        for id, pods in multiple.items():
            titles[id] = pods[0]
            for pod in pods[1:]:
                titles = pd.concat([titles, pd.Series({id: pod})], axis=0)
        titles.sort_index(inplace=True)
        # titles = [{'name': t} for t in [titl for titl in kiwilib.flatten(titles) if titl]]
        if len(titles) != len(set(titles)):  # Delete the later instances of any duplicate tokens
            for i in range(len(titles)-1, -1, -1):
                if i >= len(titles): continue  # In corner case where .pop() removes 2+ rows, next iteration could fail
                if titles.iloc[i] in titles.iloc[:i].values:
                    titles.pop(titles.index[i])
        initingRows = initingRows.df.loc[initingRows.df.index.isin(titles.index), :].tsdf
        initFields = cls.getFirstFieldDicts(initingRows)
        initFields = [{'name': titles.iloc[i], **initFields[i]} for i in range(len(titles))]
        return [cls(**collxbleDict) for collxbleDict in initFields]

    @classmethod
    def processingPrecedence(cls) -> int:
        return 10  # Relatively early


class Movie(MonolithicMedia, Reviewable):
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    # @classmethod
    # def DEFAULT_MEMBERS(cls):
    #     if len(cls._DEFAULT_MEMBERS) == 0:
    #         cls._DEFAULT_MEMBERS = {**super(Movie, cls).DEFAULT_MEMBERS(), **{
    #             'duration': pd.NaT
    #         }}
    #     return cls._DEFAULT_MEMBERS

    # @classmethod
    # def CATALOG_FIELDS(cls):
    #     if len(cls._CATALOG_FIELDS) == 0:
    #         cls._CATALOG_FIELDS = list(
    #             dict.fromkeys(super(Movie, cls).CATALOG_FIELDS() + list(cls.DEFAULT_MEMBERS().keys())))
    #     return cls._CATALOG_FIELDS

    # def pullReview(self, timesheetdf: TimesheetDataFrame):
    #     raise NotImplementedError

    @staticmethod
    def EXTERNAL_REVIEW_SOURCE(cls) -> str:
        raise NotImplementedError

    def pullExternalReview(self):
        raise NotImplementedError

    @classmethod
    def EXTERNAL_DATA_SOURCE(cls) -> str:
        raise NotImplementedError

    def pullExternalData(self):
        raise NotImplementedError

    @classmethod
    def INITIALIZATION_TSQY(cls):
        return 'description & ( Tag.NETFLIX | "Cine" | "' + cls.tempInitToken() + '," ) & !"TV" & !"' +\
               TVShow.tempInitToken() + '" :;'

    @classmethod
    def INITIALIZATION_TOKENS(cls):
        return 'CINE', cls.tempInitToken()

    @classmethod
    def INITIALIZATION_TOKENS_TO_CLEAR(cls) -> Tuple[str]:
        """Subset of `INITIALIZATION_TOKENS` which should be cleared after populating the tsdf with a Collectible."""
        return (cls.tempInitToken(), )
    
    @classmethod
    def POPULATION_TSQY(cls):
        return f'"CINE" | "{cls.tempInitToken()}" | Tag.Netflix : ;'

    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> list:
        initingRows = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())
        initingRows = initingRows.df[initingRows.filterMedia(['tvshow', 'movie']).df.media.apply(len) == 0].tsdf
        if len(initingRows) == 0: return []
        initingChild = initingRows.df[initingRows.df.description.apply(
            lambda x: any([x.hasToken(tok) and len(x.getChildToks(tok)) > 0 for tok in cls.INITIALIZATION_TOKENS()]))]
        titlesChild = initingChild.description.apply(lambda x: [x.getChildToks(tok)[0]
                                                                for tok in cls.INITIALIZATION_TOKENS() if
                                                                tok in x.tokens][0]).drop_duplicates(keep='first')
        titlesChild = titlesChild[titlesChild.apply((lambda x: len(x) > 0))]
        initingRoot = initingRows.df[~initingRows.df.index.isin(initingChild.index)]  # TODO: fix this

        titlesRoot = initingRoot.description.apply(lambda x: [c.name for c in x.tokenTree.children if c.name not in
                                                                 STDList.COLLXBLE_INSTANCES.union(STDList.STD_ROOTS)])
        titlesRoot = titlesRoot[titlesRoot.apply((lambda x: len(x) > 0))].apply(lambda x: x[0]).drop_duplicates(keep='first')

        titleSeries = pd.concat([titlesChild, titlesRoot], axis=0).sort_index().drop_duplicates()
        initingRows = initingRows.df.loc[initingRows.df.index.isin(titleSeries.index)].tsdf
        # Get all child tokens of INITIALIZATION_TOKENS()
        titles = [{'name': t} for t in titleSeries]
        initFields = cls.getFirstFieldDicts(initingRows)
        initFields = [{**titles[i], **initFields[i]} for i in range(len(titles))]
        return [cls(**collxbleDict) for collxbleDict in initFields]

    @classmethod
    def processingPrecedence(cls) -> int:
        return 40  # Relatively late, after Person, Location, other potentially unbound Collectible instance tokens

    @classmethod
    def rerunMinInterval(cls) -> datetime.timedelta:
        return datetime.timedelta(hours=60)


class TVShow(ConsumptionMedia, ManuallyReviewable):
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    # @classmethod
    # def DEFAULT_MEMBERS(cls):
    #     if len(cls._DEFAULT_MEMBERS) == 0:
    #         cls._DEFAULT_MEMBERS = {**super(TVShow, cls).DEFAULT_MEMBERS(), **{
    #             # Add default members if any arise
    #         }}
    #     return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(
                dict.fromkeys(super(TVShow, cls).CATALOG_FIELDS() + list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    # def pullReview(self, timesheetdf: TimesheetDataFrame):
    #     pass

    @staticmethod
    def EXTERNAL_REVIEW_SOURCE(cls) -> str:
        pass

    def pullExternalReview(self):
        pass

    @classmethod
    def EXTERNAL_DATA_SOURCE(cls) -> str:
        pass

    def pullExternalData(self):
        pass

    @classmethod
    def INITIALIZATION_TSQY(cls):
        return '(( description & (!"Cine" & !"' + Movie.tempInitToken() + '" & Tag.NETFLIX)) | "TV" | "' +\
            cls.tempInitToken() + ',") & ! Movie & ! TVShow  :;'

    @classmethod
    def INITIALIZATION_TOKENS(cls):
        return cls.tempInitToken(), 'TV',

    @classmethod
    def POPULATION_TSQY(cls):
        return f'"{cls.tempInitToken()}" | "TV" | Tag.Netflix : ;'

    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> list:
        initingRows = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())
        # Exclude rows if there is already a TVShow or Movie instance in the media column. Only log 1 instance per task.
        initingRows = initingRows.df[initingRows.filterMedia(['tvshow', 'movie']).df.media.apply(len) == 0].tsdf
        if len(initingRows) == 0: return []
        initingChild = initingRows.df[initingRows.df.description.apply(lambda x: any([x.hasToken(tok) for tok in
                                                                                      cls.INITIALIZATION_TOKENS()]))]
        titlesChild = initingChild.description.apply(lambda x: [x.getChildToks(tok)[0] if
                                                                len(x.getChildToks(tok)) > 0 else ''
                                                                  for tok in cls.INITIALIZATION_TOKENS() if
                                                                tok in x.tokens][0]).drop_duplicates(keep='first')
        if '' in titlesChild.values:  # A 'TV' descToken is childless, some erroneous corner case occurred
            raise NameError(f'Index {titlesChild.eq("").idxmax()} contains a childless TVShow initToken.')
        initingRoot = initingRows.df[~initingRows.df.index.isin(initingChild.index) & \
                                     initingRows.isEmpty(cls.name())]  # TODO: fix this

        titlesRoot = initingRoot.description.apply(lambda x: [c.name for c in x.tokenTree.children if c.name not in
                                                              (STDList.COLLXBLE_INSTANCES-STDList.STD_TV).union(
                                                                  STDList.STD_ROOTS)][0]
                                                   ).drop_duplicates(keep='first')
        movieTitles = set()
        frequencyDiscriminator = {
            # 2: datetime.timedelta(days=8),
            3: datetime.timedelta(weeks=26),
        }  # If <key> instances of the title occur within <value> interval of time, it's a TVShow, not a Movie
        # Must be sorted in ascending key order
        for t in titlesRoot:
            hasT = initingRows.df[initingRows.df.description.apply(lambda x: x.hasToken(t))]
            if len(hasT) < 3:
                movieTitles.add(t)
                continue
            for count, dur in frequencyDiscriminator.items():
                if len(hasT) < count: # Not a TV show
                    movieTitles.add(t)
                    break
                intervals = hasT.start - hasT.start.shift(count-1)
                if any(intervals < dur):  # It's a TVShow
                    break
        titlesRoot = titlesRoot[~titlesRoot.isin(movieTitles)]

        titleSeries = pd.concat([titlesChild, titlesRoot], axis=0).sort_index().drop_duplicates(keep='first')
        if len(titleSeries) == 0:
            return []
        initingRows = initingRows.df.loc[initingRows.df.index.isin(titleSeries.index)].tsdf
        # Get all child tokens of INITIALIZATION_TOKENS()
        titles = [{'name': t} for t in titleSeries]
        initFields = cls.getFirstFieldDicts(initingRows)
        initFields = [{**titles[i], **initFields[i]} for i in range(len(titles))]
        return [cls(**collxbleDict) for collxbleDict in initFields]

    @classmethod
    def processingPrecedence(cls) -> int:
        return Movie.processingPrecedence() - 1  # Right before Movie


class Person(Collectible, IncompletePersistent, Global.ListColumn):
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #  Assume that whenMet is the first time they appear in the TSDF record, unless a value is passed in kwargs.
        now = pd.Timestamp.now().date()
        if pd.isna(self.whenMet):
            self.whenMet = self.firstTime.date()
        if pd.isna(self.whenWith):
            self.whenWith = portion.closedopen(self.firstTime.date(),(self.firstTime+datetime.timedelta(days=1)).date())
        if pd.isna(self.age) and pd.notna(self.birthday):
            self.age = now - self.birthday
        # if sum([pd.notna(x) for x in [self.age, self.whenMet]]) >= 1:  # If able to resolve 'when's
            # if pd.isna(self.age):
            #     self.age = self.ageWhenMet + (now - self.whenMet)
            # elif pd.isna(self.whenMet):
            #     self.whenMet = self.ageWhenMet - self.age + now
            # else:
            #     self.ageWhenMet = self.age + self.whenMet - now
            # if pd.isna(self.birthday) and pd.notna(self.age):
            #     self.birthday = now - self.age
        if pd.isna(self.durationKnown) and pd.notna(self.whenMet):
            self.durationKnown = now - self.whenMet

    @classmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = {**super().DEFAULT_MEMBERS(), **{
                'birthday': pd.NA,
                'age': pd.NaT,
                'age': pd.NaT,
                # 'ageWhenMet': pd.NaT,
                'whenMet': pd.NA,  # Default value depends on self, can't set here. See __init__.
                'durationKnown': pd.NaT,
                'gender': pd.NA,
                # 'epochMet': pd.NA,
                'whenWith': pd.NA,  # Default value depends on self, can't set here. See __init__.
                'relationships': {sg.SocialGroupUndefined(), },
                'whereMet': pd.NA,  # Later replace with Location.Earth. Then make method to set to loc of firstTaskID
                'whereBorn': pd.NA,  # Later replace with Location.Earth
            }}
        return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(Collectible.CATALOG_FIELDS() + list(cls.DEFAULT_MEMBERS().keys())))
            # cls._CATALOG_FIELDS.remove('durationKnown')
        return cls._CATALOG_FIELDS

    @classmethod
    def INITIALIZATION_TSQY(cls):
        return '"Charlar," | "Hablar," | "Reunión," | "Videollamada," | "Mensajear," | "' + cls.tempInitToken() + '": ;'

    @classmethod
    def INITIALIZATION_TOKENS(cls):
        return "CHARLAR", "HABLAR", "REUNIÓN", "VIDEOLLAMADA", "MENSAJEAR", cls.tempInitToken()

    @classmethod
    def INITIALIZATION_TOKENS_TO_CLEAR(cls) -> Tuple[str]:
        """Subset of `INITIALIZATION_TOKENS` which should be cleared after populating the tsdf with a Collectible."""
        return (cls.tempInitToken(), )

    @classmethod
    def POPULATION_TSQY(cls):
        return Collectible.POPULATION_TSQY()

    @staticmethod
    def CATALOG_CLASS() -> str:
        return 'LinearCatalog'

    @classmethod
    def solveFields(cls):
        raise NotImplementedError

    @classmethod
    def colsNotCataloged(cls) -> set:
        return {'durationKnown', 'age'}

    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> List[Collectible]:
        hasPrefixRows = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())  # Rows which contain the trigger prefix
        personTokDFs = [hasPrefixRows.getDescTokenChildren(prefix).dropna() for prefix in cls.INITIALIZATION_TOKENS()]
        initingRows = pd.concat(personTokDFs).sort_index().explode().dropna().drop_duplicates(keep='first')
        return [Person(
            **{'name': name},
            **cls.getFirstFieldDicts(timesheetdf.df.loc[[taskID]].tsdf)[0]
            ) for taskID, name in initingRows.items()]

    @classmethod
    def processingPrecedence(cls) -> int:
        return 15  # Relatively early

    def primaryRelation(self) -> sg.Relation:
        """
        Returns an instance of the primary `SocialGroups.Relation` immediate subclass of `self`.
        If `self` contains multiple `Relation` instances, uses the following precedence:
        1. `SocialGroups.Family`
        2. `SocialGroups.Friend`
        3. `SocialGroups.Colleague`
        :return:
        """
        rels = list(filter(lambda x: isinstance(x, sg.Relation), self.relationships))
        if len(rels) == 0:
            return pd.NA
            # raise Global.DataEntryException(
            #     f"{self.id}'s relationships {self.relationships} contain no {sg.Relation()}.")
        if any([isinstance(r, sg.Family)       for r in rels]): return sg.Family()
        if any([isinstance(r, sg.Friend)       for r in rels]): return sg.Friend()
        if any([isinstance(r, sg.Colleague)    for r in rels]): return sg.Colleague()
        if any([isinstance(r, sg.Acquaintance) for r in rels]): return sg.Acquaintance()
        raise Exception(f"{self.id}'s relationships {self.relationships} contain an unaccounted {sg.Relation()}.")


class Food(AutofillPrevious, DAGCollectible, BareNameID, Global.ListColumn):
    """
    Unique DAG standards:
    Categories: Defined in emptyDAG() as '$'-prefixed ids. See emptyDAG() for full list of categories.
    $PLATOS: Dishes
    $PRIMITIVAS: Primitives (basically ingredients)
    $ETNIAS: Ethnicities
    Excluding the root vertex $FOOD, these all represent categories of Food instances rather than instances themselves.
    p: edge property encoding precedence.
    p in [ 0, 19]: identity relationships Dish >> Dish, Primitive >> Primitive, Ethnicity >> Ethnicity
    The parentage of any item in the catalog in the subgraph containing only these edges
    should contain exactly 1 category.
    Only assign this edge weight if the Food is an instance of that category.
    Every Food instance must have at least (maybe exactly?) 1 identity relationship to a parent.
    p in [20, 39]: Union[Dish, Primitive] >> Ethnicity edges.
    Dishes and primitives may use edge weights in this range for their ethnicities.
    Ethnicities linking to other ethnicities should use identity relationships.
    p in [40, 59]: ingredient relationships Dish >> Primitive
    Connects a dish to an ingredient that it contains.
    """
    @classmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = super(Food, cls).DEFAULT_MEMBERS()
        return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(super(Food, cls).CATALOG_FIELDS() +
                                                     list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    @classmethod
    def INITIALIZATION_TSQY(cls) -> str:
        return '"COMER, " | "' + cls.tempInitToken() + '" : ;'

    @classmethod
    def INITIALIZATION_TOKENS(cls) -> Tuple[str]:
        return 'COMER', cls.tempInitToken()

    @classmethod
    def POPULATION_TSQY(cls):
        return f'"COMER" | "COCINAR" | "PREPARAR" | "{cls.tempInitToken()}" | Tag.Comer : ;'

    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> list:
        hasPrefixRows = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())  # Rows which contain the trigger prefix
        tokDFs = [hasPrefixRows.getDescTokenChildren(prefix).dropna() for prefix in cls.INITIALIZATION_TOKENS()]
        initingRows = pd.concat(tokDFs).sort_index().explode().dropna().drop_duplicates(keep='first')
        return [Food(
            **{'name': name},
            **cls.getFirstFieldDicts(timesheetdf.df.loc[[taskID]].tsdf)[0]
            ) for taskID, name in initingRows.items()]

    @classmethod
    def processingPrecedence(cls) -> int:
        return 25  # TODO: TBD precedence of Food

    @classmethod
    def emptyDAG(cls) -> nx.DiGraph:
        out = cls._emptyDAG()
        p = {'p': 0}  # Sorting key for parental precedence
        out.add_edges_from([
            ('$ETNIAS', cls.rootVertex(), p),
            ('$PLATOS', cls.rootVertex(), p),
            ('$PRIMITIVAS', cls.rootVertex(), p),
            ('$OTRO', cls.rootVertex(), p),
            ('OCCIDENTAL', '$ETNIAS', p),
            ('ORIENTAL', '$ETNIAS', p),
            ('AFRICANA', '$ETNIAS', p),
            ('ASIÁTICA', 'ORIENTAL', p),
            ('LATINOAMERICANA', '$ETNIAS', p),
        ])
        return out

    @classmethod
    def getAutofillRows(cls, timesheetdf: TimesheetDataFrame) -> Tuple[pd.Index, pd.Index]:
        return timesheetdf.tsquery('"COCINAR" : ;').df.index, pd.Index([])
        # TODO: implement Food autofill filtering, call an EpochScheme, find which meal of the day, etc
        # return timesheetdf.tsquery('"COCINAR" : ;').df.index

    @classmethod
    def rerunMinInterval(cls) -> datetime.timedelta:
        """
        Food is a special case.
        Food.rerunMinInterval tracks the minimum temporal separation between multiple instances of cooking, not eating.
        :return:
        """
        return datetime.timedelta(days=2)
    
    
class SubjectMatter(DAGCollectible, BareNameID, Global.ListColumn):
    _DEFAULT_MEMBERS = {}
    _CATALOG_FIELDS = []
    
    @classmethod
    def DEFAULT_MEMBERS(cls):
        if len(cls._DEFAULT_MEMBERS) == 0:
            cls._DEFAULT_MEMBERS = super(SubjectMatter, cls).DEFAULT_MEMBERS()
        return cls._DEFAULT_MEMBERS

    @classmethod
    def CATALOG_FIELDS(cls):
        if len(cls._CATALOG_FIELDS) == 0:
            cls._CATALOG_FIELDS = list(dict.fromkeys(super(SubjectMatter, cls).CATALOG_FIELDS() +
                                                     list(cls.DEFAULT_MEMBERS().keys())))
        return cls._CATALOG_FIELDS

    @classmethod
    def INITIALIZATION_TSQY(cls) -> str:
        return f'"INVESTIGAR, " | "TEMAS, " | "{cls.tempInitToken()}" : ;'

    @classmethod
    def INITIALIZATION_TOKENS(cls) -> Tuple[str]:
        return 'INVESTIGAR', 'TEMAS', cls.tempInitToken()

    @classmethod
    def INITIALIZATION_TOKENS_TO_CLEAR(cls) -> Tuple[str]:
        """Subset of `INITIALIZATION_TOKENS` which should be cleared after populating the tsdf with a Collectible."""
        return (cls.tempInitToken(), )

    @classmethod
    def POPULATION_TSQY(cls):
        return f'"INVESTIGAR, " | "LEER, " | ("COMPRAR, " & Tag.Elec) | ("COMPRAR, " & ! "COMESTIBLES" & Tag.Social ) | "TEMAS, " | "{cls.tempInitToken()}" : ;'

    @classmethod
    def tsdfPopulationFilter(cls, timesheetdf: TimesheetDataFrame, collxs: pd.Series) -> Tuple[pd.Series, pd.Series]:
        df = timesheetdf.df.loc[collxs.index.drop_duplicates(),:]
        population_valid_parents = {"INVESTIGAR", "LEER", "COMPRAR", "TEMAS"}
        df = collxs.rename("subject_matter", copy=False).to_frame().merge(df.description, how="inner", left_index=True, right_index=True)
        has_valid_child = df.apply(lambda x: len(set(x.description.getParentToks(x.subject_matter)).intersection(population_valid_parents)) > 0, axis=1)
        has_duplicate_tokens = df.apply(lambda x: x.description.count(x.subject_matter) > 1, axis=1)
        tree_nodes = df.loc[has_duplicate_tokens].apply(lambda x: anytree.search.findall(x.description.tokenTree, filter_=lambda node: node.name == x.subject_matter and node.parent.name in population_valid_parents), axis=1)
        if len(tree_nodes) > 0:
            tree_nodes = tree_nodes.explode()
        else:
            tree_nodes = pd.Series([], dtype=object)
        return collxs.loc[has_valid_child & ~has_duplicate_tokens], tree_nodes

    @classmethod
    def processingPrecedence(cls) -> int:
        return 90 # Last unless something else comes up

    @classmethod
    def emptyDAG(cls) -> nx.DiGraph:
        out = cls._emptyDAG()
        p = {'p': 0}  # Sorting key for parental precedence
        out.add_edges_from([
            ('FILOSOFÍA', cls.rootVertex(), p),
            ('CIENCIA', cls.rootVertex(), p),
            ('SOCIEDAD', cls.rootVertex(), p),
            ('PROBLEMAS', cls.rootVertex(), p),
            ('ASUNTO PERSONAL', cls.rootVertex(), p),
        ])
        out.add_edges_from([
            ("CIENCIA FORMAL", "CIENCIA", p),
            ("CIENCIA NATURAL", "CIENCIA", p),
            ("CIENCIA SOCIAL", "SOCIEDAD", p),
            ("RECREO", "ASUNTO PERSONAL", p),
            ("GENTE CONOCIDA", "ASUNTO PERSONAL", p),
        ])
        out.add_edges_from([
            ("CIENCIA FÍSICA", "CIENCIA FORMAL", p),
        ])
        return out
    @classmethod
    def constructObjects(cls, timesheetdf: TimesheetDataFrame, *args) -> List['SubjectMatter']:
        hasPrefixRows: TimesheetDataFrame = timesheetdf.tsquery(cls.INITIALIZATION_TSQY())  # Rows which contain the trigger prefix
        tokDFs = [hasPrefixRows.getDescTokenChildren(prefix).dropna() for prefix in cls.INITIALIZATION_TOKENS()]
        initingRows = pd.concat(tokDFs).sort_index().explode().dropna().drop_duplicates(keep='first')
        return [cls(
            **{'name': name},
            **cls.getFirstFieldDicts(timesheetdf.df.loc[[taskID]].tsdf)[0]
            ) for taskID, name in initingRows.items()]
        
