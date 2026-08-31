#cli.py handles command-line argument parsing, subcommand routing, and data presentation

import argparse
import json
import logging
from app.api import get_users, get_devices
from app.processing import normalize_users, normalize_devices, filter_users, filter_devices, get_inactive_users, format_as_csv

#Create a logger object for this module
logger = logging.getLogger(__name__)  # NEW: Initialize module logger

def handle_user_command(args):
    """Handler function for the user subcommand"""
    logger.info("Handling 'user' command execution.")

    #Retrieve all users from Microsoft Graph
    raw_data = get_users()
    if raw_data is None:
        logger.warning("Failed to retrieve user data from Microsoft Graph API.")
        print("Failed to retrieve user data from Microsoft Graph.")
        return

    #Normalize raw data into clean dictionary object
    records = normalize_users(raw_data)
    logger.debug(f"Normalized {len(records)} raw user records.")

    #Filter results (if args.search was specified by the script executor)
    if args.search:
        records = filter_users(records, args.search)
        logger.debug(f"Applied search filter '{args.search}': {len(records)} users remaining.")

    #Find inactive users (if args.inactive_days was specified by the script executor)
    #If no value is specified for --inactive-days, it defaults to 90
    if args.inactive_days is not None:
        records = get_inactive_users(records, args.inactive_days)
        logger.debug(f"Applied inactivity filter ({args.inactive_days} days): {len(records)} users remaining.")

    #Apply limit (default is 25, so there will always be a value to apply)
    records = records[:args.limit]
    logger.debug(f"Applied record limit ({args.limit}): {len(records)} users remaining.")

    #Apply output formatting (default is text)
    if not records:
        logger.info("No records found.")
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

            print(f"\nTotal users returned: {len(records)}")

        case "csv":
            print(format_as_csv(records))

        case _:
            logger.error(f"Unknown format: {args.format}.")
            print(f"Unknown format: {args.format}.")


def handle_device_command(args):
    """Handler function for the device subcommand"""
    logger.info("Handling 'device' command execution.")

    #Rertieve all devices from Microsoft Graph
    raw_data = get_devices()
    if raw_data is None:
        logger.warning("Failed to retrieve device data from Microsoft Graph API.")
        print("Failed to retrieve device data from Microsoft Graph.")
        return


    #Normalize raw data into clean dictionary object
    records = normalize_devices(raw_data)
    logger.debug(f"Normalized {len(records)} raw device records.")

    #Filter results (if args.search was specified by the script executor)
    if args.search:
        records = filter_devices(records, args.search)
        logger.debug(f"Applied search filter '{args.search}': {len(records)} devices remaining.")

    #Apply limit (default is 25, so there will always be a value to apply)
    records = records[:args.limit]
    logger.debug(f"Applied record limit ({args.limit}): {len(records)} devices remaining.")

    # Apply output formatting (default is 'text')
    if not records:
        logger.info("No records found.")
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

            print(f"\nTotal devices returned: {len(records)}")

        case "csv":
            print(format_as_csv(records))

        case _:
            logger.error(f"Unknown format: {args.format}.")
            print(f"Unknown format: {args.format}.")

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
    device_parser.add_argument("--search", help="Filter devices by display name, ID, or device ID")
    device_parser.set_defaults(func=handle_device_command)

    return parser


def run():
    """Main cli.py entry point, invoked by main.py"""
    parser = build_parser()
    args = parser.parse_args()

    #Route the execution to assigned handler function.
    if hasattr(args, "func"):
        #If the args namespace contains the 'func' attribute, args.func(args) calls the stored function
        logger.info(f"Executing command '{args.command}' with options: search={getattr(args, 'search', None)}, limit={args.limit}, format={args.format}")
        args.func(args)
    else:
        #If the args namespace does not contain a 'func' attribute, display help.
        #(The script executor did not specify a proper subcommand)
        logger.warning("CLI executed without a subcommand. Printing help menu.")
        parser.print_help()

