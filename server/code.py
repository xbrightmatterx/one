import urllib, urllib2, collections, hmac, binascii, time, random, os, sys, urlparse
from auth import *
from hashlib import sha1
from flask import Flask, redirect, request, session

#Twitter OAuth Variables
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET']

app = Flask(__name__, static_folder='../client')
print consumer_key
print consumer_secret
@app.route('/')
def home():
  return app.send_static_file('index.html')
 
@app.route('/<path:path>')
def static_prox(path):
  return app.send_static_file(path)

@app.route('/tweetsfeed')
def authenticate():
	# session.clear()
	# session['oauth_secret'] = ''
	print("stuff")
	# requestParams = {
	# 	"oauth_callback" : "http://127.0.0.1:5000/#/feed",
	# 	"oauth_consumer_key" : consumer_key,
	# 	"oauth_nonce" : str(random.randint(1, 999999999)),
	# 	"oauth_signature_method" : "HMAC-SHA1",
	# 	"oauth_timestamp" : int(time.time()),
	# 	"oauth_version" : "1.0"
	# }

	# theSig = sign_request(requestParams, "POST", "https://api.twitter.com/oauth/request_token")
  
	# requestParams["oauth_signature"] = theSig
  
	# request = urllib2.Request("https://api.twitter.com/oauth/request_token", "")
	# request.add_header("Authorization", create_oauth_headers(requestParams))
	# try:
	# 	httpResponse = urllib2.urlopen(request)
	# except urllib2.HTTPError, e:
	# 	return e.read()

	# responseData = getParameters(httpResponse.read())

	# session['oauth_token'] = responseData['oauth_token']
	# session['oauth_secret'] = responseData['oauth_token_secret']

	# return redirect("https://api.twitter.com/oauth/authorize?oauth_token=" + session['oauth_token'])

@app.route('/authorised')
def authorised():

	if request.args.get('oauth_token', '') == session['oauth_token']:
		
		verifyRequestParams = {
			"oauth_consumer_key" : consumer_key,
			"oauth_nonce" : str(random.randint(1, 999999999)),
			"oauth_signature_method" : "HMAC-SHA1",
			"oauth_timestamp" : int(time.time()),
			"oauth_version" : "1.0",
			"oauth_token" : session['oauth_token']
		}

		signVerification = sign_request(verifyRequestParams, "POST", "https://api.twitter.com/oauth/access_token")

		verifyRequestParams["oauth_signature"] = signVerification

		verifyRequest = urllib2.Request("https://api.twitter.com/oauth/access_token", "oauth_verifier=" + request.args.get('oauth_verifier'))
		verifyRequest.add_header("Authorization", create_oauth_headers(verifyRequestParams))
		
		try:
			httpResponse = urllib2.urlopen(verifyRequest)
		except urllib2.HTTPError, e:
			return e.read()

		responseData = getParameters(httpResponse.read())

		session['oauth_token'] = responseData["oauth_token"]
  	redirect("http://127.0.0.1:5000/#/feed")
  	print "hey we got authoed" + session['oauth_token']
  	print responseData
	return "Authorised " + session['oauth_token']

def getParameters(paramString):

	paramString = paramString.split("&")

	pDict = {}

	for parameter in paramString:
		parameter = parameter.split("=")

		pDict[parameter[0]] = parameter[1]

	return pDict

def sign_request(parameters, method, baseURL):

	baseURL = urllib.quote(baseURL, '')

	p = collections.OrderedDict(sorted(parameters.items(), key=lambda t: t[0]))

	requestString = method + "&" + baseURL + "&"
	parameterString = ""

	for idx, key in enumerate(p.keys()):
		paramString = key + "=" + urllib.quote(str(p[key]), '')
		if idx < len(p.keys()) - 1:
			paramString += "&"

		parameterString += paramString

	result = requestString + urllib.quote(parameterString, '')

	signingKey = consumer_secret + "&" + session['oauth_secret']

	print signingKey

	hashed = hmac.new(signingKey, result, sha1)
	signature = binascii.b2a_base64(hashed.digest())[:-1]

	return signature

def create_oauth_headers(oauthParams):
	
	oauthp = collections.OrderedDict(sorted(oauthParams.items(), key=lambda t: t[0]))

	headerString = "OAuth "

	for idx, key in enumerate(oauthp):
		hString = key + "=\"" + urllib.quote(str(oauthp[key]), '') + "\""
		if idx < len(oauthp.keys()) - 1:
			hString += ","

		headerString += hString

	return headerString

if __name__ == '__main__':
	
	#app.secret_key = 'R4nDOMCRypt0gr4ph1cK3yf0R5355i0N'
	app.run()