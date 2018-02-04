# encoding: utf-8
import json
from io import BytesIO
import requests


def get_web_image(url):
    """
    Get image bytes by url
    """
    r = requests.get(url)
    image = BytesIO(r.content)
    return image


def get_vk_credentials(filename='vk_credentials.json'):
    """
    Get credentials from a file or from console input
    """
    try:
        with open(filename, 'r') as f:
            credentials = json.load(f)
            login, password = credentials['login'], credentials['password']
    except (FileNotFoundError, KeyError):
        login, password = input('Enter VK login: '), input('Enter VK password: ')
    return login, password


def get_scrapinghub_credentials(filename='scrapinghub_credentials.json'):
    """
    Get credentials from a file or from console input
    """
    try:
        with open(filename, 'r') as f:
            credentials = json.load(f)
            api_key = credentials['api_key']
    except (FileNotFoundError, KeyError):
        api_key = input('Enter Scrapinghub API key: ')
    return api_key


def get_photos():
    pass