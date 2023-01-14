import re
import requests
import csv
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/w/api.php'
params = {
    'action': 'parse',
    'page': 'Glossary_of_computer_science',
    'format': 'json',
    'prop': 'text',
    'redirects': ''
}

response = requests.get(url, params=params)
data = response.json()
raw_html = data['parse']['text']['*']
soup = BeautifulSoup(raw_html, 'html.parser')
terms = soup.find_all("dt", class_="glossary")
definitions = soup.find_all("dd", class_="glossary")

# TODO - handle the case where there are multiple definitions for a term
with open('data/glossary.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Term', 'Definition'])
    writer.writerow([terms[0].text, re.sub("\[[0-9]+\]", '',definitions[0].text)])
    writer.writerow([terms[1].text, re.sub("\[[0-9]+\]", '',definitions[1].text)])
    abstraction_def = re.sub("\[[0-9]+\]", '',definitions[2].text + definitions[3].text)
    writer.writerow([terms[2].text, abstraction_def])
    for term, defintion in zip(terms[4:], definitions[5:]):
        writer.writerow([term.text, re.sub("\[[0-9]+\]", '', defintion.text)])
