import sys
from PyQt6 import uic
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox

class CoffeeForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.main = False
        self.id = False
        self.show()
    
    def set_id(self, id):
        self.id = id

    def set_main(self, window):
        self.main = window   

    def is_valid(self):
        return all([
            self.name.toPlainText(),
            self.status.toPlainText(),
            self.moloti.toPlainText(),
            self.description.toPlainText(),
            self.price.toPlainText(),
            self.volume.toPlainText()
        ])
    
    def update_values(self):
        query = f"SELECT * FROM coffee WHERE id = {self.id}"
        data = self.main.do_query(query)[0]
        self.name.setPlainText(data[1])
        self.status.setPlainText(str(data[2]))
        self.moloti.setPlainText(data[3])
        self.description.setPlainText(data[4])
        self.price.setPlainText(str(data[5]))
        self.volume.setPlainText(str(data[6]))

    def create(self):
        if self.is_valid():
            name = self.name.toPlainText()
            status = self.status.toPlainText()
            moloti = self.moloti.toPlainText()
            description = self.description.toPlainText()
            price = self.price.toPlainText()
            volume = self.volume.toPlainText()
            query = f"""
            INSERT INTO coffee
            ('название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки')
            VALUES ('{name}', {status}, '{moloti}', '{description}', {price}, {volume})
            """
            self.main.do_query(query)
            self.main.update_table(self.main.do_query())
            self.close()
        
    def edit(self):
        if self.is_valid():
            name = self.name.toPlainText()
            status = self.status.toPlainText()
            moloti = self.moloti.toPlainText()
            description = self.description.toPlainText()
            price = self.price.toPlainText()
            volume = self.volume.toPlainText()
            query = f"""
            UPDATE coffee
            SET 'название сорта' = '{name}', 
            'степень обжарки' = {status}, 
            'молотый/в зернах' = '{moloti}', 
            'описание вкуса' = '{description}',
            'цена' = {price},
            'объем упаковки' = {volume}
            WHERE ID = {self.id}
            """
            self.main.do_query(query)
            self.main.update_table(self.main.do_query())
            self.close()
            

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.init_ui()
    
    def init_ui(self):
        self.update_table(self.do_query())
        self.addbtn.clicked.connect(self.add_coffee)
        self.editBtn.clicked.connect(self.edit_coffee)
        self.deleteBtn.clicked.connect(self.delete_coffee)
    
    def do_query(self, query="SELECT * FROM coffee"):
        con = sqlite3.connect('coffee.sqlite.db')
        cur = con.cursor()
        if 'SELECT' in query:
            res = cur.execute(query).fetchall()
        else:
            cur.execute(query)
            con.commit()
            res = None
        con.close()
        return res

    def update_table(self, data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        labels = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget.setHorizontalHeaderLabels(labels)
        for row in range(len(data)):
            for column in range(len(data[0])):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

    def add_coffee(self):
        form = CoffeeForm()
        form.set_main(self)
        form.setWindowTitle("Добавить кофе")
        form.button.setText("Добавить")
        form.button.clicked.connect(form.create)

    def edit_coffee(self):
        row = self.tableWidget.currentRow()
        if row >= 0:
            id = self.tableWidget.item(row, 0).text()
            form = CoffeeForm()
            form.setWindowTitle("Редактировать кофе")
            form.button.setText("Редактировать")
            form.set_main(self)
            form.set_id(id)
            form.update_values()
            form.button.clicked.connect(form.edit)
    
    def delete_coffee(self):
        if self.tableWidget.selectedIndexes():
            rows = [i.row() for i in self.tableWidget.selectedIndexes()]
            ids = ", ".join(set(self.tableWidget.item(index, 0).text() for index in rows))
            question = QMessageBox.question(
                self, 
                "Удалить выбранные сорта кофе?", 
                f"Действительно удалить элементы с id {ids}?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if question == QMessageBox.StandardButton.Yes:
                query = f"DELETE FROM coffee WHERE ID IN ({ids})"
                self.do_query(query)
                self.update_table(self.do_query())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
