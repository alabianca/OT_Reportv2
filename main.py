

from google.gmailApi import GmailApi
from google.Errors import NoMessagesFoundException
from google.gmailWorker import GmailWorker
from pytime import pytime
from queue import Queue
import HtmlReader
import base64
import json
import sys
import csv


#get the config
#currently only returns a json object with a single key
#the key will tell us when we last ran the program
def get_config():
    config_file = open('config.json')
    config = json.load(config_file)
    config_file.close();

    return config

def save_config(config):
    config_file = open('config.json', 'w')
    data = json.dumps(config)
    config_file.write(data)
    config_file.close()


#write the file to disk.
#name is generally of the format 'OTReport_<messageid>.html'
def write_to_html_file(html, name):
    path = "./htmlFilesv2/{}".format(name)
    file = open(path, "w")
    file.write(html)

    file.close()


#parses the raw byte content of an OT Email and writes it to ./htmlFilesv2 as an html file
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


#pulls the gmail data
#creates 4 worker threads to speed up the download and parsing of emails
def pull_gmail_data(query=''):



    gmail = GmailApi()
    queue = Queue()

    messages = gmail.get_ot_messages(query)

    #start 4 worker threads to speed up the download and parsing of emails
    for x in range(4):
        print('starting worker')
        worker = GmailWorker(queue)
        worker.daemon = True
        worker.start()


    #push task into the queue as a tuple
    #second item in the task tuple is always the parse_message function defined above
    for message in messages:
        id = message['id']
        queue.put((id,parse_message))


    queue.join() #wait

def do_latest(config):
    last_run = get_last_run_time(config['last_run'])
    query = 'after:{}'.format(last_run)

    pull_gmail_data(query)



def write_to_csv(events):
    with open('events.csv', 'w', newline='') as csvFile:
        field_names = ['calories', 'splat_pts', 'steps', 'date', 'time', 'coach', 'template_version', 'avg_heart_rate', 'peak_heart_rate']
        writer = csv.DictWriter(csvFile, fieldnames=field_names)

        writer.writeheader()

        for event in events:
            writer.writerow({
                'calories': event['calories'],
                'splat_pts': event['splat_pts'],
                'steps': event['steps'],
                'date': event['date'],
                'time': event['time'],
                'coach': event['coach'],
                'template_version': event['template_version'],
                'avg_heart_rate': event['avg_heart_rate'],
                'peak_heart_rate': event['peak_heart_rate']
            })


def main():

    config = get_config()
    flags = sys.argv

    pull_latest = False

    #get flags
    for flag in flags:
        if flag == '--latest':
            pull_latest = True


    query = ''

    #if we are only pulling the latest data find out when we ran the program last
    if pull_latest:
        last_run = get_last_run_time(config['last_run'])
        query = 'after:{}'.format(last_run)


    #try to find data
    try:
        pull_gmail_data(query)
        config['last_run'] = str(pytime.today())
        save_config(config)
    except NoMessagesFoundException as e:
        print(e)







    #read an html file now
    html = HtmlReader.HtmlReader()
    events = html.read_all('./htmlFilesv2/*.html')

    write_to_csv(events)




if __name__ == '__main__':
    main()