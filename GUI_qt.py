import datetime
import sys
import random


import main
import datetime, timedelta
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.initUI()

    def initUI(self):

        self.setWindowTitle('Currency Analyzer')
        self.setGeometry(300, 300, 600, 600)

        self.label = QtWidgets.QLabel(self)

        self.start_date = QtWidgets.QLineEdit(self)
        self.start_date.move(20, 20)
        self.start_date.setText(str(datetime.datetime.today().date()))

        self.end_date = QtWidgets.QLineEdit(self)
        self.end_date.move(20, 60)
        self.end_date.setText(str(datetime.datetime.today().date()))

        self.btn_request = QtWidgets.QPushButton(self)
        self.btn_request.move(20, 100)
        self.btn_request.setText('Get data')
        self.btn_request.adjustSize()
        self.btn_request.clicked.connect(self.get_data)

        self.btn_read_csv = QtWidgets.QPushButton(self)
        self.btn_read_csv.move(100, 100)
        self.btn_read_csv.setText('Read file')
        self.btn_read_csv.adjustSize()
        self.btn_read_csv.clicked.connect(self.read_file)

        self.base_line_edit = QtWidgets.QLineEdit(self)
        self.base_line_edit.setGeometry(200, 20, 50, 20)

        self.symbols_line_edit = QtWidgets.QLineEdit(self)
        self.symbols_line_edit.setGeometry(200, 60, 50, 20)

    def get_data(self):
        start_date_text = self.start_date.text()
        end_date_text = self.end_date.text()
        base_line_edit_text =self.base_line_edit.text()
        symbols_line_edit_text = self.symbols_line_edit.text()

        print('get_data : work', '\n',
              'Start :', start_date_text, '\n'
            'End :', end_date_text, '\n')
        try:
            main.get_currency \
                (start_date= start_date_text,
                 end_date= end_date_text,
                 base= base_line_edit_text,
                 symbols= symbols_line_edit_text)
        except:
            print('Wrong input')

    def read_file(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'data', "Any file (*.csv)")
        print('File name:', fname[1])

        main.currency_analysis(file_name= fname[0])

        # self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        #
        # self.button = QtWidgets.QPushButton("Click me!")
        # self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        #
        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.button)
        #
        # self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        pass
        # self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Window()
    widget.resize(600, 600)
    widget.show()

    sys.exit(app.exec())