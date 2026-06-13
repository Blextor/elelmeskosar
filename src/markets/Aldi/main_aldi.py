import subprocess
import sys


scripts = [
    ["get_all_data_aldi.py"],
    ["filter_data_aldi.py"],
    ["normalize_data_aldi.py"],
    ["validate_data_aldi.py"],
    ["../download_product_images.py", "--stores", "aldi"],
]


for script in scripts:
    print(f"\n=== {' '.join(script)} ===", flush=True)
    subprocess.run([sys.executable, *script], check=True)
