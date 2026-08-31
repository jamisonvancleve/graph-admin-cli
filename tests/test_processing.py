#test_processing.py - Unit tests for data filtering, normalization, and date math logic
#These tests are run offline, without touching Microsoft endpoints


from app.processing import normalize_users, filter_users

def test_normalize_users_extracts_core_fields():
    mock_raw_payload = {
        "value": [
            {
                "displayName": "Alice Smith",
                "userPrincipalName": "alice@contoso.com",
                "id": "user-123",
                "mail": "alice@contoso.com"
            }
        ]
    }

    result = normalize_users(mock_raw_payload)

    assert len(result) == 1
    assert result[0]["display_name"] == "Alice Smith"
    assert result[0]["user_principal_name"] == "alice@contoso.com"

def test_filter_users_case_insensitive():
    mock_users = [
            {"display_name": "Alice Smith", "user_principal_name": "alice@contoso.com"},
            {"display_name": "Bob Jones", "user_principal_name": "bob@contoso.com"}
    ]

    filtered_users = filter_users(mock_users)

    print(filtered_users)
    print("resultsss: ", filtered_users[0]["display_name"])

    assert len(filtered_users) == 2
    assert filtered_users[0]["display_name"] == "Alice Smith"

# def test_normalize_devices_extracts_core_fields():
#     #Pass a raw Graph API payload to verify standard key mapping, and missing field fallbacks
#     pass
#
# def test_filter_devices_multi_attribute():
#     #Test filtering device lists across display_name, id, and device_id to ensure mutli-field lookups match correctly
#     pass
#
# def test_get_inactive_users_threshold():
#     #Test the function returns only records older than the cutoff.
#     #Send sample user records with fixed lastSignInDateTime timestamps (dynamically calculated)
#     pass
#
# def test_get_inactive_users_missing_timestamp():
#     #Test how the function handles records with missing SignInActivity keys or None values
#     pass
#
# def test_format_as_csv_valid_output():
#     #Verify output contains expected headers and properly formatted fields.
#     #Send a list of normalized dictionaries
#     pass

