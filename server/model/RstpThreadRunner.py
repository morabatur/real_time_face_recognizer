from threading import Thread


class RstpThreadRunner(object):

    def __init__(self):
        self.threads_id = dict()

    def run_rstp_thread(self, thread: Thread, connect_url: str):
        self.threads_id[connect_url] = thread.start()
        print('self.threads_id')
        print(self.threads_id)
