from bs4 import BeautifulSoup
import requests
from PyInquirer import style_from_dict, Token, prompt, Separator
import csv

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'list',
        'message': 'Select year',
        'name': 'year',
        'choices': [
            Separator(),
            {
                'name': '2021'
            },
            {
                'name': '2020'
            },
            {
                'name': '2019'
            },
            {
                'name': '2018'
            },
            {
                'name': '2017'
            },
            {
                'name': '2016'
            }
        ]
    }
]

answers = prompt(questions, style=style)
year = answers['year']

csvfile = open(year+'.csv', 'w')
fieldnames = ['Organisation', 'Description', 'Category',
              'Tech Stack', 'Tags', 'Idea List', 'IRC Channel', 'Org Page']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

source_url = 'https://summerofcode.withgoogle.com/archive/'+year+'/organizations/'
source = requests.get(source_url)

soup = BeautifulSoup(source.text, 'html.parser')

for org in soup.find_all('li', class_='organization-card__container'):
    org_name = org.find('h4', class_='organization-card__name').text
    print(org_name)
    org_desc = org.find('div', class_='organization-card__tagline').text
    print(org_desc)
    org_url = 'https://summerofcode.withgoogle.com'+org.a['href']
    org_source = requests.get(org_url)
    org_soup = BeautifulSoup(org_source.text, 'html.parser')
    technologies = org_soup.find_all(
        'li', class_='organization__tag organization__tag--technology')
    tech_list = []
    for tech in technologies:
        tech_list.append(tech.text)
    print(tech_list)
    category = org_soup.find(
        'li', class_='organization__tag organization__tag--category').text
    print(category)
    tags = org_soup.find_all(
        'li', class_="organization__tag organization__tag--topic")
    tag_list = []
    for tag in tags:
        tag_list.append(tag.text)
    print(tag_list)
    ideas = org_soup.find(
        'div', class_="org__button-container")
    ideas = str(ideas)
    ideas = ideas.split(' ')
    ideas = ideas[4].split('"')[1]
    print(ideas)
    irc = org_soup.find('div', class_='org__meta')
    irc = str(irc).split('org__meta-button')[1].split('"')[2]
    print(irc)
    print(org_url)
    writer.writerow({'Organisation': org_name, 'Description': org_desc, 'Category': category,
                     'Tech Stack': tech_list, 'Tags': tag_list, 'Idea List': ideas, 'IRC Channel': irc, 'Org Page': org_url})
    print('-------------------------------------------------------------------------------------------')
    print()

csvfile.close()