import yaml

# Load the YAML file
with open('rac_lab/docmap (copy).yaml', 'r') as file:
    map_metadata = yaml.safe_load(file)

# Print parsed metadata for verification
print("Parsed metadata from 'map.yaml':")
print(f"Resolution: {map_metadata['resolution']}")
print(f"Origin: {map_metadata['origin']}")
# Add additional prints if there are more fields you need

# If needed, you can store the metadata in a more convenient format
metadata_dict = {
    'resolution': map_metadata['resolution'],
    'origin': map_metadata['origin'],
    # Add other metadata fields if necessary
}

# Save metadata to a JSON file (optional)
import json
with open('metadata.json', 'w') as json_file:
    json.dump(metadata_dict, json_file, indent=4)

print("Metadata has been saved to 'metadata.json'")
