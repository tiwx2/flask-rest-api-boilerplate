import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

debug_logger = logging.getLogger('debug_logger')
debug_logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler(os.path.join(basedir, 'debug.log'))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
debug_logger.addHandler(fileHandler)