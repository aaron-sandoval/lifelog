"""
Created on Jan 10, 2018
@author: Aaron
Temporary development code snippets to test out features in development. Not permanent test code.
"""
import sys
import src.TimesheetGlobals as Global
from src.Task import Task
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import numpy as np
from external_modules import kiwilib
import src.Catalogs as Cats
import src.Collectibles as Collxs
import catalogs.SocialGroups as sg
import streamlit as st
import pygraphviz as pgv
import networkx as nx
import yaml

module = 0

if module == 1:
    data1 = ['12/17/2017', '10:30 AM', '11:56 AM']
    data2 = ['12/17/2017', '10:44 AM', '11:06 AM']
    task1 = Task(data1)
    task2 = Task(data2)
    # print(task1)
    # print(task1.start)
    # print(task1.spanningTimePeriod(task2))
    # print(task1.duration())
    # print(task1.withinCalendarDay())
    # print(data1[:2])
    arr = [0, 1, 2, 3, 4]
    # for i in arr[::-1]:
    for i, num in enumerate(reversed(arr)):
        print(num)
elif module == 2:
    # -*- coding: utf-8 -*-
    """
    Created on Wed Jul 20 15:02:01 2016
    
    @author: Aaron Sandoval
    """
    import re

    # def avg(a, b, c = None):
    #    if (c is None):
    #        print ("%d and %d" % (np.average(a), np.average(b)))
    #        result = np.average([np.average(a), np.sum(b)])
    #    else:
    #        print ("%d and %d and %d" % (np.average(a), np.average(b), np.average(c)))
    #        result = np.average([np.average(a), np.sum(b), np.sum(c)])
    #    return result
    # def add(a):
    #    sum = 0
    #    for element in a:
    #        sum += element
    #    return sum

    #     genericNumberRegex = re.compile(r"((?: \d+ )?\d+[./,]?\d*)")
    #     myFloatedNumberRegex = re.compile(r"(^\d+(?:\.?)(?:\d*))(?: +)(apples)[ ,.:;']")
    subirRegex = re.compile(r"(SUBI)")

    testPhrase = 'SUBIR, 30'
    testPhrase2 = 'RESUBIX, 30'
    testPhrase3 = 'SUBI'
    testPhrase4 = 'SUBI, DUBI'
    #     res = myFloatedNumberRegex.findall(testPhrase2);
    #     print("Number: <" + str(res[0][0]) + ">")
    #     print("Phrase: <" + str(res[0][1]) + ">")
    # print(str(myFloatedNumberRegex))

    #     regex = 'SUBI(?!R)'
    regex = '(?<!\w)SUBI(?!\w)'
    retVal = re.sub(regex, 'SUBIR', testPhrase)
    print(retVal)
    retVal = re.sub(regex, 'SUBIR', testPhrase2)
    print(retVal)
    retVal = re.sub(regex, 'SUBIR', testPhrase3)
    print(retVal)
    retVal = re.sub(regex, 'SUBIR', testPhrase4)
    print(retVal)
elif (module == 3):
    def sublist(sublist, bigList):
        if (len(sublist) > len(bigList) | sublist[0] not in bigList): return False
        st = bigList.index(sublist[0])
        sublistLen = len(sublist)
        if (len(bigList) < st + sublistLen):     return False
        return (sublist == bigList[st:st + sublistLen])


    #     isSublist = sublist([0,1,3], [0,3])
    #     print(isSublist)
    isSublist = sublist([0, 3], [0, 3])
    print(isSublist)
    isSublist = sublist([0, 3], [0, 3, 1])
    print(isSublist)
    isSublist = sublist([0, 3], [0, 1, 3])
    print(isSublist)
elif (module == 4):
    df = pd.DataFrame({'name': ['User 1', 'User 2', 'User 3']})
    msgpath = Global.rootProjectPath() + 'Tests\\MP1.msgpack'
    df.to_msgpack(msgpath, encoding='utf-8')
    df1 = pd.read_msgpack(msgpath, encoding='utf-8')
    print(df)
    print(df1)
