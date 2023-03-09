import sys

from PyQt5.QtWidgets import QApplication

from Covid_proj.interface import TabsWindow

if __name__ == "__main__":
    app = QApplication([])
    width, height = 1200, 700
    Window = TabsWindow(width, height)
    sys.exit(app.exec_())