import subprocess
import sys

# A három szkript fájlneve
scripts = ["get_all_data_spar.py", "filter_data_spar.py", "normalize_data_spar.py"]

for script in scripts:
    print(f"Futtatás: {script}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Hiba történt a(z) {script} futtatása közben.")
        break
