from __future__ import annotations
import sys
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTextEdit, QPushButton, QLabel, QComboBox, QMessageBox, QListWidget, QSplitter
)
from translator import Translator, TranslationError
from translator.config import get_model
from translator.database import init_db, save_translation, get_history, clear_history

class Worker(QThread):
    finished_text = Signal(str)
    failed = Signal(str)
    progress = Signal(int, int)
    def __init__(self, text, mode):
        super().__init__()
        self.text, self.mode = text, mode
    def run(self):
        try:
            result = Translator().translate(self.text, self.mode, self.progress.emit)
            self.finished_text.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOMO Translator V2")
        self.resize(1050, 720)
        init_db()
        tabs = QTabWidget()
        tabs.addTab(self.translation_tab(), "Dịch thuật")
        tabs.addTab(self.history_tab(), "Lịch sử")
        self.setCentralWidget(tabs)

    def translation_tab(self):
        root = QWidget()
        layout = QVBoxLayout(root)
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Chế độ dịch:"))
        self.mode = QComboBox()
        self.mode.addItem("Anh ↔ Việt (tự nhận diện)", "en_vi")
        self.mode.addItem("Trung → Việt", "zh_vi")
        mode_row.addWidget(self.mode)
        mode_row.addStretch()
        mode_row.addWidget(QLabel(f"Model: {get_model()}"))
        layout.addLayout(mode_row)

        splitter = QSplitter()
        self.source = QTextEdit()
        self.source.setPlaceholderText("Nhập hoặc dán văn bản cần dịch...")
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Bản dịch sẽ xuất hiện ở đây...")
        splitter.addWidget(self.source)
        splitter.addWidget(self.output)
        layout.addWidget(splitter)

        buttons = QHBoxLayout()
        self.translate_btn = QPushButton("Dịch")
        self.translate_btn.clicked.connect(self.start_translation)
        self.copy_btn = QPushButton("Sao chép bản dịch")
        self.copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.output.toPlainText()))
        self.clear_btn = QPushButton("Xóa")
        self.clear_btn.clicked.connect(self.clear_fields)
        buttons.addWidget(self.translate_btn)
        buttons.addWidget(self.copy_btn)
        buttons.addWidget(self.clear_btn)
        layout.addLayout(buttons)
        self.status = QLabel("Sẵn sàng")
        layout.addWidget(self.status)
        return root

    def start_translation(self):
        source = self.source.toPlainText().strip()
        if not source:
            QMessageBox.information(self, "Thiếu nội dung", "Hãy nhập văn bản cần dịch.")
            return
        self.translate_btn.setEnabled(False)
        self.status.setText("Đang dịch...")
        self.output.clear()
        self.worker = Worker(source, self.mode.currentData())
        self.worker.progress.connect(lambda i, n: self.status.setText(f"Đang dịch đoạn {i}/{n}..."))
        self.worker.finished_text.connect(self.on_success)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    def on_success(self, result):
        self.output.setPlainText(result)
        save_translation(self.mode.currentData(), self.source.toPlainText(), result, get_model())
        self.status.setText("Hoàn tất")
        self.translate_btn.setEnabled(True)

    def on_error(self, message):
        self.status.setText("Có lỗi")
        self.translate_btn.setEnabled(True)
        QMessageBox.critical(self, "Lỗi dịch thuật", message)

    def clear_fields(self):
        self.source.clear()
        self.output.clear()
        self.status.setText("Sẵn sàng")

    def history_tab(self):
        root = QWidget()
        layout = QVBoxLayout(root)
        self.history_list = QListWidget()
        refresh = QPushButton("Làm mới")
        refresh.clicked.connect(self.refresh_history)
        clear = QPushButton("Xóa lịch sử")
        clear.clicked.connect(self.delete_history)
        layout.addWidget(self.history_list)
        row = QHBoxLayout()
        row.addWidget(refresh)
        row.addWidget(clear)
        layout.addLayout(row)
        self.refresh_history()
        return root

    def refresh_history(self):
        self.history_list.clear()
        for item in get_history():
            preview = item["source_text"].replace("\\n", " ")[:90]
            self.history_list.addItem(f'{item["created_at"]} | {item["mode"]} | {preview}')

    def delete_history(self):
        answer = QMessageBox.question(self, "Xác nhận", "Xóa toàn bộ lịch sử dịch?")
        if answer == QMessageBox.StandardButton.Yes:
            clear_history()
            self.refresh_history()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
