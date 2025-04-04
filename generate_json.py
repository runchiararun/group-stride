import csv
import json
from collections import defaultdict

# Use defaultdict to group runs by club
run_clubs = defaultdict(list)

with open("run_data.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        club = row.pop("club")  # Remove 'club' key and save value
        run_clubs[club].append(row)

with open("run_info.json", "w") as jsonfile:
    json.dump(run_clubs, jsonfile, indent=4)

print("✅ run_info.json created and grouped by run club!")
