import sys, os
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from typing import Type
from src.TimesheetGlobals import rootProjectPath
from src.TimesheetDataset import *


TEST_DIR = os.path.join(rootProjectPath(), 'tests')
READ_DIR = os.path.join(TEST_DIR, 'data', 'read_only')
WRITE_DIR = os.path.join(TEST_DIR, 'data', 'write')
CAT_DIR = os.path.join(rootProjectPath(), 'catalogs')
PUBLIC_TSDF = os.path.join(READ_DIR, 'PP_test3_PUBL.pkl')


def loadWithFallback(file: str = None, fallback: str = PUBLIC_TSDF) -> pd.DataFrame:
    """
    Loads a .pkl file and substitutes a reliable fallback if not found.
    Especially applicable to loading files which may or may not be present due to public/private repo status.
    :param file: .pkl serializing a `pd.DataFrame`, but this isn't enforced.
    :param fallback:
    :return:
    """
    if not os.path.exists(file):
        if Global.isPrivate():
            warnings.warn(f"File {file} does not exist. "
                          f"This could be because the specified file is private and not uploaded to the repository. "
                          f"Using public fallback file {fallback} instead", Warning)
            file = fallback
        else:
            raise FileNotFoundError(f"File {file} does not exist.")
    return pd.read_pickle(file)


def loadTestTSDF(file: str = os.path.join(READ_DIR, 'PP_2018-08-22-1640_2019-09-02-1659_PRIV.pkl')):
    return TimesheetDataFrame(loadWithFallback(file))


def loadTestCatalog(collxble: Type[Collectible], suffix='_test4') -> Catalog:
    # file = Path(CAT_DIR)/('Catalog_'+collxble.__name__+suffix+'.yaml')
    tsds = TimesheetDataset(pd.DataFrame())
    tsds.loadCatalogs([collxble], fileSuffix=suffix)
    return tsds.cats[collxble.name()]


def loadTestTSDS(file: str = os.path.join(READ_DIR, 'PP_2018-08-22-1640_2019-09-02-1659_PRIV.pkl'),
                 suffix='_test4') -> TimesheetDataset:
    """
    Testing method to load a TimesheetDataset from disk and do some setup to help avoid overwriting loaded files.
    Defaults args build a TimesheetDataset from the default testing files.
    Default catalog files are the same regardless of repo public/private status.
    Default tsdf pkl file is a more comprehensive private file.
    If that is unavailable, it falls back to a narrow scope public tsdf pkl file.
    :param file: Path to tsdf pkl file
    :param suffix: Suffix for reading catalog files.
    :return:
    """
    myTimesheetDataset = TimesheetDataset(loadWithFallback(file), fileSuffix=suffix)
    myTimesheetDataset.loadCatalogs(fileSuffix=suffix)
    myTimesheetDataset.preCatalogCorrect()
    myTimesheetDataset.catalogPopulateDF()
    myTimesheetDataset.fileSuffix = suffix + '_W'  # Don't modify original test catalogs
    # TODO: make tsdf write to test directory
    return myTimesheetDataset