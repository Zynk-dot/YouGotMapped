# yougotmapped.py
import os
import sys
import argparse
from utils.dependencies import check_dependencies
from utils.network import get_public_ip, get_geolocation
from utils.mapping import plot_ip_location
from utils.token import get_api_token


def main():
    parser = argparse.ArgumentParser(description="Geolocate an IP or domain and generate an interactive map.")
    parser.add_argument('--ip', type=str, help="Target IP address or domain (leave blank to use your public IP)")
    parser.add_argument('--no-map', action='store_true', help="Do not generate a map")
    parser.add_argument('--delete-map', action='store_true', help="Delete the map after generating")
    args = parser.parse_args()

    check_dependencies()

    API_TOKEN = get_api_token()
    if not API_TOKEN:
        return

    ip_or_domain = args.ip
    if not ip_or_domain:
        print("Using your public IP...")
        ip_or_domain = get_public_ip()
        if not ip_or_domain:
            print("Could not determine your public IP.")
            return

    print(f"Looking up location for {ip_or_domain}...")
    data = get_geolocation(ip_or_domain, API_TOKEN)

    if data:
        print("\nGeolocation Info:")
        for key in ['ip', 'hostname', 'city', 'region', 'country', 'loc', 'org', 'postal', 'timezone']:
            print(f"{key.title()}: {data.get(key, 'N/A')}")

        if not args.no_map:
            plot_ip_location(data)

        if args.delete_map:
            try:
                os.remove('ip_geolocation_map.html')
                print("Deleted the map.")
            except FileNotFoundError:
                print("Map file not found.")
        else:
            print("Map kept as 'ip_geolocation_map.html'.")
    else:
        print("Failed to get location data.")


if __name__ == "__main__":
    main()
