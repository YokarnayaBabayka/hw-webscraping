import requests
import bs4
import fake_headers
import json
from pprint import pprint

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'  # вводим адрес сайта
url = 'https://spb.hh.ru/search/vacancy?text=python%2C+django%2C+flask&salary=&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'

def gen_headers():
    headers_gen = fake_headers.Headers(os='win', browser='chrome')
    return headers_gen.generate()


response = requests.get(url, headers=gen_headers())  # выкачиваем нужную страницу
print(response.status_code)
main_html = response.text  # вытаскиваем из него текст
main_page = bs4.BeautifulSoup(main_html, 'lxml')  # закидываем в суп

vacancys_list_tag = main_page.find("div", id="a11y-main-content")  # поле вакансий
div_tags = vacancys_list_tag.find_all('div')

vacancys_data_tags = []  # карточки вакансий

for div in div_tags:
    if div.get('class') == ["vacancy-serp-item-body"]:
        vacancys_data_tags.append(div)

vacancys_data = []

for vacancy_tag in vacancys_data_tags:
    # ссылка
    a_tag = vacancy_tag.find('a', class_="bloko-link")
    # название вакансии
    name_span_tag = a_tag.find('span', class_="serp-item__title-link serp-item__title")
    # зарплата
    salary_span_tag = vacancy_tag.find('span', class_="bloko-header-section-2")
    # компания
    company_div_tag = vacancy_tag.find('div', class_="vacancy-serp-item__meta-info-company")
    company_span_tag = company_div_tag.find('span')
    # город
    city_div_tag = vacancy_tag.find_all('div', class_="bloko-text")[1]

    header = name_span_tag.text
    link = a_tag['href']
    if salary_span_tag:
        salary = salary_span_tag.text
        salary = salary.replace('\u202f', ' ')
    else:
        salary = 'не указано'
    company = company_span_tag.text.replace('\xa0', ' ')
    city = city_div_tag.text.replace('\xa0', ' ')

    vacancys_data.append({
        'header': header,
        'link': link,
        'salary': salary,
        'company': company,
        'city': city
    })

pprint(vacancys_data, sort_dicts=False)

with open('vacancys_data.txt', 'w', encoding='utf-8') as outfile:
    json.dump(vacancys_data, outfile, ensure_ascii=False)

