import logging
import os
from datetime import datetime

import boto3
import requests

URL = {
    'jod': 'https://api.jokes.one/jod',
    'chn': 'http://api.laifujiangxiaohua.com/open/xiaohua.json',
    'jdwx': 'https://way.jd.com/showapi/wbxh'
}
# FIXME: refactor how joke decoder factory works
url = URL['chn']
TYPE = 'CHN'
TIME = datetime.date(datetime.now())
PARAMS = {'time': TIME, 'page': '1', 'maxResult': '1', 'showapi_sign': 'bd0592992b4d4050bfc927fe7a4db9f3',
          'appkey': os.environ['JD_API_KEY']}
TPOIC_ARN = 'arn:aws:sns:us-east-1:683778474338:joke'


class Joke:
    def __init__(self, url, params=None):
        self.url = url
        self.params = params

    def _request(self):
        response = requests.get(self.url, params=self.params).json()
        print(f'PARAMS = {PARAMS}, response = {response}')
        return response

    def joke_decoder(self, type, response):
        title, content = None, None

        if type == 'CHN':
            title, content = response[0]['title'], response[0]['content'].lstrip().rstrip().replace('<br/>',
                                                                                                              '')
        if type == 'JOD':
            joke = response['contents']['jokes'][0]['joke']
            title, content = joke['title'], joke['text']

        if type == 'JD':
            joke = response['result']['showapi_res_body']['contentlist'][0]
            title, content = joke['title'], joke['text']

        return title, content

    def get_joke(self):
        resp = self._request()
        title, content = self.joke_decoder(TYPE, resp)
        return title, content


logger = logging.getLogger('Joker')
title, content = Joke(url, params=PARAMS).get_joke()
joke = f'{title}\n{content}'
logger.info(f'{joke}')
print(f'{joke}')


# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_ACCESS_SECRET'],
    region_name=os.environ['AWS_REGION']
)

client.publish(TopicArn=TPOIC_ARN, Message=f"{joke}")
