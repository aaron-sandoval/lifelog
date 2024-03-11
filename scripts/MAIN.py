# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 2018

@author: Aaron Sandoval
"""

import sys
import os
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from scripts import FileManagement as FM, Preprocess as PP, Visualize as VS
from scripts.DataCorrection import main as DCmain
# from scripts import Exhibit as XH
from src.TimesheetGlobals import PPPath, rootProjectPath, Privacy


def main(catalogSuffix='', locale='en_US', audience=Privacy.PUBLIC, runPublic=True):

    # dataFiles = ['timesheet_20180822202600.csv']
    # dataFiles = ['timesheet_2017-12-16.csv', '2017_20230207.csv', '20230201-20230403.csv', '20230401_20230701.csv',
    #              '20230601-20231001.csv', '20230901-20240101.csv']
    # dataFiles = ['20230201-20230403.csv', '20230401_20230701.csv', '20230601-20231001.csv']
    # dataFiles = ['timesheet_2017-12-16.csv']
    # dataFiles = ['timesheet_2018-08-01_2018-08-22.csv']
    dataFiles = ['20230901-20240101.csv']
    # dataFiles = ['timesheet_2017-12-16.csv', 'timesheet_20180822202600.csv']
    # dataFiles = ['timesheet_20180822202600.csv']
    # dataFiles = ['sample_RAW_PUBLIC.csv']

    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_test3.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2020-09-17-0747_2021-01-05-1222.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2017-09-06-2136_2024-01-01-0144.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2017-09-06-2136_2018-02-10-2211.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2017-09-06-2136_2017-12-16-1700.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2017-12-17-1030_2018-08-22-1745.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2017-09-06-2136_2018-08-22-1745.csv')
    FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2018-08-22-1640_2019-09-02-1659.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2019-09-02-1625_2020-09-17-0747.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2020-09-17-0647_2021-12-14-2208.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2021-12-14-2201_2022-04-02-1327.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2023-02-01-0005_2023-10-01-0906.csv')
    # FM_filePath = os.path.join(rootProjectPath(), 'FM_CSVs', 'FM_2023-02-01-0005_2023-06-30-2228.csv')

    # PP_filePath = os.path.join(PPPath(), "PP_2020-09-17-0747_2021-01-05-1222.pkl")
    # PP_filePath = os.path.join(PPPath(), "PP_2017-09-06-2136_2018-02-10-2211.pkl")
    # PP_filePath = os.path.join(PPPath(), "PP_2017-09-06-2136_2017-12-16-1252.pkl")
    # PP_filePath = os.path.join(PPPath(), 'PP_2017-12-17-1030_2018-08-22-1745.pkl')
    # PP_filePath = os.path.join(PPPath(), 'PP_2017-09-06-2136_2018-08-22-1745.pkl')
    # PP_filePath = os.path.join(PPPath(), 'PP_2018-08-22-1640_2019-09-02-1659_PRIV.pkl')
    # PP_filePath = os.path.join(PPPath(), 'PP_2019-09-02-1625_2020-09-17-0747.pkl')
    # PP_filePath = os.path.join(PPPath(), 'PP_2020-09-17-0647_2021-12-14-2208.pkl')
    # PP_filePath = os.path.join(PPPath(), "PP_2021-12-14-2201_2022-04-02-1327.pkl")
    # PP_filePath = os.path.join(PPPath(), 'PP_2023-02-01-0005_2023-06-30-2228.pkl')
    PP_filePath = os.path.join(PPPath(), 'PP_2017-09-06-2136_2024-01-01-0144.pkl')

    # DC_filePath = rootProjectPath() + 'DC_Persistent\\DC_2022-04-02-1305_2023-06-30-2228.pkl'
    DC_filePaths = list(map(lambda x: os.path.join(rootProjectPath(), 'DC_Persistent', x + '.pkl'),
                            [
                               # 'DC_2017-09-06-2136_2018-08-22-1745',
                               # 'DC_2017-09-06-2136_2019-09-02-1659',
                               # 'DC_2019-09-02-1625_2020-09-17-0747',
                               # 'DC_2020-09-17-0647_2021-12-14-2208',
                               # 'DC_2021-12-14-2201_2022-04-02-1327',
                               # 'DC_2022-04-02-1305_2023-06-30-2228',
                               'DC_2017-09-06-2136_2023-10-01-0906',
                            ]))

    if runPublic:
        FM_filePath = FM.main(['sample_RAW_PUBLIC.csv'])
        PP_filePath = PP.main(FM_filePath)
        DC_filePaths = [DCmain(PP_filePath, catalogSuffix=catalogSuffix)]
        # VS_filePath = VS.main(DC_filePaths, catalogSuffix=catalogSuffix, locale=locale, audience=audience)
    else:
        # FM_filePath = FM.main(dataFiles)
        PP_filePath = PP.main(FM_filePath)
        # DC_filePaths = [DCmain(PP_filePath, catalogSuffix=catalogSuffix)]
        # VS_filePath = VS.main(DC_filePaths, catalogSuffix=catalogSuffix, locale=locale, audience=audience)

    # XH.main(VS_filePath)


if __name__ == '__main__':
    # TODO: always change to runPublic=True before git commit
    main(catalogSuffix='', locale='en_US', audience=Privacy.PUBLIC, runPublic=False)
