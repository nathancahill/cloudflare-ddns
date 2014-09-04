import socket
import pydash as _
import requests

KEY = '<cloudflare api key>'
EMAIL = '<cloudflare email address>'
DOMAIN = '<domain>'  # nathancahill.com
SUBDOMAIN = '<subdomain>'  # home
LOCAL = '<local ip address>'  # 192.168.0.3

data = dict(
        a='rec_load_all',
        tkn=KEY,
        email=EMAIL,
        z=DOMAIN
    )

res = requests.post('https://www.cloudflare.com/api_json.html', data=data)
records = res.json()['response']['recs']['objs']

home =  _.select(records, dict(name='%s.%s' % (SUBDOMAIN, DOMAIN)))[0]

if socket.gethostbyname(socket.gethostname()) != LOCAL:
    return

ip = requests.get('http://httpbin.org/ip').json()['origin']

data = dict(
        a='rec_edit',
        tkn=KEY,
        email=EMAIL,
        z=DOMAIN,
        id=home['rec_id'],
        type='A',
        name=SUBDOMAIN,
        content=ip,
        ttl='1'
    )

requests.post('https://www.cloudflare.com/api_json.html', data=data)
