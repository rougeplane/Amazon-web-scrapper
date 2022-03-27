import csv
from re import template
from bs4 import BeautifulSoup
from selenium import webdriver


def get_url(search_term):
    template = 'https://www.amazon.sa/s?k={}&language=en_AE&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
   
    # add query term to url
    url = template.format(search_term)
    
    # add page query number
    url += '&page={}'

    return url

def extract_record(item):
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.sa' + atag.get('href') 
    try:
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text.replace('SAR', '').strip()
    except AttributeError:
        return    
    
    try:
        # rating
        rating = item.i.text
    except AttributeError:
        rating = ''
        
    result = (description, price, rating, url)
    
    return result

def amazon(search_term):
    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(PATH)

    records = []
    url = get_url(search_term)

    for page in range(1, 11):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    # save data to a csv file

    with open(r'C:\Users\anaje\projects\sel\bot\results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'URL'])
        writer.writerows(records)


term = input('What do you want: \n')

amazon(term)