from PyQt5.QtWidgets import QSlider, QWidget, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import Qt

from Covid_proj.set_data import CASES_data, RECOVERIES_data
from Covid_proj.plotting import Plotting


class TimeSlider(QWidget):
    def __init__(self, parent, tab):
        super().__init__()

        self.__prepare_sliders()
        self.__parent = parent
        self.__tab = tab

        if self.__tab == "cases":
            self.__DATABASE = CASES_data
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

    def __prepare_sliders(self):
        self.panel = QGridLayout()

        self.__time_box_start = QLineEdit()
        self.__time_box_start.setReadOnly(True)
        self.__time_box_start.setAlignment(Qt.AlignCenter)
        self.__time_box_start.setPlaceholderText("mm/dd/yy")
        self.__time_box_start.setFixedWidth(80)

        self.__time_box_end = QLineEdit()
        self.__time_box_end.setReadOnly(True)
        self.__time_box_end.setAlignment(Qt.AlignCenter)
        self.__time_box_end.setPlaceholderText("mm/dd/yy")
        self.__time_box_end.setFixedWidth(80)

        self.__sld_start = QSlider(Qt.Horizontal, self)
        self.__sld_start.valueChanged.connect(self.__update_slider_start)

        self.__sld_end = QSlider(Qt.Horizontal, self)
        self.__sld_end.setMaximum(99)
        self.__sld_end.setValue(99)
        self.__sld_end.valueChanged.connect(self.__update_slider_end)

        self.panel.addWidget(QLabel("Starting date:"), 0, 0)
        self.panel.addWidget(self.__time_box_start, 0, 1)
        self.panel.addWidget(self.__sld_start, 0, 2)
        self.panel.addWidget(QLabel("Ending date:"), 2, 0)
        self.panel.addWidget(self.__time_box_end, 2, 1)
        self.panel.addWidget(self.__sld_end, 2, 2)

        self.setLayout(self.panel)

    def __update_slider_start(self, value):
        timeline = self.__DATABASE.Time
        maxval = len(timeline) - 1
        self.__DATABASE.First_Day = value
        if maxval > 0:
            self.__sld_start.setMaximum(maxval)
            self.__time_box_start.setText(timeline[value])
            self.__slds_positions(timeline, maxval)

            if value > self.__sld_end.value():
                self.__wrong_range_error()
            else:
                self.__correct_range()

            Plotting(self.__tab).display_plot(self.__parent)

    def __update_slider_end(self, value):
        timeline = self.__DATABASE.Time
        maxval = len(timeline) - 1
        self.__DATABASE.Last_Day = value

        if maxval > 0:
            self.__sld_end.setMaximum(maxval)
            self.__time_box_end.setText(timeline[value])
            self.__slds_positions(timeline, maxval)

            if self.__sld_start.value() > value:
                self.__wrong_range_error()
            else:
                self.__correct_range()

            Plotting(self.__tab).display_plot(self.__parent)

    def __wrong_range_error(self):
        self.__time_box_start.setStyleSheet("QLineEdit { background: rgb(255, 50, 50) }")
        self.__time_box_end.setStyleSheet("QLineEdit { background: rgb(255, 50, 50) }")
        self.__time_box_start.setText("WRONG")
        self.__time_box_end.setText("TIME RANGE!")

    def __correct_range(self):
        self.__time_box_start.setStyleSheet("")
        self.__time_box_end.setStyleSheet("")
        self.__time_box_end.setText(self.__DATABASE.Time[self.__sld_end.value()])
        self.__time_box_start.setText(self.__DATABASE.Time[self.__sld_start.value()])

    def __slds_positions(self, timeline, maxval):
        if self.__time_box_end.text() == "":
            self.__time_box_end.setText(timeline[maxval])
        if self.__time_box_start.text() == "":
            self.__time_box_start.setText(timeline[0])
        if self.__sld_end.value() == 99:
            self.__sld_end.setMaximum(maxval)
            self.__sld_end.setValue(maxval)

