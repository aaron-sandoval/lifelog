r"""
Container for misc code usable across projects.
@author: Aaron
"""
import abc
import functools
import itertools
import datetime
import math
from enum import EnumMeta, Enum
import aenum
from collections import defaultdict
from functools import lru_cache
import portion
from pandas.core.dtypes.inference import is_list_like
import copy
from typing import \
    Union, TypeVar, Type, Any, Iterable, Tuple, List, Generator, Dict, Callable, Optional, Protocol, ClassVar, Set
import pandas as pd
import numpy as np
from yamlable import YamlCodec
from dataclasses import fields as dataclass_fields, dataclass


def kiwiTest():
    """Test function to check access to library"""
    print('kiwilib successfully accessed!')


def isin(collxn, val) -> bool:
    """
    Function wrapper for the python "in" syntax. Necessary to implement DC queries
    :param coll: Collection which supports the "in" syntax
    :param val: Item to search for
    :return:
    """
    return val in collxn


def dt64_2_dt(dt64):
    """
    Converts a datetime64 to a datetime type
    :param dt64: datetime64, behavior when passed a regular datetime untested
    :return: datetime type of the arg
    """
    return datetime.datetime.utcfromtimestamp(dt64.astype(datetime.datetime) * 1e-9)


def mapOverListLike(func, listLike: Iterable) -> Iterable:
    """
    Maps a function over the elements of a list-like object, returning the same type as the list-like.
    Basic intended usage:
    mapOverListLike is called from inside func after a is_list_like type check.
    The main body of func after the conditional call to mapOverListLike only needs to support atomic args.
    mapOverListLike handles assembling the returns of func into the appropriate iterable hierarchy.
    If listLike contains non-iterables, then the 1st level of recursion will compute func for each member of listLike.

    :param func: Function to map. Only supports function calls func(i).
    For functions with additional args of to apply object methods, the caller should pass a lambda implementing those.
    :param listLike: A list-like container to be iterated over.
    :return: An iterable of same type as listLike with func applied to its elements.
    """
    if not is_list_like(listLike):
        raise TypeError(f'{type(listLike)} is not list-like. Add a type check in the caller.')
    elif isinstance(listLike, pd.Series):
        return listLike.apply(func)
    # elif not isinstance(type(listLike), collections.Callable):
    #     raise TypeError(f'Cannot generically cast to type {type(listLike)}')
    # elif isinstance(listLike, collections.Callable):
    return type(listLike)([func(i) for i in listLike])


def flatten(it: Iterable, numLevels: int = pd.NA) -> Generator:
    """
    Flattens an arbitrarily nested iterable. Returns a generator over the flattened sequence.
    :param it: Any arbitrarily nested iterable.
    :param numLevels: Number of levels to flatten by. Defaults to full flattening.
    """
    for x in it:
        # TODO: swap type check with more general check for __iter__() or __next__() or whatever
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes, EnumMeta)) and \
                (pd.isna(numLevels) or numLevels > 0):
            yield from flatten(x, numLevels-1)
        else:
            yield x


def getAllSubclasses(class_: type, includeSelf=False) -> Set[type]:
    """
    Returns a set containing all child classes in the subclass graph of `class_`.
    I.e., includes subclasses of subclasses, etc.

    # Parameters
    - `include_self`: Whether to include `class_` itself in the returned list
    - `class_`: Superclass

    # Development
    Since most class hierarchies are small, the inefficiencies of the existing recursive implementation aren't problematic.
    It might be valuable to refactor with memoization if the need arises to use this function on a very large class hierarchy.
    """
    subs: List[Set[type]] = [
        getAllSubclasses(sub, includeSelf=True)
        for sub in class_.__subclasses__()
        if sub is not None
    ]
    subs: set = set(flatten(subs))
    if includeSelf:
        subs.add(class_)
    return subs


def leafClasses(cls: type) -> List[type]:
    """
    Returns a list of all leaf subclasses in the hierarchy DAG of cls.
    Leaf subclasses are those which have no subclasses of their own.
    :param cls:
    """
    def leafClassesRecur(myclass):
        if len(myclass.__subclasses__()) == 0:
            return myclass
        else:
            return [leafClassesRecur(subclass) for subclass in myclass.__subclasses__()]

    return list(set(leaf for leaf in flatten(leafClassesRecur(cls))))


