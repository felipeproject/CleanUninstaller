import logging
import os
import subprocess
import winreg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
from datetime import datetime

# Configuração do log
logging.basicConfig(filename='app_error.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def listar_programas_instalados():
    """
    Retorna uma lista de programas instalados no Windows, retirando duplicatas e 
    ordenando-os em ordem alfabética.
    """
    chaves = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",  # Programas 64-bit
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",  # Programas 32-bit em sistemas 64-bit
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",  # Programas do usuário atual
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"  # Programas 32-bit para o usuário atual
    ]
    
    programas = set()  # Usar um conjunto para eliminar duplicados

    for chave in chaves:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, chave)
        except Exception as e:
            print(f"Erro ao acessar o registro em {chave}: {e}")
            continue

        for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
            try:
                sub_key_name = winreg.EnumKey(reg_key, i)
                sub_key = winreg.OpenKey(reg_key, sub_key_name)

                try:
                    nome_programa = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                    programas.add(nome_programa)
                except FileNotFoundError:
                    continue

            except Exception as e:
                continue

    programas = sorted(list(programas))
    return programas

class InstalledProgramsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Lista de Programas Instalados")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Selecionar", "Nome"])

        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.table_widget.setStyleSheet("QTableWidget {border: none; padding: 5px; font-size: 12pt;}")

        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.table_widget.setEditTriggers(self.table_widget.NoEditTriggers)
        
        layout.addWidget(self.table_widget)

        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.refresh_programs)
        layout.addWidget(self.refresh_button)

        self.uninstall_button = QPushButton("Desinstalar Programa Selecionado")
        self.uninstall_button.setEnabled(False)
        self.uninstall_button.clicked.connect(self.uninstall_selected_program)
        layout.addWidget(self.uninstall_button)

        self.uninstall_mass_button = QPushButton("Desinstalar Selecionados")
        self.uninstall_mass_button.setEnabled(False)
        self.uninstall_mass_button.clicked.connect(self.uninstall_mass_programs)
        layout.addWidget(self.uninstall_mass_button)

        self.setLayout(layout)

        self.thread = None
        self.sort_column = 1
        self.sort_order = Qt.AscendingOrder

        self.refresh_programs()

    def refresh_programs(self):
        """Atualiza a lista de programas instalados."""
        try:
            self.table_widget.setRowCount(0)
            self.label.setText("Carregando lista de programas...")

            programs = listar_programas_instalados()

            self.programs = programs
            self.table_widget.setRowCount(len(programs))

            for row, program in enumerate(programs):
                select_checkbox = QCheckBox()
                select_checkbox.stateChanged.connect(self.update_buttons_state)
                self.table_widget.setCellWidget(row, 0, select_checkbox)

                name_item = QTableWidgetItem(program)
                self.table_widget.setItem(row, 1, name_item)

            self.sort_table(self.sort_column)

        except Exception as e:
            logging.error(f"Erro ao tentar atualizar a lista de programas: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao atualizar a lista de programas: {e}")

    def sort_table(self, column):
        """Ordena a tabela pela coluna selecionada com alternância de ordem."""
        try:
            if column == self.sort_column:
                self.sort_order = Qt.AscendingOrder if self.sort_order == Qt.DescendingOrder else Qt.DescendingOrder
            else:
                self.sort_column = column
                self.sort_order = Qt.AscendingOrder

            self.table_widget.sortItems(self.sort_column, self.sort_order)

        except Exception as e:
            logging.error(f"Erro ao tentar ordenar a tabela: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar ordenar a tabela de programas: {e}")

    def update_buttons_state(self):
        """Atualiza o estado dos botões conforme a seleção de programas."""
        selected_count = 0
        for row in range(self.table_widget.rowCount()):
            checkbox = self.table_widget.cellWidget(row, 0)
            if checkbox.isChecked():
                selected_count += 1

        if selected_count == 0:
            self.uninstall_button.setEnabled(False)
            self.uninstall_mass_button.setEnabled(False)
        elif selected_count == 1:
            self.uninstall_button.setEnabled(True)
            self.uninstall_mass_button.setEnabled(False)
        else:
            self.uninstall_button.setEnabled(False)
            self.uninstall_mass_button.setEnabled(True)

    def uninstall_selected_program(self):
        """Inicia o processo de desinstalação do programa selecionado."""
        try:
            selected_program = None
            for row in range(self.table_widget.rowCount()):
                checkbox = self.table_widget.cellWidget(row, 0)
                if checkbox.isChecked():
                    selected_program = self.table_widget.item(row, 1).text()
                    break

            if not selected_program:
                QMessageBox.warning(self, "Erro", "Por favor, selecione um programa para desinstalar.")
                return

            self.label.setText(f"Iniciando desinstalação de '{selected_program}'...")
            logging.info(f"Iniciando desinstalação de '{selected_program}'...")

            self.uninstall_program(selected_program)

        except Exception as e:
            logging.error(f"Erro ao tentar desinstalar o programa: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar desinstalar o programa: {e}")

    def uninstall_mass_programs(self):
        """Inicia o processo de desinstalação de múltiplos programas selecionados."""
        try:
            selected_programs = []
            for row in range(self.table_widget.rowCount()):
                checkbox = self.table_widget.cellWidget(row, 0)
                if checkbox.isChecked():
                    program_name = self.table_widget.item(row, 1).text()
                    selected_programs.append(program_name)

            if not selected_programs:
                QMessageBox.warning(self, "Erro", "Por favor, selecione ao menos um programa para desinstalar.")
                return

            self.label.setText(f"Iniciando desinstalação de {len(selected_programs)} programas...")
            logging.info(f"Iniciando desinstalação de {len(selected_programs)} programas...")

            for program_name in selected_programs:
                self.uninstall_program(program_name)

        except Exception as e:
            logging.error(f"Erro ao tentar desinstalar os programas: {e}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar desinstalar os programas: {e}")

    def uninstall_program(self, program_name):
        """Desinstala um programa usando o caminho do desinstalador ou WMIC."""
        try:
            uninstall_path = self.get_uninstall_path(program_name)
            if uninstall_path:
                logging.info(f"Tentando desinstalar '{program_name}'...")
                self.label.setText(f"Tentando desinstalar '{program_name}'...")
                logging.info(f"Executando: {uninstall_path}")
                result = subprocess.run(uninstall_path, capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    logging.info(f"Desinstalação de '{program_name}' realizada com sucesso.")
                    self.label.setText(f"Desinstalação de '{program_name}' realizada com sucesso.")
                    QMessageBox.information(self, "Sucesso", f"'{program_name}' foi desinstalado com sucesso!")
                else:
                    logging.error(f"Falha ao desinstalar '{program_name}'.")
                    self.label.setText(f"Falha ao desinstalar '{program_name}'.")
                    QMessageBox.critical(self, "Erro", f"Falha ao desinstalar '{program_name}'.")
            else:
                logging.error(f"Não foi possível encontrar o caminho de desinstalação para '{program_name}'.")
                self.label.setText(f"Não foi possível encontrar o caminho de desinstalação para '{program_name}'.")
                QMessageBox.critical(self, "Erro", f"Não foi possível encontrar o caminho de desinstalação para '{program_name}'.")

        except Exception as e:
            logging.error(f"Erro ao tentar desinstalar o programa '{program_name}': {e}")
            self.label.setText(f"Erro ao tentar desinstalar '{program_name}'.")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao tentar desinstalar '{program_name}': {e}")

    def get_uninstall_path(self, program_name):
        """Obtém o caminho do desinstalador de um programa a partir do registro do Windows."""
        try:
            for chave in [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, chave)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        if display_name == program_name:
                            uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                            return uninstall_string
                    except FileNotFoundError:
                        continue

        except Exception as e:
            logging.error(f"Erro ao tentar acessar o caminho de desinstalação: {e}")

        return None
