from .promise import Promise 
import os
from os import environ

__version__ = '0.0.2'

curr_loc = os.path.dirname(os.path.realpath(__file__))
set_cadna_env = curr_loc+'/cadna/'
environ["CADNA_PATH"] = set_cadna_env
