import sys
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QGridLayout, QPushButton, QApplication
from Covid_proj.exporting import PdfButton
from Covid_proj.set_data import CASES_data, RECOVERIES_data
from Covid_proj.loading_file import Loadingfile
from Covid_proj.plotting import Plotting
from Covid_proj.countries_panel import CountryButtonsPanel
from Covid_proj.searching import SearchPanel
from Covid_proj.timeslider import TimeSlider


class Interface(QWidget):
    def __init__(self, tab):
        super().__init__()

        self.__tab = tab
        if self.__tab == "cases":
            self.__DATABASE = CASES_data
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

        self.countries = self.__DATABASE.All_Countries
        self.__prepare_window()

    def __prepare_window(self):
        self.__search_panel = SearchPanel(self, self.__tab)
        self.__country_buttons_box = CountryButtonsPanel(self.countries, self, self.__tab)
        self.__file_btn = QPushButton("Load file")
        self.__file_btn.clicked.connect(Loadingfile(self.__tab).file_btn_click(self))
        self.__pdf_btn = PdfButton(self, self.__tab)
        self.__time_slider = TimeSlider(self, self.__tab)

        self.main_layout = QGridLayout()
        self.main_layout.setColumnStretch(5, 2)
        self.main_layout.addWidget(self.__search_panel, 0, 5, 1, 2)
        self.main_layout.addWidget(Plotting(self.__tab).display_plot(self), 0, 0, 4, 4)
        self.main_layout.addWidget(self.__country_buttons_box, 1, 5, 5, 2)
        self.main_layout.addWidget(self.__file_btn, 6, 6, 1, 1)
        self.main_layout.addWidget(self.__pdf_btn, 6, 0, 1, 1)
        self.main_layout.addWidget(self.__time_slider, 5, 3, 2, 1)

        self.setLayout(self.main_layout)


class TabsWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.__tabs = QTabWidget()
        self.__tabs.addTab(Interface("cases"), "COVID cases")
        self.__tabs.addTab(Interface("recoveries"), "Recoveries")
        self.setCentralWidget(self.__tabs)
        self.setWindowTitle("Covid project")
        self.setFixedSize(width, height)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    Window = TabsWindow(1200, 700)
    sys.exit(app.exec_())
