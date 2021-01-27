from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os

local_image_folder = './hades_icons/'
if not os.path.exists(local_image_folder):
    os.makedirs(local_image_folder)

ability_icon_urls = ['https://hades.gamepedia.com/Aphrodite',
                     'https://hades.gamepedia.com/Ares',
                     'https://hades.gamepedia.com/Artemis',
                     'https://hades.gamepedia.com/Athena',
                     'https://hades.gamepedia.com/Chaos',
                     'https://hades.gamepedia.com/Demeter',
                     'https://hades.gamepedia.com/Dionysus',
                     'https://hades.gamepedia.com/Hermes',
                     'https://hades.gamepedia.com/Poseidon',
                     'https://hades.gamepedia.com/Zeus']

for ability_icon_url in ability_icon_urls:
    page = urlopen(ability_icon_url)
    soup_page = BeautifulSoup(page.read(), features="html.parser")
    all_thumbnails = soup_page.find_all('img')

    for thumbnail_container in all_thumbnails:
        try:
            # print(vars(thumbnail_container))  # for getting all possible choices
            image_url = thumbnail_container['src']
            # image source comes in this format:
            # https://static.wikia.nocookie.net/hades_gamepedia_en/images/e/e3/Heartbreak_Strike.png/revision/latest/scale-to-width-down/100?cb=20181213173756
            # we want to truncate it to this:
            # https://static.wikia.nocookie.net/hades_gamepedia_en/images/e/e3/Heartbreak_Strike.png
            # in order to get the full detail
            image_url = image_url[:image_url.index('.png') + 4]
            image_name = thumbnail_container['alt']
            if image_name is not '':
                urlretrieve(image_url, local_image_folder + image_name.replace(' ', '_'))
        except Exception as e:
            print(e)

