import copy
import sys, os, pytest
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.parent.absolute()))
from src.TimesheetDataset import *


test_dir = os.path.join(Global.rootProjectPath(), 'tests')


def test_tsds_roundtrip():
    tsds = TimesheetDataset.loadTestTSDS()
    file1 = os.path.join(test_dir, 'test_tsds_write_1.pkl')
    tsds.write(3, tsdfFile=file1)
    tsds_rt = TimesheetDataset.loadTestTSDS(file=file1)
    for attr in ['tsdf', 'cats']:
        assert getattr(tsds, attr) == getattr(tsds_rt, attr)
    assert tsds == tsds_rt


def test_collect_idempotent():
    orig = TimesheetDataset.loadTestTSDS()
    tsds = copy.deepcopy(orig)
    for origCat, catalog in zip(orig.cats.values(), tsds.cats.values()):
        catalog.autoCollect(tsds.timesheetdf)
        assert len(catalog) == len(origCat)
        assert origCat.headerData == catalog.headerData
        assert origCat == catalog


def test_filterMedia():
    tsds = TimesheetDataset.loadTestTSDS()
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

