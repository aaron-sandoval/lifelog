import sys, os, pytest

from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))
from src.TimesheetGlobals import *


test_dir = os.path.join(rootProjectPath(), 'tests')

def test_metaproject():
    assert Metaproject.DORMIR.color[0] < Metaproject.CARRERA.color[0]
    assert Metaproject.CARRERA.id == 0
    assert Metaproject.ACADEMICO.alias()[0] < Metaproject.LOGISTICA.alias()[0]
    assert Metaproject(0) == Metaproject.CARRERA


if __name__ == "__main__":
    pass
