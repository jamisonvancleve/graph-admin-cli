# graph-admin-cli

**Microsoft Graph Administration CLI Application**\
A modular, Python command-line tool for Microsoft Entra ID administration via Microsoft Graph API. Designed for automation and system administration, graph-admin-cli uses OAuth 2.0 client credentials (via an Entra App Registration)to query users and devices.

<br />

**Architecture**\
The modular approach decouples the user interface from API calls and data transformation tasks:

```
graph-admin-cli/  
├── app/  
│   ├── __init__.py  
│   ├── api.py          #Makes HTTP requests to Microsoft Graph API endpoints using authenticated headers.  
│   ├── auth.py         #Authenticates with Microsoft Entra ID via OAuth 2.0 to retrieve access tokens.  
│   ├── cli.py          #Controls command-line argument parsing, subcommand routing, and data presentation.  
│   └── processing.py   #Handles data normalization, filtering, inactivity calculations, and export formatting.  
├── tests/              #Pytest unit tests for API, auth, CLI, and processing modules  
├── main.py             #Entry point for the app. Initializes logging.  
├── .env.example        #Environment variable template (stores Entra ID credentials)  
├── requirements.txt    #Third-party dependency specifications  
└── README.md  
```

**Key Features**

* User Management: Query user identities including group membership, manager, and usage location.
* User Auditing: Discover inactive user accounts.
* Device Auditing: Query device inventory.
* Data Processing: Export data directory to json or csv formats.

  <br />

**Prerequisites**\
Entra ID App Registration

1. Register an application in the Entra Admin Center
2. Grant the following Application Permissions (Microsoft Graph)

   User.ReadWrite.All

   Directory.ReadWrite.All

   NOTE: Write permissions are required for setting Usage Location.
3. Grant Admin Consent for your tenant
4. Generate a Client Secret under Certificates & secrets

<br />

**Entra ID Licensing**\
A Microsoft Entra ID P1 or P2 license is required to access the signInActivity property. This is used to calculate inactive users. If a license is not assigned, graph-cli-admin will fall back to using createdDateTime. This is not as meaningful, but allows the app to demonstrate the feature.

<br />

**Installation and Setup**

1. Clone the repository

   `git clone https://github.com/your-username/graph-admin-cli.git````cd graph-admin-cli`

2. Create a virtual environment

   `python -m venv .venv`\
   `source .venv/bin/activate # On Windows: .venv\Scripts\activate`

3. Install dependencies

   `pip install -r requirements.txt`

4. Configure Environment Variables

   `cp .env.example .env`

5. Open .env and supply the credentials for your tenant

   TENANT\_ID=your-entra-tenant-id

   CLIENT\_ID=your-entra-client-id

   CLIENT\_SECRET=your-entra-client-secret

**Usage Examples**\
Execute commands directly using main.py\
Query Users\
python main.py users

Query Devices\
python main.py devices

Optional Global Parameters\
-h, --help\
\--format\
\--limit\
\--search

Optional User Parameters\
\--inactive-days\
\--id\
\--groups\
\--manager\
\--usage-location

Unit Testing\
Automated testing is built using pytest:

<br />

Run the complete test suite

`pytest`

Run tests with verbose output

`pytest -v`

Target specific modules

`pytest tests/test_processing.py`

#
