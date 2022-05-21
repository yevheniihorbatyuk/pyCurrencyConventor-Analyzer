import os
import sys
import function
import main
import datetime
import openpyxl
import pandas as pd
import datetime

from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QFileDialog


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()


        self.initUI()



    def initUI(self):

        self.setWindowIcon(QtGui.QIcon('money.png'))
        self.setWindowTitle('Currency Analyzer')
        self.setGeometry(300, 300, 600, 600)

        # Start label
        self.lable_start = QtWidgets.QLabel(self)
        self.lable_start.setText('From :')
        self.lable_start.setGeometry(0, 0, 30, 30)
        self.lable_start.adjustSize()

        # Start date line edit
        self.start_date = QtWidgets.QLineEdit(self)
        self.start_date.move(20, 20)
        self.start_date.setText(str(datetime.datetime.today().date()))

        # End label
        self.label_end = QtWidgets.QLabel(self)
        self.label_end.setText('To :')
        self.label_end.setGeometry(1, 40, 30, 30)

        # End date line edit
        self.end_date = QtWidgets.QLineEdit(self)
        self.end_date.move(20, 65)
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

        # Label base
        self.label_base = QtWidgets.QLabel(self)
        self.label_base.setText('Base')
        self.label_base.setGeometry(200, 1, 30, 30)
        self.label_base.adjustSize()

        # Base line edit
        self.base_line_edit = QtWidgets.QLineEdit(self)
        self.base_line_edit.setGeometry(200, 20, 50, 20)
        self.base_line_edit.setText('USD')

        # Label symbols
        self.label_symbols = QtWidgets.QLabel(self)
        self.label_symbols.setText('Symbols')
        self.label_symbols.setGeometry(200, 40, 30, 30)
        self.label_symbols.adjustSize()

        # Symbols line edit
        self.symbols_line_edit = QtWidgets.QLineEdit(self)
        self.symbols_line_edit.setGeometry(200, 60, 50, 20)
        self.symbols_line_edit.setText('CZK')


        # Show describe
        self.output_date_describe_label = QtWidgets.QLabel(self)
        self.output_date_describe_label.move(20, 150)
        self.output_date_describe_label.setText('DESCRIBE')
        self.output_date_describe_label.adjustSize()

        # Show max values
        self.output_date_max_label = QtWidgets.QLabel(self)
        self.output_date_max_label.move(200, 150)
        self.output_date_max_label.setText('MAX')
        self.output_date_max_label.adjustSize()

        # Show mean values
        self.output_date_mean_label = QtWidgets.QLabel(self)
        self.output_date_mean_label.move(300, 150)
        self.output_date_mean_label.setText('MEAN')
        self.output_date_mean_label.adjustSize()

        # Show min values
        self.output_date_min_label = QtWidgets.QLabel(self)
        self.output_date_min_label.move(400, 150)
        self.output_date_min_label.setText('MIN')
        self.output_date_min_label.adjustSize()

        # Save report button
        self.btn_save = QtWidgets.QPushButton(self)
        self.btn_save.move(180, 100)
        self.btn_save.setText('Save report')
        self.btn_save.adjustSize()
        self.btn_save.clicked.connect(self.save_report)




    def get_data(self):
        start_date_text = self.start_date.text()
        end_date_text = self.end_date.text()
        base_line_edit_text = self.base_line_edit.text()
        symbols_line_edit_text = self.symbols_line_edit.text()

        print('get_data : work', '\n',
              'Start :', start_date_text, '\n'
                                          'End :', end_date_text, '\n')
        try:
            main.get_currency \
                (start_date=start_date_text,
                 end_date=end_date_text,
                 base=base_line_edit_text,
                 symbols=symbols_line_edit_text)
        except:
            print('Wrong input')

    def read_file(self):

        global df, describe, max_of_years, mean_of_year, min_of_year

        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                'data', "Any file (*.csv)")
            print('File name:', fname[0])

            df, describe, max_of_years, mean_of_year, min_of_year = main.currency_analysis(file_name= fname[0])

        except:
            print('File not read')

        self.output_date_describe_label.setText(str(describe))
        self.output_date_describe_label.adjustSize()

        self.output_date_max_label.setText(str(max_of_years))
        self.output_date_max_label.adjustSize()

        self.output_date_mean_label.setText(str(mean_of_year))
        self.output_date_mean_label.adjustSize()

        self.output_date_min_label.setText(str(min_of_year))
        self.output_date_min_label.adjustSize()




    def save_report(self):


        try:
            os.mkdir('report')
            print('Report directory have been CREATED')

        except OSError as e:
            print('Report directory is EXIST')

        dir_path = QFileDialog.getExistingDirectory(self, "Choose Directory", "report")
        print(dir_path)

        # save_dir =f'report{datetime.datetime.today()}'

        try:

            # Saving to csv
            df.to_csv(f'{dir_path}/DataFrame.csv')
            describe.to_csv(f'{dir_path}/describe.csv')
            max_of_years.to_csv(f'{dir_path}/max_of_year.csv')
            mean_of_year.to_csv(f'{dir_path}/mean_of_year.csv')
            min_of_year.to_csv(f'{dir_path}/min_of_year.csv')

            # Saving to xlsx
            with pd.ExcelWriter(f'{dir_path}/REPORT.xlsx') as writen:
                df.to_excel(writen, sheet_name='DataFrame')
                describe.to_excel(writen, sheet_name='describe')
                max_of_years.to_excel(writen, sheet_name='max_of_years')
                mean_of_year.to_excel(writen, sheet_name='mean_of_years')
                min_of_year.to_excel(writen, sheet_name='min_of_years')
        except:
            print('Not saved')

        # sub_df = pd.DataFrame(data= describe, copy= describe)
        # sub_df.to_csv('describe.csv')
        # return describe ,max_of_years, mean_of_year

    # def show_btn_function(self):

    # describe, max_of_years, mean_of_year = self.read_file()
    # self.output_date_describe_label.setText(describe)
    #
    # self.output_date_max_label.setText(self.read_file()[0])
    #
    # self.output_date_mean_label.setText(self.read_file()[0])
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

    # @QtCore.Slot()
    # def magic(self):
    #     pass
    #     # self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Window()
    widget.resize(600, 600)
    widget.show()

    sys.exit(app.exec())
