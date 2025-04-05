import csv
import json
from collections import defaultdict

def csv_to_json(csv_file_path, json_file_path):
    clubs = defaultdict(lambda: {"website": "", "events": []})

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
                "description": row['event_description'],
                "distance_options": [d.strip() for d in row['event_distances'].split(',')]
            }

            clubs[club_name]['events'].append(event)

    # Convert to desired format
    result = {
        "clubs": [
            {
                "name": name,
                "website": data['website'],
                "events": data['events']
            } for name, data in clubs.items()
        ]
    }

    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(result, json_file, indent=2)

# Example usage
csv_to_json('group_run_events.csv', 'run_info.json')
