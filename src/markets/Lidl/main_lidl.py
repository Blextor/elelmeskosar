import subprocess
import sys


scripts = [
    "get_all_data_lidl.py",
    "filter_data_lidl.py",
    "normalize_data_lidl.py",
]


for script in scripts:
    print(f"\n=== {script} ===", flush=True)
    subprocess.run([sys.executable, script], check=True)
