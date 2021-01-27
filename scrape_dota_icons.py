from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os

local_image_folder = './dota_icons/'
if not os.path.exists(local_image_folder):
    os.makedirs(local_image_folder)

ability_icon_urls = ['https://dota2.gamepedia.com/Category:Ability_icons',
                     'https://dota2.gamepedia.com/Category:Ability_icons?filefrom=Fiery+Soul+icon.png#mw-category-media',
                     'https://dota2.gamepedia.com/Category:Ability_icons?filefrom=Plasma+Field+icon.png#mw-category-media',
                     'https://dota2.gamepedia.com/Category:Ability_icons?filefrom=Tree+Dance+icon.png#mw-category-media']

for ability_icon_url in ability_icon_urls:
    page = urlopen(ability_icon_url)
    soup_page = BeautifulSoup(page.read(), features="html.parser")
    all_thumbnails = soup_page.find_all('img')

    for thumbnail_container in all_thumbnails:
        # print(vars(thumbnail_container))  # for getting all possible choices
        image_url = thumbnail_container['src']
        # image source comes in this format:
        # https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6b/Acid_Spray_icon.png/revision/latest/scale-to-width-down/120?cb=20120801073343
        # we want to truncate it to this:
        # https://static.wikia.nocookie.net/dota2_gamepedia/images/6/6b/Acid_Spray_icon.png
        # in order to get the full detail
        image_url = image_url[:image_url.index('.png') + 4]
        image_name = thumbnail_container['alt']
        urlretrieve(image_url, local_image_folder + image_name.replace(' ', '_'))

