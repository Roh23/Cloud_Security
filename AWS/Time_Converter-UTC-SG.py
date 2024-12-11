import re
import json
from datetime import datetime, timezone, timedelta

def convert_utc_to_sgt(utc_time_str):
    # Parse the ISO 8601 UTC time string into a datetime object
    utc_time = datetime.fromisoformat(utc_time_str)
    
    # Convert to Singapore Time (UTC+8)
    sgt_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    
    # Return the time in the desired format
    return sgt_time.strftime("%H:%M:%S %d %B %Y")

def process_json_file():
    input_file = input("Enter the JSON file name: ")
    output_file = input("Enter the output file name: ")
    
    # Regex pattern to find ISO 8601 timestamps
    iso8601_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))')

    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            data = infile.read()
            
            # Search for all timestamps in the file
            matches = iso8601_pattern.findall(data)
            
            for match in matches:
                try:
                    # Convert each timestamp and replace it in the JSON
                    converted_time = convert_utc_to_sgt(match)
                    data = data.replace(match, converted_time)
                except ValueError:
                    pass
            
            # Write the modified JSON to the output file
            outfile.write(data)
        print(f"Converted times have been saved to {output_file}")
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except json.JSONDecodeError:
        print(f"File '{input_file}' is not a valid JSON.")

def main():
    print("Choose an option:")
    print("1. Enter UTC time manually")
    print("2. Process a JSON file")
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        utc_time_str = input("Enter the UTC time (e.g., 2023-09-28T21:56:31+00:00): ")
        try:
            sgt_time = convert_utc_to_sgt(utc_time_str)
            print(f"UTC Time: {utc_time_str}")
            print(f"Singapore Time (SGT): {sgt_time}")
        except ValueError:
            print("Invalid time format. Please use the format 2023-09-28T21:56:31+00:00")
    elif choice == '2':
        process_json_file()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
