#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
general utils
- load and munchify files 
- filter list/dicts/strings
- loop scheduling

"""
from munch import munchify
from datetime import datetime
import os.path
import json
import yaml
import re
import logging




class utils():
    logging.getLogger(__name__)

    @staticmethod
    def readFile(filename):
        """
        Reads a configuration file and outputs its content in munchify styleself.
        Actually it could read YAML (yaml/yml extension) and JSON (json extension) ZipFile The class for reading and writing ZIP files.  See section 
        
        Parameters
        ----------
        filename : filename path
        """
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
            logging.error(str(e))

    @staticmethod
    def readJSON(filename):
        try:
            with open(filename) as f:
                return json.load(f)
        except Exception as e:
            logging.error(str(e))
    
    @staticmethod
    def convertedFile(filename):
        try:
            return munchify(__class__.readFile(filename))
        except Exception as e:
            logging.error(str(e))

    @staticmethod
    def applyFilter(inputA, filterlist):
        try: 
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
        except Exception as e:
            logging.error(str(e))
            
            
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