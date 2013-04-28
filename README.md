# What is this?
Google App Engine (GAE) sample for reading worksheet cells in Google Drive spreadsheet documents with OAuth 2.0, originally based on [google-api-python-client](http://code.google.com/p/google-api-python-client/) samples/appengine and modified.

* use virtualenv.
* use webapp2 and jinja2 instead of webapp
* use [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/) and [Google Drive API v2](https://developers.google.com/drive/v2/reference/) to get spreadsheet file list
* use [gdata-python-client](https://code.google.com/p/gdata-python-client/) and [Google Spreadsheets API v3](https://developers.google.com/google-apps/spreadsheets/?hl=ja) to get worksheet list and cell list

## OAuth2 configuration

* Create a GAE application at [GAE my applications](https://appengine.google.com/) page.
* Create a project at Google APIs console. See [Google Plus API Tutorial | w3resource](http://www.w3resource.com/API/google-plus/tutorial.php)
* Change status of Drive API to ON at the services page in Google APIs console.
* Create a client ID at the API Access page in Google APIs console.
    * Push the [Create an OAuth 2.0 client ID...] button.
    * Enter the product name and press the [Next] button.
    * In client ID settings, make sure the application type to be web application.
    * Change your site or hostname to
        * ```https://your_app_id_here.appspot.com``` (Replace ```your_app_id_here``` with your application identifier) for production
        * or ```http://localhost:8080``` for development
* Copy ```src/client_secrets.json.default``` to ```src/client_secrets.json```
  and edit these three lines:

```
    "client_id": "[[INSERT CLIENT ID HERE]]",
    "client_secret": "[[INSERT CLIENT SECRET HERE]]",
    "redirect_uris": [],
```

  Replace ```[[INSERT CLIENT ID HERE]]``` and ```[[INSERT CLIENT SECRET HERE]]``` with actual values.

redirect_uris example (Replace ```your_app_id_here``` with your application identifier):

```
    "redirect_uris": ["https://your_app_id_here.appspot.com/oauth2callback"],
```

When you run dev_appserver.py, set redirect_url to ```http://localhost:8080/oauth2callback```

## install python and google app engine sdk

On a mac, you can use homebrew.

```
brew install python
brew install google-app-engine
./virtual_env_setup.sh
```

## activate virtualenv

```
. bin/activate
```

## run dev server

```
dev_app_server.py src
```

Open http://localhost:8080 in your web browser.
