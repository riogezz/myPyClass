#!/usr/bin/env python3
# -*- coding=utf-8 -*-


"""
scheduler class based on python schedule
"""


from elasticsearch import Elasticsearch
import logging
from retrying import retry


class Elasticsearch(Elasticsearch):
    logging.getLogger(__name__)
    def __init__(self, *args, **kwargs):
        try:
            return super(Elasticsearch, self).__init__(*args, **kwargs)
        except Exception as e:
            logging.critical(str(e))
            raise
    
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def write(self, index_name, index_type, data, index_id=None ):
        try:
            self.indices.create(index=index_name, ignore=400)
            if isinstance(data, list):
                for i in range(0,len(data)):
                    if index_id==None:
                        self.index(index=index_name, doc_type=index_type, body={'doc': data[i]})                    
                        logging.debug(f"writing to {index_name}, {index_type} with data: {data[i]}")
                    else:
                        self.update(index=index_name, doc_type=index_type, id=index_id[i], body={'doc': data[i], 'doc_as_upsert': True})
                        logging.debug(f"writing to {index_name}, {index_type}, id: {index_id[i]} with data: {data[i]}")
            else:
                if index_id==None:
                    self.index(index=index_name, doc_type=index_type, body={'doc': data})                    
                    logging.debug(f"writing to {index_name}, {index_type} with data: {data}")
                else:
                    self.update(index=index_name, doc_type=index_type, id=index_id, body={'doc': data, 'doc_as_upsert': True})
                    logging.debug(f"writing to {index_name}, {index_type}, id: {index_id} with data: {data}")
        except Exception as e:
            logging.error(str(e))

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def read(self, index_name, query):
        try:
            return self.search(index=index_name, body=query)
        except Exception as e:
            logging.error(str(e))
    
    @staticmethod        
    def return_sources(data):
        data_array = data['hits']['hits']
        output = []
        for i in range(1, len(data_array)):
            output.append(data_array[i]['_source'])
        return output
    
    