"""
Created on Nov 22, 2018

@author: Aaron
Holds functions used to collect datasets from database and create graphics from them.
"""
import datetime

import portion
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Union, List, Set, Dict
from bisect import bisect_right
import inspect
import seaborn as sns

from src.TimesheetDataset import *
from i18n_l10n import internationalization as i18n

from src.Visualization import (
    ExhibitSection,
    ArtistAlignment,
    MatplotlibVisual,
    WordCloudVisual,
    SingleAxisStaticVisual,
    GraphicExhibit,
    babelx,
    stackplot_and_totals_stackbar,
    getDateRangeString,
    getWeekday,
    timeToFloat,
)



def main(paths: List[str], catalogSuffix='', locale='en_US', audience=Global.Privacy.PUBLIC):

    def babelExtractEnumLike() -> None:
        # classes = kiwilib.getAllSubclasses(kiwilib.HierarchicalEnum)
        for c in kiwilib.getAllSubclasses(kiwilib.HierarchicalEnum):
            _e(c()) # type: ignore
            # _a(c) # type: ignore
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
            _t(tok) # type: ignore
        babelx.flush()

    global babelx
    babelx.setLang(i18n.localeDict[locale])
    kiwilib.Aliasable.setDefaultLocale(locale)
    tsds = _loadAndMergeDatasets(paths, catalogSuffix)
    figs = _getFigs(tsds, audience)

    # babelExtractEnumLike()
    # babelExtractTSDS(tsds, 20)
    # babelx.firstWrite = True
    # babelExtractTSDS(tsds, 10)
    # vis = miscTest(tsds, 4)
    babelx.flush()
    # privacy=most private of all figs
    return Global.writePersistent(figs, 4, privacy=audience)


def _loadAndMergeDatasets(paths: list[str], fileSuffix='') -> TimesheetDataset:
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


class _GraphicMaker:
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
        title = _k('Avg Sleep Duration by Weekday and Life Phase') # type: ignore
        auxText = getDateRangeString(tsds.timesheetdf.df)
        graphic = SingleAxisStaticVisual(data=visData, kind='clusteredBar', domain='weekday',
                                         title=title, ylabel=_k('[hours]'), grid='on', text=auxText, # type: ignore
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
        enumNames = [str(e) for e in enumList]

        df = pd.concat([df, kiwilib.enum_counts(genders, enumCls)], axis=1)
        gend_copy = df[['bin', 'duration'] + enumNames].copy()

        # Compute the enum-hours for each enum instance. Enum-hours scale with the number of instances present in a row.
        # multNames = [g.name + '_mult' for g in enumCls]
        # if multNames[0] not in gend_copy.columns:
        for g in enumNames:
            gend_copy[g] = gend_copy.duration * gend_copy[g]

        visData = gend_copy.groupby('bin').sum()

        # Total person-hours for subplot(1,2,2)
        # gend_names = [g.name for g in enumList]
        totals = visData[enumNames].sum(axis=0) / np.timedelta64(1, 'h')  # float person-hours
        # totalsAug = pd.concat([pd.Series([0]), totals])
        # totalsAug = pd.Series(accumulate(totalsAug), index=np.concatenate([[0], totals.index]))

        # Data for subplot(1,2,1)
        visData = visData / np.timedelta64(1, 'h')  # Timedelta to float hours
        x = pd.arrays.IntervalArray(visData.index).left  # Get the start of each IntervalIndex for x coordinate in plots
        visData = (visData.T / pd.DatetimeIndex(x).daysinmonth).T  # Set units to hours per day

        titles = (_k('Average Person-Hours of Social Interaction per Day, by Gender'), _k('Total\nPerson-Hours'))
        graphic = stackplot_and_totals_stackbar(
            x,
            visData[enumNames],
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
        enumNames = [str(e) for e in enumList]
        df = pd.concat([df, kiwilib.enum_counts(rels, enumList)], axis=1)
        df1 = df[['bin', 'duration'] + enumNames].copy()

        # Compute the enum-hours for each enum instance. Enum-hours scale with the number of instances present in a row.
        # multNames = [g.alias('en_US') + '_mult' for g in enumList]
        # if multNames[0] not in df1.columns:
        for g in enumNames:
            df1[g] = df1.duration * df1[g]

        visData = df1.groupby('bin').sum()
        totals = visData[enumNames].sum(axis=0) / np.timedelta64(1, 'h')  # float person-hours
        visData = visData / np.timedelta64(1, 'h')  # Timedelta to float hours
        x = pd.arrays.IntervalArray(visData.index).left  # Get the start of each IntervalIndex for x coordinate in plots
        visData = (visData.T / pd.DatetimeIndex(x).daysinmonth).T  # Set units to hours per day

        titles = _k('Average Person-Hours of Social Interaction per Day, by Primary Relation'), \
                 _k('Total\nPerson-Hours')
        graphic = stackplot_and_totals_stackbar(
            x,
            visData[enumNames],
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


    @staticmethod
    def subject_matter_word_cloud_PUBL(tsds: TimesheetDataset) -> GraphicExhibit:
        """
        Generates a word cloud from the 'subjectmatter' column of the TimesheetDataset.
        
        :param tsds: TimesheetDataset object containing the data.
        :return: GraphicExhibit containing the word cloud visual.
        """
        # Extract the 'subjectmatter' column
        subject_matter_series = tsds.timesheetdf.df['subjectmatter']
        
        # Create a WordCloudVisual
        word_cloud_visual = WordCloudVisual(subject_matter_series, width=800, height=400)
        
        # Define the title and auxiliary text
        title = _k('Subject Matter Word Cloud')
        aux_text = getDateRangeString(tsds.timesheetdf.df)
        
        # Save the word cloud visual
        word_cloud_visual.save(file_name=aux_text + '_' + title.replace(' ', '_'))
        
        # Return the GraphicExhibit
        return GraphicExhibit(
            graphic=word_cloud_visual,
            privacy=Global.Privacy.PUBLIC,
            section=ExhibitSection.SUBJECT_MATTER,
            sortKey=4
        )


    


def _getFigs(tsds: TimesheetDataset, audience: Global.Privacy) -> List[GraphicExhibit]:
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
    figFuncs = [v for _, v in inspect.getmembers(_GraphicMaker(), inspect.isfunction)
                if v.__name__[-5:] in privacyMap[audience]]
    curFigFunc = _GraphicMaker.subject_matter_word_cloud_PUBL
    return [curFigFunc(tsds)]
    # return sorted([f(tsds) for f in figFuncs], key=lambda x: (x.section.value.sortKey, x.sortKey))
