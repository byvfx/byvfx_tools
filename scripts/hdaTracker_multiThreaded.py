import os
import csv
import hou
import time
from concurrent.futures import ThreadPoolExecutor

start_time = time.time()

def gather_hd_assets_in_hip_file(hip_path):
    """Gather HDA assets in a given Houdini scene file."""
    hda_data = []

    # Load the Houdini scene file
    hou.hipFile.load(hip_path, suppress_save_prompt=True, ignore_load_warnings=True)

    def gather_hdas(node, depth=0):
        if node.type().definition() is not None:
            hda_name = node.type().definition().nodeTypeName()
            hda_data.append((hip_path, hda_name, depth))
        
        # Continue traversing for child nodes
        try:
            for child in node.children():
                gather_hdas(child, depth+1)
        except hou.PermissionError:
            print(f"PermissionError: Skipped node - {node.path()}")

    gather_hdas(hou.node('/'))
    return hda_data


# Specify the root directory to search for .hip files
root_directory = r"D:/__projects/BYVFX/BunnyEater"

# Collect all the .hip files
hip_files = []

for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith('.hip'):
            file_path = os.path.join(dirpath, filename)
            hip_files.append(file_path)

# Process the .hip files in parallel using multithreading
final_hda_data = []

with ThreadPoolExecutor() as executor:
    results = executor.map(gather_hd_assets_in_hip_file, hip_files)
    for result in results:
        final_hda_data.extend(result)

# Write HDA data to CSV
output_csv_file = "hdas.csv"

try:
    with open(output_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row
        csv_writer.writerow(["HIP File", "HDA", "Depth"])
        # Write each HDA entry to a new row
        for entry in final_hda_data:
            csv_writer.writerow(entry)
except Exception as e:
    print("Error writing to CSV file:", str(e))
else:
    print("Time taken: ", time.time() - start_time, "seconds")
    print(f"{len(final_hda_data)} HDA entries written to:", output_csv_file)
    print("HIP files processed: ", len(hip_files))
