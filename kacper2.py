import sys, os
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QLineEdit,
    QSlider,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

TITLE = "Ruch harmoniczny tłumiony"
AMPLITUDE = "Podaj amplitudę"
DAMPING = "Podaj współczynnik tłumienia"
FREQUENCY = "Podaj częstotliwość"
SLIDER_1 = "Czas"
SLIDER_2 = "1"
SLIDER_3 = "200"
DRAWING = "Rysuj"
PLOT_X = "czas[s]"
PLOT_Y = "amplituda"
PLOT_TITLE = " ruch harmoniczy tłumiony "
WARNING_1 = "Coś poszło nie tak..."
WARNING_2 = "Podaj wartość liczbową amplitudy "
WARNING_3 = "Podaj wartość liczbową tłumienia"
WARNING_4 = "Podaj wartość liczbową częstotliwości"
WARNING_5 = "Podaj wartość tłumienia mniejszą lub równą częstotliwości"


class MyApp(QWidget):
    def __init__(self, w=1200, h=800):
        super().__init__()
        self.createLayout(w, h)
        self.insert_ax()

    def createLayout(self, window_width, window_height):
        self.setWindowTitle(TITLE)
        self.window_width, self.window_height = window_width, window_height
        self.setMinimumSize(self.window_width, self.window_height)
        self.layout = QGridLayout(self)
        self.input_A = QLineEdit()
        self.input_B = QLineEdit()
        self.input_W = QLineEdit()
        self.label_A = QLabel(AMPLITUDE)
        self.label_B = QLabel(DAMPING)
        self.label_W = QLabel(FREQUENCY)

        self.label_ST = QLabel(SLIDER_1)
        self.label_ST.setAlignment(Qt.AlignRight)
        self.label_ST1 = QLabel(SLIDER_2)
        self.label_ST1.setAlignment(Qt.AlignRight)
        self.label_ST2 = QLabel(SLIDER_3)
        self.plot_button = QPushButton(DRAWING)
        self.slider_t = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.label_A, 0, 0)
        self.layout.addWidget(self.input_A, 0, 1)
        self.layout.addWidget(self.label_B, 0, 2)
        self.layout.addWidget(self.input_B, 0, 3)
        self.layout.addWidget(self.label_W, 0, 4)
        self.layout.addWidget(self.input_W, 0, 5)
        self.layout.addWidget(self.plot_button, 0, 6)
        self.layout.addWidget(self.label_ST, 1, 1)
        self.layout.addWidget(self.label_ST1, 1, 2)
        self.layout.addWidget(self.label_ST2, 1, 4)
        self.layout.addWidget(self.slider_t, 1, 3)

        self.slider_t.setMinimum(1)
        self.slider_t.setMaximum(200)
        self.slider_t.valueChanged.connect(self.update_chart)

        self.plot_button.clicked.connect(self.update_chart)
        self.canvas = FigureCanvas(plt.Figure())
        self.layout.addWidget(self.canvas, 2, 0, 1, 7)

    def mathMethod(self, t, A, B, W):
        W_1 = np.sqrt(pow(W, 2) - pow(B, 2))
        return A * np.exp(-t * B) * np.cos(W_1 * t)

    def insert_ax(self):
        font = {"weight": "normal", "size": 16}
        matplotlib.rc("font", **font)

        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlabel(PLOT_X)
        self.ax.set_ylabel(PLOT_Y)
        self.ax.set_title(PLOT_TITLE)

    def get_data(self, w_input, com1, com2):
        try:
            return float(w_input.text())
        except ValueError:
            QMessageBox.warning(
                self,
                com1,
                com2,
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
            self.check = False

    def update_chart(self, time):

        self.check = True
        if time == False:
            time = self.slider_t.value()

        self.value_1 = self.get_data(
            self.input_A,
            WARNING_1,
            WARNING_2,
        )
        self.value_2 = self.get_data(
            self.input_B,
            WARNING_1,
            WARNING_3,
        )
        self.value_3 = self.get_data(
            self.input_W,
            WARNING_1,
            WARNING_4,
        )

        if self.check:
            if self.value_2 <= self.value_3:
                self.ax.clear()
                x_range = time
                self.ax.set_xlim([0, x_range])
                self.t = np.arange(
                    0.0,
                    x_range,
                    1 / (4 * self.value_3),
                )

                self.ax.plot(
                    self.t,
                    self.mathMethod(self.t, self.value_1, self.value_2, self.value_3),
                    "k",
                )
                self.ax.set_xlabel(PLOT_X)
                self.ax.set_ylabel(PLOT_Y)
                self.ax.set_title(PLOT_TITLE)

                self.canvas.draw()
            else:
                QMessageBox.warning(
                    self,
                    WARNING_1,
                    WARNING_5,
                    QMessageBox.Ok,
                    QMessageBox.Ok,
                )


if __name__ == "__main__":

    plik = "config.conf"
    if os.path.isfile(plik):

        with open(plik, "r") as f:  # odczytywanie linia po linii
            for string in f:
                Dict = eval(string)  # eval() convert string to dictionary

        app = QApplication(sys.argv)
        app.setStyleSheet("""QWidget {font-size:""" + Dict["font-size"] + """;}""")
        myApp = MyApp(Dict["width"], Dict["height"])
    else:
        app = QApplication(sys.argv)
        app.setStyleSheet("""QWidget {font-size:15px;}""")
        myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print()
