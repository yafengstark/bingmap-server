# -*- coding: utf-8 -*-
"""下载某点的影像

"""

import requests
import os
import os.path
import csv
import QuadKey.quadkey as quadkey
import shutil
import imagestoosm.config as cfg
import secrets as secrets
from random import random
from time import sleep

import datetime

tileZoom = 18
rootTileDir = "tiles_12"

lat = 30
lon = 120



# MS doesn't want you hardcoding the URLs to the tile server. This request asks for the Aerial
# url template. Replace {quadkey}
response = requests.get("https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?key=%s" % (secrets.bingKey))

# 返回结果
data = response.json()
print(data)

input('go on')

# grabs the data we need from the response.
# 例如：http://ecn.{subdomain}.tiles.virtualearth.net/tiles/a{quadkey}.jpeg?g=7786
tileUrlTemplate = data['resourceSets'][0]['resources'][0]['imageUrl']
# 例如：['t0', 't1', 't2', 't3']
imageDomains = data['resourceSets'][0]['resources'][0]['imageUrlSubdomains']

if (os.path.exists(rootTileDir) == False):
    os.mkdir(rootTileDir)

bingTilesDir = os.path.join(rootTileDir, "bing")

if (os.path.exists(bingTilesDir) == False):
    os.mkdir(bingTilesDir)



"""get pixel coordinates"""
tilePixel = quadkey.TileSystem.geo_to_pixel((lat, lon), tileZoom)

print(tilePixel)

input('go on')

pixel = tilePixel
geo = quadkey.TileSystem.pixel_to_geo(pixel, tileZoom)
# 计算四键
qk = quadkey.from_geo(geo, tileZoom)

# 四键
qkStr = str(qk)

input('go on ')

#
qkArray = []
for index in range(tileZoom):
    qkArray.append(qkStr[0:index + 1])

print(qkArray)
# 存放文件夹路径
tileCacheDirArray = []
# 创建所需的文件夹
for i in range(len(qkArray)):

    sub_path = bingTilesDir
    for j in range(i):
        sub_path = os.path.join(sub_path, qkArray[j])
    # 创建必须的文件夹
    if (os.path.exists(sub_path) == False):
        os.mkdir(sub_path)
    # 下载影像
    tileFileName = "%s/%s.jpg" % (sub_path, qkArray[i])

    if (os.path.exists(tileFileName)):
        # already downloaded
        ok = 1
    else:
        print("T", end='')

        url = tileUrlTemplate.replace("{subdomain}", imageDomains[0])
        url = url.replace("{quadkey}", qkArray[i])
        url = "%s&key=%s" % (url, secrets.bingKey)

        response = requests.get(url, stream=True)
        print(response)

        with open(tileFileName, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        del response
        neededTile = True

print('下载完毕')

