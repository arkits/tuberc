# TuberC
### 'TuberCulosis'

TuberC organizes your YouTube Subscriptions to give you videos from people you love.

## Setup

Following are the instruction to fork and setup TubeC by yourself.

* Setup a project on Google Cloud Platform - https://console.cloud.google.com/projectcreate
* From the API manager on Google Cloud Platform,
  * Enable the following APIs:
    * YouTube Data API v3	
    * Google Cloud Datastore API
    * YouTube Analytics API	
    * YouTube Reporting API
  * Create an OAuth Consent Screen
  * Create a OAuth 2.0 client ID credential, with the application type as a web application. Used for user account authorization.
    * Make sure you IP is listed in the Authorized redirect URIs
    * Download the client secret as a JSON and rename it to tuberc.json
  * Create an API key. Used for YouTube Data API.
* Install and setup gcloud sdk - https://cloud.google.com/sdk/docs/quickstarts
* Clone the tuberc repo

