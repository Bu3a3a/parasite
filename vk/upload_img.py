# encoding: utf-8
import json
import requests
from io import BytesIO
from PIL import Image

import vk_api

from utils import listify, get_vk_credentials, get_web_image
from scrapinghub import ScrapingHub


def main():

    login, password, user_id, group_id = get_vk_credentials()
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    upload = vk_api.VkUpload(vk_session)

    sh_api = ScrapingHub()
    items = sh_api.get_items(280377).json()
    items = sorted(items, key=lambda item: item['date'])    # Sort items by dates

    if not items:
        return

    # Get last scraped item
    try:
        with open('last_scraped_items.json', 'r') as f:
            last_scraped = json.load(f)
    except FileNotFoundError:
        last_scraped = dict()

    # Find a newer item than the last scraped one and assign it's value to last_scraped variable
    if not last_scraped or last_scraped['date'] >= items[-1]['date']:
        last_scraped = items[0]
    else:
        for item in items:
            if item['date'] > last_scraped['date']:
                last_scraped = item
                break

    # Load images to VK
    loaded_images = upload.photo_wall(
        [get_web_image(img) for img in listify(last_scraped['img'])],
        user_id=user_id,
        group_id=group_id
    )

    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in loaded_images)

    # Post to the wall
    vk_session.method("wall.post", {
        'owner_id': -group_id,  # Group ids must be negative
        'message': last_scraped['description'],
        'attachment': attachment,
    })

    with open('last_scraped_items.json', 'w') as f:
        json.dump(last_scraped, f)

if __name__ == '__main__':
    main()