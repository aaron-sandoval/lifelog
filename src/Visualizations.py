"""
Created on Mar 1, 2023

@author: Aaron
Holds visualization classes
"""

import matplotlib as plt
import pandas as pd
from TimesheetGlobals import VSPath
from datetime import date

# TODO: move classes and other non-script elements from Visualize.py to this module.
# class SingleAxisStaticVisual:
#     """
#     Creates visualizations. Takes inputs for chart type, standard domain types, visual features,
#     """
#
#     # TODO: add inheritance for a more general superclass
#
#     def show(self):
#         self.fig.show()
#
#     def save(self, filename: str=None, path=VSPath()):
#         if not filename:        filename = self.ax.title + date.today().strftime('%Y-%m-%d')
#         plt.savefig(path + filename)
#
#     def showText(self, text, pos='SE', margin=0.05, boxstyle='round', facecolor='wheat', alpha=0.5,
#                  fontsize=11):
#         posMap = {
#             'NE': (1 - margin, 1 - margin, 'top', 'right'),
#             'NW': (margin, 1 - margin, 'top', 'left'),
#             'SW': (margin, margin, 'bottom', 'left'),
#             'SE': (1 - margin, margin, 'bottom', 'right')
#         }
#         posP = posMap[pos]
#         # these are matplotlib.patch.Patch properties
#         props = dict(boxstyle=boxstyle, facecolor=facecolor, alpha=alpha)
#         # place text box
#         self.ax.text(posP[0], posP[1], text, transform=self.ax.transAxes, fontsize=fontsize,
#                      verticalalignment=posP[2], horizontalalignment=posP[3], bbox=props)
#
#         # a = 1
#
#     @staticmethod
#     def weekdayDomain(ser):
#         if any(ser.index > 7) or any(ser.index < 0):
#             print('ERROR: incorrect indices for weekday domain.')
#             return ser
#         vals = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
#         keys = [6, 0, 1, 2, 3, 4, 5]
#         weekdayMap = dict(zip(keys, vals))
#         ser.index = ser.index.map(weekdayMap)
#         ser = ser.reindex(vals)
#         return ser
#
#     @staticmethod
#     def workdayDomain(ser):
#         ser = weekdayDomain(ser)
#         ser = ser.drop(['Sat', 'Sun'])
#         return ser
#
#     @staticmethod
#     def realTimeDomain(ser):
#         # Everything seems to work without any trouble
#         return ser
#
#     @staticmethod
#     def weeksDomain(serdf):
#         ind = pd.Series(serdf.index)
#         weekDate = getWeekDate(ind)
#         serdf.index = list(weekDate)
#         return serdf
#
#     @staticmethod
#     def barFormat(fig, ax, pl):
#         patches = ax.patches
#         for p in patches:
#             p.set_facecolor((.2, .5, .2))
#
#     @staticmethod
#     def lineFormat(fig, ax, pl):
#         pl.grid(True, axis='x')
#
#     @staticmethod
#     def areaFormat(fig, ax, pl):
#         a = 1
#
#     @staticmethod
#     def clusteredBar(self, data, totalWidth=1000):
#         nBars = data.size
#         nClusters = len(data.iloc[:, 0])
#         nBarsPerCluster = len(data.columns)
#         barWidth = np.max([np.floor(totalWidth / nBars / 5) * 5, 5])
#         clusterSpace = barWidth
#         xPos = np.zeros([nClusters, nBarsPerCluster])
#         fig = plt.figure()
#         for i in range(nBarsPerCluster):
#             xPos[:, i] = np.arange(nClusters) * (barWidth * nBarsPerCluster + clusterSpace) + i * barWidth
#             plt.bar(xPos[:, i], data.iloc[:, i], width=barWidth, edgecolor='white', label=data.columns[i])
#         plt.xticks(xPos[:, 0] + barWidth * (nBarsPerCluster - 1) / 2, list(data.index))
#         ax = fig.axes[0]
#         plt.legend(loc='lower right')
#         # pl = 0
#         return [fig, ax, None]
#
#     nonStandardMap = {
#         'clusteredBar': clusteredBar,
#     }
#
#     kindMap = {
#         'line': lineFormat,
#         'bar': barFormat,
#         'area': areaFormat,
#     }
#     #     domLabels = getLabels(data, domain)
#     domainMap = {
#         'weekday': weekdayDomain,
#         'workday': workdayDomain,
#         'realTime': realTimeDomain,
#         'weeks': weeksDomain,
#     }
#
#     def __init__(self, data: pd.DataFrame, kind='line', domain=None, title='', xlabel=None,
#                  ylabel=None, grid='off', text=None, textPos='SE', show='False', save = False):
#         self.date_created = date.today()
#         if domain in self.domainMap:
#             data = self.domainMap[domain](data)  # Gets a preset domain from a map if needed
#         if kind in self.nonStandardMap:
#             [self.fig, self.ax, self.pl] = self.nonStandardMap[kind](self, data)
#         else:
#             self.fig = plt.figure()
#             self.pl = data.plot(kind=kind)
#             self.ax = plt.gca()
#             if kind in self.kindMap:
#                 self.kindMap[kind](fig, ax, pl)
#
#         plt.title(title)
#         if grid == 'on':    plt.grid(True, axis='y')
#         if text:            self.showText(text, pos=textPos)
#         if xlabel:          plt.xlabel(xlabel)
#         if ylabel:          plt.ylabel(ylabel)
#         if show:            self.show()
#         if save:            self.save(text + '_' + title)
#         #     a = 1
#         # return [fig, ax, pl]
#     # if domain in domainMap:
#     #     data = domainMap[domain](data)  # Gets a preset domain from a map if needed
#     # if kind in nonStandardMap:
#     #     [fig, ax, pl] = nonStandardMap[kind](data, domain)
#     # else:
#     #     fig = plt.figure()
#     #     pl = data.plot(kind=kind)
#     #     ax = plt.gca()
#     #     if kind in kindMap:
#     #         kindMap[kind](fig, ax, pl)
#     # if grid == 'on':    plt.grid(True, axis='y')
#     # if text:            showText(text, fig, pl, ax, pos=textPos)
#     # if title:           plt.title(title)
#     # if xlabel:          plt.xlabel(xlabel)
#     # if ylabel:          plt.ylabel(ylabel)
#     # plt.show()
#     # #     a = 1
#     # return [fig, ax, pl]
