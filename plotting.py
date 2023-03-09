from io import BytesIO
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np
from Covid_proj.set_data import CASES_data, RECOVERIES_data


class Plotting(FigureCanvasQTAgg):
    __IMG_FORMAT = "png"

    def __init__(self, tab):
        self.__fig, self.__ax = plt.subplots(figsize=(9, 6), dpi=100)

        super().__init__(self.__fig)
        self.__tab = tab
        if self.__tab == "cases":
            self.__DATABASE = CASES_data
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

        self.__chosen_countries = self.__DATABASE.Clicked
        self.__data = self.__DATABASE.All_Countries
        self.__new = self.__create_dict()
        self.__draw_plot()

        plt.rcParams.update({'figure.max_open_warning': 0})

    def __draw_plot(self):
        for country, value in self.__new.items():
            self.__ax.plot(value, label=country)

        if self.__tab == "cases":
            self.__ax.set_ylabel("number of cases")
            self.__ax.set_title("Covid cases")
        else:
            self.__ax.set_ylabel("number of recoveries")
            self.__ax.set_title("Covid recoveries")

        self.__ax.set_xlabel("time")

        if len(self.__new.items()) != 0:
            self.__ax.legend()
        if self.__DATABASE.Last_Day != -1 and self.__DATABASE.Last_Day != -1 \
                and self.__DATABASE.Last_Day - self.__DATABASE.First_Day > 0 \
                and self.__DATABASE.Last_Day <= len(self.__DATABASE.Time):
            self.__ax.set_xlim(self.__DATABASE.First_Day, self.__DATABASE.Last_Day)

        elif self.__data != {}:
            time = self.__DATABASE.Time
            time_value = np.linspace(1, len(time), len(time))
            self.__ax.set_xlim(time_value[0], time_value[-1])

        self.__ax.ticklabel_format(axis="y", style='plain')
        self.__ax.grid()

    def __create_dict(self):
        new = {}
        for name in self.__chosen_countries:
            new[name] = self.__data[name]
        return new

    def get_img(self):
        img_data = BytesIO()
        self.__fig.savefig(img_data, format=self.__IMG_FORMAT)

        seek_offset = 0
        img_data.seek(seek_offset)

        return img_data

    def display_plot(self, parent):
        plot = Plotting(self.__tab)
        parent.main_layout.addWidget(plot, 0, 0, 4, 4)
        parent.setLayout(parent.main_layout)