def is_locally_defined(class_: type, binding: str) -> bool:
    """
    Returns True if `binding` is a class variable uniquely defined in `class_` as opposed to inherited.
    If the value assigned to `binding` is defined in `class_` but that values matches tge value in a base class,
    it also returns True.
    """
    return hasattr(class_, binding) and \
        getattr(class_, binding) not in [getattr(b, binding, NotImplemented) for b in class_.__bases__]

def timedelta2datetime(td: datetime.timedelta) -> datetime.datetime:
    return datetime.datetime(1900, 1, 1, 0)+td


def datetime2timedelta(dt: datetime.datetime) -> datetime.timedelta:
    return dt - datetime.datetime(1900, 1, 1, 0)


def listEquals(list1: list, list2: list) -> bool:
    """
    Checks whether two lists are equal, regardless of order.
    Equality defined by having all equal elements.
    Recurs arbitrarily deep for nested lists.
    :param list1: First list
    :param list2: Second list
    :return: True if the lists contain the same elements, regardless of order.
    """
    if type(list1) != list:
        return list1 == list2
    elif type(list1) != type(list2) or len(list1) != len(list2):
        return False
    elif type(list1) == list:
        return all([listEquals(list1[i], list2[i]) for i in range(len(list1))])
    elif len(list1)==0:
        return True


def consolidateInterval(iv: portion.Interval, minIv) -> portion.Interval:
    """
    Consolidates AtomicIntervals in an Interval such that there is no gap less than minIv between any atomicIntervals.
    Where such gaps are found, they are filled via portion.enclosure().
    :param minIv: Shortest allowable gap between any atomicIntervals.
    Must be comparable to the data type returned by T.__sub__(), where T is the type contained in iv.
    """
    return functools.reduce(lambda x, y: x | y if y.lower-x.upper > minIv else x[:-1] | (x[-1] | y).enclosure, iv)


def consolidateIntervalGaps(iv: portion.Interval, minIv) -> portion.Interval:
    """
    Deletes all AtomicIntervals in an Interval whose length is below minIv.
    :param minIv: Shortest allowable AtomicInterval.
    Must be comparable to the data type returned by T.__sub__(), where T is the type contained in iv.
    """
    return iv.apply(lambda x: x.replace(upper=x.upper-(x.upper-x.lower)) if x.upper-x.lower < minIv else x)


def addLineBreaks(s: str, delim: str = ' ', maxLen=None, delimIndices: List[int] = None, insert: int = 0) -> str:
    """
    Replaces certain occurences of delim with newlines into a string
    :param s: String to process
    :param delim: Substring to replace with or insert a newline at certain instances
    :param maxLen: Either maxLen or delimIndices, but not both may be specified.
    Max number of characters to reach before inserting a newline.
    :param delimIndices: Either maxLen or delimIndices, but not both may be specified.
    Indices of the occurences of delim to replace with a newline.
    Similarly to the stdlib str.split, consecutive instances of delim are not grouped together for indexing purposes.
    :param insert: -1: insert newline before delim; 0: replace delim with newline; 1: insert newline after delim
    :return:
    """
    if delim not in s:
        return s
    if maxLen is not None:
        raise NotImplementedError('maxLen functionality not yet implemented.')
    if not ((maxLen is None) ^ (delimIndices is None)):
        raise ValueError('Either maxLen or delimIndices, but not both, must be specified.')
    if delimIndices is not None:
        segments = s.split(delim)
        delimIndices = set(delimIndices)
        out = segments[0]
        for i, seg in enumerate(segments[:-1]):
            # if i == 0:
            #     continue
            if i in delimIndices:
                out = '\n'.join([out, segments[i+1]])
            else:
                out = delim.join([out, segments[i+1]])
    return out
        # return '\n'.join([delim.join([])])


class IsDataclass(Protocol):
    # the most reliable way to ascertain that something is a dataclass
    __dataclass_fields__: ClassVar[Dict]


_T = TypeVar('_T')


