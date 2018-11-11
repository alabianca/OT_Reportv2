
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google.config import OT_LABEL_ID

from google import Errors





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
        results = self.service.users().messages().list(userId="me", labelIds=[OT_LABEL_ID], q=query).execute()

        if(results['resultSizeEstimate'] == 0):
            raise Errors.NoMessagesFoundException(userId='me', labelIds=[OT_LABEL_ID], q=query)

        return results["messages"]

    def get_message(self, message_id):
        m_res = self.service.users().messages().get(id=message_id, userId='me').execute()

        return m_res



