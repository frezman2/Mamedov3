# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

from main_window import Ui_MainWindow
from form import Ui_Form

import sqlite3
import sys


class Form(Ui_Form, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.commit_button.clicked.connect(self._click)
    
    def initUI(self) -> None:
        """
        db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()
        model: QSqlDatabase = QSqlTableModel(self, db)
        model.setTable('main')
        model.select()
        self.table.setModel(model)
        """
        self.connect = sqlite3.connect('coffee.sqlite')
        '''
        cursor = self.connect.cursor()
        data = cursor.execute("""
        SELECT * FROM main
        WHERE id = ?
        """, [])
        self.line_id.setText()
        '''
    
    def _click(self) -> None:
        cursor = self.connect.cursor()
        data = (
            self.line_title.text(),
            self.line_roast.text(),
            self.line_ground.text(),
            self.line_about.text(),
            self.line_about.text(),
            self.line_volume.text(),
            self.line_id.text()
        )
        result = cursor.execute("""
        SELECT * FROM main
        WHERE id = ?
        """, [self.line_id])
        if result:
            cursor.execute("""
            UPDATE main
            SET
                title = ?,
                roast = ?,
                ground = ?,
                about = ?,
                price = ?,
                volume = ?
            WHERE id = ?
            """, data)
        else:
            cursor.execute("""
            INSERT INTO main (id, title, roast, ground, about, price, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)
        self.connect.commit()
    
    def __del__(self) -> None:
        self.connect.close()


class Window(Ui_MainWindow, QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.add_edit_button.clicked.connect(self._click)
    
    def initUI(self) -> None:
        self.connect = sqlite3.connect('coffee.sqlite')
        cursor = self.connect.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS main
        (id TEXT, title TEXT, roast TEXT, ground TEXT, about TEXT, price TEXT, volume TEXT)
        """)
        db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()
        model: QSqlDatabase = QSqlTableModel(self, db)
        model.setTable('main')
        model.select()
        self.table.setModel(model)
    
    def _click(self) -> None:
        app: QApplication = QApplication([])
        form: Form = Form()
        form.show()
        sys.exit(app.exec())

    def __del__(self) -> None:
        self.connect.close()
