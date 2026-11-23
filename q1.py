import sys
import os
import platform
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QLabel, QFileDialog
)
from About import AboutWindow


class GradesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("תיקון קובץ ציונים")
        self.resize(550, 600)
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''
        self.about_window = AboutWindow()
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.load_btn = QPushButton("בחר קובץ ציונים")
        self.load_btn.clicked.connect(self.load_file)
        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.about_window.show)
        top_layout.addWidget(self.load_btn)
        top_layout.addWidget(self.about_btn)
        main_layout.addLayout(top_layout)
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        main_layout.addWidget(self.table)
        bonus_layout = QHBoxLayout()
        bonus_label = QLabel("נקודות תיקון (לחץ Enter):")
        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(-100, 100)
        self.bonus_input.editingFinished.connect(self.apply_bonus)
        bonus_layout.addWidget(bonus_label)
        bonus_layout.addWidget(self.bonus_input)
        main_layout.addLayout(bonus_layout)
        self.update_btn = QPushButton("Update File")
        self.update_btn.clicked.connect(self.update_file)
        main_layout.addWidget(self.update_btn)
        self.setLayout(main_layout)

    def update_table(self):
        """מעדכנת את הטבלה מתוך שלושת הרשימות"""
        self.table.setRowCount(len(self.student_ids))
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def open_file_in_excel(self, filepath):
        """פותחת את הקובץ בתוכנת ברירת המחדל (אקסל) בכל מערכות ההפעלה"""
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":  
            subprocess.call(["open", filepath])
        else:  
            subprocess.call(["xdg-open", filepath])

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "בחר קובץ ציונים", "", "CSV Files (*.csv)")
        if not file_path:
            return
        self.selected_file = file_path
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        with open(self.selected_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            student_id = parts[0]
            grade = int(parts[1])
            self.student_ids.append(student_id)
            self.original_grades.append(grade)
            self.corrected_grades.append(grade)
        self.update_table()

    def apply_bonus(self):
        bonus = self.bonus_input.value()

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade
        self.update_table()

    def update_file(self):
        if self.selected_file == "":
            return
        with open(self.selected_file, "w", encoding="utf-8") as f:
            f.write("ID,Grade\n")
            for i in range(len(self.student_ids)):
                f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")
        self.open_file_in_excel(self.selected_file)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # טעינת קובץ העיצוב QSS
    with open("style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = GradesWindow()
    window.show()
    sys.exit(app.exec())