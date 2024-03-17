# User Disable Automation function

This folder contains code that will be deployed to function-app in Azure.
The function contains an automatic process for disabling access of external users after a specified period of time from their creation.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-functions
- azure-identity
- azure-keyvault-secrets
- pytest
- python-dotenv==1.0.0
- pytz
- requests
- ruff

These dependencies exist in the 'requirements.txt' file.

## Running the code

The code is automatically run using CI CD processes through workflow.

## Tests

The code has undergone in-depth TEST tests with respect to end situations,
the tests are also automatically run in the CI CD process through workflow.
