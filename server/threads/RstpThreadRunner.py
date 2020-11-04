from threading import Thread


class RstpThreadRunner(object):

    def __init__(self):
        self.threads_id = dict()
        self.last_udp_stream_thread = None

    def run_rstp_thread(self, thread: Thread, connect_url: str):
        thread_name = str(connect_url)
        if thread_name in self.threads_id:
            print('Thread already exist')
            threads_in_dict = self.threads_id.get(thread_name)
            if threads_in_dict is None:
                self.create_thread(thread, thread_name)
                return 're-created'
            elif threads_in_dict.stopped():
                print('thread is runnning status - ' + str(threads_in_dict.stopped()))
                threads_in_dict.continue_thread()
                return 'stopped'
            else:
                print('try recreate exsisting thread')
                return 'try-recreate'
        else:
            self.create_thread(thread, thread_name)
            return 'created'

    def create_thread(self, thread, thread_name):
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
        if str(thread_name) in self.threads_id:
            self.threads_id.get(str(thread_name)).stop()
            return 'stopped'
        else:
            return 'not foud'


    def rtrsp_status(self) -> list:
        status = []
        for key, thread_value in self.threads_id.items():
            item_satus = {'thread_name': key, 'stopped': thread_value.stopped()}
            status.append(item_satus)

        return status

    def rtrsp_item_status(self, connect_url):
        name = 'null'
        status = 'null'
        if str(connect_url) in self.threads_id:
            thread = self.threads_id[str(connect_url)]
            name = connect_url
            status = thread.stopped()

        return {'thread_name': name, 'stopped': status}


    def reload_all_model(self):
        for key, thread_value in self.threads_id.items():
            thread_value.reload_model()

