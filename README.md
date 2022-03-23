# MeetApp

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

## Overview

A user can create an account and log in to the app. Once logged in, a user can create events, comment on events any user has created, and click a button to indicate they are going to an event. An event may be created as anonymous, in which case users only see how many people are going to the event but not which users. Different types of actions users perform create notifications, e.g. if a user has created an event, they get notifications when people sign up for the event or leave comments. Admin users can also see deleted events and other hidden information. They can also ban users or elevate regular users to admins.

## Testing the app

The app runs at TBA

## Architecture

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. The architecture is as follows:

GitHub --GitHub Actions--> Azure Functions <--> Azure Database for PostgreSQL

Please note that the folder structure in this repo follows the [recommended folder structure for a Python Functions project](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#folder-structure).

## Views and functionality

The app shall have the following views:
* Login
* Create user account
* Home, which shows newest events, latest notifications, and contains links to other views
* List events
* List users
* View 1 event, allows commenting & signing up for event, also suggesting event to other users (more controls shown if you created it, e.g. delete event)
* View 1 user, which shows their public information as well as what events they have created or signed up for
