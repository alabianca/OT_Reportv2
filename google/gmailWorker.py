from threading import Thread
from google.gmailApi import GmailApi



class GmailWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.gmail = GmailApi()

    def run(self):
        while True:
            message_id,parse = self.queue.get()

            content = self.gmail.get_message(message_id)

            parse(content,message_id)

            self.queue.task_done()
