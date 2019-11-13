# -*- coding: utf-8 -*-
"""下载区域影像
从第一层到指定层

多线程版

存储到sqlite中

"""

import requests
# python3的thread模块
import _thread
import random
import time
from random import random
import os.path
import QuadKey.quadkey as quadkey
import shutil
import secrets as secrets

import sqlite_util as dbutil


# 下载的最细层
tileZoom = 10
rootTileDir = "tiles_db"

# 分的db数量，采用质数

db_num = 1511
lat_min = -90
lat_max = 90
lon_min = -180
lon_max = 180
# MS doesn't want you hardcoding the URLs to the tile server. This request asks for the Aerial
# url template. Replace {quadkey}
response = requests.get("https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?key=%s" % (secrets.bingKey))

# 返回结果
data = response.json()
print(data)

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



def get_tiles_by_pixel(tilePixel):
    """
    下载该点之上的瓦片

    :param lat:
    :param lon:
    :return:
    """

    """get pixel coordinates"""
    # tilePixel = quadkey.TileSystem.geo_to_pixel((lat, lon), tileZoom)

    # print(tilePixel)

    pixel = tilePixel
    geo = quadkey.TileSystem.pixel_to_geo(pixel, tileZoom)
    # 计算四键
    qk = quadkey.from_geo(geo, tileZoom)

    # 四键
    qkStr = str(qk)


    #
    qkArray = []
    for index in range(tileZoom):
        qkArray.append(qkStr[0:index + 1])

    print(qkArray)
    # 存放路径
    for qk in qkArray:
        # db位置
        dbPath = "%s/%s.db" % (bingTilesDir, int(qk) % db_num )
        print(dbPath)

        if (os.path.exists(dbPath) == False):
            # os.mkdir(dbPath)
            dbutil.create_db(dbPath)



        # 下载影像

        if (dbutil.is_exists(dbPath, qk)):
            # already downloaded
            dbutil.save_images(dbPath, qk)
            ok = 1
        else:
            print("下载中", end='')

            url = tileUrlTemplate.replace("{subdomain}", imageDomains[0])
            url = url.replace("{quadkey}", qk)
            url = "%s&key=%s" % (url, secrets.bingKey)

            response = requests.get(url, stream=True)
            print(response)
            dbutil.insert(dbPath, qk, response.content)

            del response
            # 强制睡一会，防止bing服务器限制
            sleepTime = random() * 3
            time.sleep(sleepTime)

# 左上为原点
tilePixelMax = quadkey.TileSystem.geo_to_pixel((lat_max, lon_max), tileZoom)
tilePixelMin = quadkey.TileSystem.geo_to_pixel((lat_min, lon_min), tileZoom)
print(tilePixelMax)
print(tilePixelMin)

tile_pixel_list = []

for x in range(tilePixelMin[0], tilePixelMax[0], 256):
    for y in range(tilePixelMax[1], tilePixelMin[1], 246):
        tile_pixel_list.append((x, y))

# 取决与服务器的硬件性能
thread_pause = 30
for i in range(len(tile_pixel_list)):
    print("处理"+str(i))
    _thread.start_new_thread(get_tiles_by_pixel,(tile_pixel_list[i],) )

    if(i % thread_pause == (thread_pause-1)):
        print("让正常运行的线程执行完，睡眠开始")
        time.sleep(5)
        print("睡眠结束")

# _thread.start_new_thread( get_tiles_by_pixel, ( ) )


print('下载完毕')
