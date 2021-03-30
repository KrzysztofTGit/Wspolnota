# Wspolnota

## Purpose
This application was created for homeowner associations and residents of a housing estate.
The main purpose of the application is to enable residents to vote remotely during the Covid-19 pandemic.

## Features
- user accounts, permissions and cookie-based user sessions handling using Django User Authentication
- basic frontend
- resident notices - logged resident can create notice and read other residents notices
- news sent by the administration
- voting - new polls can be created by the administration, each logged resident can vote once on each poll
- permissions required for most of views

Features for logged user - resident:
read messages sent by administrators
Read notices posted by other residents
Post notices
Vote in polls added by administrators
See results of polls

Administrators can also:
create new polls
Send messages to users
See detailed poll’s results
Modify/add groups and privileges using Django administration

## Tools
- backend in Python
- Django framework
- PostgreSQL or SQLite database
- basic Django tests
