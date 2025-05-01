# Cloud Cost Guard

Cloud Cost Guard is a tool designed to help manage and optimize cloud costs by scanning cloud resources, generating reports, and sending notifications.

## Features
- Scans cloud resources for cost optimization opportunities.
- Generates detailed reports.
- Sends email notifications with cost insights.
- Terraform scripts for infrastructure setup.

## Project Structure
```
README.md
requirements.txt
app/
    email.py
    main.py
    report.py
    scan.py
    utils.py
terraform/
    iam.tf
    lambda.tf
    main.tf
    scheduler.tf
    variables.tf
tests/
    test_scan.py
```

## Prerequisites
- Python 3.8 or higher
- Terraform 1.0 or higher

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cloud-cost-guard
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize Terraform:
   ```bash
   cd terraform
   terraform init
   ```

## Usage
1. Run the main application:
   ```bash
   python app/main.py
   ```
2. Execute tests:
   ```bash
   pytest tests/
   ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.