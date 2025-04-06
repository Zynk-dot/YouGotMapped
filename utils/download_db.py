import os
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

HF_BASE = "https://huggingface.co/datasets/some1-lonely/data/resolve/main"

FILES = {
    "GeoLite2-City.mmdb": DATA_DIR / "GeoLite2-City.mmdb",
    "GeoLite2-ASN.mmdb": DATA_DIR / "GeoLite2-ASN.mmdb",
    "ip2asn-v4.tsv": DATA_DIR / "ip2asn-v4.tsv"
}

def ensure_data_folder():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, dest_path):
    try:
        print(f" → Downloading {dest_path.name}...")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {dest_path}")
    except Exception as e:
        print(f"Failed to download {dest_path.name}: {e}")
        raise

def check_and_download_files():
    ensure_data_folder()
    print(f"\nChecking geolocation DBs in: {DATA_DIR}")

    for filename, path in FILES.items():
        if not path.exists():
            print(f"   [MISSING] {filename}")
            download_file(f"{HF_BASE}/{filename}", path)
        else:
            print(f"   [OK] {filename} found")

if __name__ == "__main__":
    check_and_download_files()
