import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QLabel, QHBoxLayout, QMessageBox, QDialog, QHeaderView
)
from PyQt5.QtCore import Qt


# File to store the data
CSV_FILE = "accountBook.csv"

class AccountManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 600, 400)

        # Main Layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Table for displaying credentials
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Website", "Username", "Password"])
        self.layout.addWidget(self.table)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Buttons for actions
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.layout.addLayout(self.button_layout)

        # Connect buttons to actions
        self.add_button.clicked.connect(self.add_entry)
        self.edit_button.clicked.connect(self.edit_entry)
        self.delete_button.clicked.connect(self.delete_entry)

        # Load data from CSV
        self.load_data()

    def load_data(self):
        """Load credentials from the CSV file into the table."""
        self.table.setRowCount(0)  # Clear table
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                rows.sort(key=lambda x: x[0])
                for row in rows:
                    self.add_table_row(row)
        except FileNotFoundError:
            pass  # If the file doesn't exist, do nothing

    def save_data(self):
        """Save credentials from the table to the CSV file."""
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in range(self.table.rowCount()):
                data = [
                    self.table.item(row, col).text()
                    for col in range(self.table.columnCount())
                ]
                writer.writerow(data)

    def add_table_row(self, row_data):
        """Add a row to the table."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for col, data in enumerate(row_data):
            self.table.setItem(row_position, col, QTableWidgetItem(data))

    def add_entry(self):
        """Add a new credential entry."""
        website, username, password = self.get_input_dialog()
        if website and username and password:
            self.add_table_row([website, username, password])
            self.save_data()

    def edit_entry(self):
        """Edit the selected credential."""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select an entry to edit.")
            return
        current_data = [
            self.table.item(selected, col).text() if self.table.item(selected, col) else ""
            for col in range(self.table.columnCount())
        ]
        website, username, password = self.get_input_dialog(*current_data)
        if website and username and password:
            for col, data in enumerate([website, username, password]):
                self.table.setItem(selected, col, QTableWidgetItem(data))
            self.save_data()

    def delete_entry(self):
        """Delete the selected credential."""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "No Selection", "Please select an entry to delete.")
            return
        self.table.removeRow(selected)
        self.save_data()

    def get_input_dialog(self, website="", username="", password=""):
        """Show an input dialog to get credential data."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Input Credential")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Website:"))
        website_input = QLineEdit(website)
        layout.addWidget(website_input)

        layout.addWidget(QLabel("Username:"))
        username_input = QLineEdit(username)
        layout.addWidget(username_input)

        layout.addWidget(QLabel("Password:"))
        password_input = QLineEdit(password)
        layout.addWidget(password_input)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        def accept():
            dialog.accept()

        def reject():
            dialog.reject()

        ok_button.clicked.connect(accept)
        cancel_button.clicked.connect(reject)

        # Show the dialog and return values if accepted
        if dialog.exec() == QDialog.Accepted:
            return website_input.text(), username_input.text(), password_input.text()
        return "", "", ""

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = AccountManager()
    manager.show()
    sys.exit(app.exec_())
