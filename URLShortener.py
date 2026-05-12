import sys
import sqlite3
import qrcode
import pyshorteners
from urllib.parse import urlparse

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QFrame)
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt

class ModernUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_database()
        self.initUI()

    def init_database(self):
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ShortUrls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shorturl TEXT NOT NULL,
                originalurl TEXT NOT NULL
            );
        ''')
        self.connection.commit()

    def initUI(self):
        self.setWindowTitle('PyQt6 QR & Link Tool')
        self.setGeometry(100, 100, 500, 700)
        self.setStyleSheet("background-color: #ffffff; color: #333333;")

        layout = QVBoxLayout()
        layout.setSpacing(15)

    
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Írj be egy URL-t vagy szöveget...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
                color: #000000;
                font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #3498db; }
        """)
        layout.addWidget(self.input_field)

      
        button_layout = QVBoxLayout() 
        
        button_style = """
            QPushButton {
                padding: 10px; background-color: #3498db; color: white; 
                border-radius: 5px; font-weight: bold; min-height: 20px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """
        
        self.btn_shorten = QPushButton("Rövid link generálása")
        self.btn_qr = QPushButton("QR kód generálása")
        self.btn_find = QPushButton("Eredeti link visszakeresése")
        
      
        for btn in [self.btn_shorten, self.btn_qr, self.btn_find]:
            btn.setStyleSheet(button_style)
            button_layout.addWidget(btn)
            
        layout.addLayout(button_layout)

       
        result_label = QLabel("Eredmény:")
        result_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        result_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(result_label)

        self.output_area = QFrame()
        self.output_area.setStyleSheet("QFrame { border: 2px dashed #bdc3c7; background-color: #f9f9f9; border-radius: 10px; }")
        self.output_layout = QVBoxLayout()
        
        self.result_text = QLabel("Adj meg egy adatot és válassz műveletet!")
        self.result_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.result_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_text.setWordWrap(True)
        self.result_text.setStyleSheet("color: #000000; padding: 10px;")
        
        self.result_image = QLabel()
        self.result_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.output_layout.addWidget(self.result_text)
        self.output_layout.addWidget(self.result_image)
        self.output_area.setLayout(self.output_layout)
        layout.addWidget(self.output_area)

  
        self.btn_shorten.clicked.connect(self.handle_short_url)
        self.btn_qr.clicked.connect(self.display_image)
        self.btn_find.clicked.connect(self.find_original_url)

        self.setLayout(layout)

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def handle_short_url(self):
        user_input = self.input_field.text().strip()
        self.result_image.clear()
        
        if not user_input:
            self.result_text.setText("Hiba: A mező üres!")
            return

        if self.is_valid_url(user_input):
            try:
                s = pyshorteners.Shortener()
                short_url = s.isgd.short(user_input)
                
                self.cursor.execute("INSERT INTO ShortUrls (shorturl, originalurl) VALUES (?, ?)", 
                                   (short_url, user_input))
                self.connection.commit()
                
                self.result_text.setText(f"Rövid URL:\n{short_url}")
            except Exception as e:
                self.result_text.setText(f"Hiba a rövidítés során: {e}")
        else:
            self.result_text.setText("Hiba: Érvénytelen URL! (Pl: https://google.com)")

    def find_original_url(self):
        short_url = self.input_field.text().strip()
        self.result_image.clear()

        if not short_url:
            self.result_text.setText("Hiba: Másold be a rövid linket a kereséshez!")
            return

        self.cursor.execute("SELECT originalurl FROM ShortUrls WHERE shorturl = ?", (short_url,))
        result = self.cursor.fetchone()

        if result:
            original_url = result[0]
            self.result_text.setText(f"Eredeti link megtalálva:\n{original_url}")
        else:
            self.result_text.setText("Ez a rövid link nem szerepel a helyi adatbázisban.")

    def display_image(self):
        data = self.input_field.text().strip()
        if not data:
            self.result_text.setText("Hiba: Nincs adat a QR kódhoz!")
            self.result_image.clear()
            return

        qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        bytes_data = img.tobytes("raw", "RGB")
        qim = QImage(bytes_data, img.size[0], img.size[1], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qim)

        self.result_image.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        self.result_text.setText("QR kód elkészült!")

    def closeEvent(self, event):
        """Program bezárásakor lezárja az adatbázis kapcsolatot."""
        self.connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModernUI()
    ex.show()
    sys.exit(app.exec())