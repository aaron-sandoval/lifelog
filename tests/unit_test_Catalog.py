import copy
import sys, os, pytest
import warnings
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from src.TimesheetDataset import *


test_dir = os.path.join(Global.rootProjectPath(), 'tests')


def loadTestTSDS(file=os.path.join(test_dir, 'PP_2018-08-22-1640_2019-09-02-1659_PRIV.pkl'), suffix='_test4'):
    if not os.path.exists(file):
        if Global.isPrivate():
            fallback = os.path.join(test_dir, 'PP_test3_PUBL.pkl')
            warnings.warn(f"File {file} does not exist. "
                          f"This could be because the specified file is private and not uploaded to the repository. "
                          f"Using public fallback file {fallback} instead", Warning)
            file = fallback
        else:
            raise FileNotFoundError(f"File {file} does not exist.")
    myTimesheetDataset = TimesheetDataset(pd.read_pickle(file), fileSuffix=suffix)
    myTimesheetDataset.preCatalogCorrect()
    myTimesheetDataset.loadCatalogs(fileSuffix=suffix)
    myTimesheetDataset.fileSuffix = suffix + '_W'  # Don't modify original test files
    # TODO: get tsdf to write to test directory
    return myTimesheetDataset


def test_tsds_write():
    tsds = loadTestTSDS()
    tsds.write(3)


def test_collect_idempotent():
    orig = loadTestTSDS()
    tsds = copy.deepcopy(orig)
    for origCat, catalog in zip(orig.cats.values(), tsds.cats.values()):
        catalog.autoCollect(tsds.timesheetdf)
        assert len(catalog) == len(origCat)
        assert origCat.headerData == catalog.headerData
        assert origCat == catalog


def test_Header():
    file = os.path.join(test_dir, 'Catalog_Audiobook_TEST1.yaml')
    file_out = os.path.join(test_dir, 'Catalog_Audiobook_TEST1_w.yaml')
    a = LinearCatalog(Audiobook, loadYaml=False)
    a.write(file_out)
    assert a.headerData['CATALOG COUNT'] == 0
    assert a.headerData['TASK ID RANGE'] == portion.empty()
    emptyHeader = {'HEADER': {
        'FILE TYPE': 'Catalog',
        'DATE WRITTEN': None,
        'TASK ID RANGE': portion.empty(),
        'COLLECTIBLE TYPE': '',
        'CATALOG COUNT': 0,
    }}
    assert a._METADATA_HEADER_DEFAULT == emptyHeader
    a.collect([Audiobook.NULL_INSTANCE()])
    assert a._METADATA_HEADER_DEFAULT == emptyHeader
    a.write(file_out)
    assert a._METADATA_HEADER_DEFAULT == emptyHeader
    assert a.headerData['CATALOG COUNT'] == 1
    assert a.headerData['TASK ID RANGE'] == portion.empty()
    a = LinearCatalog(Audiobook, loadYaml=True, file=file)
    assert a._METADATA_HEADER_DEFAULT == emptyHeader
    assert a.headerData['CATALOG COUNT'] == 1
    assert a.headerData['TASK ID RANGE'] == portion.empty()


