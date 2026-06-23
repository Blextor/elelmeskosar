import subprocess
import sys


scripts = [
    ["get_all_data_coopshop.py"],
    ["filter_data_coopshop.py"],
    ["normalize_data_coopshop.py"],
    # A coopshop.hu WAF-ja miatt a kepeket is gyengeden (keves szallal + keslektetessel) toltjuk.
    ["../download_product_images.py", "--stores", "coopshop", "--workers", "2", "--delay", "0.25"],
]


for script in scripts:
    print(f"\n=== {' '.join(script)} ===", flush=True)
    subprocess.run([sys.executable, *script], check=True)
