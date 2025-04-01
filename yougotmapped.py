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
            print(f"   \u2611 {pkg} found")
        else:
            print(f"   \u2612 {pkg} MISSING! Please install it.")
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


# Psst... you’ll need an API token to unlock internet secrets (free!): https://ipinfo.io/signup
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