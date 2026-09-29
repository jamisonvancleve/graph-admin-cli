# graph-admin-cli

**Microsoft Graph Administration CLI Application**\
A modular, enterprise-grade Python command-line application and DevOps automation pipeline for Microsoft Entra ID administration via the Microsoft Graph API. Designed for system administrators and DevOps engineers, graph-admin-cli uses non-interactive OAuth 2.0 client credentials to query user identities, audit device inventories, and identify inactive user accounts.

The project features full containerization, Infrastructure as Code (IaC) provisioning via Terraform, and automated CI/CD deployments using GitHub Actions.
<br />

**Architecture**\
The modular approach decouples the user interface execution, API communication, data processing, infrastructure provisioning, and CI/CD pipelines:

```
graph-admin-cli/
├── .github/
│   └── workflows/
│       ├── ci.yml               #Continuous Integration & DevSecOps pipeline
│       └── cd.yml               #Continuous Deployment, Azure Container Registry (ACR) push & Terraform pipeline
├── app/
│   ├── __init__.py              #Package marker
│   ├── api.py                   #Makes HTTP requests to Microsoft Graph API endpoints using authenticated headers.
│   ├── auth.py                  #Authenticates with Microsoft Entra ID via OAuth 2.0 to retrieve access tokens.
│   ├── cli.py                   #Controls command-line argument parsing, subcommand routing, and data presentation.
│   └── processing.py            #Handles data normalization, filtering, inactivity calculations, and export 
├── terraform/                   #Modular Infrastructure as Code definitions
│   ├── main.tf                  #Primary Azure resource declarations
│   ├── variables.tf             #Input variable definitions
│   ├── outputs.tf               #Terraform output attributes
│   └── terraform.tfvars.example #Example variable input values
├── tests/                       #Pytest unit tests for API, auth, CLI, and processing modules  
├── Dockerfile                   #Non-root production container definition
├── main.py                      #Entry point for the app. Initializes logging. 
├── .env.example                 #Environment variable template (stores Entra ID credentials)  
├── requirements.txt             #Third-party application dependencies
└── README.md                    #Project documentation
```

<br />

**Key Features**

* User Management: Query user identities including group membership, manager, and usage location.
* User Auditing: Discover inactive user accounts.
* Device Auditing: Query device inventory.
* Data Processing: Export data directory to json or csv formats.
* Containerized Execution: Runs as an isolated, non-root container image for enhanced security.
* Automated DevOps Pipeline: Continuous linting, SAST code analysis, IaC policy compliance checks, and container vulnerability scanning built into GitHub Actions.

<br />

**Prerequisites**\
Entra ID App Registration

1. Register an application in the Entra Admin Center
2. Grant the following Application Permissions (Microsoft Graph)

   User.ReadWrite.All (Required for setting Usage Location)
   Directory.ReadWrite.All (Required for setting Usage Location)
   AuditLog.Read.All (Required for sign-in activity and log auditing)

3. Grant Admin Consent for your tenant
4. Generate a Client Secret under Certificates & secrets

<br />

**Entra ID Licensing**\
A Microsoft Entra ID P1 or P2 license is required to access the signInActivity property. This is used to calculate inactive users. If a license is not assigned, graph-cli-admin will fall back to using createdDateTime. This is not as meaningful, but allows the app to demonstrate the feature.

<br />

**Installation and Setup**

Option A: Local Python Environment
1. Clone the repository

   `git clone https://github.com/your-username/graph-admin-cli.git`\
   `cd graph-admin-cli`

2. Create a virtual environment

   `python -m venv .venv`\
   `source .venv/bin/activate `\
   `#On Windows: source .venv\Scripts\activate`

3. Install dependencies

   `pip install -r requirements.txt`

4. Configure Environment Variables

   `cp .env.example .env`

5. Open .env and supply the credentials for your tenant

   `TENANT_ID=your-entra-tenant-id`
   `CLIENT_ID=your-entra-client-id`
   `CLIENT_SECRET=your-entra-client-secret`

Option B: Docker Execution
1. Build the container image:

   `docker build -t graph-admin-cli:latest .`

2. Run the container passing local environment variables:

   `docker run --rm --env-file .env graph-admin-cli:latest users --limit 10`


<br />

**Usage Examples**\
Execute commands directly using main.py

Query Users\
`python main.py users`

<br />

Query Devices\
`python main.py devices`

<br />

Optional Global Parameters\
`-h, --help      show this help message and exit`\
`--format        Select output format {text,json,csv}`\
`--limit         Maximum number of records to return (default = 25)`\
`--search        Filter users by display name or UPN`\
`--inactive-days Threshold for inactive users (default = 90 days)`

<br />

Optional User Parameters\
`--id ID           Target user ID or UPN for detailed lookup`\
`--groups          Include user group memberships`\
`--manager         Include user manager details`\
`--usage-location  Set the 2-letter ISO country code (e.g., US, CA, GB)`

<br />

**Unit Testing**\
Automated testing is built using pytest. Run the commands below to test the app.

Run the complete test suite

  `pytest`

Run tests with verbose output

  `pytest -v`

Target specific modules

  `pytest tests/test_processing.py`


<br />


**Infrastructure as Code (Terraform)**\
All Azure resources (rg-graph-admin-cli-dev and acrgraphadmincli2026) are declared as code under the terraform/ directory.

Initialize & Apply Locally
1. Change directory

    `cd terraform`

2. Initialize state backend

    `terraform init`

3. Run speculative execution plan

    `terraform plan`

4. Provision resources

    `terraform apply`

Teardown Cloud Resources
* To prevent unnecessary Azure cloud costs when not actively using:

    `terraform destroy`

<br />

**CI/CD & DevSecOps Pipeline**
The repository utilizes two automated, chained GitHub Actions workflows:

1. Continuous Integration (ci.yml)
  * Triggers on Pull Requests and pushes to main. Executes parallel quality gates:
  * Python Code Quality: flake8 for syntax enforcement and pytest for unit testing with coverage.
  * IaC Speculative Checks: terraform fmt validation and speculative terraform plan against live Azure remote state.
  * DevSecOps Security Audit:
      * bandit: Static Application Security Testing (SAST) for Python code.
      * checkov: Infrastructure as Code security compliance scanning.
      * trivy: Container filesystem and vulnerability auditing (CRITICAL, HIGH).

2. Continuous Deployment (cd.yml)
  * Triggers sequentially via workflow_run after ci.yml completes successfully on main:
  * Azure & ACR Authentication: Authenticates non-interactively using an Azure Service Principal (azure/login@v2).
  * Container Build & Push: Compiles the Docker image, tags it with both the Git commit SHA (:${{ github.sha }}) and :latest, and pushes to Azure Container Registry (acrgraphadmincli2026.azurecr.io).
  * Automated IaC Deployment: Executes terraform apply -auto-approve to maintain synchronized infrastructure.
  * Deployment Smoke Test: Pulls the newly pushed image from ACR and executes entrypoint health checks (docker run --rm  --help) to verify image integrity.

<br />

**GitHub Branch Protection**

Direct pushes to main are restricted. All Pull Requests require all three CI jobs (python-ci, terraform-ci, and devsecops-ci) to complete successfully before code can be merged.
<br />


