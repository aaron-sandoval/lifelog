import copy
import os
import sys
from pathlib import Path

sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.parent.absolute()))
from src.TimesheetDataset import *
from tests import testing_utils


def test_tsds_roundtrip():
    tsds = testing_utils.loadTestTSDS(file=testing_utils.PUBLIC_TSDF, suffix='_test4')
    file1 = os.path.join(testing_utils.WRITE_DIR, 'test_tsds_roundtrip_W.pkl')
    tsds.write(3, tsdfFile=file1)
    tsds_rt = testing_utils.loadTestTSDS(file=file1, suffix='_test4_W')
    tsds_rt.fileSuffix = tsds.fileSuffix
    assert tsds == tsds_rt


def test_deepcopy():
    a = testing_utils.loadTestTSDS(testing_utils.PUBLIC_TSDF, suffix='_test4')
    b = copy.deepcopy(a)
    assert a is not b
    assert a.timesheetdf == b.timesheetdf
    assert a.timesheetdf is not b.timesheetdf

    # Single task
    assert a.timesheetdf.df.iloc[0, :].description == b.timesheetdf.df.iloc[0, :].description
    assert a.timesheetdf.df.iloc[0, :].description is not b.timesheetdf.df.iloc[0, :].description
    # assert a.timesheetdf.df.iloc[0, :].description.tokenTree == b.timesheetdf.df.iloc[0, :].description.tokenTree
    assert a.timesheetdf.df.iloc[0, :].description.tokenTree is not b.timesheetdf.df.iloc[0, :].description.tokenTree

    # All tasks
    assert a.timesheetdf.df.description.equals(b.timesheetdf.df.description)

def test_collect_idempotent():
    orig = testing_utils.loadTestTSDS(testing_utils.PUBLIC_TSDF, suffix='_test5')
    tsds = copy.deepcopy(orig)
    for origCat, catalog in zip(orig.cats.values(), tsds.cats.values()):
        catalog.autoCollect(tsds.timesheetdf)
        if Global.isPrivate() and catalog.COLLXBLE_CLASS == Person:
            continue
        assert len(catalog) == len(origCat)
        assert origCat.headerData == catalog.headerData
        assert origCat == catalog


def test_filterMedia():
    tsds = testing_utils.loadTestTSDS()
    tsds.catalogPopulateDF()

    """ filterMedia, isEmpty """
    b = tsds.timesheetdf.isEmpty('movie')
    a = tsds.timesheetdf.filterMedia('tvshow')
    assert all(a.isEmpty('movie'))
    assert a.isEmpty('tvshow').equals(tsds.timesheetdf.isEmpty('tvshow'))
    assert tsds.timesheetdf.isEmpty('movie').equals(b)  # Ensure call to filterMedia() didn't change b

    movie = tsds.timesheetdf.tsquery('Movie : ;')
    tv = tsds.timesheetdf.tsquery('TVShow : ;')
    neither = tsds.timesheetdf.tsquery('! TVShow & ! Movie : ;')
    assert set(tsds.timesheetdf.df.index.values) - set(movie.df.index.values) - set(tv.df.index.values) ==\
           set(neither.df.index.values)


if __name__=='__main__':
    test_collect_idempotent()