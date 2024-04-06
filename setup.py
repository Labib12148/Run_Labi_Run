import sys
import os
from cx_Freeze import setup, Executable

SETUP_DIR = os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = os.path.join(SETUP_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(SETUP_DIR, 'tcl', 'tk8.6')

include_files = [
    (os.path.join(SETUP_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86.dll')),
    (os.path.join(SETUP_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86.dll')),
    ('assets', 'assets')
]
ICON_PATH = "assets\icons\icon1.jpg"

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("Run_Labi_Run.py",base=base,icon= ICON_PATH,
                            shortcut_name="Run Labi Run",
                            shortcut_dir="DesktopFolder")]

setup(
    name="Run Labi Run",
    version="1.4.8",
    author="Sadman Labib",
    description="This is a game made with pygame. You might have seem similar game called \"T-Rex\". It is Run Labi Run!, my version of T-Rex.",
    options={"build_exe": {"include_files": include_files}},
    executables=executables
)
