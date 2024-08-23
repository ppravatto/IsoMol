import isomol

from os.path import join

from base import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


class MplWidget(QtWidgets.QWidget):
    
    def __init__(self, parent=None, dpi=100):

        QtWidgets.QWidget.__init__(self, parent)
        
        self.fig = Figure(dpi=dpi)
        self.canvas = FigureCanvas(self.fig)
        
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.tight_layout()

        self.canvas.axes.set_xlabel("Mass [amu]")
        self.canvas.axes.set_ylabel("Intensity [a.u.]")

        self.setLayout(vertical_layout)
    
    def plot_data(self, masses, intensities, ylogscale = False):
        self.canvas.axes.clear()
        self.canvas.axes.stem(masses, intensities, basefmt="none", markerfmt="none")

        if ylogscale:
            self.canvas.axes.set_yscale("log")
        else:
            self.canvas.axes.set_yscale("linear")
            self.canvas.axes.set_ylim([0, 105])
        
        self.canvas.axes.grid(which="major", c="#DDDDDD")
        self.canvas.axes.grid(which="minor", c="#EEEEEE")

        self.canvas.axes.set_xlabel("Mass [amu]")
        self.canvas.axes.set_ylabel("Intensity [a.u.]")


class Ui_IsoMol(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.__masses = []
        self.__intensities = []
        self.__ylogscale = False

        MainWindow.setFixedSize(MainWindow.size())

        geometry = self.mplWidget.geometry()
        self.mplWidget = MplWidget(self.centralwidget)
        self.mplWidget.setGeometry(geometry)

        self.tableWidget.setColumnCount(2)
        self.reset_table()

        self.formulaEdit.textChanged.connect(self.formula_changed)
        
        self.computeButton.clicked.connect(self.compute)
        self.computeButton.setEnabled(False)

        self.saveButton.clicked.connect(self.save_plot)
        self.saveButton.setEnabled(False)
        
        self.exportButton.clicked.connect(self.save_csv)
        self.exportButton.setEnabled(False)

        self.YLogscaleCheckBox.clicked.connect(self.set_ylogscale)
        self.YLogscaleCheckBox.setEnabled(False)
    
    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)

    def reset_table(self):
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(["Mass (amu)", "Intensity (%)"])
        self.tableWidget.setRowCount(0)

    def formula_changed(self):

        self.reset_table()
        self.mplWidget.canvas.axes.clear()
        self.mplWidget.canvas.draw()
        self.saveButton.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.YLogscaleCheckBox.setEnabled(False)

        self.__masses = []
        self.__intensities = []

        if self.formulaEdit.text() == "":
            self.computeButton.setEnabled(False)
        else:
            self.computeButton.setEnabled(True)


    def compute(self):
        self.__formula = self.formulaEdit.text()

        try:
            composition = isomol.parse_formula(self.__formula)
            peaks = isomol.process(composition, normalize=True)
            peaks.sort(key=lambda peak: peak[0])
        
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Invalid formula")
            msg.setInformativeText('The formula given by the user is invalid')
            msg.setWindowTitle("Input error")
            msg.exec_()
        
        else:
            self.__masses = [peak[0] for peak in peaks]
            self.__intensities = [peak[1] for peak in peaks]

            self.tableWidget.setRowCount(len(peaks))
            for i, (mass, intensity) in enumerate(zip(self.__masses, self.__intensities)):
                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(f"{mass:.6f}"))
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{intensity:.3e}"))

            self.update_plot()

            self.saveButton.setEnabled(True)
            self.exportButton.setEnabled(True)
            self.YLogscaleCheckBox.setEnabled(True)

    def update_plot(self):
        self.mplWidget.plot_data(self.__masses, self.__intensities, self.__ylogscale)
        self.mplWidget.canvas.draw()

    def save_plot(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', '/home', QtWidgets.QFileDialog.ShowDirsOnly)
        self.mplWidget.canvas.figure.savefig(join(folder, f"{self.__formula}.png"), dpi=600)
    
    def save_csv(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', '/home', QtWidgets.QFileDialog.ShowDirsOnly)
        with open(join(folder, f"{self.__formula}.csv"), "w") as csv:
            for mass, intensity in zip(self.__masses, self.__intensities):
                csv.write(f"{mass:.10f}, {intensity:.10f}\n")
    
    def set_ylogscale(self):
        self.__ylogscale = self.YLogscaleCheckBox.isChecked()
        self.update_plot()

        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_IsoMol()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())