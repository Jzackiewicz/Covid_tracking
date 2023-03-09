from PyQt5.QtWidgets import QGroupBox, QFormLayout, QScrollArea, QPushButton

from Covid_proj.exceptions import TooManyPlotsException
from Covid_proj.plotting import Plotting
from Covid_proj.set_data import CASES_data, RECOVERIES_data


class CountryButtonsPanel(QScrollArea):
    def __init__(self, countries, parent, tab):
        super().__init__()
        self.__tab = tab
        self.__prepare_buttons(countries)
        self.__parent = parent
        if self.__tab == "cases":
            self.__DATABASE = CASES_data
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

    def __prepare_buttons(self, data):
        btn_layout = QFormLayout()
        btn_group = QGroupBox()

        self.__current_list = []

        for i in data:
            if i == "time":
                continue
            name = i
            btn = QPushButton(name)
            btn.clicked.connect(self.__click_func(i))
            btn.clicked.connect(self.__display_plot())
            btn_layout.addRow(btn)

        btn_group.setLayout(btn_layout)
        self.setWidget(btn_group)
        self.setWidgetResizable(True)

    def __click_func(self, name):
        return lambda _: self.__add_country_to_list(name)

    def __display_plot(self):
        return lambda _: Plotting(self.__tab).display_plot(self.__parent)

    def __add_country_to_list(self, name):
        if name in self.__DATABASE.Clicked:
            self.__DATABASE.Clicked.remove(name)
        elif len(self.__DATABASE.Clicked) < 10:
            self.__DATABASE.Clicked.append(name)
        else:
            TooManyPlotsException()
        return self.__DATABASE.Clicked


