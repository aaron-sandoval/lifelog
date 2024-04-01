import copy
import sys, os, pytest
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from tests.testing_utils import READ_DIR, WRITE_DIR
import tests.testing_utils as testing_utils
from src.TimesheetDataset import *


def test_equality():
    a = LinearCatalog(Audiobook, loadYaml=False)
    b = LinearCatalog(Audiobook, loadYaml=False)
    assert a == b
    loaded = testing_utils.loadTestCatalog(Audiobook, suffix='_test4')
    assert len(loaded) > 0
    a.collect(loaded.getObjects(loaded.collxn.iloc[[0], :]))
    assert a != b
    b.collect(loaded.getObjects(loaded.collxn.iloc[[0], :]))
    assert a == b

    temp = a.CATALOG_FILE
    a.CATALOG_FILE = 'blah'
    assert a == b
    a.CATALOG_FILE = temp

    a.updateHeaderData()
    assert a == b

    loaded2 = testing_utils.loadTestCatalog(Audiobook, suffix='_test4')
    assert loaded == loaded2

def test_header():
    file = os.path.join(READ_DIR, 'Catalog_Audiobook_TEST1.yaml')
    file_out = os.path.join(WRITE_DIR, 'Catalog_Audiobook_TEST1_w.yaml')
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
    cat = DAGCatalog(Food, file=os.path.join(READ_DIR, 'unit_test_DAGCatalog_3.yaml'))
    assert type(cat.dag) == nx.DiGraph
    # read1_nodes = set(cat.dag.nodes)
    # read1_adj = cat.dag.adj
    cat.write(file=os.path.join(WRITE_DIR, 'unit_test_DAGCatalog_2rw.yaml'))
    catRoundTrip = DAGCatalog(Food, file=os.path.join(WRITE_DIR, 'unit_test_DAGCatalog_2rw.yaml'))
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
    catFromEmpty = DAGCatalog(Food, file=os.path.join(READ_DIR, 'empty.yaml'))
    assert len(catFromEmpty) == 0
    assert catFromEmpty == DAGCatalog(Food, loadYaml=False)

    # parents() and children()
    assert len(catFromEmpty.parents('$FOOD')) == 0
    assert catFromEmpty.parents('$PLATOS') == ['$FOOD']

    # Test yamls with missing entries
    with pytest.raises(AssertionError):
        catMissingItemFromAdj = DAGCatalog(Food, file=os.path.join(READ_DIR, 'unit_test_DAGCatalog_Food_missing_1.yml'))
    with pytest.raises(AssertionError):
        catMissingItemFromCollxn = DAGCatalog(Food, file=os.path.join(READ_DIR, 'unit_test_DAGCatalog_Food_missing_2.yml'))
    # TODO: bare header w/ document divider, bare header w/out doc divider,


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
    test_Gender()
    test_SocialGroup()
    test_Review()
