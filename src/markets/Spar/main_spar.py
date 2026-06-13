import subprocess
import sys

# A futtatandó szkriptek
scripts = [
    ["get_all_data_spar.py"],
    ["filter_data_spar.py"],
    ["normalize_data_spar.py"],
    ["../download_product_images.py", "--stores", "spar"],
]

for script in scripts:
    print(f"Futtatás: {' '.join(script)}")
    result = subprocess.run([sys.executable, *script])
    if result.returncode != 0:
        print(f"Hiba történt a(z) {' '.join(script)} futtatása közben.")
        break
