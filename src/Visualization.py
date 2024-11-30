"""
Reusable procedures and classes related to visualization
"""

from enum import Enum
from itertools import accumulate
from typing import Any, Iterable, List, NamedTuple, Tuple, Dict, Set, Union
import re
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.dtypes.inference import is_list_like
import streamlit as st
from external_modules import kiwilib
from wordcloud import WordCloud
from pathlib import Path

from i18n_l10n import internationalization as i18n
from src.TimesheetDataset import Global, Iterable, List, Tuple, abc, datetime, np, os, pd


global babelx  # Babel extractor wrapper, must be accessible everywhere in the module
babelx = i18n.babelx
STR_BACKEND = _k('👀 *Peek into the Backend*') # type: ignore

_enum_alias_map: Dict[str, kiwilib.AliasableEnum] = \
    kiwilib.AliasableEnum.aliases_to_members_deep(alias_func=_e) # type: ignore
# Also add keys for the alternative language since the dict isn't updated upon a change in language selection
babelx.setLang(i18n.lang_es)
_enum_alias_map.update(kiwilib.AliasableEnum.aliases_to_members_deep(alias_func=_e)) # type: ignore

babelx.setLang(i18n.lang_en)
_hier_enum_alias_map: Dict[str, kiwilib.AliasableHierEnum] = \
    kiwilib.AliasableHierEnum.aliases_to_members(alias_func=_e) # type: ignore
babelx.setLang(i18n.lang_es)
_hier_enum_alias_map.update(kiwilib.AliasableHierEnum.aliases_to_members(alias_func=_e)) # type: ignore
babelx.setLang(i18n.lang_en)


class XHSectionData(NamedTuple):
    """Enum member values for ExhibitSection."""
    sortKey: int = 0  # TODO: get rid of sortKey, sorting determined by pages filename prefixes


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

    METAPROJECT = XHSectionData(sortKey=4)
    PEOPLE = XHSectionData(sortKey=16)
    SUBJECT_MATTER = XHSectionData(sortKey=32)
    SLEEP = XHSectionData(sortKey=48)


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
                artist.set_text(_e(_enum_alias_map[t])) # type: ignore
            elif t in _hier_enum_alias_map:
                artist.set_text(_e(_hier_enum_alias_map[t]())) # type: ignore
            else:
                artist.set_text(_k(t)) # type: ignore




class WordCloudVisual(Visual):
    """Visual representation of a word cloud using the wordcloud library."""

    def __init__(self, words: pd.Series, **kwargs):
        """
        Initialize the WordCloudVisual with a series of words.

        Args:
            words (pd.Series): A Series of lists of strings.
            **kwargs: Additional keyword arguments for WordCloud.
        """
        self.wordcloud = WordCloud(**kwargs).generate(' '.join(words.explode()))

    def save(self, file_name: str) -> None:
        """Save the word cloud image to a file."""
        output_path = Path(Global.rootProjectPath()) / 'VS_Figures' / f'{file_name}.png'
        self.wordcloud.to_file(output_path)

    def localize(self) -> None:
        """Localize the word cloud if necessary."""
        # TODO: implement localization
        pass

    def exhibit(self) -> None:
        """Display the word cloud using Streamlit."""
        st.image(self.wordcloud.to_array(), use_column_width=True)


def getWeekDate(ser):
    EP = Global.TASK_ID_EPOCH
    ser1 = EP + ser.apply(lambda x: datetime.timedelta(weeks=x))
    return ser1 - datetime.timedelta(days=EP.weekday())


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
        vals = [_a(x) for x in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']] # type: ignore
        keys = [6, 0, 1, 2, 3, 4, 5]
        weekdayMap = dict(zip(keys, vals))
        ser.index = ser.index.map(weekdayMap)
        ser = ser.reindex(vals)
        return ser

    @staticmethod
    def workdayDomain(ser):
        return SingleAxisStaticVisual.weekdayDomain(ser).drop([_a('Sat'), _a('Sun')]) # type: ignore

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
        if xlabel:          plt.xlabel(_k(xlabel)) # type: ignore
        if ylabel:          plt.ylabel(_k(ylabel)) # type: ignore
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


def word_cloud(words: pd.Series, **kwargs) -> WordCloudVisual:
    """
    Returns a WordCloudVisual object featuring a word cloud of the words in `words`.
    The size of each word is proportional to its frequency in `words`.

    Args:
        words (pd.Series): A Series of lists of strings.
        **kwargs: Additional keyword arguments for WordCloud.

    Returns:
        WordCloudVisual: An instance of WordCloudVisual.
    """
    return WordCloudVisual(words, **kwargs)


def getDateRangeString(df) -> str:
    """
    Produces a string representing the date range of a dataframe. Useful for title or auxiliary plot text
    :param df:
    :return: String representing the date range of a dataframe
    """
    startString = df.head(1).circad.values[0].strftime('%Y-%m-%d')
    endString = df.tail(1).circad.values[0].strftime('%Y-%m-%d')
    return startString + '_' + endString


def getWeekday(ser):
    day = ser.apply(lambda x: x.weekday())
    return day.rename('weekday')



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


def getWeek(ser):
    #     For a series of dates, returns Timesheet week numbers, measured since TASK_ID_EPOCH
    ser = ser - Global.TASK_ID_EPOCH
    daysSinceEpoch = [t.days for t in list(ser)]
    weekList = [int(np.ceil(t / 7)) for t in daysSinceEpoch]
    week = pd.Series(weekList, name='week', index=ser.index)
    #     week = week.rename('week')
    return week


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

# TODO: move classes and other non-script elements from Visualize.py to this module.
