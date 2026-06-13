import subprocess
import sys


commands = [
    ["get_all_data_metro.py", "--allow-partial-download"],
    ["filter_data_metro.py"],
    ["normalize_data_metro.py"],
    ["../download_product_images.py", "--stores", "metro"],
]

for command in commands:
    print(f"Futtatas: {' '.join(command)}")
    result = subprocess.run([sys.executable, *command])
    if result.returncode != 0:
        print(f"Hiba tortent a(z) {' '.join(command)} futtatasa kozben.")
        break
