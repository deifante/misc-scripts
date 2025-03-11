import threading, datetime

class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print '%s says Hello World @ time :%s' % (self.getName(), now)

for i in range(2):
    t = ThreadClass()
    t.start()
