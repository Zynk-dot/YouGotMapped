# yougotmapped.py
import os
import sys
import argparse
import ipaddress
from utils.dependencies import check_dependencies
from utils.network import get_public_ip, get_geolocation, resolve_domain_to_ip
from utils.mapping import plot_ip_location, plot_multiple_ip_locations
from utils.token import get_api_token
from utils.ping import ping_target
from utils.trace import run_traceroute


def main():
    parser = argparse.ArgumentParser(description="Geolocate one or more IPs/domains and generate an interactive map.")
    parser.add_argument('--ip', nargs='*', help="One or more IPs/domains separated by space")
    parser.add_argument('--file', type=str, help="Path to a file containing IPs/domains (one per line)")
    parser.add_argument('--ping', action='store_true', help="Ping each IP or domain and show latency")
    parser.add_argument('--trace', action='store_true', help="Show traceroute to each IP or domain")
    parser.add_argument('--no-map', action='store_true', help="Do not generate a map")
    parser.add_argument('--delete-map', action='store_true', help="Delete the map after generating")
    args = parser.parse_args()

    check_dependencies()

    API_TOKEN = get_api_token()
    if not API_TOKEN:
        return

    targets = []

    if args.ip:
        targets.extend(args.ip)

    if args.file:
        try:
            with open(args.file, 'r') as f:
                targets.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"File not found: {args.file}")
            return

    if not targets:
        print("No IP or file input provided. Defaulting to public IP lookup.")
        ip_or_domain = get_public_ip()
        if not ip_or_domain:
            print("Could not determine your public IP.")
            return
        targets = [ip_or_domain]

    geolocated = []

    for target in targets:
        try:
            ipaddress.ip_address(target)
            ip_or_domain = target
        except ValueError:
            resolved_ip = resolve_domain_to_ip(target)
            if resolved_ip:
                ip_or_domain = resolved_ip
            else:
                print(f"Skipping unresolved domain: {target}")
                continue

        print(f"Looking up location for {target}...")
        data = get_geolocation(ip_or_domain, API_TOKEN)
        if data:
            geolocated.append(data)
            print("---")
            for key in ['ip', 'hostname', 'city', 'region', 'country', 'loc', 'org', 'postal', 'timezone']:
                print(f"{key.title()}: {data.get(key, 'N/A')}")

            if args.ping:
                print("\n[ PING RESULT ]")
                print(ping_target(target))

            if args.trace:
                print("\n[ TRACEROUTE RESULT ]")
                trace_output = run_traceroute(target)
                print(trace_output)

            print("---")
        else:
            print(f"Failed to get location data for {target}.")

    if not args.no_map:
        if len(geolocated) == 1:
            m = plot_ip_location(geolocated[0], color="red")

            if args.trace and isinstance(trace_output, str):
                lines = trace_output.strip().split("\n")
                for line in reversed(lines):
                    if "(" in line and ")" in line:
                        last_ip = line.split()[1]
                        try:
                            ipaddress.ip_address(last_ip)
                            last_data = get_geolocation(last_ip, API_TOKEN)
                            if last_data:
                                plot_ip_location(last_data, color="blue", map_object=m)
                        except Exception:
                            pass
                        break
            if m:
                m.save('ip_geolocation_map.html')
                print("Map saved as 'ip_geolocation_map.html'")

        elif len(geolocated) > 1:
            plot_multiple_ip_locations(geolocated)

    if args.delete_map:
        try:
            os.remove('ip_geolocation_map.html')
            print("Deleted the map.")
        except FileNotFoundError:
            print("Map file not found.")
    elif geolocated:
        print("Map kept as 'ip_geolocation_map.html'.")


if __name__ == "__main__":
    main()