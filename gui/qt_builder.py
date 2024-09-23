from qtpy import uic
from pathlib import Path

PATH_TO_GUI_DIR = Path.cwd() / "gui" / "src"


def main():
    uic.compileUiDir(PATH_TO_GUI_DIR)


if __name__ == "__main__":
    main()
