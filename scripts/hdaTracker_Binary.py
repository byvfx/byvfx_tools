import csv
import re

# Your HIP file path
HIP_FILE_PATH = r"E:\_houdiniFiles\hdaTrackerTest.hip"

with open(HIP_FILE_PATH, "r", errors="replace") as f:
    content = f.read()

# Regular expression pattern to detect HDA names within { ... } brackets.
pattern = re.compile(r'{\s*name\s+([A-Za-z0-9_]+::\d+\.\d+)', re.IGNORECASE | re.DOTALL)

hda_names = pattern.findall(content)

print("Total HDA Names Detected:", len(hda_names))

# Now, let's write these to a CSV
output_csv_file = "hda_names.csv"
with open(output_csv_file, 'w', newline='', encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
    # Write the header row
    csv_writer.writerow(["HDA Names"])
    # Write each HDA name to a new row
    for hda_name in hda_names:
        csv_writer.writerow([hda_name])