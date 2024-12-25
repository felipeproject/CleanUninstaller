import os
import subprocess

def list_installed_programs():
    try:
        result = subprocess.run(["wmic", "product", "get", "name"], capture_output=True, text=True)
        return result.stdout.splitlines()[1:]  # Exclui a primeira linha (cabeçalho)
    except Exception as e:
        return str(e)

def uninstall_program(program_name):
    try:
        command = f"wmic product where name='{program_name}' call uninstall"
        subprocess.run(command, shell=True, check=True)
        return True
    except Exception as e:
        return str(e)
