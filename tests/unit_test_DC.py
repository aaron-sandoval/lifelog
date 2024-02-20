import sys
from pathlib import Path

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import numpy as np
import pytest
from external_modules import kiwilib

# import src.TimesheetGlobals as Global
# from src.Catalogs import *
from src.TimesheetDataset import *

# def test_getColumnClassDict():
#     a = Global.ListColumn.getColumnClassDict()
#     assert Media not in a
#     assert Person in a
#     assert Global.Project not in a
#     assert isinstance(tsds.timesheetdf, TimesheetDataFrame)


PP_path = os.path.join(Global.PPPath(), "PP_2020-09-17-0747_2021-01-05-1222.pkl")
tsds = pd.read_pickle(PP_path)


