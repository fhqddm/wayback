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
    "2022-06-08":"44710",
    "2022-02-02": "26083",
    "2021-02-24": "9812",
    "2020-05-20": "32645",
    "2019-04-24": "18063",
    "2018-01-31": "10768",
    "2017-02-27": "31026",
    "2014-02-20": "10",
}

#年份设置
year_str = "2022-06-08"
year_code = year_dic[year_str]
#截取的瓦片等级
level = 17
#起始经纬度112.89062,28.19549,112.96980,28.23467
start_lon = 112.89062
start_lat = 28.23467
end_lon = 112.96980
end_lat = 28.19549
start_y, start_x = deg2num(start_lat, start_lon, level)
end_y, end_x = deg2num(end_lat, end_lon, level)
outName = year_str+"_"+str(level)+"_"+"cs.tiff"
wayback = Wayback(year_code, str(level), outName, False, start_x, start_y, end_x, end_y)
wayback.crawlWayback()