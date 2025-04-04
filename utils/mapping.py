# utils/mapping.py
import folium


def plot_ip_location(ip_data):
    if 'loc' not in ip_data:
        print("Location data not available.")
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
        popup="Approximate Area"
    ).add_to(m)

    m.save('ip_geolocation_map.html')
    print("Map saved as 'ip_geolocation_map.html'")


def plot_multiple_ip_locations(ip_data_list):
    if not ip_data_list:
        print("No valid IP data to plot.")
        return

    # Use the first valid IP as the map center
    center_data = next((d for d in ip_data_list if 'loc' in d), None)
    if not center_data:
        print("No valid location data found in input list.")
        return

    latitude, longitude = map(float, center_data['loc'].split(','))
    m = folium.Map(location=[latitude, longitude], zoom_start=2)

    for data in ip_data_list:
        if 'loc' not in data:
            continue
        lat, lon = map(float, data['loc'].split(','))
        folium.Marker(
            [lat, lon],
            popup=f"IP: {data.get('ip', 'N/A')}\nCity: {data.get('city', 'N/A')}\nRegion: {data.get('region', 'N/A')}\nCountry: {data.get('country', 'N/A')}"
        ).add_to(m)

        folium.Circle(
            radius=10000,
            location=[lat, lon],
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.2,
            popup="Approximate Area"
        ).add_to(m)

    m.save('ip_geolocation_map.html')
    print("Map saved with multiple IPs as 'ip_geolocation_map.html'")