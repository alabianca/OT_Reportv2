

from google.gmailApi import GmailApi
from google.Errors import NoMessagesFoundException
from pytime import pytime
import base64
import json


def get_config():
    config_file = open('config.json')
    config = json.load(config_file)
    config_file.close();

    return config

def save_config(config):
    config_file = open('config.json', 'w')
    data = json.dumps(config)
    config_file.write(data)



def write_to_html_file(html, name):
    path = "./htmlFiles/{}".format(name)
    file = open(path, "w")
    file.write(html)

    file.close()


def parse_message(msg_json, msg_id):
    message_parts = msg_json["payload"]["parts"]

    for k in message_parts:

        for pi in k['parts']:
            data = pi['body']['data'] + "="
            result = base64.urlsafe_b64decode(data).decode()
            file_name = 'OTReport_{}.html'.format(msg_id)
            write_to_html_file(result, file_name)

def get_last_run_time(timestamp):
    yesterday = str(pytime.before(timestamp, '1d')).split(' ')[0]

    return yesterday

def pull_latest_gmail_data(config):

    last_run = get_last_run_time(config['last_run'])

    query = 'after:{}'.format(last_run)

    gmail = GmailApi()

    messages = gmail.get_ot_messages(query)

    for message in messages:
        id = message['id']
        m_res = gmail.get_message(id)

        parse_message(m_res, id)


def main():

    config = get_config()

    try:
        pull_latest_gmail_data(config)
        config['last_run'] = str(pytime.today())
        save_config(config)
    except NoMessagesFoundException as e:
        print(e)




if __name__ == '__main__':
    main()