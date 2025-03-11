#!/usr/bin/env python
import Queue, threading, string, sys

from illustration_check import TeamsOracle

class ThreadCheck(threading.Thread):
    """Threaded ID check."""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            istock_id, local_teams_id = self.queue.get()
            to = TeamsOracle()
            teams_id = to.get_teams_id(istock_id)
            try:
                if int(local_teams_id) != int(teams_id):
                    print int(local_teams_id), int(teams_id)
            except ValueError:
                pass

            self.queue.task_done()

if __name__ == '__main__':
    queue = Queue.Queue()
    for i in range(15):
        t = ThreadCheck(queue)
        t.setDaemon(True)
        t.start()

    for line in sys.stdin:
        id_pair = string.split(string.strip(line))
        queue.put(id_pair)

    queue.join()

    print 'Done'
