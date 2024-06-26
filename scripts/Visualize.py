"""
Created on Nov 22, 2018

@author: Aaron
Holds functions used to collect datasets from database and create graphics from them.
"""
import abc
import datetime
import os
import re

import portion
import matplotlib.text
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Union, Iterable, List, Tuple, Set, NamedTuple, Type, Any, Dict
from enum import Enum
from bisect import bisect_right
from itertools import accumulate
import inspect
import streamlit as st
import seaborn as sns

from src.TimesheetDataset import *
from src.Description import Description
from i18n_l10n import internationalization as i18n


global babelx  # Babel extractor wrapper, must be accessible everywhere in the module
babelx = i18n.babelx
STR_BACKEND = _k('👀 *Peek into the Backend*')

_enum_alias_map: Dict[str, kiwilib.AliasableEnum] = \
    kiwilib.AliasableEnum.aliases_to_members_deep(alias_func=_e)
# Also add keys for the alternative language since the dict isn't updated upon a change in language selection
babelx.setLang(i18n.lang_es)
_enum_alias_map.update(kiwilib.AliasableEnum.aliases_to_members_deep(alias_func=_e))

babelx.setLang(i18n.lang_en)
_hier_enum_alias_map: Dict[str, kiwilib.AliasableHierEnum] = \
    kiwilib.AliasableHierEnum.aliases_to_members(alias_func=_e)
babelx.setLang(i18n.lang_es)
_hier_enum_alias_map.update(kiwilib.AliasableHierEnum.aliases_to_members(alias_func=_e))
babelx.setLang(i18n.lang_en)

def main(paths: List[str], catalogSuffix='', locale='en_US', audience=Global.Privacy.PUBLIC):

    def babelExtractEnumLike() -> None:
        # classes = kiwilib.getAllSubclasses(kiwilib.HierarchicalEnum)
        for c in kiwilib.getAllSubclasses(kiwilib.HierarchicalEnum):
            _e(c())
            # _a(c)
        babelx.flush()

    def babelExtractTSDS(tsds: TimesheetDataset, minTokCount=5) -> None:
        """
        Uses BabelIntermediateExtractor to extract the most commonly-used tokens in tsds.
        :param tsds:
        :param minTokCount: Cutoff token count. Tokens with at least minTokCount instances in tsds will be extracted.
        The rest will be ignored for extraction purposes.
        """
        toks = tsds.timesheetdf.tokenCounter()
        toks = toks[:bisect_right(-toks.values, -minTokCount)]
        for tok in toks.index:
            _t(tok)
        babelx.flush()

    global babelx
    babelx.setLang(i18n.localeDict[locale])
    kiwilib.Aliasable.setDefaultLocale(locale)
    tsds = loadAndMergeDatasets(paths, catalogSuffix)
    figs = getFigs(tsds, audience)

    # babelExtractEnumLike()
    # babelExtractTSDS(tsds, 20)
    # babelx.firstWrite = True
    # babelExtractTSDS(tsds, 10)
    # vis = miscTest(tsds, 4)
    babelx.flush()
    # privacy=most private of all figs
    return Global.writePersistent(figs, 4, privacy=audience)


def loadAndMergeDatasets(paths: List[str], fileSuffix='') -> TimesheetDataset:
    """
    Loads one or more TimesheetDataset objects from pickle files.
    If >1 file specified, merges the TimesheetDataFrame objects and writes the merged tsdf to a pickle.
    :param paths: List of full paths to TimesheetDataset .pkl files.
    :param fileSuffix: TimesheetDataset write and Catalog read/write file suffixes.
    :return: Merged TimesheetDataset.
    """
    tsdsList = [TimesheetDataset(pd.read_pickle(p), fileSuffix=fileSuffix) for p in paths]
    if len(tsdsList) > 1:
        mergedTSDF = TimesheetDataFrame.mergeTSDFs([t.timesheetdf for t in tsdsList])
        tsds = TimesheetDataset(mergedTSDF, fileSuffix=fileSuffix)
    else:
        tsds = tsdsList[0]
    tsds.loadCatalogs(fileSuffix=fileSuffix)
    tsds.validate()
    if len(tsdsList) > 1:
        Global.writePersistent(tsds.timesheetdf.df, 3, tsds.fileSuffix)
    return tsds


class XHSectionData(NamedTuple):
    """Enum member values for ExhibitSection."""
    sortKey: int = 0  # TODO: get rid of sortKey, sorting determined by pages filename prefixes
    # title: str = 'Section Title'
    # intro: str = 'Section intro.'
    # outro: str = 'Section outro.'


