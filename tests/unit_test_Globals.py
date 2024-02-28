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
    assert Epoch.e2018_Boulder_Solo.alias('es_MX')[:2] == Epoch.e2021_Tour_Start.alias('es_MX')[:2]
    assert Epoch(0) == Epoch.eEND
    assert Epoch.e2017_Cornell.dt() == Epoch.e2017_Cornell.start


if __name__ == "__main__":
    pass
