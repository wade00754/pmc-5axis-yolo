import sys

from PySide6.QtWidgets import QApplication

from pmc_5axis_yolo import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
