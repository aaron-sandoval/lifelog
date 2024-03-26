"""
Created on March 5, 2023

@author: Aaron
Implements several steps to bring the pre-processed dataset to its full depth.
Applies a series of rules to populate data fields based on the existing contents of others
Initiates and populates Catalogs, and re-populates the dataframe with appropriate Catalog data
"""

import pandas as pd
from typing import Union
from src.TimesheetDataset import TimesheetDataset
# import src.TimesheetGlobals as Global


def main(PP_path, catalogSuffix='', write=True) -> Union[str, TimesheetDataset]:
    myTSDS = TimesheetDataset(pd.read_pickle(PP_path))
    myTSDS.preCatalogCorrect()
    myTSDS.initCatalogs(fileSuffix=catalogSuffix)
    myTSDS.postCatalogCorrect()
    if write:
        return myTSDS.write(phaseFlag=3)
    return myTSDS
