import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import subprocess
import json
import os
from datetime import datetime

# Configuração do log
logging.basicConfig(filename='app_error.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class InstalledProgramsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Lista de Programas Instalados")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Usando QTableWidget para exibir os programas
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)  # 3 colunas: Nome, Data, Tamanho
        self.table_widget.setHorizontalHeaderLabels(["Nome", "Data", "Tamanho (MB)"])

        # Ajuste automático das colunas com largura mínima e ajustável
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Nome: ocupa o espaço restante
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Data: ajusta conforme o conteúdo
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Tamanho: ajusta conforme o conteúdo

        # Ajuste de espaçamento entre as células
        self.table_widget.setStyleSheet("QTableWidget {border: none; padding: 5px; font-size: 12pt;}")

        # Conecta o clique nas colunas para ordenar
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)
        layout.addWidget(self.table_widget)

        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.refresh_programs)
        layout.addWidget(self.refresh_button)

        self.uninstall_button = QPushButton("Desinstalar Programa Selecionado")
        self.uninstall_button.clicked.connect(self.uninstall_selected_program)
        layout.addWidget(self.uninstall_button)

        self.add_folder_button = QPushButton("Adicionar Pasta de Programas")
        self.add_folder_button.clicked.connect(self.add_program_folder)
        layout.addWidget(self.add_folder_button)

        self.setLayout(layout)

        # Inicializar variáveis
        self.thread = None
        self.sort_column = 0  # Indica a coluna que está sendo usada para ordenação (0: Nome, 1: Data, 2: Tamanho)
        self.sort_order = Qt.AscendingOrder  # Ordem da ordenação

        # Carregar programas e pastas adicionais
        self.load_program_folders()
        self.programs = []
        self.refresh_programs()

    def refresh_programs(self):
        """Atualiza a lista de programas instalados, incluindo pastas adicionais."""
        try:
            if self.thread is not None and self.thread.isRunning():
                self.thread.quit()
                self.thread.wait()

            self.table_widget.setRowCount(0)
            self.label.setText("Carregando lista de programas...")

            self.thread = InstalledProgramsThread()
            self.thread.finished_list.connect(self.update_table)
            self.thread.start()

        except Exception as e:
            logging.error(f"Erro ao tentar atualizar a lista de programas: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao atualizar a lista de programas: {e}")

    def update_table(self, programs):
        """Atualiza a tabela com os programas e dados adicionais."""
        try:
            self.programs = programs
            self.table_widget.setRowCount(len(programs))

            for row, program in enumerate(programs):
                name_item = QTableWidgetItem(program)
                date_item = QTableWidgetItem(str(self.get_program_install_date(program)))
                size_item = QTableWidgetItem(str(self.get_program_size(program) / (1024 * 1024)))  # Convertendo para MB

                self.table_widget.setItem(row, 0, name_item)
                self.table_widget.setItem(row, 1, date_item)
                self.table_widget.setItem(row, 2, size_item)

            self.sort_table(self.sort_column)  # Aplicar ordenação inicial

        except Exception as e:
            logging.error(f"Erro ao tentar atualizar a tabela de programas: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar exibir a tabela de programas: {e}")

    def sort_table(self, column):
        """Ordena a tabela pela coluna selecionada com alternância de ordem."""
        try:
            if column == self.sort_column:
                # Inverte a ordem de ordenação
                self.sort_order = Qt.AscendingOrder if self.sort_order == Qt.DescendingOrder else Qt.DescendingOrder
            else:
                # Se clicar em uma nova coluna, ordena em ordem ascendente
                self.sort_column = column
                self.sort_order = Qt.AscendingOrder

            self.table_widget.sortItems(self.sort_column, self.sort_order)

        except Exception as e:
            logging.error(f"Erro ao tentar ordenar a tabela: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar ordenar a tabela de programas: {e}")

    def get_program_install_date(self, program_name):
        """Obtém a data de instalação de um programa (baseada no arquivo principal)."""
        try:
            program_path = f"C:\\Program Files\\{program_name}\\{program_name}.exe"
            if os.path.exists(program_path):
                timestamp = os.path.getctime(program_path)
                return datetime.fromtimestamp(timestamp).date()
            return None
        except Exception as e:
            logging.error(f"Erro ao tentar obter a data de instalação de '{program_name}': {e}")
            return None

    def get_program_size(self, program_name):
        """Obtém o tamanho do programa (baseado no arquivo principal)."""
        try:
            program_path = f"C:\\Program Files\\{program_name}\\{program_name}.exe"
            if os.path.exists(program_path):
                return os.path.getsize(program_path)
            return 0
        except Exception as e:
            logging.error(f"Erro ao tentar obter o tamanho de '{program_name}': {e}")
            return 0

    def uninstall_selected_program(self):
        """Inicia o processo de desinstalação do programa selecionado."""
        try:
            selected_item = self.table_widget.currentItem()
            if not selected_item:
                QMessageBox.warning(self, "Erro", "Por favor, selecione um programa para desinstalar.")
                return

            program_name = selected_item.text()
            confirm = QMessageBox.question(
                self, "Confirmar Desinstalação", 
                f"Você tem certeza que deseja desinstalar '{program_name}'?", 
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.label.setText(f"Desinstalando '{program_name}'...")
                self.thread = UninstallProgramThread(program_name)
                self.thread.uninstall_status.connect(self.show_uninstall_status)
                self.thread.start()

        except Exception as e:
            logging.error(f"Erro ao tentar desinstalar o programa: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar desinstalar o programa: {e}")

    def show_uninstall_status(self, success, program_name):
        """Exibe o status da desinstalação."""
        try:
            if success:
                QMessageBox.information(self, "Sucesso", f"'{program_name}' foi desinstalado com sucesso!")
                self.refresh_programs()
            else:
                QMessageBox.critical(self, "Erro", f"Erro ao desinstalar '{program_name}'. Verifique se ele ainda está instalado.")
        except Exception as e:
            logging.error(f"Erro ao tentar exibir o status da desinstalação para '{program_name}': {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao exibir o status de desinstalação para '{program_name}': {e}")

    def add_program_folder(self):
        """Abre um diálogo para adicionar uma pasta de programas e salvar no JSON."""
        try:
            folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Programas")
            if folder_path:
                program_folders = self.load_program_folders()
                program_folders.append(folder_path)

                with open("program_folders.json", "w") as file:
                    json.dump(program_folders, file)

                QMessageBox.information(self, "Pasta Adicionada", f"A pasta '{folder_path}' foi adicionada com sucesso!")
                self.refresh_programs()

        except Exception as e:
            logging.error(f"Erro ao adicionar a pasta de programas '{folder_path}': {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao adicionar a pasta de programas: {e}")

    def load_program_folders(self):
        """Carrega as pastas de programas salvas no arquivo JSON."""
        try:
            if os.path.exists("program_folders.json"):
                with open("program_folders.json", "r") as file:
                    return json.load(file)
            return []
        except Exception as e:
            logging.error(f"Erro ao carregar pastas de programas: {e}")
            return []

class InstalledProgramsThread(QThread):
    """Thread para obter programas instalados."""
    finished_list = pyqtSignal(list)

    def run(self):
        """Obtém a lista de programas instalados."""
        try:
            # Usando o WMIC para listar programas
            result = subprocess.run(
                ["wmic", "product", "get", "name"], capture_output=True, text=True, shell=True
            )
            if result.returncode == 0:
                programs = result.stdout.splitlines()[1:]  # Ignora o cabeçalho
                programs = [program.strip() for program in programs if program.strip()]
                self.finished_list.emit(programs)
            else:
                self.finished_list.emit([])
        except Exception as e:
            logging.error(f"Erro ao obter programas instalados: {e}")
            self.finished_list.emit([])


class UninstallProgramThread(QThread):
    """Thread para desinstalar programas."""
    uninstall_status = pyqtSignal(bool, str)

    def __init__(self, program_name):
        super().__init__()
        self.program_name = program_name

    def run(self):
        """Desinstala o programa usando WMIC."""
        try:
            command = f"wmic product where name='{self.program_name}' call uninstall"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if "ReturnValue = 0;" in result.stdout:
                self.uninstall_status.emit(True, self.program_name)
            else:
                self.uninstall_status.emit(False, self.program_name)
        except Exception as e:
            logging.error(f"Erro ao desinstalar '{self.program_name}': {e}")
            self.uninstall_status.emit(False, self.program_name)
