import requests
import re

def solve_lab(session, domain):
    data = {'username': 'carlos', 'password': 'montoya'}
    r = session.post(domain + '/login', data=data)
    r = session.get(domain + '/my-account')
    return

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
        solve_lab(session, domain)
        verify(session, domain)
    except requests.exceptions.ConnectionError:
        print('Connection Error. Please check your network connection.')