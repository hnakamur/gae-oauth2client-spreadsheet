#!/usr/bin/env python

# The MIT License (MIT)
# Copyright (c) 2013 Hiroaki Nakamura <hnakamur@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import httplib2
import logging
import os
import webapp2

from controllers.base import BaseHandler
from apiclient.discovery import build
from oauth2client.appengine import oauth2decorator_from_clientsecrets
from oauth2client.client import AccessTokenRefreshError
from oauth2client_gdata_bridge import OAuth2BearerToken
from gdata.spreadsheets.client import SpreadsheetsClient


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(os.path.dirname(__file__)),
    'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS

decorator = oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://spreadsheets.google.com/feeds"
    ],
    MISSING_CLIENT_SECRETS_MESSAGE)

def getSpreadsheetsClient():
  token = OAuth2BearerToken(decorator.credentials)
  return SpreadsheetsClient(auth_token=token)

class MainHandler(BaseHandler):

  @decorator.oauth_aware
  def get(self):
    variables = {
        'url': decorator.authorize_url(),
        'has_credentials': decorator.has_credentials()
        }
    self.render_response('grant.html', **variables)

SPREADSHEET_MIMETYPE = "application/vnd.google-apps.spreadsheet"

class SpreadsheetsHandler(BaseHandler):
  @decorator.oauth_required
  def get(self):
    try:
      http = decorator.http()
      service = build("drive", "v2", http=http)
      fields = "items(id,title,mimeType),nextLink,nextPageToken"
      list = service.files().list(fields=fields).execute(http)
      spreadsheets = [spreadsheet for spreadsheet in list["spreadsheets"]
        if spreadsheet["mimeType"] == SPREADSHEET_MIMETYPE]
      self.render_response('spreadsheets.html', spreadsheets=spreadsheets)
    except AccessTokenRefreshError:
      self.redirect('/')

class WorksheetsHandler(BaseHandler):
  @decorator.oauth_required
  def get(self, spreadsheet_key):
    try:
      feed = getSpreadsheetsClient().get_worksheets(spreadsheet_key)
      worksheets = [{'id': entry.get_worksheet_id(), 'title': entry.title.text}
        for entry in feed.entry]
      self.render_response('worksheets.html',
        spreadsheet_key=spreadsheet_key,
        worksheets=worksheets)
    except AccessTokenRefreshError:
      self.redirect('/')

class CellsHandler(BaseHandler):
  @decorator.oauth_required
  def get(self, spreadsheet_key, worksheet_id):
    try:
      feed = getSpreadsheetsClient().get_cells(spreadsheet_key, worksheet_id)
      cells = [{'title': entry.title.text, 'content': entry.content.text}
        for entry in feed.entry]
      self.render_response('cells.html', cells=cells)
    except AccessTokenRefreshError:
      self.redirect('/')

app = webapp2.WSGIApplication(
    [
     ('/', MainHandler),
     ('/spreadsheets', SpreadsheetsHandler),
     ('/spreadsheet/(\w+)/worksheets', WorksheetsHandler),
     ('/spreadsheet/(\w+)/(\w+)/cells', CellsHandler),
     (decorator.callback_path, decorator.callback_handler())
    ],
    debug=True)
