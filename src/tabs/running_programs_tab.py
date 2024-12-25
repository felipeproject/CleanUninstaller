from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import psutil

class RunningProgramsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Lista de Programas em Execução")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.running_list = QListWidget()
        layout.addWidget(self.running_list)

        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.refresh_running_programs)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def refresh_running_programs(self):
        self.running_list.clear()
        self.thread = RunningProgramsThread()
        self.thread.finished_list.connect(self.update_list)
        self.thread.start()

    def update_list(self, programs):
        self.running_list.addItems(programs)

class RunningProgramsThread(QThread):
    finished_list = pyqtSignal(list)

    def run(self):
        running_programs = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
        self.finished_list.emit(running_programs)
