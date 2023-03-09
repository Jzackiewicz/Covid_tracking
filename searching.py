from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit
from Covid_proj.set_data import CASES_data, RECOVERIES_data
from countries_panel import CountryButtonsPanel


class SearchPanel(QLineEdit):
    def __init__(self, parent, tab):
        super().__init__()
        self.__tab = tab
        self.__parent = parent
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPlaceholderText("Search...")
        self.textChanged.connect(self.__find_phrase)

        if self.__tab == "cases":
            self.__DATABASE = CASES_data
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

    def __find_phrase(self):
        phrase = self.text()
        countries = self.__DATABASE.All_Countries.keys()
        found_countries = []
        for k in countries:
            temp = k.lower().split(", ")
            for i in temp:
                if phrase.lower() == i[0:len(phrase)]:
                    found_countries.append(k)
        btn_panel = CountryButtonsPanel(found_countries, self.__parent, self.__tab)
        self.__parent.main_layout.addWidget(btn_panel, 1, 5, 5, 2)
        self.__parent.setLayout(self.__parent.main_layout)
