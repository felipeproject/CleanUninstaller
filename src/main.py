# src/main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import launch_gui

def main():
    # Inicializar o QApplication
    app = QApplication(sys.argv)
    
    try:
        # Lançar a interface gráfica
        launch_gui()
    except Exception as e:
        print(f"Erro ao iniciar a interface gráfica: {e}")
        sys.exit(1)  # Saída com erro, caso haja algum problema durante a execução.
    
    # Iniciar o loop de eventos do Qt
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
