import math
import re

import requests

# The Regex pattern to extract: Date, Username, and IP address from auth logs
LOG_PATTERN = (
    r"(\w{3}\s+\d+\s\d{2}:\d{2}:\d{2}).*Accepted password for (\w+) from ([\d\.]+)"
)


def get_ip_coords(ip):
    """
    Look up Latitude, Longitude, and City for a given IP address.
    Uses the free ip-api.com endpoint.
    """
    try:
        # API call to get geographic data from the IP
        response = requests.get(f"http://ip-api.com/json/{ip}").json()

        if response.get("status") == "success":
            return response["lat"], response["lon"], response["city"]
    except Exception as e:
        print(f"[!] Error locating IP {ip}: {e}")

    return None, None, "Unknown"


def parse_logs(file_path):
    """
    Reads the log file line-by-line and performs geographic analysis.
    """
    print(f"--- Analyzing Log File: {file_path} ---")

    last_location = None  # Store (lat, lon, timestamp)
    with open(file_path, "r") as f:
        for line in f:
            # Step 1: Extract data using Regex
            match = re.search(LOG_PATTERN, line)
            if match:
                timestamp, user, ip = match.groups()
                lat, lon, city = get_ip_coords(ip)

                # 1. Identify immediately
                print(f"[FOUND] {user} in {city}")

                # 2. Show detailed forensic data
                print(f"[ANALYSIS] User: {user}")
                print(f"           Time: {timestamp}")
                print(f"           Loc:  {city} ({lat}, {lon})")

                # 3. Calculate travel if we have a previous point
                if last_location:
                    prev_lat, prev_lon = last_location
                    dist = calculate_distance(prev_lat, prev_lon, lat, lon)
                    print(f"[MATH] Distance from last login: {dist:.2f} km")

                    if dist > 500:
                        print("[!] ALERT: Impossible Travel Detected!")

                # 4. Close the record
                print("-" * 40)

                # 5. Update state for the next line
                last_location = (lat, lon)


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points in kilometers.
    """
    # Convert degrees to radians
    r_lat1, r_lon1, r_lat2, r_lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = r_lat2 - r_lat1
    dlon = r_lon2 - r_lon1

    # Haversine calculation
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(r_lat1) * math.cos(r_lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return 6371 * c  # Result in kilometers


if __name__ == "__main__":
    # Pointing to the mock log file we created
    test_log = "tools/test_auth.log"
    parse_logs(test_log)
