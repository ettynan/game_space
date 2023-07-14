'''Logger model for logging information '''
import logging
import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')

logging.config.fileConfig(log_file_path)
#logging.info('this is the root logger')
# instantiates it
def get_logger(nom):
    '''returns a logger for the module that called the function'''
    return logging.getLogger(nom)