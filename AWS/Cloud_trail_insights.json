import json
import requests
from collections import Counter
from datetime import datetime
from termcolor import colored

# Function to lookup country for an IP using ipinfo
def get_country(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return response.get("country", "Unknown")
    except Exception as e:
        return "Unknown"

# Function to analyze the CloudTrail logs
def analyze_cloudtrail(log_file):
    with open(log_file, 'r') as f:
        logs = json.load(f).get("Records", [])

    ip_counter = Counter()
    user_api_counter = Counter()
    suspicious_users = []
    login_failures = []
    privileged_actions = []

    for record in logs:
        ip = record.get("sourceIPAddress", "Unknown")
        user = record.get("userIdentity", {}).get("userName", "Unknown")
        event_name = record.get("eventName", "Unknown")
        event_time = record.get("eventTime", "Unknown")
        user_agent = record.get("userAgent", "Unknown")

        # Count IP addresses
        ip_counter[ip] += 1

        # Count API actions by user
        user_api_counter[user] += 1

        # Identify suspicious login failures
        if event_name == "ConsoleLogin" and "Failure" in str(record.get("responseElements", "")):
            login_failures.append({"ip": ip, "user": user, "time": event_time, "agent": user_agent})

        # Identify privileged actions
        privileged_actions_list = ["AssumeRole", "AttachRolePolicy", "PutRolePolicy", "CreateUser"]
        if event_name in privileged_actions_list:
            privileged_actions.append({"user": user, "action": event_name, "time": event_time})

    # Top IP countries
    ip_countries = Counter(get_country(ip) for ip in ip_counter.keys())

    # Summary
    print(colored("\n--- Summary ---", "cyan", attrs=["bold"]))
    print(colored("Top IP Countries:", "yellow"))
    for country, count in ip_countries.most_common(5):
        print(f"  {country}: {count} requests")

    print(colored("\nHighest API Action Users:", "yellow"))
    for user, count in user_api_counter.most_common(5):
        print(f"  {user}: {count} actions")

    print(colored("\nMost Suspicious Users (Login Failures):", "yellow"))
    for failure in login_failures:
        print(f"  User: {failure['user']}, IP: {failure['ip']}, Time: {failure['time']}, Agent: {failure['agent']}")

    print(colored("\nPrivileged Actions Identified:", "yellow"))
    for action in privileged_actions:
        print(f"  User: {action['user']}, Action: {action['action']}, Time: {action['time']}")

    # Detailed Questions
    print(colored("\n--- Investigation Questions ---", "cyan", attrs=["bold"]))

    print(colored("1. Who Accessed the Account?", "green"))
    for user, count in user_api_counter.most_common():
        print(f"  User: {user}, Actions: {count}")

    print(colored("\n2. What Actions Were Taken?", "green"))
    for action in privileged_actions:
        print(f"  {action['user']} performed {action['action']} at {action['time']}")

    print(colored("\n3. When Did It Happen?", "green"))
    for record in logs[:5]:  # Example of timeline
        print(f"  Event: {record['eventName']}, Time: {record['eventTime']}")

    print(colored("\n4. Where Did the Requests Originate?", "green"))
    for ip, count in ip_counter.most_common(5):
        country = get_country(ip)
        print(f"  IP: {ip}, Country: {country}, Requests: {count}")

    print(colored("\n5. Were Any Privileged Actions Performed?", "green"))
    for action in privileged_actions:
        print(f"  User: {action['user']}, Action: {action['action']}, Time: {action['time']}")

# Example Usage
if __name__ == "__main__":
    log_file_path = input("Enter the path to the CloudTrail log file: ")
    analyze_cloudtrail(log_file_path)
