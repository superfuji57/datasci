import oauth2 as oauth
import urllib2 as urllib
import json

# See Assginment 6 instructions or README for how to get these credentials
access_token_key = "111099573-b5EEgsnN0KBrVa5uvSWg6ZFY6NAokapkqssPSR1E"
access_token_secret = "QM71YtGuHXsUhNE1epOzekmLJMMoHAVWUwDYp2RG8"

consumer_key = "KkAaImAb8fYPV5AKWkXJOw"
consumer_secret = "iSZw64eqCXybDnnuktH1nRu1LwhcXwvtvUDCNeUSJYo"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

# Get created tweets with language EN

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    line = line.strip()
    line_as_json = json.loads(line)
    # filters out delete tweets
    if 'text' in line_as_json:
        # filters out non-english tweets (not perfectly though)
        # we trust on twitter for that
        if 'lang' in line_as_json and line_as_json['lang'] == u'en':
            print line

if __name__ == '__main__':
  fetchsamples()
