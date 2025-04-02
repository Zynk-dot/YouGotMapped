import requests
import ipaddress
import folium
import os
import sys
import importlib.util


def check_dependencies():
    required = ["requests", "ipaddress", "folium"]
    print("\n\u2705 Checking dependencies:")
    for pkg in required:
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            print(f"   \u2611 {pkg} found — nice!")
        else:
            print(f"   \u2612 {pkg} MISSING! Please install it (pip install {pkg})")
            print("\n\u26A0 Script cannot run until missing packages are installed.")
            sys.exit(1)


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"\u26A0 Error fetching public IP: {e}")
        return None


def get_geolocation(ip_or_domain, api_token):
    url = f"https://ipinfo.io/{ip_or_domain}/json"
    params = {'token': api_token} if api_token else {}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\U0001F4E1 Error fetching geolocation data: {e}")
        return None


def plot_ip_location(ip_data):
    if 'loc' not in ip_data:
        print("\U0001F9ED Location data not available. Are we mapping ghosts now?")
        return

    latitude, longitude = map(float, ip_data['loc'].split(','))
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker(
        [latitude, longitude],
        popup=f"IP: {ip_data.get('ip', 'N/A')}\nCity: {ip_data.get('city', 'N/A')}\nRegion: {ip_data.get('region', 'N/A')}\nCountry: {ip_data.get('country', 'N/A')}"
    ).add_to(m)

    folium.Circle(
        radius=10000,
        location=[latitude, longitude],
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.2,
        popup="\U0001F5FA\uFE0F Approximate Area — definitely somewhere on Earth."
    ).add_to(m)

    m.save('ip_geolocation_map.html')
    print("\U0001F4CD Map has been saved as 'ip_geolocation_map.html'. Treasure hunt begins.")


def main():
    check_dependencies()
    # Psst... you’ll need an API token to unlock internet secrets (free, promise!): https://ipinfo.io/signup
    API_TOKEN = '<your_token_here>'

    ip_or_domain = input("\U0001F50E Enter an IP address or domain (leave blank to use your public IP): ").strip()

    if not ip_or_domain:
        print("\U0001F6F0\uFE0F Using your public IP... brace for exposure.")
        ip_or_domain = get_public_ip()
        if not ip_or_domain:
            print("\u274C Could not determine your public IP. Wi-Fi goblins strike again.")
            return
    else:
        try:
            ip_obj = ipaddress.ip_address(ip_or_domain)
            if ip_obj.is_private:
                print("\U0001F512 Private IP addresses are not for public adventures. Try a public one!")
                return
        except ValueError:
            pass  # Treat as domain name

    print(f"\U0001F310 Fetching geolocation data for {ip_or_domain}... fingers crossed")
    data = get_geolocation(ip_or_domain, API_TOKEN)

    if data:
        print("\n\U0001F4CC Geolocation Info:")
        print(f"IP Address: {data.get('ip', 'N/A')} — ✈️ Incoming signal!")
        print(f"Hostname: {data.get('hostname', 'N/A')} — \U0001F3E0 Probably lives here")
        print(f"City: {data.get('city', 'N/A')} — \U0001F306 Urban legend?")
        print(f"Region: {data.get('region', 'N/A')} — \U0001F5FA Somewhere in the wild")
        print(f"Country: {data.get('country', 'N/A')} — \U0001F1FA\U0001F1F8 Passport required")
        print(f"Location: {data.get('loc', 'N/A')} — \U0001F30D Pinned on Earth")
        print(f"Organization: {data.get('org', 'N/A')} — \U0001F4BC Powered by suits")
        print(f"Postal Code: {data.get('postal', 'N/A')} — \U0001F4EC Just mail it")
        print(f"Timezone: {data.get('timezone', 'N/A')} — ⏰ Time travelers, take note")

        plot_ip_location(data)

        delete_choice = input("\U0001F5D1\uFE0F Delete the generated map? (yes/no): ").strip().lower()
        if delete_choice == 'yes':
            try:
                os.remove('ip_geolocation_map.html')
                print("\U0001F9F9 Map file deleted. Like it never happened.")
            except FileNotFoundError:
                print("\U0001F4C1 Map file not found. Magic?")
        else:
            print("\U0001F4C2 Map has been kept. Share it, frame it, name it.")
    else:
        print("\u274C Failed to retrieve geolocation data. Maybe try bribing the internet gods.")


if __name__ == "__main__":
    main()