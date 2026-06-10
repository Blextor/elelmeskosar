import subprocess
import sys


scripts = [
    "get_all_data_coop.py",
    "filter_data_coop.py",
    "normalize_data_coop.py",
]


for script in scripts:
    print(f"\n=== {script} ===", flush=True)
    subprocess.run([sys.executable, script], check=True)
