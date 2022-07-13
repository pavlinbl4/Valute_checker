from bs4 import BeautifulSoup
import requests
import datetime
import csv
import os
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
old_token = getenv('old_token')
channel_id = getenv('channel_id')

url_bank = 'http://valuta812.ru'
url_RBK = 'https://cash.rbc.ru/cash/json/cash_rates/?city=2&currency=3&deal=buy&amount=1000&'

columns_name = ["Date", "Price"]
file_name = 'currency_history'
csv_file_path = f'/Volumes/big4photo/Documents/Инвестиции/{file_name}.csv'


def valuta_rbk():
    rezult = json.loads(get_html(url_RBK))
    all_banks = {}
    for i in range(len(rezult['banks'])):
        name = rezult['banks'][i]['name']
        metro = rezult['banks'][i]['metro'][0][0]
        phone = rezult['banks'][i]['phone']
        sell_price = float(rezult['banks'][i]['rate']['sell'])
        all_banks[sell_price] = [name, metro, phone]

    message_line = str()
    for x in range(3):
        message_line += str(sorted(all_banks)[x]) + '--' + " ".join(all_banks[sorted(all_banks)[x]]) + '\n'

    # print(message_line)
    return message_line


def send_telegram(text: str):
    token = old_token
    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


def notification(message):
    title = "USD sell price"
    command = f'''
    osascript -e 'display notification "{message}" with title "{title}"'
    '''
    os.system(command)


def csv_writer(info):
    def write_csv_file():
        with open(csv_file_path, 'a') as input_file:
            writer = csv.writer(input_file)
            writer.writerow(info)

    if os.path.exists(csv_file_path):
        write_csv_file()
    else:
        info = columns_name
        write_csv_file()
        csv_writer([datetime.datetime.now(), get_data(get_html(url_bank))])


def get_html(url):
    req = requests.get(url)
    return req.text


def get_data(html):  # функция парсящая сайт по созданному запросу и возвращающая информацию
    soup = BeautifulSoup(html, 'lxml')
    return soup.find(class_="cours-table").find(course_flag="usd_sell_from_10000").text


if __name__ == '__main__':
    usd_sell = get_data(get_html(url_bank))
    rbk_data = valuta_rbk()
    # notification(usd_sell)
    send_telegram(f'Dollar - {usd_sell}\n{rbk_data}')
    csv_writer([datetime.datetime.now(), usd_sell])
