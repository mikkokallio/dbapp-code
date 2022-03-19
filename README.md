# dbapp-code

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

The app runs at https://functions-dbapp.azurewebsites.net/

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. The architecture is as follows:

GitHub --GitHub Actions--> Azure Functions <--> Azure Database for PostgreSQL

Please note that the folder structure in this repo follows the [recommended folder structure for a Python Functions project](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#folder-structure).
