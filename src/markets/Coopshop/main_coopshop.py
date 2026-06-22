import subprocess
import sys


scripts = [
    ["get_all_data_coopshop.py"],
    ["filter_data_coopshop.py"],
    ["normalize_data_coopshop.py"],
    ["../download_product_images.py", "--stores", "coopshop"],
]


for script in scripts:
    print(f"\n=== {' '.join(script)} ===", flush=True)
    subprocess.run([sys.executable, *script], check=True)
