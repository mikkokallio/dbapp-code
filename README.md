# dbapp-code

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

The app runs at https://functions-dbapp.azurewebsites.net/

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. The architecture is as follows:

GitHub --GitHub Actions--> Azure Functions <--> Azure Database for PostgreSQL

Please note that the folder structure in this repo follows the [recommended folder structure for a Python Functions project](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#folder-structure).

## Views and functionality

The app shall have the following views:
* Login
* Create user account
* Home
* List events
* List users
* View 1 event, allows commenting & signing up for event, also suggesting event to other users (more controls shown if you created it, e.g. delete event)
* View 1 user (more info shown if it is your profile)
