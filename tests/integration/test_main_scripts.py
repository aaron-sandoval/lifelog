import sys
import os
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.parent.absolute()))
from scripts.FileManagement import main as FMmain
from scripts.Preprocess import main as PPmain
from scripts.DataCorrection import main as DCmain


def test_FM_PP_DC():
    # Just needs to run without raising an exception
    FM_filePath = FMmain(['test_1_PUBLIC.csv'])
    PP_filePath = PPmain(FM_filePath)
    DCmain(PP_filePath, catalogSuffix='', write=False)

