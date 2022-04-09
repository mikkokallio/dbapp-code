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

* When giving invalid information in a form, show error proactively, or preserve information in fields so it doesn't have to be entered again.
* Show all errors at once if there are multiple fields with invalid inputs. Message could be array, then for-each loop through those.
* Validate dates, passwords, username more rigorously. E.g. no events occurring in the past allowed.
* Past events should not allow registering anymore, and they should be listed under a different heading: past events.
* Add notifications for different kinds of actions.
* Editing user or event information should be possible.
* Add locations to events.
* Deleting an event should be possible.
* Intro transition screen for new users after registration: go to events and show modal "welcome, blah blah"
* In user modal, show what events they've signed up for.

## Architecture

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. Github and Github Actions are used for CI/CD, deploying the app automatically to Azure each time the main branch is updated.
