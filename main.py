from wayback import Wayback
import math


#经纬度换算瓦片
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)


#瓦片换算经纬度
def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)



year_dic = {
    "44710": "2022-06-08",
    "26083": "2022-02-02",
    "9812": "2021-02-24",
    "32645": "2020-05-20",
    "18063": "2019-04-24",
    "10768": "2018-01-31",
    "31026": "2017-02-27",
    "10": "2014-02-20",
}

#截取的瓦片等级
level = 17
#起始经纬度
start_lon = 112.87628
start_lat = 28.26949
start_y, start_x = deg2num(start_lat, start_lon, level)
wayback = Wayback("44710",str(level),start_x, start_y, 50, "cs_17_2022.tiff", False)
wayback.crawlWayback()