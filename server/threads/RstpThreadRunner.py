from threading import Thread


class RstpThreadRunner(object):

    def __init__(self):
        self.threads_id = dict()
        self.last_udp_stream_thread = None

    def run_rstp_thread(self, thread: Thread, connect_url: str):
        thread_name = str(connect_url)
        thread.setName(thread_name)
        self.threads_id[thread_name] = thread
        thread.start()
        print('start thread ' + 'thread for ' + thread_name)

    def set_upd_stream(self, thread_name) -> str:
        if self.last_udp_stream_thread is not None:
            self.last_udp_stream_thread.udp_stream = False
        stream_thread = self.threads_id.get(thread_name)
        if stream_thread is not None:
            stream_thread.udp_stream = True
            self.last_udp_stream_thread = stream_thread
            return 'OK'
        else:
            print('cant find this thread ' + str(thread_name))
            return 'cant find this thread ' + str(thread_name)


    def stop_rstp_thread(self, thread_name):
        self.threads_id.get(thread_name).stop()