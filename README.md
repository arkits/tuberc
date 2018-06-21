# TuberC
### 'TuberCulosis'

TuberC organizes your YouTube Subscriptions to give you videos from people you love. It is meant to be an alternative homepage for your YouTube viewing fun!

The flask branch of TuberC is a re-write of the original TuberC proof-of-concept (originally built on Google App Engine). Re-writing in Flask alsos TuberC to be hosted locally or deployed to Heroku with much ease. This re-writing also implements multithreading for retriving videos. This highly improves the refresh times!


## Setup

Following are the instruction to fork and setup TubeC by yourself -

* Follow Step 1 from this guide - https://developers.google.com/youtube/v3/quickstart/python#step_1_turn_on_the_api_name
  * Enable the following API - YouTube Data API v3	
  * Create an OAuth Consent Screen
  * Create an OAuth 2.0 Client ID credential, with the application type as a web application. This is used for user account authorization to download the subscription list from your actual YouTube account.
    * Make sure your website/localhost is listed in the Authorized redirect URIs
    * Download the client secret as a JSON and rename it to client-secrets.json
* Clone the tuberc repo
* Initialize the SQLlite DB
```
flask db init
flask db migrate
flask db upgrade
```
* Let it rip!
```
export FLASK_APP=main.py
flask run
```

## Libraries and Utils Used 

Please refer to requirements.txt. TuberC also uses Materialize CSS v1.

## Questions, Comments, Feedback?

Send them along at `arkits@outlook.com`
