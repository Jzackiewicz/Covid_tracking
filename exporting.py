from PyQt5.QtWidgets import QPushButton, QFileDialog
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from Covid_proj.exceptions import EmptyChartError
from Covid_proj.plotting import Plotting
from Covid_proj.set_data import CASES_data, RECOVERIES_data


class PdfGenerator:
    def __init__(self, tab):

        self.__tab = tab

        if self.__tab == "cases":
            self.__DATABASE = CASES_data
            self.__chart_type = "Covid cases"
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data
            self.__chart_type = "Covid recoveries"

    def create_and_save_report(self, img, filepath, pagesize=A4):
        pdf_template = self.__create_pdf_template(filepath, img, pagesize)
        pdf_template.setTitle("Covid Chart")
        pdf_template.save()

    def __create_pdf_template(self, filepath, img, pagesize):
        canvas = Canvas(filepath, pagesize=pagesize)
        canvas.setFont("Times-Roman", 16)
        title_magic_offset, img_magic_offset = 100, 600
        imagesize_x, imagesize_y = 600, 400
        title_x, title_y = A4[0] / 2, A4[1] - title_magic_offset
        img_x, img_y = (A4[0] - imagesize_x) / 2, A4[1] - 550

        if self.__DATABASE.First_Day == -1 or self.__DATABASE.Last_Day == -1:
            self.__title = f"{self.__chart_type} chart in " \
                           f"{self.__DATABASE.Time[0]} - {self.__DATABASE.Time[len(self.__DATABASE.Time) - 1]}"
        else:
            self.__title = f"{self.__chart_type} chart in " \
                           f"{self.__DATABASE.Time[self.__DATABASE.First_Day]} - " \
                           f"{self.__DATABASE.Time[self.__DATABASE.Last_Day]}"

        canvas.drawCentredString(title_x, title_y, self.__title)
        canvas.drawImage(img, img_x, img_y, imagesize_x, imagesize_y)

        return canvas


class PdfButton(QPushButton):
    def __init__(self, parent, tab):
        super().__init__("Export to PDF")
        self.__parent = parent
        self.__tab = tab
        self.__pdf_generator = PdfGenerator(self.__tab)

        if self.__tab == "cases":
            self.__DATABASE = CASES_data
            self.__chart_type = "Covid cases"
        elif self.__tab == "recoveries":
            self.__DATABASE = RECOVERIES_data

        self.clicked.connect(self.__save_btn_action)

    def __save_btn_action(self):
        if not self.__DATABASE.Clicked:
            EmptyChartError()
        else:
            self.__chart = Plotting(self.__tab)
            img_data = self.__chart.get_img()

            img = ImageReader(img_data)

            filename = self.__prepare_file_chooser()
            if filename == "":
                pass
            else:
                self.__pdf_generator.create_and_save_report(img, filename)

    def __prepare_file_chooser(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save PDF report", filter="*.pdf")
        return filename
