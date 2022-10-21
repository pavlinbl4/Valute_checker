import requests
import json

url_RBK = 'https://cash.rbc.ru/cash/json/cash_rates/?city=2&currency=3&deal=buy&amount=1000&'


def get_html(url):
    req = requests.get(url)
    return req.text

def valuta_rbk():
    rezult = json.loads(get_html(url_RBK))
    all_banks = {}
    for i in range(len(rezult['banks'])):
        name = rezult['banks'][i]['name']
        try:
            metro = rezult['banks'][i]['metro'][0][0]
        except TypeError:
            metro = "no information"
        phone = rezult['banks'][i]['phone']
        sell_price = float(rezult['banks'][i]['rate']['sell'])
        all_banks[sell_price] = [name, metro, phone]

    message_line = str()
    for x in range(5):
        message_line += str(sorted(all_banks)[x]) + '--' + " ".join(all_banks[sorted(all_banks)[x]])  + '\n'
    print(message_line)

if __name__ == '__main__':
    valuta_rbk()
