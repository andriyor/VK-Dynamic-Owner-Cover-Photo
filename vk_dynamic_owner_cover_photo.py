import time

import requests
import vk
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import grequests
from bs4 import BeautifulSoup

access_token = ''
session = vk.Session(access_token=access_token)
vkapi = vk.API(session, v='5.62', lang='ru')
serer_url = vkapi.photos.getOwnerCoverPhotoUploadServer(group_id=1)


def fetch_youtube_subscriber(page):
    soup = BeautifulSoup(page, 'html.parser')
    about_stat = soup.find_all("span", {"class": "about-stat"})
    ys, bl, jl, = map(lambda x: x.text, about_stat)
    ys = ys.split()[0]
    return ys


def fetch_twitter_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'}) \
        .find('span', {'class': 'ProfileNav-value'}).text
    return followers


def fetch_instagram_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    followers = soup.find("meta", property="og:description")["content"]
    followers = followers.split()[0]
    return followers


def fetch_facebook_followers(page):
    soup = BeautifulSoup(page, 'html.parser')
    desc = soup.find(attrs={"name": "description"})["content"]
    descl = desc.split()

    for i in descl:
        if i.isdigit():
            first_int = i
            break

    followers = ''
    for j in descl[descl.index(first_int):]:
        if j.isdigit():
            followers += j
        else:
            break
    return followers

handle = 'rozetked'

link_list = ["https://www.youtube.com/user/{}/about?hl=en".format(handle),
             "https://twitter.com/{}".format(handle),
             "https://www.instagram.com/{}".format(handle),
             "https://www.facebook.com/{}".format(handle)]

font = ImageFont.truetype("OpenSans-Italic.ttf", 30)
tcolor    = (244, 210, 77)
text_pos1 = (50, 10)
text_pos2 = (620, 10)
text_pos3 = (50, 100)
text_pos4 = (620, 100)
img = Image.open("templates.jpg")

while True:
    rs = (grequests.get(u) for u in link_list)
    y, t, i, f = list(map(lambda r: r.text, grequests.map(rs)))
    ys = fetch_youtube_subscriber(y)
    tf = fetch_twitter_followers(t)
    instagram_followers = fetch_instagram_followers(i)
    ff = fetch_facebook_followers(f)

    draw = ImageDraw.Draw(img)
    draw.text(text_pos1, "  {} \n YouTube".format(ys), fill=tcolor, font=font)
    draw.text(text_pos2, "   {} \n Twitter".format(tf), fill=tcolor, font=font)
    draw.text(text_pos3, "     {} \n Instagram".format(instagram_followers), fill=tcolor, font=font)
    draw.text(text_pos4, "     {} \n Facebook".format(ff), fill=tcolor, font=font)

    del draw
    img.save("result.png")

    files = {'photo': open('result.png', 'rb')}
    r = requests.post(serer_url['upload_url'], files=files).json()
    vkapi.photos.saveOwnerCoverPhoto(hash=r['hash'], photo=r['photo'])
    time.sleep(10)
