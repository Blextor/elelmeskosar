import subprocess
import sys


commands = [
    ["get_all_data_auchan.py", "--allow-partial-download"],
    ["filter_data_auchan.py"],
    ["normalize_data_auchan.py"],
]

for command in commands:
    print(f"Futtatas: {' '.join(command)}")
    result = subprocess.run([sys.executable, *command])
    if result.returncode != 0:
        print(f"Hiba tortent a(z) {' '.join(command)} futtatasa kozben.")
        break
