# utils/network.py
import requests
import ipaddress
import socket


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None


def get_geolocation(ip_or_domain, api_token):
    url = f"https://ipinfo.io/{ip_or_domain}/json"
    params = {'token': api_token} if api_token else {}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation data: {e}")
        return None


def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"Could not resolve domain: {domain}")
        return None
