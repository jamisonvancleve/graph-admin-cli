from datetime import date, timedelta, datetime


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
            "signInActivity": user.get("signInActivity"),
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
    """
    Returns users whose last sign-in date is older than days_threshold.
    If no value is specified for the --inactive-days parameter, it defaults to 90
    Users with no sign-in data are considered inactive.
    """
    #Calculate the threshold date
    threshold_date = date.today() - timedelta(days=days_threshold)

    #Initialize the
    inactive_users = []

    #Construct a filtered list, based on lastSignInDateTime
    #If lastSignInDateTime < threshold_date, any records that are True are considered Inactive and returned
    for u in records:
        #Handle missing key or None values
        activity = u.get("signInActivity") or {}
        last_sign_in_raw = activity.get("lastSignInDateTime")

        #Handle accounts that have never signed in (considered inactive)
        if not last_sign_in_raw:
            inactive_users.append(u)
            #User is inactive. Skip the code below and continue to the next record.
            continue

        try:
            #Replace the UTC 'Z' indicator for ISO compatibility
            clean_datetime = last_sign_in_raw.replace("Z", "+00:00")
            sign_in_date = datetime.fromisoformat(clean_datetime).date()

            if sign_in_date < threshold_date:
                inactive_users.append(u)
        except (ValueError, TypeError):
            #Safe fallback - the user's datetime is invalid. Do nothing and continue to the next record.
            continue

    return inactive_users

