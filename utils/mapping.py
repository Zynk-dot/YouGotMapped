# utils/mapping.py
import folium


def plot_ip_location(ip_data):
    if 'loc' not in ip_data:
        print("\U0001F9ED Location data not available.")
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
        popup="\U0001F5FA\ufe0f Approximate Area"
    ).add_to(m)

    m.save('ip_geolocation_map.html')
    print("\U0001F4CD Map saved as 'ip_geolocation_map.html'")
