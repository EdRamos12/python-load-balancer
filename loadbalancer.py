import os
import random
import requests
import yaml
from flask import Flask, request

loadbalancer = Flask(__name__)

def load_configuration(path):
  with open(path) as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
  return config

config = load_configuration('config.yaml')

@loadbalancer.route('/')
def router():
  # Load balance by Header
  host_header = request.headers['Host']
  for entry in config['hosts']:
    if host_header == entry['host']:
      response = requests.get(f'http://{random.choice(entry["servers"])}')
      return response.content, response.status_code

@loadbalancer.route('/<path>')
def path_router(path):
  # Load balance by Path
  for entry in config['paths']:
    if ('/' + path) == entry['path']:
      response = requests.get(f'http://{random.choice(entry["servers"])}')
      return response.content, response.status_code
  return 'Not Found', 404