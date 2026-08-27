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

