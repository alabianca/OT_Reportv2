
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google.config import OT_LABEL_ID

from google import Errors

import glob


def load_already_parsed_message_ids():
    ids = {}
    gl = './htmlFilesv2/*.html'
    files = glob.glob(gl)

    for file in files:
        file = file.split('_')[1].split('.')[0]
        ids[file] = 1

    return ids




class GmailApi:
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

        store = file.Storage('token.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)

        self.service = build('gmail', 'v1', http=creds.authorize(Http()))


    def get_labels(self):
        results = self.service.users().labels().list(userId="me").execute()

        return results.get('labels', [])


    def get_ot_messages(self, query=''):
        no_new_messages = True

        #gets the ids of all messages that match the OT LabelId and provided query
        results = self.service.users().messages().list(userId="me", labelIds=[OT_LABEL_ID], q=query).execute()

        saved_templates = load_already_parsed_message_ids()

        #if no query is provided we default to pull all data
        if(query == ''):
            no_new_messages = False


        #find out the ids of messages that are saved locally
        for result in results['messages']:
            if(result['id'] not in saved_templates):
                no_new_messages = False


        #if no new messages are found in any case raise error to catch accordingly
        if(results['resultSizeEstimate'] == 0 or no_new_messages):
            raise Errors.NoMessagesFoundException(userId='me', labelIds=[OT_LABEL_ID], q=query)


        log_msg = "Found {} new OT Email(s).".format(len(results["messages"]))
        print(log_msg)


        return results["messages"]



    def get_message(self, message_id):
        m_res = self.service.users().messages().get(id=message_id, userId='me').execute()

        return m_res