def test_DAGCatalog():
    cat = DAGCatalog(Food, file=os.path.join(test_dir, 'unit_test_DAGCatalog_2.yaml'))
    assert type(cat.dag) == nx.DiGraph
    # read1_nodes = set(cat.dag.nodes)
    # read1_adj = cat.dag.adj
    cat.write(file=os.path.join(test_dir, 'unit_test_DAGCatalog_2rw.yaml'))
    catRoundTrip = DAGCatalog(Food, file=os.path.join(test_dir, 'unit_test_DAGCatalog_2rw.yaml'))
    assert type(catRoundTrip.dag) == nx.DiGraph
    assert set(cat.dag.nodes) == set(catRoundTrip.dag.nodes)
    assert cat.dag.adj == catRoundTrip.dag.adj
    assert cat == catRoundTrip

    nx.relabel_nodes(catRoundTrip.dag, {'$PLATOS': '$PLATEOS'}, copy=False)
    assert set(cat.dag.nodes) != set(catRoundTrip.dag.nodes)
    assert cat.dag.adj != catRoundTrip.dag.adj
    assert cat != catRoundTrip
    nx.relabel_nodes(catRoundTrip.dag, {'$PLATEOS': '$PLATOS'}, copy=False)  # Reverse the modification

    catRoundTrip.collect(Food.NULL_INSTANCE())
    assert len(catRoundTrip) == len(cat) + 1
    assert Food.NULL_INSTANCE().id in catRoundTrip.dag.nodes
    assert catRoundTrip.COLLXBLE_CLASS.undefinedVertex() in catRoundTrip.dag.adj[Food.NULL_INSTANCE().id]
    assert len(catRoundTrip.dag.adj[Food.NULL_INSTANCE().id]) == 1
    catRoundTrip.collect(Food.NULL_INSTANCE())  # Collect duplicate, shouldn't change Catalog
    assert len(catRoundTrip) == len(cat) + 1
    # Empty file
    catFromEmpty = DAGCatalog(Food, file=os.path.join(test_dir, 'empty.yaml'))
    assert len(catFromEmpty) == 0
    assert catFromEmpty == DAGCatalog(Food, loadYaml=False)

    # parents() and children()
    assert len(catFromEmpty.parents('$FOOD')) == 0
    assert catFromEmpty.parents('$PLATOS') == ['$FOOD']

    # Test yamls with missing entries
    with pytest.raises(AssertionError):
        catMissingItemFromAdj = DAGCatalog(Food, file=os.path.join(test_dir, 'unit_test_DAGCatalog_Food_missing_1.yml'))
    with pytest.raises(AssertionError):
        catMissingItemFromCollxn = DAGCatalog(Food, file=os.path.join(test_dir, 'unit_test_DAGCatalog_Food_missing_2.yml'))
    # TODO: bare header w/ document divider, bare header w/out doc divider,


def test_TimesheetDF():
    tsds = loadTestTSDS()
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


def test_Relation():
    ppl = [
        Person(
            name='Jim',
            firstTaskID=1,
            firstTime=datetime.datetime(2020, 1, 1, 1),
            firstCircad=datetime.date(2020, 1, 1),
            relationships={sg.Friend(), sg.ActivityMusic()}
        ),
        Person(
            name='Vin',
            firstTaskID=2,
            firstTime=datetime.datetime(2018, 1, 1, 1),
            firstCircad=datetime.date(2020, 1, 1),
            relationships={sg.Friend(), sg.ColleagueAcademic(), sg.Peer()}
        ),
        Person(
            name='Mom',
            firstTaskID=2,
            firstTime=datetime.datetime(1900, 1, 1, 1),
            firstCircad=datetime.date(1900, 1, 1),
            relationships={sg.FamilyMom(), sg.ActivityGames()}
        ),
        Person(
            name='Andy',
            firstTaskID=2,
            firstTime=datetime.datetime(2013, 1, 1, 1),
            firstCircad=datetime.date(2013, 1, 1),
            relationships={sg.ColleagueWork(), sg.Superior()}
        ),
    ]
    assert list(map(lambda x: x.primaryRelation(), ppl)) == [sg.Friend(), sg.Friend(), sg.Family(), sg.Colleague()]


def test_Gender():
    # pass
    assert sg.Gender.MALE == yaml.load(yaml.dump(sg.Gender.MALE), Loader=yaml.SafeLoader)
    h = sg.Gender.FEMALE.color_hex
    assert isinstance(h, str)
    assert len(h) == 7
    assert sg.Gender.NOTAPPLICABLE.alias() == 'N/A'


def test_SocialGroup():
    assert sg.SocialGroup() == yaml.load(yaml.dump(sg.SocialGroup()), Loader=yaml.SafeLoader)
    assert sg.FamilyMom() == yaml.load(yaml.dump(sg.FamilyMom()), Loader=yaml.SafeLoader)


def test_Review():
    assert sg.Review.POOR.color[0] > sg.Review.EXCELLENT.color[0]
    assert all([hasattr(sg.Review.NOREVIEW, k) for k in sg.Review.dataclass.__dataclass_fields__])
    assert sg.Review.GOOD == yaml.load(yaml.dump(sg.Review.GOOD), Loader=yaml.SafeLoader)


if __name__ == "__main__":
    test_TimesheetDF()
    test_Gender()
    test_SocialGroup()
    test_Review()