elif (module == 5):
    #     with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Monroe
    # http://xkcd.com/418/

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xticks([])
    plt.yticks([])
    ax.set_ylim([-30, 10])

    data = np.ones(100)
    data[70:] -= np.arange(30)

    plt.annotate(
        'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
        xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

    plt.plot(data)

    plt.xlabel('time')
    plt.ylabel('my overall health')
    fig.text(
        0.5, 0.05,
        '"Stove Ownership" from xkcd by Randall Monroe',
        ha='center')

    # Based on "The Data So Far" from XKCD by Randall Monroe
    # http://xkcd.com/373/

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.bar([0, 1], [0, 100], 0.25)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks([0, 1])
    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([0, 110])
    ax.set_xticklabels(['CONFIRMED BY\nEXPERIMENT', 'REFUTED BY\nEXPERIMENT'])
    plt.yticks([])

    plt.title("CLAIMS OF SUPERNATURAL POWERS")

    fig.text(
        0.5, 0.05,
        '"The Data So Far" from xkcd by Randall Monroe',
        ha='center')

    plt.show()
elif (module == 6):
    fnx = lambda: np.random.randint(3, 10, 10)
    y = np.row_stack((fnx(), fnx(), fnx()))
    z = pd.DataFrame(y, columns=list('ABCDEFGHIJ'))
    # this call to 'cumsum' (cumulative sum), passing in your y data, 
    # is necessary to avoid having to manually order the datasets
    x = np.arange(3)
    case = 0
    if (case == 0):
        fig = plt.figure()
        pl = z.plot(kind='area')
        ax = plt.gca()

    if (case == 1):
        y_stack = np.cumsum(z, axis=1)  # a 3x10 array

        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        ax1.fill_between(x, 0, y_stack[0, :], facecolor="#CC6666", alpha=.7)
        ax1.fill_between(x, y_stack[0, :], y_stack[1, :], facecolor="#1DACD6", alpha=.7)
        ax1.fill_between(x, y_stack[1, :], y_stack[2, :], facecolor="#6E5160")


# def test7(): TimesheetQuery parser
#     from antlr4 import *
#     from TimesheetQueryLexer import TimesheetQueryLexer
#     from TimesheetQueryParser import TimesheetQueryParser
#     from MyTimesheetQueryListener import MyTimesheetQueryListener
#
#     filePath = Global.rootProjectPath() + '\\tsqparser\\testQueries_1.txt'
#     with open(filePath, 'r', encoding='utf-8') as rulesList:
#         text = rulesList.read()
#     lexer = TimesheetQueryLexer(InputStream(text))
#     stream = CommonTokenStream(lexer)
#     parser = TimesheetQueryParser(stream)
#     tree = parser.ruleList()
#
#     # outputPath = filePath[:-4] + '_OUT'+ '.txt'
#     # with open(outputPath, 'w', encoding='utf-8') as :
def PickleTest(df):
    pass


def test8():
    kiwilib.kiwiTest()


def test9():
    class T1:
        def __init__(self, val):
            self.val = [val]

        def addVal(self, newVal):
            self.val.append(newVal)

        def __str__(self):
            return self.val.__str__()

    class HasDF:
        def __init__(self, df):
            self.df = df

    df = pd.DataFrame({'a': [1, 2, 3], 'b': [T1(1), T1(2), T1(3)]})
    myDF = HasDF(df)
    mask = myDF.df['a'] % 2 == 1
    myDF.df.loc[mask, 'b'].apply(lambda object: object.addVal(5))
    print(f'{myDF.df}')


def test10():
    df1 = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], index=range(3), columns=['a', 'b', 'c'])
    df2 = pd.DataFrame([[-1, -2, -3], [-4, -5, -6]], index=[2, 11], columns=['a', 'b', 'c'])
    # a = df1.copy()
    a = df1.join(df2)
    b = 2
    print(df1)


