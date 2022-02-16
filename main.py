import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

def link(driver, page, links, l):
    p = '?p='
    url = (f'{l}{p}{str(page)}')
    driver.get(url)

    it = driver.find_elements_by_class_name('ProductCardHorizontal__header-block')
    for item in it:
        link = item.find_element(By.CLASS_NAME, 'Link_type_default').get_attribute('href')
        links.append(link)

    if links == []:
        it = driver.find_elements_by_class_name('ProductCardVerticalLayout__header')
        for item in it:
            link = item.find_element(By.CLASS_NAME, 'Link_type_default').get_attribute('href')
            links.append(link)

    print(links)

def info(driver, links, total):
    for link in links:
        driver.get(link)

        x = []
        try:
            x.append({
                'title': driver.find_element(By.XPATH, "//h1[@class='Heading Heading_level_1 ProductHeader__title']").text,
                'price': driver.find_element(By.CLASS_NAME, "ProductHeader__price-default_current-price").text,
                'product_id': driver.find_element(By.XPATH, "//div[@class='ProductHeader__product-id']").text.replace('Код товара: ', ''),
                'estimation': driver.find_element(By.CLASS_NAME, "js--IconWithCount__count").text,
                'link': link
            })

        except Exception:
            x.append({
                'title': driver.find_element(By.XPATH, "//h1[@class='Heading Heading_level_1 ProductHeader__title']").text,
                'price': driver.find_element(By.CLASS_NAME, "ProductHeader__price-default_current-price").text,
                'product_id': driver.find_element(By.XPATH, "//div[@class='ProductHeader__product-id']").text.replace('Код товара: ', ''),
                'estimation': 'нету отзывов',
                'link': link
            })

        print(x)
        total.extend(x)

def save(x):
    with open('parser.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['название', 'цена', 'id', 'оценка', 'ссылка',])
        for dict in x:
            writer.writerow([dict['title'], dict['price'], dict['product_id'], dict['estimation'], dict['link']])

def parser():
    l = input('укажите ссылку ситилинка: ')
    pages = int(input('сколько страниц: '))
    driver = webdriver.Chrome()

    links = []
    for page in range(1, pages + 1):
        link(driver, page, links, l)

    total = []
    info(driver, links , total)


    save(total)
    os.startfile('parser.csv')

    driver.close()

parser()