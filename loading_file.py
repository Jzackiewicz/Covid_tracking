from PyQt5.QtWidgets import QFileDialog

from Covid_proj.exceptions import WrongFileExtension
from Covid_proj.set_data import CASES_data, RECOVERIES_data
from exceptions import FileNotChosenException
from countries_panel import CountryButtonsPanel


class Loadingfile:
    def __init__(self, tab):

        self.__tab = tab
        if self.__tab == "cases":
            self.__DATABASE = CASES_data
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

        self.__name = self.__DATABASE.Filename

    def __read_file(self):
        data = {}

        f = open(self.__name, "r")
        date = f.readline()
        date = date.split(",")[4:]
        date[-1] = date[-1].replace("\n", "")
        self.__DATABASE.Time = date
        self.__DATABASE.Last_Day = len(self.__DATABASE.Time)

        for temp in f:
            if temp[0] == ",":
                temp = temp[1:]
            temp = temp.split(",")

            if temp[1][0].isalpha() or temp[1][0] == " ":
                country_key = temp[0] + ", " + temp[1]
                country_value = temp[4:]
                if temp[2] != "" and temp[2][0].isalpha():
                    country_key = temp[0] + ", " + temp[2]
                    country_value = temp[5:]
            else:
                country_key = temp[0]
                country_value = temp[3:]

            country_value = [int(val) for val in country_value]
            data[country_key] = country_value
        f.close()

        return data

    def __choose_file(self, parent):
        filename = QFileDialog.getOpenFileName(parent)
        try:
            self.__DATABASE.Filename = filename[0]
            fin = Loadingfile(self.__tab)
            self.__DATABASE.All_Countries = fin.__read_file()
            parent.__country_buttons_box = CountryButtonsPanel(self.__DATABASE.All_Countries, parent, self.__tab)
            parent.main_layout.addWidget(parent.__country_buttons_box, 1, 5, 5, 2)
            parent.setLayout(parent.main_layout)
            parent.show()
        except:
            if filename[0] == "":
                FileNotChosenException()
            elif filename[0].split(".")[-1] != "csv":
                WrongFileExtension()

    def file_btn_click(self, parent):
        fin = Loadingfile(self.__tab)
        return lambda _: fin.__choose_file(parent)