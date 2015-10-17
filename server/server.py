# -*- coding: utf-8 -*-
import urlparse
import oauth2 as oauth
import os, sys
from auth import *
from flask import Flask, request, redirect

 
app = Flask(__name__, static_folder='../client')      
 
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET']

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'



# Step 1: Get a request token. This is a temporary token that is used for 
# having the user authorize an access token and to sign the request to obtain 
# said access token.

@app.route('/tweetsfeed')

def getTweets():
  consumer = oauth.Consumer(consumer_key, consumer_secret)
  client = oauth.Client(consumer)
  resp, content = client.request(request_token_url, "GET")
  if resp['status'] != '200':
      raise Exception("Invalid response %s." % resp['status'])

  request_token = dict(urlparse.parse_qsl(content))

  # print "Request Token:"
  # print "    - oauth_token        = %s" % request_token['oauth_token']
  # print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
  # print 

  # # Step 2: Redirect to the provider. Since this is a CLI script we do not 
  # # redirect. In a web application you would redirect the user to the URL
  # # below.

  # print "Go to the following link in your browser:"
  print "Location:%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
  # print 

  # After the user has granted access to you, the consumer, the provider will
  # redirect you to whatever URL you have told them to redirect to. You can 
  # usually define this in the oauth_callback argument as well.
  accepted = 'n'
  while accepted.lower() == 'n':
      accepted = raw_input('Have you authorized me? (y/n) ')
  oauth_verifier = raw_input('What is the PIN? ')

  # Step 3: Once the consumer has redirected the user back to the oauth_callback
  # URL you can request the access token the user has approved. You use the 
  # request token to sign this request. After this is done you throw away the
  # request token and use the access token returned. You should store this 
  # access token somewhere safe, like a database, for future use.
  token = oauth.Token(request_token['oauth_token'],
      request_token['oauth_token_secret'])
  token.set_verifier(oauth_verifier)
  client = oauth.Client(consumer, token)

  resp, content = client.request(access_token_url, "POST")
  access_token = dict(urlparse.parse_qsl(content))

  print "Access Token:"
  print "    - oauth_token        = %s" % access_token['oauth_token']
  print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
  print
  print "You may now access protected resources using the access tokens above." 
  print

  def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
      consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
      token = oauth.Token(key=key, secret=secret)
      client = oauth.Client(consumer, token)
      resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
      return content
   
  home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', access_token['oauth_token'], access_token['oauth_token_secret'])
  return home_timeline
@app.route('/')
def home():
  return app.send_static_file('index.html')
 
@app.route('/<path:path>')
def static_prox(path):
  return app.send_static_file(path)

if __name__ == '__main__':
  app.run()
