# encoding: utf-8
# -*- coding: utf-8 -*-
import requests
from io import BytesIO
from PIL import Image

import vk_api

from utils import get_credentials, get_web_image


def main():
    """ Пример загрузки фото """

    login, password = get_credentials()
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    """ В VkUpload реализованы методы загрузки файлов в ВК
    """

    upload = vk_api.VkUpload(vk_session)

    photos = ['http://78.media.tumblr.com/097c0e97b2cc4e27d722a618a3dacd83/tumblr_omh9qftW0k1qezkcbo1_1280.jpg',]

    loaded_photos = upload.photo_wall(  # Подставьте свои данные
        [get_web_image(photo) for photo in photos],
        user_id=138330346,
        group_id=161443085
    )

    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in loaded_photos)

    # Добавление записи на стену
    vk_session.method("wall.post", {
        'owner_id': -161443085,  # Идентификаторы групп указываются со знаком минус
        'message': 'Test!',
        'attachment': attachment,
    })

if __name__ == '__main__':
    main()