# def test11():
    # from kiwilib import HeapNode
    # lists = [HeapNode(1, HeapNode(3, HeapNode(5, HeapNode(7, HeapNode(9))))),
    #          # HeapNode(0, HeapNode(2, HeapNode(3, HeapNode(10, HeapNode(11))))),
    #          # HeapNode(2, HeapNode(2, HeapNode(3, HeapNode(18, HeapNode(19))))),
    #          # HeapNode(7, HeapNode(7, HeapNode(12, HeapNode(18, HeapNode(19))))),
    #          # HeapNode(2, HeapNode(2, HeapNode(3, HeapNode(18, HeapNode(19))))),
    #          # HeapNode(2, HeapNode(2, HeapNode(3, HeapNode(18, HeapNode(19))))),
    #          HeapNode(4, HeapNode(4, HeapNode(4, HeapNode(8, HeapNode(11)))))
    #          ]
    # # list2 = HeapNode(0,HeapNode(2,HeapNode(3,HeapNode(8,HeapNode(11)))))
    # # lists = [list1, list2]
    # h = kiwilib.MinHeap(lists, lambda x: x.val)
    # outHead = h.pop()
    # cur = outHead
    # while h.size > 0:
    #     print(f'h:\n{h}')
    #     if cur.next:
    #         h.push(cur.next)
    #         assert h.validate(), f'Invalid heap post-push: {h}'
    #     cur.next = h.pop()
    #     assert h.validate(), f'Invalid heap post-pop: {h}'
    #     cur = cur.next
    # i = outHead
    # while i:
    #     print(i.val)
    #     i = i.next


def test12():
    # print(Collxs.Collectible.CATALOG_FIELDS)
    cat = Cats.LinearCatalog(Collxs.Collectible)
    a = Collxs.Collectible(name='Steve', firstTaskID=5, firstTime=datetime.datetime(2020, 1, 2, 1, 1),
                           firstCircad=datetime.date(2020, 1, 1))
    b = Collxs.Collectible(name='Mare', firstTaskID=6, firstTime=datetime.datetime(2020, 1, 1, 12, 6),
                           firstCircad=datetime.date(2020, 1, 1))
    cat.collect(a)
    print(f'has a: {cat.hasCollectible(a)}')
    print(f'has b: {cat.hasCollectible(b)}')
    cat.collect([a, b])
    c = cat.getMostRecent(datetime.datetime(2020, 1, 1, 1))
    c = cat.getMostRecent(datetime.datetime(2020, 1, 2, 1))
    c = cat.getMostRecent(datetime.datetime(2020, 3, 1, 1))
    c = cat.getMostRecent([datetime.datetime(2020, 1, 1, 1), datetime.datetime(2020, 3, 1, 1)])
    # cat.write()
    # cat.read()
    # print(a.CATALOG_FIELDS)
    # print(Collxs.Collectible.CATALOG_FIELDS)


def test13():
    # cm = Collxs.ConsumptionMedia(name='Steve', firstTaskID=5, firstTime=datetime.datetime(2020, 1, 2, 1, 1),
    #                        firstCircad=datetime.date(2020, 1, 1))
    cCat = Collxs.Collectible.CATALOG_FIELDS()
    mCat = Collxs.Media.CATALOG_FIELDS()
    cmCat = Collxs.ConsumptionMedia.CATALOG_FIELDS()
    cDef = Collxs.Collectible.DEFAULT_MEMBERS()
    mDef = Collxs.Media.DEFAULT_MEMBERS()
    cmDef = Collxs.ConsumptionMedia.DEFAULT_MEMBERS()
    # mdict = Collxs.Media.boilerplateDict()
    # mCat = Collxs.Media.CATALOG_FIELDS()


# Audiobook catalog
def test14():
    bCat = Collxs.Audiobook.CATALOG_FIELDS()
    bDef = Collxs.Audiobook.DEFAULT_MEMBERS()
    b = Collxs.Audiobook(name='Steve', firstTaskID=5, firstTime=datetime.datetime(2020, 1, 2, 1, 1),
                         firstCircad=datetime.date(2020, 1, 1))
    bookCat = Cats.LinearCatalog(Collxs.Audiobook, loadYaml=True)
    bookCat.collect(b)
    a = 1


# getColumnClassDict
def test15():
    a = Global.ListColumn.getColumnClassDict()
    b = 1


# Enum tree: class hierarchy
def test16():
    class Structure:
        def __repr__(self):
            if type(self) == Structure:
                return type(self).__name__
            else:
                # return cls.__bases__[0].name() + '.' +  cls.__name__
                return type(self).__bases__[0]().__repr__() + '.' + type(self).__name__

        def __eq__(self, other):
            return type(self) == type(other)

    class House(Structure):
        pass

    class Tower(Structure):
        pass

    class GreenHouse(House):
        pass

    class YellowHouse(House):
        pass

    class SmallTower(Tower):
        pass

    class BigTower(Tower):
        pass

    print(BigTower() == BigTower())
    print(BigTower() is BigTower())
    print(House() != GreenHouse())
    print(Structure() == BigTower())
    print(str(Tower()))
    print(str(Tower))


