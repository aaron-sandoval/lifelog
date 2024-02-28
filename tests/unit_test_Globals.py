import sys, os, pytest

from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from src.TimesheetGlobals import *

test_dir = os.path.join(rootProjectPath(), 'tests')


def test_metaproject():
    assert Metaproject.DORMIR.color[0] < Metaproject.CARRERA.color[0]
    assert Metaproject.CARRERA.id == 0
    assert Metaproject.ACADEMICO.alias('en_US')[0] < Metaproject.LOGISTICA.alias('en_US')[0]
    assert Metaproject(0) == Metaproject.CARRERA


def test_project():
    assert Project.CARRERA.default_metaproject == 0
    assert Project.DORMIR.alias('es_MX')[0] < Project.MAE_5730.alias('en_US')[0]
    assert len(Project.OPIR_ARQ.color) == 3
    assert Project.CARRERA_ED < Project.ESCRITURA


def test_tag():
    assert len(Tag.BICI.color) == 3
    assert Tag.MUSICA.alias('en_US')[0] < Tag.RUTINA.alias('en_US')[0]
    assert Tag.TREN.alias('es_MX')[0] > Tag.FAMILIA.alias('es_MX')[0]
    assert Tag(1) == Tag.BICI


def test_epoch():
    assert len(Epoch.e2023_EA_Discovery.color) == 3
    assert Epoch.e2018_Boulder_Solo.alias('en_US')[:2] == Epoch.e2021_Tour_Start.alias('en_US')[:2]
    assert Epoch.e2018_Boulder_Solo.alias('en_US')[:4] == Epoch.e2018_BCH.alias('en_US')[:4]
    assert Epoch.e2018_Boulder_Solo.alias('es_MX')[:2] == Epoch.e2021_Tour_Start.alias('es_MX')[:2]
    assert Epoch(0) == Epoch.eEND
    assert Epoch.e2017_Cornell.dt() == Epoch.e2017_Cornell.start


def test_epochscheme():
    assert EpochScheme.MP_COARSE_ATOMIC.alias('en_US')[0] == 'M'
    assert EpochScheme.MP_COARSE.id(datetime(2017, 10, 1, 1)) == 0
    assert EpochScheme.MP_COARSE.id(datetime(2018, 10, 1, 1)) == 2
    assert EpochScheme.MP_COARSE_ATOMIC.labelDT(datetime(2023, 2, 1, 1)) == '2023 Career Pivot'
    assert EpochScheme.INDIVIDUAL.labelDT(datetime(2017, 9, 7, 1)) == '2017 Cornell'
    assert EpochScheme.INDIVIDUAL.labelDT(datetime(2022, 7, 10, 14, 59)) == '2022 Tim Start'
    assert EpochScheme.INDIVIDUAL.labelDT(datetime(2022, 7, 10, 14, 59), locale='es_MX') == '2022 Inicio con Tim'
    assert EpochScheme.MP_COARSE_ATOMIC.labelDT(datetime(2018, 1, 1, 1), locale='es_MX') == 'Posgrado'

if __name__ == "__main__":
    pass