class ExhibitSection(Enum):
    @classmethod
    def srted(cls):
        """Sorts the ExhibitSection instances by their XHSectionData.sortKey"""
        if not hasattr('_srted', cls):
            cls._srted = sorted(cls._member_map_.values(), key=lambda x: x.value.sortKey)
        return cls._srted

    def exhibitStreamlitEnter(self):
        st.header(self.value.title)
        if self.value.intro not in (None, ''):
            st.markdown(self.value.intro)

    def exhibitStreamlitExit(self):
        if self.value.outro not in (None, ''):
            st.markdown(self.value.outro)

    SLEEP = XHSectionData(sortKey=64)
    PEOPLE = XHSectionData(sortKey=96)
    METAPROJECT = XHSectionData(sortKey=8)


_ArtistAlignment = NamedTuple('_ArtistAlignment', [('name', str), ('x', float), ('y', float),
                                                  ('ha', str), ('va', str)])


class ArtistAlignment(Enum):
    def text(self, text, ax: plt.Axes, **kwargs):
        _, textX, textY, ha, va = self.value
        ax.text(textX, textY, text, ha=ha, va=va, transform=ax.transAxes,
                 bbox={'facecolor': 'white' if 'facecolor' not in kwargs else kwargs['facecolor'],
                       'alpha': .6 if 'alpha' not in kwargs else kwargs['alpha']})

    NW = _ArtistAlignment('NW', .05, .95, 'left', 'top')
    NE = _ArtistAlignment('NE', .95, .95, 'right', 'top')
    SE = _ArtistAlignment('NE', .95, .05, 'right', 'bottom')
    SW = _ArtistAlignment('NE', .05, .05, 'left', 'bottom')


