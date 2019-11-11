# -*- coding: utf-8 -*-
"""下载区域影像
从第一层到指定层
"""

import requests
import os.path
import QuadKey.quadkey as quadkey
import shutil
import secrets as secrets

# 下载的最细层
tileZoom = 5
rootTileDir = "tiles_cache"

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



def get_tiles(lat, lon):
    """
    下载该点之上的瓦片

    :param lat:
    :param lon:
    :return:
    """

    """get pixel coordinates"""
    tilePixel = quadkey.TileSystem.geo_to_pixel((lat, lon), tileZoom)

    print(tilePixel)

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
        # 下载影像
        tileFileName = "%s/%s.jpg" % (bingTilesDir, qk)

        if (os.path.exists(tileFileName)):
            # already downloaded
            ok = 1
        else:
            print("下载中", end='')

            url = tileUrlTemplate.replace("{subdomain}", imageDomains[0])
            url = url.replace("{quadkey}", qk)
            url = "%s&key=%s" % (url, secrets.bingKey)

            response = requests.get(url, stream=True)
            print(response)

            with open(tileFileName, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            del response
            neededTile = True

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
        # 下载影像
        tileFileName = "%s/%s.jpg" % (bingTilesDir, qk)

        if (os.path.exists(tileFileName)):
            # already downloaded
            ok = 1
        else:
            print("下载中", end='')

            url = tileUrlTemplate.replace("{subdomain}", imageDomains[0])
            url = url.replace("{quadkey}", qk)
            url = "%s&key=%s" % (url, secrets.bingKey)

            response = requests.get(url, stream=True)
            print(response)

            with open(tileFileName, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            del response
            neededTile = True
# 左上为原点
tilePixelMax = quadkey.TileSystem.geo_to_pixel((lat_max, lon_max), tileZoom)
tilePixelMin = quadkey.TileSystem.geo_to_pixel((lat_min, lon_min), tileZoom)
print(tilePixelMax)
print(tilePixelMin)

for x in range(tilePixelMin[0], tilePixelMax[0], 256):
    for y in range(tilePixelMax[1], tilePixelMin[1], 246):
        get_tiles_by_pixel((x, y))

# get_tiles(lat_max, lon_max)
# get_tiles(lat_max, lon_min)
# get_tiles(lat_min, lon_max)
# get_tiles(lat_min, lon_min)

print('下载完毕')
