# Libraries
import re
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

# Create app_details dictionary
app_details = dict()

# Read app_id file
number_list = pd.read_csv('app_id_list.csv')


def map_app_numbers(app_number_list, n):

    f = open('app_dict_{}.csv'.format(n), mode='w+', newline='\n')
    print('Length of app number list is {}'.format(len(app_number_list)))
    i = 0

    for app_n in app_number_list:

        try:

            # enter website
            i += 1
            url = 'https://www.qimai.cn/app/rank/appid/{}'.format(app_n)
            print('{}. Got successfull response from: {}'.format(i, url))

            # send user agent, read and parse website
            cred = {'user-agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; \
            +http://www.baidu.com/search/spider.html)'}
            html_doc = requests.get(url, headers=cred)
            parsed_website = BeautifulSoup(html_doc.text, 'lxml')

            # find appname within source code
            app_name = parsed_website.find('div', {'class': 'appname'}).text
            app_details[app_n] = ".".join(re.findall('\\w+', app_name))

            # merge app number and app name and save to the file
            app = "-".join([str(app_n), str(app_details[app_n])])
            f.write(str(app) + '\n')
            time.sleep(1.0)
            print(app)

        except ConnectionResetError:
            print('ConnectionResetError occured')
            time.sleep(30.0)
            continue

    f.close()


for i in range(50):
    number_list = pd.read_csv('app{}'.format(i))
    print(number_list)
    map_app_numbers(number_list.unique_id, i)
    time.sleep(60.0)