class AenumABCMeta(abc.ABCMeta, aenum.EnumMeta):
    pass


class DataclassValuedEnum(abc.ABC, aenum.Enum, metaclass=AenumABCMeta):
    """
    ABC for Enum classes whose members have dataclass-like attribute access.
    Each subclass is associated with a dataclass containing the member attributes.
    However, the Enum values for each member are NOT the dataclass instances.
    Instead, these are defined in `_enum_data`.
    This is to overcome a drawback of storing complex data directly in the Enum member values.
    In this implementation, the properties of the dataclass and the member's data to be updated
    without invalidating any previous instance of that enum stored in files.
    When the enum is read from a file, its attributes will effectively be updated to the latest values in `_enum_data`.
    """
    # TODO: public method that can be called in `subclass._get_dataclass` which auto-builds a new dataclass inherited from its superclasses' dataclasses

    @staticmethod
    @abc.abstractmethod
    def _get_dataclass() -> IsDataclass:
        """
        Returns a existing dataclass or constructs and returns a new one.
        Called only once by __init_subclass__ and stored in `cls.dataclass`.
        This dataclass holds all the attributes of the outer class enum members.
        It's recommended that these dataclasses be frozen.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def _enum_data(cls) -> Dict[Enum, 'Type[DataclassValuedEnum]._DATACLASS']:
        """
        Instantiates dataclass members associated with each enum member.
        This method contains the data that would traditionally be located in the enum definitions.
        :param c: Will always be passed `cls._DATACLASS`. Only here so that each subclass need not make that reference.
        :return: Mapping from enum members to their data.
        """
        pass

    @staticmethod
    def _init_DVE(cls: Type['DataclassValuedEnum']):
        """
        Decorator procedure to initialize the internal dataclass and fields of a DataclassValuedEnum subclass.
        Never call this method on DataclassValuedEnum itself. Only used for its (abstract) subclasses.
        """
        cls.dataclass = cls._get_dataclass()
        cls._data = cls._enum_data()
        if cls._data is not None:
            for fld in cls.dataclass.__dataclass_fields__:
                setattr(cls, fld, property(lambda slf, f=fld: getattr(slf._data[slf], f)))
        return cls

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls = cls._init_DVE(cls)

    def __repr__(self):
        return ''.join(['<', str(self), ': ', repr(self.value), '; ', repr(self._data[self]), '>'])

    def asdict(self):
        return self._data[self].__dict__


class HierarchicalEnum(abc.ABC):
    """
    A superclass for defining a hierarchical enum-like data structure using a class hierarchy.
    Supports any hierarchical structure supported by python class inheritance.
    This is, namely, any directed acyclic graph (DAG), as long as there is a single root node in the DAG (root_class).
    """

    @classmethod
    @abc.abstractmethod
    def root_class(cls) -> type:
        """
        Return the common superclass for all nodes in the hierarchy.
        Default behavior is to return the member of the hierarchy which is a direct subclass of HierarchicalEnum.
        In the case of multiple inheritance, this will return the first superclass in the MRO which is a direct
        subclass of HierarchicalEnum.
        """
        return HierarchicalEnum

    def __repr__(self):
        if type(self) == self.root_class():
            return type(self).__name__
        else:
            # return type(self).__bases__[0]().__repr__() + '.' + type(self).__name__
            return self.root_class().__name__ + '.' + type(self).__name__
            # return type(self).__name__

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(repr(type(self)))

    def __iter__(self):
        return iter([c() for c in getAllSubclasses(type(self))])

    def __len__(self):
        return len(getAllSubclasses(type(self)))


def date_range_bins(ser: pd.Series, freq: str = 'W', normalize: bool = True, **kwargs) -> pd.Series:
    """
    Maps `ser` of datetime-like values to a Categorical dtype Series.
    Categories are pd.IntervalIndex instances, each of which is a time interval as specified by `freq`.
    :param ser: Series of type `date` or `datetime`-like. Must be processable by `pd.to_datetime()`.
    :param freq: pd.DateOffset alias. See https://pandas.pydata.org/docs/user_guide/timeseries.html#offset-aliases
    :param normalize: Whether to start the bins at midnight of the first day.
    If False, bins will start at `ser.iloc[0]` and `freq` will be applied from there.
    Generally, `bool=True` for `freq` specs of days or longer base intervals.
    """
    circ = pd.to_datetime(ser)
    if 'bins' not in kwargs:
        a: pd.DatetimeIndex = pd.date_range(circ.head(1).values[0], circ.tail(1).values[0], freq=freq,
                                            normalize=normalize)

        # `a` spans most of `ser`, but due to pandas' design both the head and tail of `ser` may lie outside.
        # `ser.head(1)` should only be at worst 1 `a.freq` less than `a[0]`, so extend head by 1.
        headExtension = np.expand_dims(np.array(a[0] - a.freq), axis=(0,))

        if a.freq.name in 'W D C B BH H T S L U N us ms min':  # frequency in weeks, days, or shorter
            # `ser.tail(1)` may be many units of `a.freq` greater than `a[-1]` if `normalize`==True.
            # Concatenate however many are needed to `a` to bound `ser.tail(1)`.
            tailExtension = a[-1] + np.arange(((circ.iloc[-1] - a[-1]) // a.freq + 2)) * a.freq
        else:
            tailExtension = np.expand_dims(np.array(a[-1] + a.freq), axis=(0,))
        # Expand the DateTimeIndex by on either end. Ensures that `ser.head` and `ser.tail` are both contained inside.
        a = a.union(np.concatenate([headExtension, tailExtension]))
        kwargs['bins'] = a
    return pd.cut(circ, right=False, **kwargs)


def enum_counts(ser: pd.Series, enumCls: Union[Type[Enum], Iterable[Type[HierarchicalEnum]]]) -> pd.DataFrame:
    """
    Counts the instances of `enumCls` members in a Series of iterables.
    :param ser: Series of Iterable[Any], possibly containing members of `enumCls`.
    :param enumCls: An Enum subclass whose instances in the rows of `ser` are to be counted
    :return: A integer-valued DataFrame with columns as all the members of `enumCls`.
    Data is the count of instances of that enum member in that row in `ser`.
    """
    def make_count(lst: Iterable, enumCls1: Iterable[type]) -> List[int]:
        if len(lst) == 0:
            lst.extend([0] * len(enumCls1))
            return lst
        countDict = defaultdict(lambda: 0)
        for item in lst:
            countDict[item] += 1
        lst.clear()
        lst.extend([countDict[e] for e in enumCls1])

    enumList = list(enumCls)
    ser.apply(make_count, args=(enumList,))
    out = pd.DataFrame(np.vstack(ser.values), index=ser.index)
    # TODO: bugfix: rename goes crazy on SocialGroups
    if isinstance(enumList[0], HierarchicalEnum):
        target_names = [str(a) for a in enumList]
    else:
        target_names = [str(e) for e in list(enumList)]
    return out.rename(columns=dict(zip(range(len(enumList)), target_names)))


def backtrack(sol, cur):
    """

    :param sol:
    :param cur:
    :return:
    """
    # TODO: generalize this to be callable like a library function.
    # Prob pass in procedures for isSolution, constructCandidates, processSolution
    # Figure out how to handle processSolution appending to an outside list.

    def isSolution(a, k):
        # nonlocal n
        return k == n

    def constructCandidates(a, k):
        return [a[:k] + [i] + a[k + 1:] for i in nums if i not in a]

    def processSolution(a):
        # nonlocal out
        out.append(a)

    if isSolution(sol, cur):
        processSolution(sol)
    else:
        nextSols = constructCandidates(sol, cur)
        cur += 1
        for nextSol in nextSols:
            # print(f'nextSol: {nextSol}')
            backtrack(nextSol, cur)


class LinkedHeapNode:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return str(self.val)


class LinkedMinHeap:
    """
    Manual heap implementation using LinkedHeapNode found in the same module.
    Currently only supports LinkedHeapNode directly. Doesn't support subclasses which have additional data members.
    """

    def __init__(self, items, compFunction):
        self.last = None
        self.size = 0
        self.head = None
        self.compF = compFunction
        self.heapify(items)

    def heapify(self, items):
        if len(items) == 0:
            return
        for item in items:
            self.push(item)

    def validate(self, head=-1) -> bool:
        if head is None:
            return True
        if head == -1:  # Head of entire heap
            # head = self.head
            if not self.head:
                return self.size == 0 and self.last == None
            else:
                return self.size > 0 and self.last != None and \
                    self.validate(self.head.left) and self.validate(self.head.right)
        return self.compF(head) >= self.compF(head.parent) and self.validate(head.left) and self.validate(head.right)

    # @staticmethod
    def _swapWithParent(self, item):
        # print(f'item = {item.val}; Pre-swap w/ parent:\n{self}')
        if not item: return
        tempL = item.left
        tempR = item.right
        tempP = item.parent
        item.parent = item.parent.parent
        if self.last == item:
            self.last = tempP
        if not tempP.parent:
            self.head = item
        else:  # Reassign item.parent.parent's pointers
            if tempP.parent.left == tempP:
                tempP.parent.left = item
            else:
                tempP.parent.right = item
        if tempP.left == item:
            if tempP.right: tempP.right.parent = item
            item.right = tempP.right
            tempP.left = tempL
            tempP.right = tempR
            item.left = tempP
        else:
            if tempP.left: tempP.left.parent = item
            item.left = tempP.left
            tempP.left = tempL
            tempP.right = tempR
            item.right = tempP
        tempP.parent = item
        if tempL: tempL.parent = tempP
        if tempR: tempR.parent = tempP
        # print(f'Post-swap:\n{self}')
        a = 1

    def push(self, item):
        if not item: return
        # print(f'Start push:\n{self}')
        parent = self._getNextParent()
        if not parent:
            self.head = item
        elif self.size % 2 == 0:
            parent.right = item
        else:
            parent.left = item
        self.size += 1
        self.last = item
        item.left = None
        item.right = None
        item.parent = parent
        self._bubbleUp(item)
        # print(f'End push:\n{self}')

    def pop(self):
        """Bubble down the head until reaching a leaf, then swap the last element in the heap and bubble that one up"""
        # print(f'Start pop:\n{self}')
        if self.size == 0:
            raise IndexError(f'Empty heap cannot be popped')
        if self.size == 1:  # If the heap contains exactly 1 element
            self.size = 0
            out = self.head
            self.head = None
            self.last = None
            return out
        out = self.head
        firstIter = True
        while out.right:  # Impossible for a node to have a right child but no left child
            if self.compF(out.left) > self.compF(out.right):
                self._swapWithParent(out.right)
            else:
                self._swapWithParent(out.left)
            if firstIter:
                self.head = out.parent
                firstIter = False
        if out.left:
            self._swapWithParent(out.left)
            # out.parent.left = None
            # self.size -= 1
            # return out
        # Either a leaf or the parent of the last element

        # elif out.right:
        #     _swapWithParent(out.right)
        #     out.parent.right = None
        #     self.size -= 1
        #     return out
        # last = self.last
        oldLast = self.last
        if oldLast != out:
            self._swapVals(out, oldLast)  # _swapVals just swaps values, not pointers, so out now points to oldLast
            temp = out
            out = oldLast
            oldLast = temp
            self._bubbleUp(oldLast)
        self.size -= 1
        if out.parent.right:
            self.last = out.parent.left
            # assert self.last is not None
            out.parent.right = None
        elif self.height() == self._getHeight(self.size + 1):  # Haven't removed last leaf on a level
            out.parent.left = None
            self.last = self._getNextParent(self.size - 1).right
            # assert self.last is not None
        else:  # Just removed last leaf on a level. Last is now rightmost leaf
            out.parent.left = None
            self.last = self.head
            while self.last.right:
                self.last = self.last.right
            # assert self.last is not None
        # if out.parent.right:
        # else:
        # assert self.last is not None
        out.parent = None
        # print(f'Post-pop:\n{self}')
        return out

    def popPush(self, item):
        """A pop and push in a single operation. Need only traverse heap height 1 time instead of 3 times"""
        out = self.head
        self.head = item
        item.left = out.left
        item.right = out.right
        if item.left:   item.left.parent = item
        if item.right:  item.right.parent = item
        out.left = None
        out.right = None
        self._bubbleDown(item)
        if item.parent == self.last:
            self.last = item

    def _swapVals(self, a, b):
        # if a == self.last:
        #     b = self.last
        # elif b == self.last:
        #     a = self.last
        # temp = a.parent
        # a.parent = b.parent
        # b.parent = temp
        # temp = a.right
        # a.right = b.right
        # b.right = temp
        # temp = a.left
        # a.left = b.left
        # b.left = temp
        temp = a.val
        a.val = b.val
        b.val = temp
        # temp = a.next
        # a.next = b.next
        # b.next = temp

    def _getNextParent(self, size=None):
        def _getChild(parent, treeSize):
            if treeSize == 0:
                return None
            elif treeSize < 3:
                return parent
            else:
                h = self._getHeight(treeSize)
                nOnAboveLevels = round(math.pow(2, h - 1)) - 1
                nOnInsertionRow = (treeSize - nOnAboveLevels) % round(math.pow(2, h - 1))
                if nOnInsertionRow == 0:  # or nOnInsertionRow == round(math.pow(2, h-1)):
                    child = parent.left
                    while child.left:
                        child = child.left
                    return child
                # Could optimize here and add a shortcut if nOnInsertionRow==0 or ==2^(h-1), go all the way down left/right
                if nOnInsertionRow >= round(math.pow(2, h - 2)):
                    # print(f'BranchR')
                    return _getChild(parent.right, treeSize - round(math.pow(2, h - 1)))
                else:
                    # print(f'BranchL')
                    return _getChild(parent.left, treeSize - round(math.pow(2, h - 2)))

        if not size: size = self.size
        return _getChild(self.head, size)

    def height(self):
        return self._getHeight(self.size)

    @staticmethod
    def _getHeight(treeSize):
        # if not self.head: return 0
        h = 1
        a = treeSize
        while a > 1:
            h += 1
            a = int(a / 2)
        return h

    def _bubbleUp(self, item):
        # if not item.left:
        #     leaf = True
        # else:
        #     leaf = False
        while item.parent and self.compF(item) < self.compF(item.parent):
            if item == self.last:
                self.last = item.parent
            self._swapWithParent(item)

    def _bubbleDown(self, node):
        # print(f'enter bubdown\n{self.__str__(node)}')
        firstIter = True
        while node.right:  # Impossible for a node to have a right child but no left child
            if (self.compF(node.left) > self.compF(node.right)) and (self.compF(node) > self.compF(node.right)):
                self._swapWithParent(node.right)
            elif (self.compF(node.left) < self.compF(node.right)) and (self.compF(node) > self.compF(node.left)):
                self._swapWithParent(node.left)
            else:
                break
            if firstIter:
                self.head = node.parent
                firstIter = False
        if node.left and self.compF(node.left) < self.compF(node):
            self._swapWithParent(node.left)
        # print(f'exit bubdown\n{self.__str__(self.head)}')
        # if node.parent == self.last:
        #     self.last = node

    def __str__(self, node=-1, level=0):
        if not node or not self.head: return ''
        if node == -1:
            node = self.head
        ret = "\t" * level + str(node.val) + "\n"
        ret += self.__str__(node.left, level + 1)
        ret += self.__str__(node.right, level + 1)
        return ret

"""Yaml Codecs"""
# 2-way mappings between the types and the yaml tags


class YamlCodecDatetimes(YamlCodec):
    types_to_yaml_tags = {datetime.datetime: ("datetime.datetime", ('year', 'month', 'day', 'hour', 'minute', 'second',
                                                                    'microsecond', 'tzinfo')),
                          datetime.timedelta: ("datetime.timedelta", ('days', 'seconds', 'microseconds')),
                          pd.Timestamp: ('pd.Timestamp', ('year', 'month', 'day', 'hour', 'minute', 'second',
                                                          'microsecond', 'tzinfo')),
                          pd._libs.tslibs.nattype.NaTType: ('pd.NaT', ()),
                          pd._libs.missing.NAType: ('pd.NA', ()),
                          pd._libs.tslibs.timedeltas.Timedelta: ('pd.Timedelta', ('days', 'seconds', 'microseconds')),
                          np.timedelta64: ('np.timedelta64', ('days', 'seconds', 'microseconds')),
                          }
    yaml_tags_to_types = dict(zip([val[0] for val in types_to_yaml_tags.values()], types_to_yaml_tags.keys()))

    @classmethod
    def get_yaml_prefix(cls):
        return "!CodecDatetimes/"  # This is our root yaml tag

    @classmethod
    def get_known_types(cls) -> Iterable[Type[Any]]:
        # return the list of types that we know how to encode
        return cls.types_to_yaml_tags.keys()

    @classmethod
    def is_yaml_tag_supported(cls, yaml_tag: str) -> bool:
        # return True if the given yaml tag suffix is supported
        return yaml_tag in cls.yaml_tags_to_types.keys()

    @classmethod
    def from_yaml_dict(cls, yaml_tag_suffix: str, dct, **kwargs):
        # Create an object corresponding to the given tag, from the decoded dict
        typ = cls.yaml_tags_to_types[yaml_tag_suffix]
        return typ(**dct)

    @classmethod
    def to_yaml_dict(cls, obj) -> Tuple[str, Any]:
        # Encode the given object and also return the tag that it should have
        return cls.types_to_yaml_tags[type(obj)][0],\
            {key: obj.__getattribute__(key) for key in cls.types_to_yaml_tags[type(obj)][1]
             if obj.__getattribute__(key) not in (None, 0)}

    @classmethod
    def from_yaml_scalar(cls, yaml_tag_suffix, scalar, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_yaml_list(cls, yaml_tag_suffix, seq, **kwargs):
        raise NotImplementedError


class YamlCodecMisc(YamlCodec):
    types_to_yaml_tags = {
        tuple: ("tuple", ()),
        portion.Interval: ("portion.Interval", ()),
        }
    yaml_tags_to_types = dict(zip([val[0] for val in types_to_yaml_tags.values()], types_to_yaml_tags.keys()))

    @classmethod
    def get_yaml_prefix(cls):
        return "!CodecMisc/"  # This is our root yaml tag

    @classmethod
    def get_known_types(cls) -> Iterable[Type[Any]]:
        # return the list of types that we know how to encode
        return cls.types_to_yaml_tags.keys()

    @classmethod
    def is_yaml_tag_supported(cls, yaml_tag: str) -> bool:
        # return True if the given yaml tag suffix is supported
        return yaml_tag in cls.yaml_tags_to_types.keys()

    @classmethod
    def from_yaml_dict(cls, yaml_tag_suffix: str, dct, **kwargs):
        # Create an object corresponding to the given tag, from the decoded dict
        # typ = yaml_tags_to_types[yaml_tag_suffix]
        if cls.yaml_tags_to_types[yaml_tag_suffix] == portion.Interval:
            return portion.from_data(dct['atomicIntervals'])
        # elif cls.yaml_tags_to_types[yaml_tag_suffix] == tuple:
        #     return tuple(dct['tupleItems'])

    @classmethod
    def to_yaml_dict(cls, obj) -> Tuple[str, Any]:
        # Encode the given object and also return the tag that it should have
        if isinstance(obj, portion.Interval):
            return cls.types_to_yaml_tags[type(obj)][0], \
                {'atomicIntervals': [list(x) for x in portion.to_data(obj)]}
        # elif isinstance(obj, tuple):
        #     return cls.types_to_yaml_tags[type(obj)][0], \
        #         {'tupleItems': list(obj)}

    @classmethod
    def from_yaml_scalar(cls, yaml_tag_suffix, scalar, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_yaml_list(cls, yaml_tag_suffix, seq, **kwargs):
        return cls.yaml_tags_to_types[yaml_tag_suffix](seq)


YamlCodecDatetimes.register_with_pyyaml()
YamlCodecMisc.register_with_pyyaml()


class Aliasable(abc.ABC):
    def alias(self, locale: str = None):
        if locale is None:
            # locale = self.aliasFuncs()[self.defaultLocale]
            locale = self._defaultLocale
        return self._aliasFuncs[locale](self)

    @classmethod
    @abc.abstractmethod
    def aliasFuncs(cls) -> Dict[str, Callable[['Aliasable'], str]]:
        """
        Defines a map between locale strings, e.g., 'en_US', and Callables returning the localization of an instance.
        Callables must match the API of no-arg methods in a class, taking only a single `self` arg.
        """
        return {}  # Essentially this defines abstract static class data

    @classmethod
    def defaultLocale(cls) -> str:
        # if not hasattr(cls, '_defaultLocale'):
        #     cls._defaultLocale: str = next(iter(cls.aliasFuncs().keys()))
        return cls._defaultLocale

    @classmethod
    def setDefaultLocale(cls, locale: str):
        cls._defaultLocale = locale

    @staticmethod
    def initAliasable(cls_: type):
        cls_._aliasFuncs: Dict[str, Callable] = cls_.aliasFuncs()
        cls_._defaultLocale: str = next(iter(cls_._aliasFuncs.keys()))

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__isabstractmethod__" not in cls.aliasFuncs.__dict__ or not cls.aliasFuncs.__isabstractmethod__:
            # Only for subclasses which have implemented `aliasFuncs`
            cls.initAliasable(cls)
        # if not any([hasattr(base, '_subclasses') and cls._subclasses == base._subclasses for base in cls.__bases__]):
        #     cls._subclasses: List[Type['Aliasable']] = []
        #     for c in cls.__bases__:  # Register subclasses since Aliasable.__subclasses__() doesn't seem to do so reliably
        #         if issubclass(c, Aliasable):
        #             c._subclasses.append(cls)

    # @classmethod
    # def subclasses(cls):
    #     return cls._subclasses


class AliasableEnum(Aliasable, DataclassValuedEnum, metaclass=AenumABCMeta):
    @classmethod
    @lru_cache
    def aliases_to_members_deep(
            cls,
            alias_func: Callable[['AliasableEnum', str], str] = lambda x, loc: x.alias(loc)
    ) -> Dict[str, 'AliasableEnum']:
        """
        Returns a mapping from aliases to enum members for the members of all subclasses of `cls`.
        Warning: In the case of duplicate keys among multiple subclasses,
        the function behavior is undefined for which enum member is returned in the value.
        """
            # return {sub: {a.alias(locale): a for a in sub} for sub in getAllSubclasses(cls, includeSelf=True)}
        return {alias_func(a): a for sub in getAllSubclasses(cls, includeSelf=True) for a in sub}


class AliasableHierEnum(Aliasable, HierarchicalEnum):
    @classmethod
    def root_class(cls) -> type:
        """
        Return the common superclass for all nodes in the hierarchy.
        Default behavior is to return the member of the hierarchy which is a direct subclass of HierarchicalEnum.
        In the case of multiple inheritance, this will return the first superclass in the MRO which is a direct
        subclass of HierarchicalEnum.
        """
        if cls._ROOT_CLASS is not None:
            return cls._ROOT_CLASS
        elif cls == AliasableHierEnum:
            return cls
        elif AliasableHierEnum in cls.__bases__:
            cls._ROOT_CLASS = cls
            return cls
        else:
            return cls.__bases__[0].root_class()

    @classmethod
    @lru_cache
    def aliases_to_members(
            cls,
            alias_func: Callable[['AliasableHierEnum', str], str] = lambda x, loc: x.alias(loc)
    ) -> Dict[str, 'AliasableHierEnum']:
        """
        Returns a mapping from aliases to enum members for the members of all subclasses of `cls`.
        Warning: In the case of duplicate keys in the subclass DAG,
        the function behavior is undefined for which enum member is returned in the value.
        :param alias_func: Alias function. Defaults to standard alias, but others might be wanted, like `builtins._e`.
        """
        out = {alias_func(sub()): sub for sub in getAllSubclasses(cls)}
        if len(out) < len(getAllSubclasses(cls)):
            subs: Dict[type, str] = {c: c().alias(locale) for c in getAllSubclasses(cls)}
            for sub, alias in copy.copy(subs).items():
                if alias in out:
                    subs.pop(sub)
                    out.pop(alias)
            raise ValueError(f'The subclass DAG of {cls} contains duplicate localizations: {subs.keys()}')
        return out