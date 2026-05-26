import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QMessageBox
)

from PyQt5.QtCore import Qt

API = "http://127.0.0.1:8000"

class CurrencyConverter(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Currency Converter")
        self.setFixedSize(600, 600)

        self.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            color: #e2e8f0;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QLabel {
            color: #f8fafc;
            font-size: 14px;
        }

        QLineEdit, QComboBox {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 14px;
            padding: 12px;
            color: white;
            font-size: 14px;
        }

        QLineEdit:focus, QComboBox:focus {
            border: 2px solid #38bdf8;
        }

        QComboBox::drop-down {
            border: none;
        }

        QComboBox QAbstractItemView {
            background-color: #1e293b;
            border: 1px solid #334155;
            selection-background-color: #38bdf8;
            color: white;
        }

        QPushButton {
            background-color: #06b6d4;
            color: white;
            border: none;
            border-radius: 14px;
            padding: 14px;
            font-size: 15px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0891b2;
        }

        QPushButton:pressed {
            background-color: #0e7490;
        }

        QLabel#result {
            background-color: #111827;
            border: 2px solid #334155;
            border-radius: 18px;
            padding: 18px;
            font-size: 20px;
            font-weight: bold;
            color: #22c55e;
        }
    """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("Конвертер валют")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
        """)

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Введите сумму")

        self.from_cur = QComboBox()
        self.to_cur = QComboBox()

        self.result = QLabel("Результат: ---")
        self.result.setObjectName("result")
        self.result.setAlignment(Qt.AlignCenter)

        convert_btn = QPushButton("Конвертировать")
        convert_btn.clicked.connect(self.convert_currency)

        layout.addWidget(title)

        layout.addWidget(QLabel("Сумма"))
        layout.addWidget(self.amount)

        layout.addWidget(QLabel("Из валюты"))
        layout.addWidget(self.from_cur)

        layout.addWidget(QLabel("В валюту"))
        layout.addWidget(self.to_cur)

        layout.addWidget(convert_btn)
        layout.addWidget(self.result)

        self.setLayout(layout)

        self.load_currencies()

    def load_currencies(self):

        try:
            r = requests.get(f"{API}/currencies")

            currencies = r.json()

            self.from_cur.addItems(currencies)
            self.to_cur.addItems(currencies)

            self.from_cur.setCurrentText("USD")
            self.to_cur.setCurrentText("EUR")

        except:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Сервер не запущен"
            )

    def convert_currency(self):

        try:
            amount = float(self.amount.text())

        except:
            self.result.setText("Введите число")
            return

        data = {
            "from_cur": self.from_cur.currentText(),
            "to_cur": self.to_cur.currentText(),
            "amount": amount
        }

        try:
            r = requests.post(
                f"{API}/convert",
                json=data
            )

            if r.status_code != 200:
                self.result.setText(
                    f"{r.json()['detail']}"
                )
                return

            result = r.json()

            self.result.setText(
                f"{result['amount']} {result['from']} = "
                f"{result['result']} {result['to']}"
            )

        except:
            self.result.setText("Ошибка подключения")

app = QApplication(sys.argv)

window = CurrencyConverter()
window.show()

sys.exit(app.exec_())





