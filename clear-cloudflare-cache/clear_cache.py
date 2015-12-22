import os
import requests
import json
import yaml
import logging

LOG_FORMAT = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
BASE_DIR = os.path.dirname((__file__))
YAML_CFG = {}

with open(os.path.join(BASE_DIR, 'cloudflare.yaml')) as fp:
    YAML_CFG = yaml.load(fp)

ZONE = YAML_CFG['config']['zone_id']
HEADERS = {'X-Auth-Email': YAML_CFG['config']['email'],
           'X-Auth-Key': YAML_CFG['config']['api_key'],
           'Content-Type': 'application/json'}
DATA = {'purge_everything': True}
URL = 'https://api.cloudflare.com/client/v4/zones/' + ZONE + '/purge_cache'


def main():
    r = requests.api.delete(URL, headers=HEADERS, data=json.dumps(DATA))
    a = json.loads(r.content)
    if a['success'] is True:
        logging.info('Cache cleared')


if __name__ == '__main__':
    main()
