# Minglerz.net

![workflow status](https://github.com/mikkokallio/dbapp-code/actions/workflows/main_functions-dbapp.yml/badge.svg)

## Overview

A user can create an account and log in to the app. Once logged in, a user can create events, comment on events any user has created, and register to join an event.

## Running the app

The app runs at https://minglerz.net/. Most functionality should work ok also on cell phone, but there are a few bugs still.

You can test the app by trying out the following features:
1. **Create a new user account and log in**.
2. **Create a new place**. When searching for locations, use street name with address number and city, e.g. Leppäsuonkatu 11, 00100 Helsinki. Otherwise, the results may be inaccurate.
3. Admins only: You can delete places but only if no events are currently using that place.
4. **Create new events**. You can create events either in the events view or through the places view.
5. **Edit events** you have created or delete them. Admins can also edit or delete events created by other users.
6. While **viewing events** people have created, **register to join an event, or comment on an event**. Try also zooming in and out, rotating and tilting the map.
7. **View other users' profiles** in a popup view by clicking their username.
8. Click the user icon in the top bar to **view your own profile, and edit your profile or log out**.

## Reviewing the code

The code is structured so that the application code is in the **FlaskApp** folder.

## Technologies used

* The app is written Python, SQL, HTML, and JS using Flask as the web framework and Bulma as a style library. 
* Azure Functions provides serverless compute for running Flask.
* Azure Database for PostgreSQL is used for persisting the app data.
* Azure Maps APIs are used for fetching street address information and displaying maps in events.
* Github and Github Actions are used for CI/CD, deploying the app automatically to Azure each time the main branch is updated.
