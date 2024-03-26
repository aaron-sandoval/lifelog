import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.path.abspath(__file__)).parent.parent.absolute()))

def test_1(n = 0):
    # if n > 800:
    #     print('Hello')
    # else:
    #     test_1(n+1)
    print(f'cwd = {os.getcwd()}')
    print(f'path0 = {sys.path[0]}')

    try:
        import src.TimesheetGlobals as Global
        print('Global imported successfully')
    except Exception as e:
        print(f'import TImesheetGlobals failed: {e}')