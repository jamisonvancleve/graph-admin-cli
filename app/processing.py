import datetime

def normalize_users(raw_data):
    """Normalizes raw data payload from Microsoft Graph API"""
    if isinstance(raw_data, dict):
        users = raw_data.get("value", [])
    else:
        users = raw_data

    normalized = []
    for user in users:
        upn = user.get("userPrincipalName") or "N/A"
        businessPhones = user.get("businessPhones") or []

        normalized.append({
            "id": user.get("id") or "N/A",
            "display_name": user.get("displayName") or "N/A",
            "user_principal_name": upn,
            "job_title": user.get("jobTitle") or "N/A",
            "office_location": user.get("officeLocation") or "N/A",
            "email": user.get("mail") or upn,
            "business_phones": ", ".join(businessPhones) if businessPhones else "N/A",
            "mobile_phone": user.get("mobilePhone") or "N/A",
            "preferred_language": user.get("preferredLanguage") or "N/A",
        })

    return normalized


def normalize_devices(raw_data):
    """Normalizes raw data payload from Microsoft Graph API"""

    if isinstance(raw_data, dict):
        devices = raw_data.get("value", [])
    else:
        devices = raw_data

    normalized = []
    for device in devices:
        normalized.append({
            "id": device.get("id") or "N/A",
            "device_id": device.get("deviceId") or "N/A",
            "display_name": device.get("displayName") or "N/A",
            "operating_system": device.get("operatingSystem") or "N/A",
            "operating_system_version": device.get("operatingSystemVersion") or "N/A",
        })

    return normalized


def filter_users(records, search_term):
    """Filters a list of normalized users by display name or UPN."""
    if not search_term:
        return records

    term = search_term.lower()
    return [
        u for u in records
            if term in u.get("display_name", "").lower()
            or term in u.get("user_principal_name", "").lower()
        ]


def filter_devices(records, search_term):
    """Filters a list of normalized devices by display name, ID, or device ID."""
    if not search_term:
        return records

    term = search_term.lower()
    return [
        d for d in records
        if term in d.get("display_name", "").lower()
        or term in d.get("id", "").lower()
        or term in d.get("device_id", "").lower()
    ]

def get_inactive_users(records, days_threshold):
    #Calculate the cutoff date
    cutoff_date = datetime.today() - days_threshold

    return [
        u for u in records
            if cutoff_date < u.get("signInActivity")
    ]

