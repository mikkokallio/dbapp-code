# MeetApp

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

## Overview

A user can create an account and log in to the app. Once logged in, a user can create events, comment on events any user has created, and click a button to indicate they are going to an event. An event may be created as anonymous, in which case users only see how many people are going to the event but not which users. Different types of actions users perform create notifications, e.g. if a user has created an event, they get notifications when people sign up for the event or leave comments. Admin users can also see deleted events and other hidden information. They can also ban users or elevate regular users to admins.

## Testing the app

The app runs at https://functions-dbapp.azurewebsites.net/

Not all features mentioned above exist yet. But you can try doing the following:
1. Try creating a user account by clicking Create user account.
2. Once logged in, try creating a new event. You can view events e.g. by clicking the star in the top pane.
3. Try also writing a comment in an event, whether one you created or an existing one.

## Reviewing the code

Because of the production environment's requirements, the code is structured so that the application code is in the **FlaskApp** folder.

## Todo list

* Indicate "you and n are going" when user is one of the people going.
* Create links from usernames shown in comments, events view, and individual event view that open that user's profile. This could be a modal.
* When clicking "n are going", show in a modal all users that have so far signed up to an event.
* When giving invalid information in a form, show error proactively, or preserve information in fields so it doesn't have to be entered again.
* Validate dates, passwords, username more rigorously. E.g. no events occurring in the past allowed.
* Show all errors at once if there are multiple fields with invalid inputs.
* Add notifications for different kinds of actions.

## Architecture

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. The architecture is as follows:

GitHub --GitHub Actions--> Azure Functions <--> Azure Database for PostgreSQL

## Views and functionality

The app shall have the following views:
* Login
* Create user account
* Home, which shows newest events, latest notifications, and contains links to other views
* List events
* List users
* View 1 event, allows commenting & signing up for event, also suggesting event to other users (more controls shown if you created it, e.g. delete event)
* View 1 user, which shows their public information as well as what events they have created or signed up for
