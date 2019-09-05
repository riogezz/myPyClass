import os.path
import logging
import json
import yaml
from munch import munchify
from datetime import datetime
import re
import sched
import time
import logging




class utils():
    logging.getLogger(__name__)

    @staticmethod
    def readFile(filename):
        extension = os.path.splitext(filename)[1][1:]
        if extension.lower() in ['yaml', 'yml']:
            return __class__.readYAML(filename)
        elif extension.lower() == 'json':
            return __class__.readJSON(filename)
        else:
            quit('file ' + filename + 'not valid')

    @staticmethod
    def readYAML(filename):
        try:
            with open(filename) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error("Error: "+str(e))

    @staticmethod
    def readJSON(filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except Exception as e:
            logging.error("Error: "+str(e))
    
    @staticmethod
    def convertedFile(filename):
        try:
            return munchify(__class__.readFile(filename))
        except Exception as e:
            logging.error("Error: "+str(e))

    @staticmethod
    def applyFilter(inputA, filterlist):
        output = []
        if isinstance(inputA, dict):
            inputlist = list(inputA.keys())
        elif isinstance(inputA, list):
            inputlist = inputA
        else:
            inputlist = list(inputA)
        if isinstance(filterlist, str):
            filterlist = list(filterlist)
        for f in filterlist:
            f1 = re.compile(f)
            output.extend(list(filter(f1.match, inputlist)))
        return output
    @staticmethod
    def loop(action, delay=1, argument=(), kwargs={}):
        try:
            s = scheduler()
            while True:
                logging.debug(f"LOOP {action} with {delay}s")
                s.add(action=action, delay=delay, argument=argument, kwargs=kwargs)
                logging.debug(f"LOOP {action} run")
                s.run()
        except Exception as e:
            logging.error(f"LOOP: {e}")

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


