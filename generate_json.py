import csv
import json
from collections import defaultdict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import certifi
import ssl
from time import sleep

def safe_geocode(geolocator, address, retries=3):
    """
    Tries to geocode an address with retries if a timeout occurs.
    """
    print("I am in safe_geocode function")
    for attempt in range(retries):
        try:
            # print(f"Attempt {attempt + 1} to geocode: {address}")
            return geolocator.geocode(address)
        except GeocoderTimedOut:
            # print(f"⏳ Timeout for: {address}. Retrying ({attempt + 1}/{retries})...")
            sleep(2)  # wait before retry
    # print(f"❌ Failed to geocode after {retries} retries: {address}")
    return None

def csv_to_json_with_geocoding(csv_file_path, json_file_path):
    # Check if the function is entered
    print("I am in csv_to_json_with_geocoding function")
    
    try:
        # Set up geocoder with increased timeout
        geolocator = Nominatim(user_agent="run-club-mapper", timeout=10)
        
        clubs = defaultdict(lambda: {"website": "", "events": []})

        # Read CSV and build structured data
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                
                club_name = row['club_name']
                clubs[club_name]['website'] = row['club_website']
                
                
                event = {
                    "name": row['event_name'],
                    "date": row['event_date'],
                    "time": row['event_time'],
                    "location": row['event_location'],
                    "address": row['event_address'],
                    "registration": row['event_registration'],
                    "description": row['event_description'],
                    "distance_options": [d.strip() for d in row['event_distances'].split(',')]
                }

                # Geocode address to get lat/lng
                address = event["location"]
                if address:
                    location = safe_geocode(geolocator, address)
                    if location:
                        event["latitude"] = location.latitude  # Save latitude inside the event
                        event["longitude"] = location.longitude  # Save longitude inside the event
                        
                    else:
                        print(f"   → ⚠️  Address not found.")
                    sleep(1)  # Respect rate limits

                clubs[club_name]['events'].append(event)

        # Format as final JSON
        result = {
            "clubs": [
                {
                    "name": name,
                    "website": data['website'],
                    "events": data['events']
                } for name, data in clubs.items()
            ]
        }

        # Write JSON file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=2)

        print(f"\n✅ Done! JSON with coordinates saved to {json_file_path}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        raise  # Re-raise the exception to stop execution and see the error traceback

# Example usage
csv_to_json_with_geocoding('group_run_events.csv', 'run_info.json')
