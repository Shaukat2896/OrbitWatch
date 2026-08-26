import urllib.request
import os

# Dataset URLs provided
GROUPS = {
    # Operational satellites
    "ACTIVE": "https://celestrak.org/NORAD/elements/gp.php?GROUP=ACTIVE&FORMAT=tle",

    # Major debris clouds
    "COSMOS_2251_DEBRIS": "https://celestrak.org/NORAD/elements/gp.php?GROUP=COSMOS-2251-DEBRIS&FORMAT=tle",
    "IRIDIUM_33_DEBRIS": "https://celestrak.org/NORAD/elements/gp.php?GROUP=IRIDIUM-33-DEBRIS&FORMAT=tle",
    "FENGYUN_1C_DEBRIS": "https://celestrak.org/NORAD/elements/gp.php?GROUP=FENGYUN-1C-DEBRIS&FORMAT=tle",
}

# Output location
OUTPUT_FILE = r"C:\Users\shauk\OneDrive\personal\projects\personal\OrbitWatch\data\objects_orbiting_data.tle"


def download_and_merge_tle(urls, output_filename):
    #print(f"Starting download and merge process into:\n{output_filename}\n")

    # Make sure the data directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Open the output file
    with open(output_filename, "w", encoding="utf-8") as merged_file:

        for group_name, url in urls.items():
            #print(f"Downloading {group_name} data...")

            try:
                # Fetch TLE data
                with urllib.request.urlopen(url) as response:
                    data = response.read().decode("utf-8")

                    # Ensure newline between datasets
                    if data and not data.endswith("\n"):
                        data += "\n"

                    # Add data to merged file
                    merged_file.write(data)

                #print(f"Successfully added {group_name} data.")

            except Exception as e:
                print(f"Error downloading {group_name}: {e}")

            #print("-" * 40)

    #print("\nAll done!")
    #print(f"Merged TLE file saved at:\n{os.path.abspath(output_filename)}")

if __name__ == "__main__":
    download_and_merge_tle(GROUPS, OUTPUT_FILE)