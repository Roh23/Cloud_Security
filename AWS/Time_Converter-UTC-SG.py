from datetime import datetime, timezone, timedelta

def convert_utc_to_sgt(utc_time_str):
    # Parse the UTC time string into a datetime object
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")
    
    # Set the UTC timezone
    utc_time = utc_time.replace(tzinfo=timezone.utc)
    
    # Convert to Singapore Time (UTC+8)
    sgt_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    
    return sgt_time.strftime("%Y-%m-%d %H:%M:%S")

def process_user_input():
    utc_time_str = input("Enter the UTC time (YYYY-MM-DD HH:MM:SS): ")
    sgt_time = convert_utc_to_sgt(utc_time_str)
    print(f"UTC Time: {utc_time_str}")
    print(f"Singapore Time (SGT): {sgt_time}")

def process_file():
    input_file = input("Enter the file name (with UTC timestamps): ")
    output_file = input("Enter the output file name: ")
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                utc_time_str = line.strip()
                try:
                    sgt_time = convert_utc_to_sgt(utc_time_str)
                    outfile.write(f"{utc_time_str} -> {sgt_time}\n")
                except ValueError:
                    outfile.write(f"Invalid time format: {utc_time_str}\n")
        print(f"Converted times have been saved to {output_file}")
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")

def main():
    print("Choose an option:")
    print("1. Enter UTC time manually")
    print("2. Read UTC times from a file")
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        process_user_input()
    elif choice == '2':
        process_file()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
