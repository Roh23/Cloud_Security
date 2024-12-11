import re
import json
import os

def hunt_keys(file_path):
    # Regex patterns for AWS access keys and secret keys
    access_key_pattern = re.compile(r'(AKIA[0-9A-Z]{16})')
    secret_key_pattern = re.compile(r'([A-Za-z0-9/+=]{40})')

    try:
        # Check if the file exists and is accessible
        if not os.path.isfile(file_path):
            print(f"File not found or inaccessible: {file_path}")
            return

        with open(file_path, 'r') as file:
            lines = file.readlines()

        found_keys = []

        for line_number, line in enumerate(lines, start=1):
            # Search for access keys
            access_keys = access_key_pattern.findall(line)
            if access_keys:
                for key in access_keys:
                    found_keys.append((line_number, key, "Access Key"))

            # Search for secret keys
            secret_keys = secret_key_pattern.findall(line)
            if secret_keys:
                for key in secret_keys:
                    found_keys.append((line_number, key, "Secret Key"))

        if found_keys:
            print("Found keys:")
            for key_info in found_keys:
                print(f"Line {key_info[0]}: {key_info[1]} ({key_info[2]})")
        else:
            print("No keys found.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {file_path}")
    except OSError as e:
        print(f"An OS error occurred: {e}")

if __name__ == "__main__":
    file_path = input("Enter the path to the .json file: ").strip()
    hunt_keys(file_path)
