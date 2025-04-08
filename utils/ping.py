# utils/pings.py
from ping3 import ping
import statistics

def classify_rtt_latency(latency):
    if latency < 1:
        return "LAN or loopback — same machine or local router"
    elif latency < 5:
        return "Local network — same building or direct fiber"
    elif latency < 20:
        return "Nearby region — very low-latency ISP link"
    elif latency < 50:
        return "Fast WAN — CDN, local data center, or strong routing"
    elif latency < 100:
        return "Typical internet — stable ISP-to-ISP connection"
    elif latency < 200:
        return "Remote server — possible transcontinental routing"
    elif latency < 400:
        return "High latency — distant, congested, or routed via relay"
    else:
        return "Unstable or suspicious — VPN, proxy, or degraded network"

def ping_target(host, count=4):
    """
    Pings the given host and returns avg latency, loss %, estimated distance, and a basic label.
    """
    latencies = []

    for _ in range(count):
        try:
            delay = ping(host, timeout=1)
            if delay:
                latencies.append(delay)
        except Exception:
            continue

    received = len(latencies)
    lost = count - received

    if received == 0:
        return f"Ping to {host}: unreachable ({count} packets lost)"

    avg_latency_ms = round(statistics.mean(latencies) * 1000, 2)
    packet_loss = round((lost / count) * 100, 1)

    # Go back to fast, rough RTT-based estimate: 200 km/ms
    estimated_distance_km = round((avg_latency_ms / 2) * 200)
    label = classify_rtt_latency(avg_latency_ms)

    return (
        f"Ping to {host} ({count} packets):\n"
        f"  Avg Latency: {avg_latency_ms} ms\n"
        f"  Packet Loss: {packet_loss}%\n"
        f"  Est. Distance: ~{estimated_distance_km} km (RTT-based)\n"
        f"  Inference: {label}"
    )
