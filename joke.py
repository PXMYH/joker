import requests
import logging
import os

URL = {
    'jod': 'https://api.jokes.one/jod',
    'chn': 'http://api.laifujiangxiaohua.com/open/xiaohua.json',
    'jdwx': 'https://way.jd.com/showapi/wbxh'
}
# FIXME: refactor how joke decoder factory works
url = URL['chn']
TYPE = 'CHN'
PARAMS = {'time': '2020-07-18', 'page': '1', 'maxResult': '1', 'showapi_sign': 'bd0592992b4d4050bfc927fe7a4db9f3',
          'appkey': os.environ['API_KEY']}


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
logger.info(f'{title}\n{content}')
print(f'{title}\n{content}')