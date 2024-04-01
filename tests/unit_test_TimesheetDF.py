import copy
import sys, os
from pathlib import Path

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
# import src.TimesheetGlobals as Global
# from src.Catalogs import *
import copy
from src.TimesheetDF import *
import tests.testing_utils as testing_utils


def test_deepcopy():
    a = testing_utils.loadTestTSDF(testing_utils.PUBLIC_TSDF)
    b = copy.deepcopy(a)
    assert a.df.iloc[0, :].description is not b.df.iloc[0, :].description
    assert a.df.iloc[0, :].description.tokenTree is not b.df.iloc[0, :].description.tokenTree


def test_equality():
    a = testing_utils.loadTestTSDF(testing_utils.PUBLIC_TSDF)
    b = copy.deepcopy(a)
    assert a == b

    a.df.loc[29100749, :].description.removeToken('STRAVA')
    assert a != b
    a.df.loc[29100749, :].description.addToken('STRAVA')
    assert a == b

    a = a.tsquery('Tag.Bici : !Tag.Bici ;')
    assert a != b
    b = b.tsquery('Tag.Bici : !Tag.Bici ;')
    assert a == b
