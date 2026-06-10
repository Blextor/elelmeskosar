import subprocess
import sys


scripts = [
    "get_all_data_penny.py",
    "filter_data_penny.py",
    "normalize_data_penny.py",
    "validate_data_penny.py",
]


for script in scripts:
    print(f"\n=== {script} ===", flush=True)
    subprocess.run([sys.executable, script], check=True)
