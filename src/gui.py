import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from tabs.installed_programs_tab import InstalledProgramsTab
from tabs.running_programs_tab import RunningProgramsTab
from tabs.custom_uninstall_tab import CustomUninstallTab

def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CleanUninstaller")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Instanciando as abas
        self.programs_tab = InstalledProgramsTab()
        self.running_tab = RunningProgramsTab()
        self.custom_tab = CustomUninstallTab()

        # Adicionando as abas dinamicamente
        self.tabs.addTab(self.programs_tab, "Programas Instalados")
        self.tabs.addTab(self.running_tab, "Programas em Execução")
        self.tabs.addTab(self.custom_tab, "Selecione o Executável")
