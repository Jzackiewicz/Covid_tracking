from PyQt5.QtWidgets import QMessageBox


class FileNotChosenException(QMessageBox):
    def __init__(self):
        super().__init__()
        msg = "File not chosen!"
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.exec_()


class TooManyPlotsException(QMessageBox):
    def __init__(self):
        super().__init__()
        msg = "Maximum number of plots reached!"
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.exec_()


class WrongFileExtension(QMessageBox):
    def __init__(self):
        super().__init__()
        msg = "Wrong file extension (*.csv expected)!"
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.exec_()


class EmptyChartError(QMessageBox):
    def __init__(self):
        super().__init__()
        msg = "Choose plot to draw before exporting!"
        self.setWindowTitle("Error!")
        self.setText(msg)
        self.exec_()
