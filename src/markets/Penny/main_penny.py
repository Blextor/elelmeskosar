import subprocess
import sys


scripts = [
    ["get_all_data_penny.py"],
    ["filter_data_penny.py"],
    ["normalize_data_penny.py"],
    ["validate_data_penny.py"],
    ["../download_product_images.py", "--stores", "penny"],
]


for script in scripts:
    print(f"\n=== {' '.join(script)} ===", flush=True)
    subprocess.run([sys.executable, *script], check=True)
