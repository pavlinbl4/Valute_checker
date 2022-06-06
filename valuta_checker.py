from bs4 import BeautifulSoup
import requests
import datetime
import csv
import os
from dotenv import load_dotenv
from os import getenv

load_dotenv()
old_token = getenv('old_token')
channel_id = getenv('channel_id')

url = 'http://valuta812.ru'
columns_name = ["Date", "Price"]
file_name = 'currency_history'
csv_file_path = f'/Volumes/big4photo/Documents/Инвестиции/{file_name}.csv'

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
        csv_writer([datetime.datetime.now(), get_data(get_html())])


def get_html():
    req = requests.get(url)
    return req.text


def get_data(html):  # функция парсящая сайт по созданному запросу и возвращающая информацию
    soup = BeautifulSoup(html, 'lxml')
    return soup.find(class_="cours-table").find(course_flag="usd_sell_from_10000").text


if __name__ == '__main__':
    usd_sell = get_data(get_html())
    notification(usd_sell)
    send_telegram(f'Dollar - {usd_sell}')
    csv_writer([datetime.datetime.now(), usd_sell])
