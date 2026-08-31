#test_cli.py - Unit tests for CLI argument parsing and subcommands
#These tests are run offline, without touching Microsoft endpoints


from app.cli import build_parser, handle_user_command

def test_build_parser_default_args():
    #Test default arguments
    #args.limit defaults to 25
    #args.format defaults to "text"
    #args.search is None
    #args.func points to handle_user_command

    #Instantiate the parser configuration
    parser = build_parser()
    args = parser.parse_args(["user"])


    #Assert default values and proper command routing
    assert args.command == "user"
    assert args.format == "text"
    assert args.limit == 25
    assert args.search is None
    assert args.inactive_days is None
    assert args.func == handle_user_command


def test_build_parser_custom_flags():
    #Verify arg values match command-line values
    #Instantiate the parser configuration
    parser = build_parser()

    #Pass explicit custom flags into parse_args
    args = parser.parse_args([
        "user",
        "--search", "alice",
        "--format", "json",
        "--limit", "10",
        "--inactive-days", "60"
    ])

    #Assert all explicit CLI overrides match expected values and types
    assert args.command == "user"
    assert args.search == "alice"
    assert args.format == "json"
    assert args.limit == 10
    assert args.inactive_days == 60
    assert args.func == handle_user_command


# def test_handle_user_command_no_records():
#     #Simulate returning a valid payload, with no records
#     #Verify the function handles it correctly
#     pass
#
# def handle_device_command_json_format():
#     #Send mock data and verify it is returned in the proper format
#     pass



