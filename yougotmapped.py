import requests
import ipaddress
import folium
import os
import sys
import importlib.util
import subprocess


def check_dependencies():
    required = ["requests", "ipaddress", "folium"]
    print("\n\u2705 Checking dependencies like a pro installer:")
    for pkg in required:
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            print(f"   \u2611 {pkg} found — solid!")
        else:
            print(f"   \u2612 {pkg} MISSING! Uh oh.")
            choice = input(f"   \U0001F4A1 Wanna install '{pkg}' now? (yes/no): ").strip().lower()
            if choice in ['yes', 'y']:
                print(f"   \U0001F6E0 Installing '{pkg}'... brace yourself.")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                    print(f"   \u2705 '{pkg}' installed like a charm!")
                except subprocess.CalledProcessError:
                    print(f"   \u274C Failed to install '{pkg}'. Manual install might be needed. Sorry!")
                    sys.exit(1)
            else:
                print(f"   \u26a0 Can't proceed without '{pkg}'. Exiting gracefully like a polite script.")
                sys.exit(1)


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"\u26a0 Error fetching public IP (the internet ghosted you): {e}")
        return None


def get_geolocation(ip_or_domain, api_token):
    url = f"https://ipinfo.io/{ip_or_domain}/json"
    params = {'token': api_token} if api_token else {}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\U0001F4E1 Error fetching geolocation data (coordinates lost in space): {e}")
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
        popup="\U0001F5FA\ufe0f Approximate Area — definitely somewhere on Earth."
    ).add_to(m)

    m.save('ip_geolocation_map.html')
    print("\U0001F4CD Map saved as 'ip_geolocation_map.html'. It's like Google Maps, but you made it.")


def main():
    check_dependencies()
    API_TOKEN = os.environ.get("IPINFO_TOKEN")  # Psst... you’ll need a (totally free) API token to unlock internet secrets: https://ipinfo.io/signup
    # Having trubble putting the token in?
    # 1. Go to https://ipinfo.io/signup — it’s free, I promise.
    # 2. Get your token, looks like: e4xcke5hgus92d (but not this one!)
    # 3. Open your terminal and type:
    #   export IPINFO_TOKEN=your_real_token_here
    # 4. Then run this script again like a boss.
    if not API_TOKEN:
        print("\u26a0 Missing API token. Set the 'IPINFO_TOKEN' environment variable. (We're not made of tokens, okay?)")
        return

    ip_or_domain = input("\U0001F50E Enter an IP or domain (or hit Enter to expose yourself): ").strip()

    if not ip_or_domain:
        print("\U0001F6F0\ufe0f Using your public IP... hope you weren't hiding.")
        ip_or_domain = get_public_ip()
        if not ip_or_domain:
            print("\u274C Could not determine your public IP. Are you living in a Faraday cage?")
            return
    else:
        try:
            ip_obj = ipaddress.ip_address(ip_or_domain)
            if ip_obj.is_private:
                print("\U0001F512 That's a private IP! Respect the boundaries.")
                return
        except ValueError:
            pass  # Treat as domain name, like the rebel you are

    print(f"\U0001F310 Looking up location for {ip_or_domain}... fingers crossed.")
    data = get_geolocation(ip_or_domain, API_TOKEN)

    if data:
        print("\n\U0001F4CC Geolocation Info:")
        print(f"IP Address: {data.get('ip', 'N/A')}")
        print(f"Hostname: {data.get('hostname', 'N/A')}")
        print(f"City: {data.get('city', 'N/A')}")
        print(f"Region: {data.get('region', 'N/A')}")
        print(f"Country: {data.get('country', 'N/A')}")
        print(f"Location: {data.get('loc', 'N/A')}")
        print(f"Organization: {data.get('org', 'N/A')}")
        print(f"Postal Code: {data.get('postal', 'N/A')}")
        print(f"Timezone: {data.get('timezone', 'N/A')}")

        plot_ip_location(data)

        delete_choice = input("\U0001F5D1\ufe0f Delete the map? (yes/no): ").strip().lower()
        if delete_choice == 'yes':
            try:
                os.remove('ip_geolocation_map.html')
                print("\U0001F9F9 Deleted like a secret agent covering tracks.")
            except FileNotFoundError:
                print("\U0001F4C1 Map file not found. It disappeared like magic.")
        else:
            print("\U0001F4C2 Map kept. Hang it on your digital wall.")
    else:
        print("\u274C Failed to get location data. The internet is moody today.")


if __name__ == "__main__":
    main()
