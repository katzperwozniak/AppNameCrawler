import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Create
app_details = dict()


def map_app_numbers(app_number_list):

    print('Length of app number list is {}'.format(len(app_number_list)))
    f = open('app_dictionary.txt', mode='w+', newline='\n')
    i = 0
    for app_n in app_number_list:

        i += 1
        url = 'https://www.qimai.cn/app/rank/appid/{}'.format(app_n)
        print('{}. Got successfull response from: {}'.format(i, url))
        credentials = {'user-agent': 'MyCompany-Spider (kacper@mycompany.com)'}
        html_doc = requests.get(url, headers=credentials)
        parsed_website = BeautifulSoup(html_doc.text, 'lxml')

        app_name = parsed_website.find('div', {'class': 'appname'}).text
        app_details[app_n] = ".".join(re.findall('\\w+', app_name))

        app = "-".join([str(app_n), str(app_details[app_n])])
        print(app)
        f.write(str(app))
        f.write('\n')

    f.close()


number_list = pd.read_csv('app_id_list.csv')
dictionary = map_app_numbers(number_list.unique_id)
