from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("אודות")
        self.resize(300, 400)
        layout = QVBoxLayout()
        self.image_label = QLabel()
        pixmap = QPixmap("my_pic.jpg") 
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)     
        self.name_label = QLabel("מפתח: ערן וטר")
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)
        self.email_label = QLabel("אימייל: eranv@example.com")
        self.email_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.email_label)
        self.linkedin_label = QLabel('<a href="https://linkedin.com">לעמוד ה-LinkedIn שלי</a>')
        self.linkedin_label.setAlignment(Qt.AlignCenter)
        self.linkedin_label.setOpenExternalLinks(True) 
        layout.addWidget(self.linkedin_label)   
        github_label = QLabel('<a href="https://github.com/eranvatter12381/HW4-GRADES">למאגר הקוד ב-GitHub</a>')
        github_label.setOpenExternalLinks(True)
        layout.addWidget(github_label)  
        github_label.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)