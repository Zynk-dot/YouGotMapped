# utils/trace.py
import subprocess
import platform
import re
import ipaddress
from utils.network import get_geolocation

def run_traceroute(host, max_hops=30, timeout=60):
    system = platform.system()
    if system == "Windows":
        cmd = ["tracert", "-h", str(max_hops), host]
    elif system in ["Linux", "Darwin"]:
        cmd = ["traceroute", "-m", str(max_hops), "-w", "1", host]
    else:
        return f"Traceroute not supported on {system}"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return format_trace_output(result.stdout)
    except subprocess.TimeoutExpired:
        return f"Traceroute to {host} timed out after {timeout} seconds."
    except FileNotFoundError:
        return f"Traceroute command not found on this system."
    except Exception as e:
        return f"Traceroute failed: {e}"


def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False


def extract_ip_latency(line):
    ip_match = re.findall(r"(\d+\.\d+\.\d+\.\d+)", line)
    rtt_match = re.findall(r"(\d+\.\d+) ms", line)
    return ip_match[0] if ip_match else None, rtt_match[0] if rtt_match else None


def format_trace_output(raw_output):
    lines = raw_output.strip().split("\n")
    formatted_lines = []
    last_ip = None

    for index, line in enumerate(lines):
        ip, rtt = extract_ip_latency(line)
        if not ip:
            continue

        label = "(Private)" if is_private_ip(ip) else extract_label(line)
        formatted_lines.append(f"[{index+1}] {ip.ljust(18)} {label.ljust(30)} {rtt} ms")
        last_ip = ip

    # Append final geolocation if last IP is public
    if last_ip and not is_private_ip(last_ip):
        data = get_geolocation(last_ip, None)
        if data:
            geo_info = f"  --> {data.get('city', 'N/A')}, {data.get('region', '')} ({data.get('org', 'N/A')})"
            formatted_lines.append(geo_info)

    return "\n".join(formatted_lines)


def extract_label(line):
    parts = line.split()
    for part in parts:
        if any(ext in part for ext in [".com", ".net", ".org"]):
            return f"({part})"
    return "(Public)"
