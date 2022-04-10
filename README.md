# MeetApp

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

## Overview

A user can create an account and log in to the app. Once logged in, a user can create events, comment on events any user has created, and click a button to indicate they are going to an event. An event may be created as anonymous, in which case users only see how many people are going to the event but not which users. Different types of actions users perform create notifications, e.g. if a user has created an event, they get notifications when people sign up for the event or leave comments. Admin users can also see deleted events and other hidden information. They can also ban users or elevate regular users to admins.

## Testing the app

The app runs at https://functions-dbapp.azurewebsites.net/

Not all features mentioned above exist yet. But you can try doing the following:
1. Create a new user account and log in.
2. View events and register to join an event, or comment on an event.
3. View profiles for users that have left comments, and view who have registered to join an event.
4. Click the user icon in the top bar to view your own profile, and edit your profile or log out.

## Reviewing the code

Because of the production environment's requirements, the code is structured so that the application code is in the **FlaskApp** folder.

## Todo list

* When giving invalid information in a form, show error proactively, or preserve information in fields so it doesn't have to be entered again.
* Show all errors at once if there are multiple fields with invalid inputs. Message could be array, then for-each loop through those.
* Validate dates, passwords, username more rigorously. E.g. no events occurring in the past allowed.
* Past events should not allow registering anymore, and they should be listed under a different heading: past events.
* Add notifications for different kinds of actions.
* Editing event information should be possible.
* Add locations to events.
* User can change password.
* Comments, events, etc should be shown in order.
* Deleting an event should be possible. Or canceling, so the event doesn't just vanish.
* Intro transition screen for new users after registration: go to events and show modal "welcome, blah blah"
* In user modal, show what events they've signed up for.
* Create also modal as transition between create and edit user, with a reminder that user can later come back using the (user) icon.

## Architecture

In this app, Azure Functions provides serverless compute for running Flask, and the database is also a PaaS offering from Azure. Github and Github Actions are used for CI/CD, deploying the app automatically to Azure each time the main branch is updated.
