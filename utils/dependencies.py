# utils/dependencies.py
import importlib.util
import subprocess
import sys


def check_dependencies():
    required = ["requests", "ipaddress", "folium"]
    print("\nChecking dependencies:")
    for pkg in required:
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            print(f"   [OK] {pkg} found")
        else:
            print(f"   [MISSING] {pkg} not found")
            choice = input(f"   Install '{pkg}' now? (yes/no): ").strip().lower()
            if choice in ['yes', 'y']:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                    print(f"   '{pkg}' installed")
                except subprocess.CalledProcessError:
                    print(f"   Failed to install '{pkg}'.")
                    sys.exit(1)
            else:
                print(f"   Cannot continue without '{pkg}'. Exiting.")
                sys.exit(1)
