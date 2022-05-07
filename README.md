# Minglerz.net

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

## Overview

A user can create an account and log in to the app. Once logged in, a user can create events, comment on events any user has created, and register to join an event.

## Running the app

The app runs at https://minglerz.net/. Most functionality should work ok also on cell phone, but there are a few bugs still.

You can test the app by trying out the following features:
1. **Create a new user account and log in**. Try entering intentionally bad usernames and poor passwords first, then viewing the error messages and changing the values accordingly.
2. **Create a new place**. When searching for locations, use street name with address number and city, e.g. Leppäsuonkatu 11, 00100 Helsinki. Otherwise, the results may be inaccurate. Try fooling the validation with weird inputs.
3. Admins only: You can delete places but only if no events are currently using that place.
4. **Create new events**. Here too, you can try submitting e.g. an empty event, then fixing the values according to instructions.
5. **Edit events** you have created or delete them. Admins can also edit or delete events created by other users.
6. While viewing events other people have created, **register to join an event, or comment on an event**. You can also check that you can't register to a past event or when max number of attendees is reached.
7. **View other users' profiles** in a popup view by clicking their username.
8. Click the user icon in the top bar to **view your own profile, and edit your profile or log out**. Password change doesn't work yet.

## Reviewing the code

The code is structured so that the application code is in the **FlaskApp** folder.

## Technologies used

* The app is written Python, SQL, HTML, and JS using Flask as the web framework and Bulma as a style library. 
* Azure Functions provides serverless compute for running Flask.
* Azure Database for PostgreSQL is used for persisting the app data.
* Azure Maps APIs are used for fetching street address information and displaying maps in events.
* Github and Github Actions are used for CI/CD, deploying the app automatically to Azure each time the main branch is updated.

## Todo list

The following features are on the roadmap, but haven't been implemented yet.

* When viewing the list of places, there should be a button "Create event here" as a shortcut so that the place gets inserted in the form automatically.
* User should be able to change password.
* Other users, too, should have full profiles. When viewing participant list in a modal, there should be links to full profiles.
* Bug: On mobile, viewing the list of who's going to an event sometimes triggers the button that registers participation.
* Admin users should be able to see deleted events and other hidden information. They should also be able to ban users or elevate regular users to admins.
* Users can cancel events ("soft delete") without immediately removing the event. Also, there should be a confirmation dialog for deleting an event.
