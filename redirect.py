# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Android Issue Tracker Redirect
"""

PROJECT = 'http://code.google.com/p/android'

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def _CreateApplication():
  return webapp.WSGIApplication([
    (r'^/(\d+)$',  RedirectExistingIssue),
    (r'^/new$',    RedirectNewIssue),
    (r'^/entry$',  RedirectNewIssue),
    (r'^/create$', RedirectNewIssue),
    (r'^/list$',   RedirectList),
    (r'^/',        RedirectList),
    (r'^/.*',      PageNotFound),
  ],
  debug=False)

class RedirectHandler(webapp.RequestHandler):
  def issue(self, rest):
    self.redirect('%s/issues/%s' % (PROJECT, rest), permanent=True)

class RedirectExistingIssue(RedirectHandler):
  def get(self, id):
    self.issue('detail?id=%s' % id)

class RedirectNewIssue(RedirectHandler):
  def get(self):
    self.issue('entry')

class RedirectList(RedirectHandler):
  def get(self):
    self.issue('list')

class PageNotFound(webapp.RequestHandler):
  def get(self):
    self.response.set_status(404)
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write("""<html>
<head>
  <title>Not Found</title>
</head>
<body>
<h1>Not Found</h1>
<p>The request resource is not available.</p>
<p>Try searching the <a href="%s/issues/list">active issue list</a>.</p>
</html>
""" % PROJECT)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  application = _CreateApplication()
  main()