class Visual(abc.ABC):
    @abc.abstractmethod
    def save(self, fileName: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def localize(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def exhibit(self) -> None:
        raise NotImplementedError


class MatplotlibVisual(Visual):
    def __init__(self, figsize=(10, 5), **kwargs):
        self.fig: plt.Figure = plt.figure(figsize=figsize, **kwargs)

    def save(self, fileName):
        self.fig.savefig(os.path.join(Global.rootProjectPath(), 'VS_Figures', fileName + '.png'))

    def exhibit(self) -> None:
        self.localize()
        st.pyplot(self.fig, use_container_width=True)

    def localize(self):
        def artist_filter(a: plt.Artist):
            """
            Filters out artists which aren't translatable text, such as numbers.
            """
            return (
                isinstance(a, matplotlib.text.Text) and
                len(a.get_text()) > 0 and
                re.search(r'[a-zA-Z]', a.get_text()) is not None
            )

        text_artists: List[matplotlib.text.Text] = self.fig.findobj(artist_filter)
        for artist in text_artists:
            t: str = artist.get_text()
            if t in _enum_alias_map:
                artist.set_text(_e(_enum_alias_map[t]))
            elif t in _hier_enum_alias_map:
                artist.set_text(_e(_hier_enum_alias_map[t]()))
            else:
                artist.set_text(_k(t))




class SingleAxisStaticVisual(MatplotlibVisual):
    """
    Creates visualizations. Takes inputs for chart type, standard domain types, visual features, etc.
    """

    # TODO: add inheritance for a more general superclass
    def show(self):
        self.fig.show()

    @staticmethod
    def weekdayDomain(ser):
        if any(ser.index > 7) or any(ser.index < 0):
            print('ERROR: incorrect indices for weekday domain.')
            return ser
        vals = [_a(x) for x in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']]
        keys = [6, 0, 1, 2, 3, 4, 5]
        weekdayMap = dict(zip(keys, vals))
        ser.index = ser.index.map(weekdayMap)
        ser = ser.reindex(vals)
        return ser

    @staticmethod
    def workdayDomain(ser):
        return SingleAxisStaticVisual.weekdayDomain(ser).drop([_a('Sat'), _a('Sun')])

    @staticmethod
    def realTimeDomain(ser):
        # Everything seems to work without any trouble
        return ser

    @staticmethod
    def weeksDomain(serdf):
        ind = pd.Series(serdf.index)
        weekDate = getWeekDate(ind)
        serdf.index = list(weekDate)
        return serdf

    @staticmethod
    def barFormat(fig, ax, pl):
        for p in ax.patches:
            p.set_facecolor((.2, .5, .2))

    @staticmethod
    def lineFormat(fig, ax, pl):
        pl.grid(True, axis='x')

    @staticmethod
    def areaFormat(fig, ax, pl):
        raise NotImplementedError

    @staticmethod
    def clusteredBar(data, totalWidth=None, **kwargs):
        nBars = data.size
        nClusters = len(data.iloc[:, 0])
        nBarsPerCluster = len(data.columns)
        if totalWidth is None:
            totalWidth = min(nClusters * (nBarsPerCluster+1) * 1500 // 42, 1800)
        barWidth = np.max([np.floor(totalWidth / nBars / 5) * 5, 5])
        clusterSpace = barWidth
        xPos = np.zeros([nClusters, nBarsPerCluster])
        fig = plt.figure(figsize=kwargs['figsize'] if 'figsize' in kwargs else None)
        for i in range(nBarsPerCluster):
            xPos[:, i] = np.arange(nClusters) * (barWidth * nBarsPerCluster + clusterSpace) + i * barWidth
            plt.bar(xPos[:, i], data.iloc[:, i], width=barWidth, edgecolor='white', label=data.columns[i])
        plt.xticks(xPos[:, 0] + barWidth * (nBarsPerCluster - 1) / 2, [d for d in data.index])
        ax = fig.axes[0]
        plt.legend(loc='lower right')
        # pl = 0
        return [fig, ax, None]

    # nonStandardMap = {
    #     'clusteredBar': clusteredBar,
    # }
    @classmethod
    def nonStandardMap(cls):
        if not hasattr(cls, '_nonStandardMap'):
            cls._nonStandardMap = {
                'clusteredBar': cls.clusteredBar,
            }
        return cls._nonStandardMap

    @classmethod
    def kindMap(cls):
        if not hasattr(cls, '_kindMap'):
            cls._kindMap = {
                'line': cls.lineFormat,
                'bar': cls.barFormat,
                'area': cls.areaFormat,
            }
        return cls._kindMap
    #     domLabels = getLabels(data, domain)
    # domainMap = {
    #     'weekday': weekdayDomain,
    #     'workday': workdayDomain,
    #     'realTime': realTimeDomain,
    #     'weeks': weeksDomain,
    # }
    @classmethod
    def domainMap(cls):
        if not hasattr(cls, '_domainMap'):
            cls._domainMap = {
                'weekday': cls.weekdayDomain,
                'workday': cls.workdayDomain,
                'realTime': cls.realTimeDomain,
                'weeks': cls.weeksDomain,
            }
        return cls._domainMap

    def __init__(self, data: pd.DataFrame, kind='line', domain: str = None, title:str = None, xlabel=None,
                 ylabel=None, grid='off', text:str = None, textPos: ArtistAlignment = ArtistAlignment.SE, show=False,
                 **kwargs):
        if title is None: title = _a('Untitled')
        if domain in self.domainMap():
            data = self.domainMap()[domain](data)  # Gets a preset domain from a map if needed
        if kind in self.nonStandardMap():
            [self.fig, self.ax, self.pl] = self.nonStandardMap()[kind](data, **kwargs)
        else:
            self.fig = plt.figure()
            self.pl = data.plot(kind=kind)
            self.ax = plt.gca()
            if kind in self.kindMap():
                self.kindMap()[kind](self.fig, self.ax, self.pl)
        if grid == 'on':    plt.grid(True, axis='y')
        if text:
            _, textX, textY, ha, va = textPos.value
            plt.text(textX, textY, text, ha=ha, va=va, transform=self.ax.transAxes,
                     bbox={'facecolor': 'white', 'alpha': .6})
        if title:           plt.title(title)
        if xlabel:          plt.xlabel(_k(xlabel))
        if ylabel:          plt.ylabel(_k(ylabel))
        if show:            self.show()


class GraphicExhibit:
    """ Type containing data for exhibiting generic graphics. See GRAPHIC_TYPE_FUNCS for supported graphic types. """
    # GRAPHIC_TYPE_FUNCS = {
    #     plt.Figure: lambda x: st.pyplot(x, use_container_width=True)
    # }

    def __init__(self,
                 graphic: Visual,
                 privacy: Global.Privacy = Global.Privacy.PRIVATE,  # Default to PRIVATE for security.
                 preText: str = None,
                 postText: str = None,
                 section: ExhibitSection = None,
                 sortKey: int = 0
                 ):
        # if type(graphic) not in self.GRAPHIC_TYPE_FUNCS:
        #     raise TypeError(f'{type(graphic)} graphic type not supported.')
        self.graphic = graphic
        self.privacy = privacy
        self.preTextMD = preText  # Markdown-format text.
        self.postTextMD = postText  # Markdown-format text.
        self.section = section
        self.sortKey = sortKey

    def __repr__(self):
        return f'{type(self).__name__}: {self.section} at {id(self)}'

    def exhibitStreamlit(self):
        if self.preTextMD is not None:
            st.markdown(self.preTextMD)
        self.graphic.localize()
        self.graphic.exhibit()
        if self.postTextMD is not None:
            st.markdown(self.postTextMD)


def stackplot_and_totals_stackbar(
        x: pd.Series,
        y: pd.DataFrame,
        totals: pd.Series = None,
        stack_names: Iterable[Any] = None,
        figsize: Tuple = (10, 4),
        titles: Tuple[str, str] = (None, 'Totals'),
        xlabel: str = None,
        ylabels: Tuple[str, str] = (None, None),
        colors: Iterable[Union[Tuple, str]] = None,
        legend_labels: Iterable[str] = None,
        legend_loc: str = 'best',
        xlabel_major_formatter=mdates.DateFormatter('%Y-%m'),
        xtick_minor_locator=mdates.MonthLocator(bymonth=(1, 4, 7, 10)),
        **kwargs
) -> MatplotlibVisual:
    """
    Returns a figure primarily featuring a stackplot.
    Also includes a small subplot with a stacked bar plot of the totals.
    """

    # Assign defaults for None-valued args
    if stack_names is None: stack_names = y.columns
    if colors is None: colors = [x.color_hex for x in stack_names]
    if legend_labels is None: legend_labels = [_e(x) for x in stack_names]

    graphic = MatplotlibVisual(figsize=figsize, constrained_layout=True)
    fig = graphic.fig
    gridspec = fig.add_gridspec(1, 10 if 'gridspec_w' not in kwargs else kwargs['gridspec_w'])
    ax0 = fig.add_subplot(gridspec[0, :-1])
    ax1 = fig.add_subplot(gridspec[0, -1])

    # Subplot 1
    ax0.stackplot(x, y.T, colors=colors)
    ax0.legend(legend_labels, loc=legend_loc)
    ax0.grid(axis='y', alpha=0.4)
    if xlabel is not None: ax0.set_xlabel(xlabel)
    if ylabels[0] is not None: ax0.set_ylabel(ylabels[0])
    if titles[0] is not None: ax0.set_title(titles[0])
    if xlabel_major_formatter is not None: ax0.xaxis.set_major_formatter(xlabel_major_formatter)
    if xtick_minor_locator is not None: ax0.xaxis.set_minor_locator(xtick_minor_locator)

    # Calculate totals for subplot 2
    if totals is None:
        totals = y.sum(axis=0)
    totalsAug = pd.concat([pd.Series([0]), totals])
    totalsAug = pd.Series(accumulate(totalsAug), index=np.concatenate([[0], totals.index]))

    # Subplot 2
    ax1.bar([1], totals, bottom=totalsAug.iloc[:-1], color=colors)
    if titles[1] is not None: ax1.set_title(titles[1])
    if ylabels[1] is not None: ax1.set_ylabel(ylabels[1])
    for side in ['top', 'right', 'bottom', 'left']:
        ax1.spines[side].set_visible(False)
    ax1.get_xaxis().set_visible(False)

    return graphic


def stackbarplot_and_totals(
        x: pd.Series,
        y: pd.DataFrame,
        totals: pd.Series = None,
        stack_names: Iterable[Any] = None,
        figsize: Tuple = (10, 4),
        titles: Tuple[str] = (None, 'Totals'),
        xlabel: str = None,
        ylabels: Tuple[str] = (None, None),
        colors: Iterable[Union[Tuple, str]] = None,
        legend_labels: Iterable[str] = None,
        legend_loc: str = 'best',
        xlabel_major_formatter=mdates.DateFormatter('%Y-%m'),
        xtick_minor_locator=mdates.MonthLocator(bymonth=(1, 4, 7, 10)),
        **kwargs
) -> MatplotlibVisual:
    """
    Returns a figure primarily featuring a stacked bar plot.
    Also includes a small subplot with a stacked bar plot of the totals.
    """
    # Assign defaults for None-valued args
    if stack_names is None: stack_names = y.columns
    if colors is None: colors = [x.color_hex for x in stack_names]
    if legend_labels is None: legend_labels = [_e(x) for x in stack_names]

    graphic = MatplotlibVisual(figsize=figsize, constrained_layout=True)
    fig = graphic.fig
    gridspec = fig.add_gridspec(1, 10 if 'gridspec_w' not in kwargs else kwargs['gridspec_w'])
    ax0 = fig.add_subplot(gridspec[0, :-1])
    ax1 = fig.add_subplot(gridspec[0, -1])

    # Prepare subplot 1 `plt.stairs` data
    bottom = pd.Series(0, index=x)
    # a = pd.DatetimeIndex([x[0]-0.5*x[0].daysinmonth*pd.Timedelta(1, 'D')])
    # edges = (x+0.5*pd.DatetimeIndex(x).daysinmonth*pd.Timedelta(1, 'D')).union(a)
    # a = pd.DatetimeIndex([x[0]-np.diff(x)[0]])
    # import pdb; pdb.set_trace()
    # d = x.union(np.array([x[0] - x.freq, x[-1] + x.freq]))
    # # c = np.diff(x, append=x[-1]+np.diff(x)[-1])
    # c = np.diff(d)
    # b = pd.DatetimeIndex(0.5*c)
    # edges = d[:-1]+b

    # Subplot 1
    for i, c in enumerate(y.columns):
        # import pdb; pdb.set_trace()
        ax0.bar(x, y[c].T, color=colors[i], width=pd.DatetimeIndex(x).daysinmonth + 1, bottom=bottom)
        # ax0.stairs(y.iloc[:,i].values+bottom, edges, color=colors[i], baseline=bottom, fill=True)
        # print(f'{c}: {bottom =}')
        bottom += y[c].values
    ax0.grid(axis='y', alpha=0.4)
    # ax0.autoscale_view(tight=True)
    ax0.legend(legend_labels, loc=legend_loc)
    if xlabel is not None: ax0.set_xlabel(xlabel)
    if ylabels[0] is not None: ax0.set_ylabel(ylabels[0])
    if titles[0] is not None: ax0.set_title(titles[0])
    if xlabel_major_formatter is not None: ax0.xaxis.set_major_formatter(xlabel_major_formatter)
    if xtick_minor_locator is not None: ax0.xaxis.set_minor_locator(xtick_minor_locator)

    # Calculate totals for subplot 2
    if totals is None:
        totals = y.sum(axis=0)
    totalsAug = pd.concat([pd.Series([0]), totals])
    totalsAug = pd.Series(accumulate(totalsAug), index=np.concatenate([[0], totals.index]))

    # Subplot 2
    ax1.bar([1], totals, bottom=totalsAug.iloc[:-1], color=colors)
    if titles[1] is not None: ax1.set_title(titles[1])
    if ylabels[1] is not None: ax1.set_ylabel(ylabels[1])
    for side in ['top', 'right', 'bottom', 'left']:
        ax1.spines[side].set_visible(False)
    ax1.get_xaxis().set_visible(False)

    return graphic


def getDateRangeString(df) -> str:
    """
    Produces a string representing the date range of a dataframe. Useful for title or auxiliary plot text
    :param df:
    :return: String representing the date range of a dataframe
    """
    startString = df.head(1).circad.values[0].strftime('%Y-%m-%d')
    endString = df.tail(1).circad.values[0].strftime('%Y-%m-%d')
    return startString + '_' + endString


def getLabels(data, domain, subset=-1):
    domainMap = {
        'weekday': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'monthday': range(1, 32),
        'epoch': [epoch.alias() for epoch in list(Global.Epoch)]
    }
    try:
        labels = domainMap[domain]
    except(KeyError):
        print('Domain not in map')
    if (subset != -1):
        labels = np.array(labels)[subset].tolist()
    return labels


def getWeekday(ser):
    day = ser.apply(lambda x: x.weekday())
    return day.rename('weekday')


def getWeek(ser):
    #     For a series of dates, returns Timesheet week numbers, measured since TASK_ID_EPOCH
    ser = ser - Global.TASK_ID_EPOCH
    daysSinceEpoch = [t.days for t in list(ser)]
    weekList = [int(np.ceil(t / 7)) for t in daysSinceEpoch]
    week = pd.Series(weekList, name='week', index=ser.index)
    #     week = week.rename('week')
    return week


def getWeekDate(ser):
    EP = Global.TASK_ID_EPOCH
    ser1 = EP + ser.apply(lambda x: datetime.timedelta(weeks=x))
    return ser1 - datetime.timedelta(days=EP.weekday())


def timeToFloat(dfser, units='hour'):
    divisorMap = {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'week': 604800
    }
    if (units not in divisorMap.keys()):
        print('Invalid time unit arg')
    if (isinstance(dfser, pd.Series)):
        dfser = dfser.apply(datetime.timedelta.total_seconds) / divisorMap[units]
    elif (isinstance(dfser, pd.DataFrame)):
        for col in dfser.columns:
            dfser[col] = timeToFloat(dfser[col], units)
    else:
        if (not is_list_like(dfser)):
            dfser = (dfser,)
            dfser = [datetime.timedelta.total_seconds(i) / divisorMap[units] for i in dfser]
            return dfser[0]
        else:
            dfser = [datetime.timedelta.total_seconds(i) / divisorMap[units] for i in dfser]
    return dfser


class GraphicMaker:
    """
    Not really used as a class, merely a container for a collection of visualization functions.
    Each function takes a TimesheetDataset object as an input and outputs a figure object.
    The figure may be a matplotlib.pyplot Figure, or possibly figure objects from other plotting libraries.
    To be registered and processed by Visualize.getFigs, the name of each method must end with one of the following:
    [
        '_PRIV',  # Resulting plot is for private use only.
        '_FRND',  # Resulting plot may be shown to friends and colleagues, but not published for the general public.
        '_PUBL',  # Resulting plot may be published for general public viewing.
    ]
    """
    @staticmethod
    def avg_Sleep_by_Weekday_and_Epoch_Group_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        # df1 = tsds.timesheetdf.df[tsds.timesheetdf.df.project == Global.Project.DORMIR]
        df1 = tsds.timesheetdf.tsquery('Project.DORMIR & ( !description | "DORMIR" | "Siesta") : ;').df
        df1 = pd.concat([df1, getWeekday(df1.circad)], axis=1)
        epochScheme = Global.EpochScheme.MP_COARSE_ATOMIC
        df1 = pd.concat([df1, epochScheme.labelDT(df1.start.rename('epochGroup', copy=False))], axis=1)
        df1 = df1[['duration', 'weekday', 'epochGroup']]
        grouped = df1.groupby(['weekday', 'epochGroup'])
        wkdayCount = grouped.count().unstack()
        wkdayDuration = grouped.sum().unstack()
        visData = (wkdayDuration / wkdayCount)['duration']
        # TODO: add another cluster for the average over each epoch group
        visData = timeToFloat(visData, 'hour')
        visData = visData[[col for col in epochScheme.sortedEpochGroupNames() if col in visData.columns]]
        # visData.rename(lambda x: Global.Epoch[x].alias(), axis=1)
        title = _k('Avg Sleep Duration by Weekday and Life Phase')  # + ': ' + epochScheme.alias()
        auxText = getDateRangeString(tsds.timesheetdf.df)
        graphic = SingleAxisStaticVisual(data=visData, kind='clusteredBar', domain='weekday',
                                         title=title, ylabel=_k('[hours]'), grid='on', text=auxText,
                                         textPos=ArtistAlignment.SW, figsize=(10, 5))
        # sleep_epoch_wkday_VIS.show()
        graphic.save(fileName=auxText + '_' + title)
        return GraphicExhibit(graphic=graphic, privacy=Global.Privacy.PUBLIC,
                              section=ExhibitSection.SLEEP, sortKey=64)

    @staticmethod
    def sleep_start_and_end_violin_by_epoch_group_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        df = tsds.timesheetdf.tsquery(
            'Project.DORMIR & !description & duration<timedelta(hours=20) & duration>timedelta(minutes=30) : ;').df
        group = df[['start', 'end', 'circad']].groupby('circad')
        df = pd.concat([group.min().start, group.max().end], axis=1)
        df['duration'] = df.end - df.start
        df['durationHours'] = df['duration'].apply(lambda x: x.total_seconds()/3600)

        df['wakeTimeHours'] = (df['end'] - df['end'].dt.normalize()) / pd.Timedelta(hours=1)
        df['fallAsleepTimeHours'] = (df['start'] - df['start'].dt.normalize()) / pd.Timedelta(hours=1)
        df['fallAsleepTimeHoursNorm'] = (df['fallAsleepTimeHours'] + 6) % 24 - 6

        epochScheme = Global.EpochScheme.MP_COARSE_ATOMIC
        df['epochGroup'] = epochScheme.labelDT(df.start)
        cat = pd.concat([df[['fallAsleepTimeHoursNorm', 'epochGroup']],
                         df[['wakeTimeHours', 'epochGroup']]]
                        , axis=0)
        cat['isWake'] = pd.isna(cat.fallAsleepTimeHoursNorm)
        cat['time'] = cat.fallAsleepTimeHoursNorm.fillna(0) + cat.wakeTimeHours.fillna(0)

        title = _k('Distributions of Time of Falling Asleep and Waking Up by Life Phase')

        graphic = MatplotlibVisual(figsize=(10, 6))
        ax = sns.violinplot(data=cat,
                            # y='wakeTimeHours',
                            x='time',
                            # y='duration',
                            y='epochGroup',
                            hue='isWake',
                            cut=True,
                            dodge=True,
                            scale='width',
                            scale_hue=False,
                            # width=1.2,
                            bw=.12,
                            )

        # Set tick values and format display as HH:MM
        from matplotlib.ticker import MaxNLocator, MultipleLocator
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_minor_locator(MultipleLocator())
        rawTicks = plt.xticks()[0]
        hr = list(map(lambda x: int(x % 24), rawTicks))
        labels = [f'{h}:00' for h in hr]
        plt.xticks(rawTicks, labels=labels)
        ax.yaxis.set_ticklabels([kiwilib.addLineBreaks(s.get_text(), delimIndices=[0]) for s in plt.yticks()[1]])

        ax.autoscale(enable=True, axis='x')
        plt.grid(axis='x', alpha=0.4)
        plt.xlabel(_k('Time of day'))
        plt.ylabel(_k('Life Phase'))
        h, _ = ax.get_legend_handles_labels()
        ax.legend(h, [_k('Fall asleep'), _k('Wake up')])
        plt.title(title)
        auxText = getDateRangeString(tsds.timesheetdf.df)
        ArtistAlignment.SW.text(auxText, ax)

        return GraphicExhibit(graphic=graphic, privacy=Global.Privacy.PUBLIC,
                              section=ExhibitSection.SLEEP, sortKey=32)

    @staticmethod
    def time_spent_by_person_stairs_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        # df1 = tsds.timesheetdf.df[tsds.timesheetdf.df.project == Global.Project.DORMIR]
        # df1 = tsds.timesheetdf.tsquery('Person : ;').df
        df1 = tsds.cats['person'].collxn['timeSpent'].sort_values(ascending=False).reset_index(drop=True)\
            .apply(lambda x: x.total_seconds() / 3600)
        title = _k('Total Time Spent\n with Individual People, Sorted')  # + ': ' + epochScheme.alias()
        auxText = getDateRangeString(tsds.timesheetdf.df)
        xlabel = _k('Person index')
        ylabel = _k('[hours]')

        graphic = MatplotlibVisual(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.stairs(df1, fill=True, color='orange')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(axis='y')

        plt.subplot(1, 2, 2)
        plt.stairs(df1, fill=True, color='orange')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.semilogy()
        plt.title(_k('Total Time Spent\n with Individual People, Sorted, Log Scale'))
        plt.grid(axis='y')
        ArtistAlignment.NE.text(auxText, graphic.fig.axes[1])
        graphic.save(fileName=auxText + '_' + title.replace('\n', ''))
        return GraphicExhibit(graphic=graphic, privacy=Global.Privacy.PUBLIC,
                              section=ExhibitSection.PEOPLE, sortKey=128)

    @staticmethod
    def avg_social_interaction_by_gender_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        df = copy.copy(tsds.timesheetdf.df)
        df = df[Global.Epoch.e2018_Data_Log_Person < df.start]
        df['bin'] = kiwilib.date_range_bins(df['circad'], 'MS', normalize=True)
        genders = df.person.apply(lambda plist: [tsds.cats['person'].collxn.loc[pid].gender for pid in plist])

        enumCls = sg.Gender
        enumList = list(enumCls)

        df = pd.concat([df, kiwilib.enum_counts(genders, enumCls)], axis=1)
        gend = df[['bin', 'duration'] + enumList]

        # Compute the enum-hours for each enum instance. Enum-hours scale with the number of instances present in a row.
        multNames = [g.name + '_mult' for g in enumCls]
        if multNames[0] not in gend.columns:
            for g, col in zip(enumList, multNames):
                gend.loc[:, col] = gend.duration * gend[g]
        gend = gend[['bin'] + multNames]
        visData = gend.groupby('bin').sum()

        # Total person-hours for subplot(1,2,2)
        totals = visData[multNames].sum(axis=0) / np.timedelta64(1, 'h')  # float person-hours
        # totalsAug = pd.concat([pd.Series([0]), totals])
        # totalsAug = pd.Series(accumulate(totalsAug), index=np.concatenate([[0], totals.index]))

        # Data for subplot(1,2,1)
        visData = visData / np.timedelta64(1, 'h')  # Timedelta to float hours
        x = pd.arrays.IntervalArray(visData.index).left  # Get the start of each IntervalIndex for x coordinate in plots
        visData = (visData.T / pd.DatetimeIndex(x).daysinmonth).T  # Set units to hours per day

        titles = (_k('Average Person-Hours of Social Interaction per Day, by Gender'), _k('Total\nPerson-Hours'))
        graphic = stackplot_and_totals_stackbar(
            x,
            visData[multNames],
            totals,
            stack_names=enumList,
            ylabels=(_k('[person-hours/day]'), None),
            titles=titles,
            legend_loc='upper left'
        )

        auxText = getDateRangeString(df)
        graphic.save(fileName=auxText + '_' + titles[0].replace('\n', ''))
        return GraphicExhibit(graphic=graphic, privacy=Global.Privacy.PUBLIC,
                              section=ExhibitSection.PEOPLE, sortKey=180)

    @staticmethod
    def avg_social_interaction_by_primary_relation_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        cat = tsds.cats['person']
        df = copy.copy(tsds.timesheetdf.df)
        df = df[Global.Epoch.e2018_Data_Log_Person < df.start]
        df['bin'] = kiwilib.date_range_bins(df['circad'], 'MS', normalize=True)

        primaryMap = dict(zip(cat.collxn.index, map(lambda x: x.primaryRelation(), cat.getObjects())))
        rels = df.person.apply(lambda pList: [primaryMap[pid] for pid in pList])

        enumList = [c() for c in sg.Relation.__subclasses__()]
        df = pd.concat([df, kiwilib.enum_counts(rels, enumList)], axis=1)
        df1 = df[['bin', 'duration'] + enumList]

        # Compute the enum-hours for each enum instance. Enum-hours scale with the number of instances present in a row.
        multNames = [g.alias('en_US') + '_mult' for g in enumList]
        if multNames[0] not in df1.columns:
            for g, col in zip(enumList, multNames):
                df1.loc[:, col] = df1.duration * df1[g]
        df1 = df1[['bin'] + multNames]

        visData = df1.groupby('bin').sum()
        totals = visData[multNames].sum(axis=0) / np.timedelta64(1, 'h')  # float person-hours
        visData = visData / np.timedelta64(1, 'h')  # Timedelta to float hours
        x = pd.arrays.IntervalArray(visData.index).left  # Get the start of each IntervalIndex for x coordinate in plots
        visData = (visData.T / pd.DatetimeIndex(x).daysinmonth).T  # Set units to hours per day

        titles = _k('Average Person-Hours of Social Interaction per Day, by Primary Relation'), \
                 _k('Total\nPerson-Hours')
        graphic = stackplot_and_totals_stackbar(
            x,
            visData[multNames],
            totals,
            stack_names=enumList,
            ylabels=(_k('[person-hours/day]'), None),
            titles=titles,
            legend_loc='upper left'
        )

        auxText = getDateRangeString(df)
        graphic.save(fileName=auxText + '_' + titles[0].replace('\n', ''))
        return GraphicExhibit(graphic=graphic, privacy=Global.Privacy.PUBLIC,
                              section=ExhibitSection.PEOPLE, sortKey=190)

    @staticmethod
    def metaproject_area_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        # df1 = tsds.timesheetdf.df[tsds.timesheetdf.df.project == Global.Project.DORMIR]
        # df1 = tsds.timesheetdf.tsquery('Person : ;').df
        df1 = tsds.timesheetdf.df
        df1['week'] = df1.circad - df1.circad.apply(datetime.date.weekday).apply(lambda x: datetime.timedelta(days=x))
        df1 = df1[['week', 'duration', 'metaproject']]
        visData = df1.groupby(['week', 'metaproject']).sum().unstack().duration.fillna(datetime.timedelta(hours=0))
        visData = visData[sorted(visData.columns.values, reverse=True)].applymap(lambda x: x.total_seconds()/3600/7)
        # visData[_k('Untracked')] = datetime.timedelta(weeks=1) - visData.sum(axis=1)
        title = _k('Duration by Metaproject per Day, Averaged over 1 Week')  # + ': ' + epochScheme.alias()
        auxText = getDateRangeString(tsds.timesheetdf.df)
        # xlabel = _k('')
        ylabel = _k('[hours/day]')

        graphic = MatplotlibVisual(figsize=(10, 7))
        plt.stackplot(visData.index, visData.values.transpose())
        plt.title(title)
        # plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend([_e(col) for col in visData.columns.values], loc='lower right')
        plt.yticks(range(0, 28, 4))
        plt.grid(axis='y', alpha=0.4)
        # ArtistAlignment.SW.text(auxText, graphic.fig.axes[1])
        ax = plt.gca()
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
        # plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        lineDates = [e.lower for e in Global.EpochScheme.MP_COARSE_ATOMIC.scheme.keys()]
        ep = Global.Epoch
        lineLabels = [kiwilib.addLineBreaks(" ".join(word.capitalize() for word in _e(a).split(" ")), delimIndices=[0]) for a in
                      [ep.e2017_Cornell, ep.e2018_Boulder_Solo, ep.e2022_Tour_Start, ep.e2022_Tour_End]]
        lineLabels[1] = _k('Start\nFirst Job')
        plt.vlines(lineDates, 24, 26.5, linestyles='dashed')
        for dat, label in zip(lineDates, lineLabels):
            ax.text(dat, 26.5, label, ha='center', va='bottom')

        graphic.save(fileName=auxText + '_' + title)
        return GraphicExhibit(graphic=graphic, privacy=Global.Privacy.PUBLIC,
                              section=ExhibitSection.METAPROJECT, sortKey=4)


def getFigs(tsds: TimesheetDataset, audience: Global.Privacy) -> List[GraphicExhibit]:
    """
    Returns a list of full exhibit graphics data in the format expected by Exhibit.py.
    Contains any number of graphics and the accompanying inline text commentary and exhibit structural information.
    :param tsds: Data from which to create graphics.
    :param audience:
    :return:
    """
    privacyMap = {
        Global.Privacy.PUBLIC : '_PUBL',
        Global.Privacy.FRIENDS: '_FRND_PUBL',
        Global.Privacy.PRIVATE: '_PRIV_FRND_PUBL',
    }  # Concatenated strings encoding the method privacy ratings accepted for each acceptable value of audience
    # inversePrivacyMap = {v[:5]: k for k,v in privacyMap.items()}
    figFuncs = [v for _, v in inspect.getmembers(GraphicMaker(), inspect.isfunction)
                if v.__name__[-5:] in privacyMap[audience]]
    curFigFunc = GraphicMaker.avg_social_interaction_by_primary_relation_PUBL
    # return [curFigFunc(tsds)]
    return sorted([f(tsds) for f in figFuncs], key=lambda x: (x.section.value.sortKey, x.sortKey))
