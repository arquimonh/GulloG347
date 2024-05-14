from cx_Freeze import setup, Executable
import sys
from pathlib import Path

include_files = Path(__file__).parent / "assets"

ico = include_files / "ico.ico"

# Dependências do seu projeto
build_exe_options = {
    "packages": ["tkinter", "pynput", "ttkbootstrap", "queue", "pathlib"],
    "excludes": [],
    "include_files": [include_files],
    "optimize": 2
    }

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "ContadorElden",
    version = "0.1",
    description = "Aplicativo ContadorElden",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base, icon=ico)]
)
