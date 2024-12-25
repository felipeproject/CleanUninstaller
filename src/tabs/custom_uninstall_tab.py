from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import Qt

class CustomUninstallTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Selecione um Executável para Desinstalação")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.file_button = QPushButton("Selecionar Executável")
        self.file_button.clicked.connect(self.select_executable)
        layout.addWidget(self.file_button)

        self.file_label = QLabel("Nenhum arquivo selecionado")
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        self.setLayout(layout)

    def select_executable(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Executável", "", "Executáveis (*.exe)")
        if file_path:
            self.file_label.setText(f"Selecionado: {file_path}")
        else:
            self.file_label.setText("Nenhum arquivo selecionado")
