# utils/anonymity.py
import requests
import socket

TOR_EXIT_LIST = "https://check.torproject.org/torbulkexitlist"

VPN_KEYWORDS = [
    "vpn", "m247", "nord", "express", "ovh", "digitalocean", "linode",
    "datacamp", "host", "colo", "server", "vultr", "heficed", "leaseweb"
]


def is_tor_exit_node(ip):
    try:
        response = requests.get(TOR_EXIT_LIST, timeout=5)
        exit_nodes = response.text.strip().splitlines()
        return ip in exit_nodes
    except Exception:
        return False


def detect_anonymity(ip_data):
    org = ip_data.get("org", "").lower()
    hostname = ip_data.get("hostname", "").lower()
    ip = ip_data.get("ip")

    tor = is_tor_exit_node(ip)
    vpn = any(keyword in org or keyword in hostname for keyword in VPN_KEYWORDS)

    result = {
        "ip": ip,
        "tor": tor,
        "vpn": vpn,
        "org": org,
        "hostname": hostname,
    }

    return result


def format_anonymity_result(result):
    ip = result["ip"]
    print(f"IP: {ip}")
    print(f"Org: {result['org'] or 'N/A'}")
    print(f"Hostname: {result['hostname'] or 'N/A'}")
    if result['tor']:
        print("Tor Exit Node: YES")
    else:
        print("Tor Exit Node: No")
    if result['vpn']:
        print("VPN / Proxy Suspected: YES")
    else:
        print("VPN / Proxy Suspected: No")
