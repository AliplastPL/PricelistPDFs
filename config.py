import os
import sys
import base64

def get_config_value(key):
    # 1. Sprawdź zmienną środowiskową
    val = os.environ.get(key)
    if val:
        return val

    # 2. Szukaj pliku config.txt
    if getattr(sys, 'frozen', False):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        exe_dir = os.path.dirname(sys.executable)
        paths_to_check = [
            os.path.join(bundle_dir, "config.txt"),
            os.path.join(exe_dir, "config.txt")
        ]
    else:
        paths_to_check = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")]

    for config_path in paths_to_check:
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding='utf-8') as f:
                    for line in f:
                        if line.startswith(f"{key}="):
                            raw_val = line.split("=", 1)[1].strip()
                            try:
                                return base64.b64decode(raw_val).decode('utf-8')
                            except Exception:
                                return raw_val
            except Exception as e:
                pass

    return None
