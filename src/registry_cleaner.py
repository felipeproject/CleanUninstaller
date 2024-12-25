import winreg

def clean_registry(program_name):
    try:
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        ]

        for path in reg_paths:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    sub_key_name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, sub_key_name)
                    try:
                        if program_name in winreg.QueryValueEx(sub_key, "DisplayName")[0]:
                            winreg.DeleteKey(key, sub_key_name)
                            print(f"Chave do registro removida: {sub_key_name}")
                            break
                    except FileNotFoundError:
                        continue
    except Exception as e:
        print(f"Erro ao limpar registro: {e}")
