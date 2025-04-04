# utils/token.py
import os

def get_api_token():
    token = os.environ.get("IPINFO_TOKEN")
    if token:
        return token

    print("'IPINFO_TOKEN' environment variable not found.")
    print("To use this tool, you need a free API token from ipinfo.io.")
    print("Visit: https://ipinfo.io/signup")
    token = input("Enter your IPInfo token: ").strip()

    if not token:
        print("No token provided. Exiting.")
        return None

    save = input("Would you like to save this token to a .env file for future runs? (yes/no): ").strip().lower()
    if save in ["yes", "y"]:
        with open(".env", "w") as f:
            f.write(f"IPINFO_TOKEN={token}\n")
        print("Token saved to .env file. Make sure to load it in your script using python-dotenv or similar.")

    return token