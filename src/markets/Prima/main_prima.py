import subprocess
import sys

# A három szkript fájlneve
scripts = ["get_all_data_prima.py", "filter_data_prima.py", "normalize_data_prima.py"]

for script in scripts:
    print(f"Futtatás: {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Hiba történt a(z) {script} futtatása közben.")
        break
