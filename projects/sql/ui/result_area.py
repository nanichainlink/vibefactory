from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class ResultArea(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.msg_label = QLabel("")
        self.table = QTableWidget()
        self.layout.addWidget(self.msg_label)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def show_results(self, headers, rows):
        self.msg_label.setText("")
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(headers)
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def show_message(self, msg):
        self.msg_label.setText(msg)
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)