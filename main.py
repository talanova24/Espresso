import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class AddItem(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton_ok.clicked.connect(self.ok)
        self.pushButton_cancel.clicked.connect(self.close)

    def ok(self):
        sort = self.lineEdit_sort.text()
        fry = self.lineEdit_fry.text()
        description = self.lineEdit_description.text()
        beans = self.comboBox_bean.currentText()
        price = self.doubleSpinBox.value()
        volume = self.spinBox_2.value()
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO coffee_info '
                       '(sort_coffee, roasting, "ground grains", taste, price, volum) '
                       'VALUES (?, ?, ?, ?, ?, ?)', (sort, fry, description, beans, price, volume))
        conn.commit()
        conn.close()
        self.close()


class EditItem(QWidget):
    def __init__(self, id_item, sort, fry, description, beans, price, volume):
        QWidget.__init__(self)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.lineEdit_sort.setText(sort)
        self.lineEdit_fry.setText(fry)
        self.lineEdit_description.setText(description)
        self.comboBox_bean.setCurrentText(beans)
        self.doubleSpinBox.setValue(float(price))
        self.spinBox_2.setValue(int(volume))
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_ok.clicked.connect(self.ok)
        self.id_item = id_item

    def ok(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        sort = self.lineEdit_sort.text()
        fry = self.lineEdit_fry.text()
        description = self.lineEdit_description.text()
        beans = self.comboBox_bean.currentText()
        price = self.doubleSpinBox.value()
        volume = self.spinBox_2.value()
        # sort_coffee, roasting, "ground grains", taste, price, volum
        cursor.execute('UPDATE coffee_info SET sort_coffee=?, roasting=?, "ground grains"=?, taste=?, price=?, '
                       'volum=? WHERE ID=?', (sort, fry, description, beans, price, volume, self.id_item))
        connection.commit()
        connection.close()
        self.close()


    def cancel(self):
        self.close()

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки',
                                                    'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])

        self.tableWidget.resizeColumnsToContents()

        self.conn = sqlite3.connect('coffee.sqlite')
        self.cursor = self.conn.cursor()
        self.pushButton_add.clicked.connect(self.add)
        self.pushButton_edit.clicked.connect(self.edit)

    def edit(self):
        selected_row = self.tableWidget.currentRow()
        id_item = int(self.tableWidget.item(selected_row, 0).text())
        sort = self.tableWidget.item(selected_row, 1).text()
        fry = self.tableWidget.item(selected_row, 2).text()
        beans = self.tableWidget.item(selected_row, 3).text()
        description = self.tableWidget.item(selected_row, 4).text()

        price = self.tableWidget.item(selected_row, 5).text()
        volume = self.tableWidget.item(selected_row, 6).text()
        self.edit = EditItem(id_item, sort, fry, description, beans, price, volume)
        self.edit.show()

        # connection = sqlite3.connect('coffee.sqlite')
        # cursor = connection.cursor()
        # # sort_coffee, roasting, "ground grains", taste, price, volum
        # cursor.execute('UPDATE coffee_info SET sort_coffee=?, roasting=?, "ground grains"=?, taste=?, price=?, '
        #                'volum=? WHERE ID=?', (sort, fry, description, beans, price, volume, id_item))
        # connection.commit()
        # connection.close()

    def add(self):
        self.item = AddItem()
        self.item.show()

    def run(self):
        self.tableWidget.setRowCount(0)
        query = 'SELECT * FROM coffee_info'
        data = self.cursor.execute(query).fetchall()

        for row_number, row_data in enumerate(data):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
