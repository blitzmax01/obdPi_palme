from PyQt5 import QtWidgets
import sys
from gui.src.dashboard_palme import Ui_MainWindow
from pathlib import Path

PATH_TO_DASHBOARD_UI = Path.cwd() / "dashboard_palme.ui"


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Dashboard")
    window.setStyleSheet("background-color: black")

    ui_window = Ui_MainWindow()
    ui_window.setupUi(window)

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
