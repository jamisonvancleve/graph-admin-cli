import argparse
import logging
import json

#import sys
from app.api import get_users, get_devices
from app.processing import normalize_users, normalize_devices, filter_users, filter_devices, get_inactive_users, format_as_csv

def handle_user_command(args):
    """Handler function for the user subcommand"""
    #Debug print
    #print("args passed to handle_user_command: ", args)

    #Retrieve all users from Microsoft Graph
    raw_data = get_users()
    if raw_data is None:
        print("Failed to retrieve user data from Microsoft Graph.")
        return

    #Normalize raw data into clean dictionary object
    records = normalize_users(raw_data)

    #Filter results (if args.search was specified by the script executor)
    records = filter_users(records, args.search)

    #Find inactive users (if args.inactive_days was specified by the script executor)
    #If no value is specified for --inactive-days, it defaults to 90
    if args.inactive_days is not None:
        records = get_inactive_users(records, args.inactive_days)

    #Apply limit (default is 25, so there will always be a value to apply)
    records = records[:args.limit]

    #Apply output formatting (default is text)
    if not records:
        print("No records found.")
        return

    match args.format:
        case "json":
            print(json.dumps(records, indent=2))

        case "text":
            for user in records:
                last_sign_in_date = (user.get('signInActivity') or {}).get('lastSignInDateTime') or "N/A"
                print(f"{user.get('display_name')}:"
                      f"\n\tdisplay_name: {user.get('display_name')}"
                      f"\n\tUPN: {user.get('user_principal_name')}"
                      f"\n\tid: {user.get('id')}"
                      f"\n\tjob_title: {user.get('job_title')}"
                      f"\n\toffice_location: {user.get('office_location')}"
                      f"\n\temail: {user.get('email')}"
                      f"\n\tbusiness_phones: {user.get('business_phones')}"
                      f"\n\tmobile_phone: {user.get('mobile_phone')}"
                      f"\n\tpreferred_language: {user.get('preferred_language')}"
                      f"\n\tlastSignInDateTime: {last_sign_in_date}")

        case "csv":
            print(format_as_csv(records))

        case _:
            print("Unknown format: {args.format}.")

    print(f"\nTotal users returned: {len(records)}")


def handle_device_command(args):
    """Handler function for the device subcommand"""
    #Debug print
    #print("args passed to handle_device_command: ", args)

    #Rertieve all devices from Microsoft Graph
    raw_data = get_devices()
    if raw_data is None:
        print("Failed to retrieve device data from Microsoft Graph.")
        return


    #Normalize raw data into clean dictionary object
    records = normalize_devices(raw_data)

    #Filter results (if args.search was specified by the script executor)
    records = filter_devices(records, args.search)

    #Apply limit (default is 25, so there will always be a value to apply)
    records = records[:args.limit]

    # Apply output formatting (default is 'text')
    if not records:
        print("No records found.")
        return

    match args.format:
        case "json":
            print(json.dumps(records, indent=2))

        case "text":
            for device in records:
                print(f"{device.get('display_name')}: "
                      f"\n\tdisplay_name: {device.get('display_name')}"
                      f"\n\tid: {device.get('id')}"
                      f"\n\tdevice_id: {device.get('device_id')}"
                      f"\n\toperating_system: {device.get('operating_system')}"
                      f"\n\toperating_system_version: {device.get('operating_system_version')}")

        case "csv":
            print(format_as_csv(records))

        case _:
            print("Unknown format: {args.format}.")

    print(f"\nTotal devices returned: {len(records)}")

def build_parser():
    """Function to build the argument parser"""
    parser = argparse.ArgumentParser(description="Graph Admin CLI Tool")

    #Create a parent parser to hold flags shared by all subcommands
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Set output format bassed on --format argument
    parent_parser.add_argument("--format", choices=["text", "json", "csv"], default="text", help="Select output format")
    parent_parser.add_argument("--limit", type=int, default=25, help="Maximum number of records to return (default = 25)")

    #Define subcommands (i.e. user or device)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    #Configure subcommand: user
    user_parser = subparsers.add_parser("user", aliases=["users"], parents=[parent_parser], help="Manage user objects")
    user_parser.add_argument("--search", help="Filter users by display name or UPN")
    user_parser.add_argument("--inactive-days", nargs="?", type=int, const=90, default=None, help="Threshold for inactive users (default = 90 days)")
    user_parser.set_defaults(func=handle_user_command)

    #Configure subcommand: device
    device_parser = subparsers.add_parser("device", aliases=["devices"], parents=[parent_parser], help="Manage device objects")
    device_parser.add_argument("--search", help="Filter devices by display name")
    device_parser.set_defaults(func=handle_device_command)

    return parser


def run():
    """Function to run the cli parser"""

    parser = build_parser()
    args = parser.parse_args()

    #Debug print
    #print("args namespace: ",args)

    #Route the execution to assigned handler function.
    if hasattr(args, "func"):
        #If the args namespace contains the 'func' attribute, args.func(args) calls the stored function
        args.func(args)
    else:
        #If the args namespace does not contain a 'func' attribute, display help.
        #(The script executor did not specify a proper subcommand)
        parser.print_help()

