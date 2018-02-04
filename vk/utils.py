# encoding: utf-8
import json
from io import BytesIO
import requests


def is_sequence(arg):
    if isinstance(arg, str):
        return False
    elif hasattr(arg, "__iter__"):
        return True
    else:
        return False


def listify(arg):
    if is_sequence(arg) and not isinstance(arg, dict):
        return arg
    return [arg, ]


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
            login, password, user_id, group_id = credentials['login'], credentials['password'], \
                                                 credentials['user_id'], credentials['group_id']
    except (FileNotFoundError, KeyError):
        login, password, user_id, group_id = input('Enter VK login: '), input('Enter VK password: '), \
                                             input('Enter VK user_id: '), input('Enter VK group_id: ')
    return login, password, user_id, group_id


def get_scrapinghub_credentials(filename='scrapinghub_credentials.json'):
    """
    Get credentials from a file or from console input
    """
    try:
        with open(filename, 'r') as f:
            credentials = json.load(f)
            api_key = credentials['api_key']
    except (FileNotFoundError, KeyError):
        api_key = input('Enter ScrapingHub API key: ')
    return api_key