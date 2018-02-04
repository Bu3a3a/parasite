# encoding: utf-8
import json
import requests


BASE_SH_URL = 'https://storage.scrapinghub.com'


class ScrapingHub(object):

    def __init__(self, filename='scrapinghub_credentials.json', project_id=None):
        """
        Initialize with API key from a file or shell input
        """
        try:
            with open(filename, 'r') as f:
                credentials = json.load(f)
                api_key = credentials['api_key']
        except (FileNotFoundError, KeyError):
            api_key, project_id = input('Enter Scrapinghub API key: ')
        self.api_key = api_key

    def get_items(self, project_id, spider_id=None, job_id=None, resp_format='json', meta=None, nodata=None):
        """
        Get items from Scrapinghub project[/spider[/job]]

        Read more: https://doc.scrapinghub.com/api/items.html
        """
        url = '{base_url}/items/{project_id}/'.format(base_url=BASE_SH_URL, project_id=project_id)
        params = {'format': resp_format, 'meta': meta, 'nodata': nodata}

        if spider_id:
            url = '{url}{spider_id}/'.format(url=url, spider_id=spider_id)
            if job_id:
                url = '{url}{job_id}/'.format(url=url, job_id=job_id)

        return requests.get(url, params, auth=(self.api_key, ''))
