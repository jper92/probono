#!/usr/bin/python
# -*- encoding:UTF-8 -*-

# Conexión a linkedin.
import oauth2 as oauth
import urlparse
from xml.dom.minidom import parseString
 
# Llaves de la aplicación en LinkedIn
consumer_key           = "lj807j9heurb"
consumer_secret        = "VlBCQxt8ocp54MJn"
consumer = oauth.Consumer(consumer_key, consumer_secret)

request_token_url      = 'https://api.linkedin.com/uas/oauth/requestToken?scope=r_basicprofile+r_emailaddress+r_fullprofile+r_contactinfo'
access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
url = "https://api.linkedin.com/v1/people/~:(id,first-name,last-name,email-address,date-of-birth,main-address)"

# Devuelve los tokens que identificarán al usuario
def requestToken():
	client = oauth.Client(consumer)
	resp, content = client.request(request_token_url, "POST")
	if resp['status'] != '200':
		raise Exception("Invalid response %s." % resp['status'])
	request_token = dict(urlparse.parse_qsl(content))
	authorize_url =      'https://api.linkedin.com/uas/oauth/authorize'
	return "<input type='hidden' name='token1' value= '" + request_token['oauth_token'] + "' >\n<input type='hidden' name='token2' value='" + request_token['oauth_token_secret'] + "'>" + "<a role='button' class='btn' href='" + authorize_url + "?oauth_token=" + request_token['oauth_token'] + "' target='_blank'>Ir a LinkedIn</a><input type='text' name='pin' placeholder='Ingrese el PIN de verificación'> <input type='submit' name='pin_submit' value='Verificar PIN'>"
	
	#return "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
	
"""	print "Go to the following link in your browser:"
	print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
	print 
"""

# Devuelve los datos de LinkedIn para el usuario por medio de los tokens y el pin de verificación
def getAccess(pin, oauth_token, oauth_token_secret):
	request_token = {'oauth_token': oauth_token, 'oauth_token_secret':oauth_token_secret}
	oauth_verifier = pin
	token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)
	resp, content = client.request(access_token_url, "POST")
	access_token = dict(urlparse.parse_qsl(content))
	print "    - oauth_token        = %s" % access_token['oauth_token']
	print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
	resp, content = client.request(url)
	#dom = parseString(content)
	return content
	"""return {'first-name': dom.getElementsByTagName('first-name')[0].childNodes[0].data, 'last-name': dom.getElementsByTagName('last-name')[0].childNodes[0].data,
			'year': dom.getElementsByTagName('year')[0].childNodes[0].data, 'month':dom.getElementsByTagName('month')[0].childNodes[0].data,
			'day': dom.getElementsByTagName('day')[0].childNodes[0].data, 'e-mail': dom.getElementsByTagName('email-address')[0].childNodes[0].data
			}
	"""

def hola():
	return '<p>Hola</p>'
