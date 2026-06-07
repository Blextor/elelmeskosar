import subprocess
import sys


scripts = ["get_all_data_tesco.py", "filter_data_tesco.py", "normalize_data_tesco.py"]

for script in scripts:
    print(f"Futtatas: {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Hiba tortent a(z) {script} futtatasa kozben.")
        break
