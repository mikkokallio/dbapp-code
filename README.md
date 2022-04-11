# Minglerz.net

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

## Overview

A user can create an account and log in to the app. Once logged in, a user can create events, comment on events any user has created, and register to join an event.

## Testing the app

The app runs at https://functions-dbapp.azurewebsites.net/

Not all features mentioned above exist yet. But you can try doing the following:
1. Create a new user account and log in. Try entering intentionally bad usernames and poor passwords first, then viewing the error messages and changing the values accordingly.
2. Create new events. Here too, you can try submitting e.g. an empty event, then fixing the values according to instructions.
3. View events other people have created and register to join an event, or comment on an event.
4. View other users' profiles wherever their username appears as a link.
5. Click the user icon in the top bar to view your own profile, and edit your profile or log out.

## Reviewing the code

The code is structured so that the application code is in the **FlaskApp** folder.

## Todo list

* Past events should not allow registering anymore, and they should be listed under a different heading: past events.
* Add notifications for different kinds of actions.
* Editing event information should be possible.
* Add locations to events.
* User can change password.
* Deleting an event should be possible. Or canceling, so the event doesn't just vanish.
* Intro transition screen for new users after registration: go to events and show modal "welcome, blah blah"
* In user modal, show what events they've signed up for.
* Bug: On mobile, viewing who's going triggers the button that determines who's going.
* Add cross-site scripting protection and other security measures.
* Admin users can also see deleted events and other hidden information. They can also ban users or elevate regular users to admins.
* Different types of actions users perform create notifications, e.g. if a user has created an event, they get notifications when people sign up for the event or leave comments.

## Architecture

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. Github and Github Actions are used for CI/CD, deploying the app automatically to Azure each time the main branch is updated.
