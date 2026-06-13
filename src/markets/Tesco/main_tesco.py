import subprocess
import sys


commands = [
    ["get_all_data_tesco.py"],
    ["filter_data_tesco.py"],
    ["normalize_data_tesco.py"],
    ["../download_product_images.py", "--stores", "tesco"],
]

for command in commands:
    print(f"Futtatas: {' '.join(command)}")
    result = subprocess.run([sys.executable, *command])
    if result.returncode != 0:
        print(f"Hiba tortent a(z) {' '.join(command)} futtatasa kozben.")
        break
