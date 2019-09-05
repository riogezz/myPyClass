import sched
import time
import logging

class scheduler():

    logging.getLogger(__name__)
    
    def __init__(self):
        self.schedule = sched.scheduler(time.time, time.sleep)

    def add(self, action, time=None, delay=None, priority=1, argument=(), kwargs={}):
        try:
            if delay != None:
                self.schedule.enter(int(delay), int(priority), action, argument, kwargs)
            elif time != None:
                self.schedule.enterabs(int(time), int(priority), action, argument, kwargs)
            else:
                self.schedule.enter(1, int(priority), action, argument, kwargs)
        except Exception as e:
            logging.error(f"while adding schedule {action} occurred: {e}")

    def run(self):
        try:
            self.schedule.run()
        except Exception as e:
            logging.error(f"while running scheduler, occurred: {e}")

    def list(self):
        try:
            return self.schedule.queue
        except Exception as e:
            logging.error(f"while listing schedule queue, occurred {e}")


