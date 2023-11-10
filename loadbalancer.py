import random
import requests
import yaml
from flask import Flask, request
from itertools import cycle

loadbalancer = Flask(__name__)

def load_configuration(path):
  with open(path) as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
  return config

config = load_configuration('config.yaml')

if config['method'] == 'host':
  @loadbalancer.route('/')
  def router():
    # Load balance by Header
    host_header = request.headers['Host']
    for entry in config['hosts']:
      if host_header == entry['host']:
        response = requests.get(f'http://{random.choice(entry["servers"])}')
        return response.content, response.status_code

if config['method'] == 'path':
  @loadbalancer.route('/<path>')
  def path_router(path):
    # Load balance by Path
    for entry in config['paths']:
      if ('/' + path) == entry['path']:
        response = requests.get(f'http://{random.choice(entry["servers"])}')
        return response.content, response.status_code
    return 'Not Found', 404
  
if config['method'] == 'no-content':
  servers = config['no-content']['servers']
  ITER = cycle(servers)
  def round_robin(iter):
      # round_robin([A, B, C, D]) --> A B C D A B C D A B C D ...
      return next(iter)

  @loadbalancer.route('/')
  def router():
    algorithm = config['no-content']['algorithm']

    if algorithm == 'random':
        return random.choice(servers)
    elif algorithm == 'round robin':
        return round_robin(ITER)
    else:
        raise Exception('unknown algorithm: %s' % algorithm)