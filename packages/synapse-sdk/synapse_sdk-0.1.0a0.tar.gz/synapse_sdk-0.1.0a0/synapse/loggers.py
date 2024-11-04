import datetime

from synapse.client import ClientError


class BaseLogger:
    progress_records = {}
    logs_queue = []
    client = None

    def __init__(self, client=None, task=None):
        self.client = client
        self.task = task

    def set_progress(self, current, total, category=''):
        percent = 0
        if total > 0:
            percent = (current / total) * 100
            percent = float(round(percent, 2))

        self.progress_records[category] = {'current': current, 'total': total, 'percent': percent}
        if self.task:
            self.task.update_state(state='PROGRESS', meta=self.progress_records)
        else:
            print(self.progress_records)

    def log(self, action, data):
        log = {'action': action, 'data': data, 'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}

        if self.client and self.task:
            log['task_id'] = self.task.request.id
            self.logs_queue.append(log)
            try:
                self.client.create_logs(self.logs_queue)
                self.logs_queue.clear()
            except ClientError as e:
                print(e)
        else:
            print(log)


class ConsoleLogger(BaseLogger):
    def log(self, action, data):
        print(action, data)


class SynapseLogger(BaseLogger):
    pass
