import os
import sys
import argparse
import ipaddress
from datetime import datetime
from pathlib import Path

from utils.dependencies import check_dependencies
from utils.network import get_public_ip, get_geolocation, resolve_domain_to_ip
from utils.mapping import plot_ip_location, plot_multiple_ip_locations
from utils.token import get_api_token
from utils.ping import ping_target
from utils.trace import run_traceroute
from utils.anonymity import detect_anonymity, format_anonymity_result
from utils.output import write_formatted_output


def main():
    parser = argparse.ArgumentParser(description="Geolocate one or more IPs/domains and generate an interactive map.")
    parser.add_argument('-i', '--ip', nargs='*', help="One or more IPs/domains separated by space")
    parser.add_argument('-f', '--file', type=str, help="Path to a file containing IPs/domains (one per line)")
    parser.add_argument('-p', '--ping', action='store_true', help="Ping each IP or domain and show latency")
    parser.add_argument('-t', '--trace', action='store_true', help="Show traceroute to each IP or domain")
    parser.add_argument('-c', '--hidecheck', action='store_true', help="Check if the IP is a Tor exit node or VPN")
    parser.add_argument('-o', '--output', type=str, help="Specify output file or use format shorthand (e.g., f:csv, f:json, f:normal)")
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
    full_results = [] 

    for target in targets:
        target_result = {}
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
            target_result.update(data)
            print("---")
            for key in ['ip', 'hostname', 'city', 'region', 'country', 'loc', 'org', 'postal', 'timezone']:
                print(f"{key.title()}: {data.get(key, 'N/A')}")

            if args.ping:
                print("\n[ PING RESULT ]")
                ping_result = ping_target(target)
                print(ping_result)
                target_result["ping"] = ping_result

            if args.trace:
                print("\n[ TRACEROUTE RESULT ]")
                trace_output = run_traceroute(target)
                print(trace_output)
                target_result["traceroute"] = trace_output
            
            if args.hidecheck:
                print("\n[ ANONYMITY CHECK ]")
                anonymity = detect_anonymity(data)
                format_anonymity_result(anonymity)
                target_result["anonymity"] = anonymity

            print("---")
            full_results.append(target_result)
        else:
            print(f"Failed to get location data for {target}.")

    # --- Output & Summary ---
    map_saved = False
    map_path = Path("ip_geolocation_map.html").resolve()
    log_path = None

    if not args.no_map and geolocated:
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
                m.save(str(map_path))
                map_saved = True

        elif len(geolocated) > 1:
            plot_multiple_ip_locations(geolocated)
            map_saved = True

    if args.delete_map:
        try:
            os.remove(map_path)
            map_saved = False
        except FileNotFoundError:
            pass

    if args.output:
        os.makedirs("logs", exist_ok=True)
        now = datetime.now()
        date_str = now.strftime("%m-%d-%y")
        time_str = now.strftime("%H-%M")

        if args.output.startswith("f:"):
            fmt_type = args.output[2:].lower()
            ext = {"json": "json", "csv": "csv"}.get(fmt_type, "txt")
            target_name = targets[0].replace(":", "-").replace("/", "-")
            filename = f"{target_name}--{date_str}--{time_str}--YouGotMapped.{ext}"
        else:
            filename = args.output
            fmt_type = filename.split('.')[-1].lower()
            if fmt_type not in ["json", "csv", "txt"]:
                fmt_type = "normal"

        log_path = Path("logs") / filename
        write_formatted_output(full_results, str(log_path), fmt_type=fmt_type)
        log_path = log_path.resolve()

    # Final summary
    if map_saved or log_path:
        print("\n----- OUTPUT SUMMARY -----")
        if map_saved:
            print(f"Map Location: {map_path}")
            print(f"Map URL: file://{map_path}")
        if log_path:
            print(f"Log File: {log_path}")
            print(f"Log URL: file://{log_path}")


if __name__ == "__main__":
    main()
