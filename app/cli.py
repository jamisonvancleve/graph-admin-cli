import argparse
import logging
import json
import sys
from app.api import get_users, get_devices

def handle_user_command(args):
    """Handler function for the user subcommand"""
    #Debug print
    #print("args passed to handle_user_command: ", args)

    #Rertieve all users from Microsoft Graph
    data = get_users()
    records = data.get("value",[]) if data else []

    #Filter results (if args.search was specified by the script executor)
    if args.search:
        search_term = args.search.lower()
        records = [
            u for u in records
            if search_term.lower() in u.get("displayName", "").lower()
            or search_term in u.get("userPrincipalName", "").lower()
        ]

    #Apply limit (default is 25, so there will always be a value to apply)
    records = records[:args.limit]

    #Apply output formatting (default is text)
    if args.format == "json":
        print(json.dumps(records, indent=2))
    else:
        if not records:
            print("No matching users found.")
            return

        for user in records:
            print(f"Name: {user.get('displayName')}, UPN: {user.get('userPrincipalName')}")


def handle_device_command(args):
    """Handler function for the device subcommand"""
    #Debug print
    #print("args passed to handle_device_command: ", args)

    #Rertieve all devices from Microsoft Graph
    data = get_devices()
    records = data.get("value",[]) if data else []

    #Filter results (if args.search was specified by the script executor)
    if args.search:
        search_term = args.search.lower()
        records = [
            d for d in records
            if search_term in d.get("displayName", "").lower()
        ]

    #Apply limit (default is 25, so there will always be a value to apply)
    records = records[:args.limit]

    # Apply output formatting (default is 'text')
    if args.format == "json":
            print(json.dumps(records, indent=2))
    else:
        if not records:
            print("No matching devices found.")
            return

        for device in records:
            print(f"Name: {device.get('displayName')}, ID: {device.get('deviceId')}")
            print(f"Device: {device.get('displayName')}, ID: {device.get('deviceId')}, OS: {device.get('operatingSystem')}, OS version: {device.get('operatingSystemVersion')}")


def build_parser():
    """Function to build the argument parser"""
    parser = argparse.ArgumentParser(description="Graph Admin CLI Tool")

    #Create a parent parser to hold flags shared by all subcommands
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Set output format bassed on --format argument
    parent_parser.add_argument("--format", choices=["text", "json"], default="text", help="Select output format")

    #Define subcommands (i.e. user or device)
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    #Configure subcommand: user
    user_parser = subparsers.add_parser("user", aliases=["users"], parents=[parent_parser], help="Manage user objects")
    user_parser.add_argument("--search", help="Filter users by display name or UPN")
    user_parser.add_argument("--limit", type=int, default=25, help="Maximum number of records to return (default = 25)")
    user_parser.set_defaults(func=handle_user_command)

    #Configure subcommand: device
    device_parser = subparsers.add_parser("device", aliases=["devices"], parents=[parent_parser], help="Manage device objects")
    device_parser.add_argument("--search", help="Filter devices by display name")
    device_parser.add_argument("--limit", type=int, default=25, help="Maximum number of records to return (default = 25)")
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

