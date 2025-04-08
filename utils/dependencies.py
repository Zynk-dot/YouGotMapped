# utils/dependencies.py
import importlib.util
import subprocess
import sys


def check_dependencies():
    required = {
        "requests": "requests",
        "folium": "folium",
        "ping3": "ping3",
        "python-dotenv": "dotenv"
    }

    print("\nChecking dependencies:\n")

    for package_name, module_name in required.items():
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"   [OK] {package_name} found")
        else:
            print(f"   [MISSING] {package_name} not found")
            choice = input(f"   Install '{package_name}' now? (yes/no): ").strip().lower()
            if choice in ['yes', 'y']:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                    print(f"   '{package_name}' successfully installed\n")
                except subprocess.CalledProcessError:
                    print(f"    Failed to install '{package_name}'. Please install manually.")
                    sys.exit(1)
            else:
                print(f"   Cannot continue without '{package_name}'. Exiting.")
                sys.exit(1)
