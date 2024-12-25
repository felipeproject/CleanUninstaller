import os
import shutil

def clean_files(directory, program_name):
    try:
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                if program_name.lower() in dir_name.lower():
                    dir_path = os.path.join(root, dir_name)
                    shutil.rmtree(dir_path)
                    print(f"Diretório removido: {dir_path}")
    except Exception as e:
        print(f"Erro ao limpar arquivos: {e}")