# Enum tree: class hierarchy 2
def test17():
    class Structure:
        @classmethod
        def name(cls):
            if cls == Structure:
                return cls.__name__
            else:
                return cls.__bases__[0].name() + '.' + cls.__name__

    class House(Structure):
        pass

    class Tower(Structure):
        pass

    class GreenHouse(House):
        pass

    class YellowHouse(House):
        pass

    class SmallTower(Tower):
        pass

    class BigTower(Tower):
        pass

    print(BigTower.name())  # Structure.Tower.BigTower
    print(House.name())  # Structure.House
    print(Structure.name())  # Structure


# Enum tree: kiwilib implementation test
def test18():
    class Treenum(kiwilib.HierarchicalEnum): pass

    # @staticmethod
    # def ROOT_CLASS(): return Treenum

    class Branch1(Treenum): pass

    class Twig1(Branch1): pass

    print(f'Treenum: {Treenum()}')
    print(f'Branch1: {Branch1()}')
    print(f'Twig1: {Twig1()}')


# Audiobook genres, write to yaml
def test19():
    b = Collxs.Audiobook(name='Steve', firstTaskID=5, firstTime=datetime.datetime(2020, 1, 2, 1, 1),
                         firstCircad=datetime.date(2020, 1, 1), genres=[Collxs.Media.Fiction(), Collxs.Media.Educational()])
    a = Collxs.Audiobook(name='Mare', firstTaskID=6, firstTime=datetime.datetime(2020, 1, 1, 12, 6),
                         firstCircad=datetime.date(2020, 1, 1), timeSpent=datetime.timedelta(days=4, hours=3),
                         genres=[Collxs.Media.Genre()])
    bookCat = Cats.LinearCatalog(Collxs.Audiobook, loadYaml=False)
    bookCat.collect([b, a])
    # g, e, s = Collxs.Media.Genre(), Collxs.Media.Educational(), Collxs.Media.SelfHelp()
    # gStr = yaml.dump([g,e,s])
    bookCat.write()
    roundTrip = Cats.LinearCatalog(Collxs.Audiobook, loadYaml=True)
    print(roundTrip.collxn)


# Various Github Copilot tests
def test20():
    a = kiwilib.getAllSubclasses(Collxs.Media.Genre)
    b = 1


# Create a graph of the Person.SocialGroup subclass hierarchy
def test21():
    """
    Creates a graph of the Person.SocialGroup subclass hierarchy.
    Uses the graphviz library to create the graph, and streamlit to display it.
    """
    Sg = sg.SocialGroup
    G = pgv.AGraph(directed=True)
    G.node_attr["shape"] = "box"
    G.edge_attr["color"] = "blue"
    G.add_node(repr(Sg()))
    for cls in kiwilib.getAllSubclasses(Sg):
        for superclass in cls.__bases__:
            G.add_edge(repr(superclass()), repr(cls()))
    st.graphviz_chart(G.string(), use_container_width=True)


# Streamlit basic test
def test22():
    print('test22')
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    st.line_chart(chart_data)


# DAGCatalog YAML write
def test23():
    g = nx.gn_graph(5, seed=8)
    with open(Global.rootProjectPath()+r'/tests/NX_test1.yaml', 'w') as file:
        yaml.dump(g, file, sort_keys=False)


# DAGCatalog YAML write
def test24():
    with open(Global.rootProjectPath() + r'/tests/NX_test1.yaml', 'r') as file:
        yaml_data = yaml.safe_load_all(file)
        a = [d for d in yaml_data]
    a[1]['nodes'][55] = set()
    a[1]['adj'][55] = [3, 4]
    with open(Global.rootProjectPath() + r'/tests/NX_test1.yaml', 'w') as file:
        yaml.dump_all(a, file, sort_keys=False)
    b=1


# Debug TimesheetDataset.fileSuffix assignment to str rather than ''. It was just a bug in @fileSuffix.setter method.
def test25():
    class A:
        def __init__(self, df, cats=None, f: str = ''):
            self.f = f
            if self.f != f or self.f is str:
                raise TypeError(f'f assignment error: {f=}, {self.f=}')

    df = pd.DataFrame([1, 2, 3])
    a = A(df)
    a = A(df, f='hi')
    a = A(df, f='')


test25()
