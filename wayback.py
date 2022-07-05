import cv2
import requests
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
import shutil



class Wayback():
    def __init__(self, time_code, level, outName, deleteTiles, start_x, start_y,end_x=-1, end_y=-1, size=-1):
        self.time_code = time_code # time_code 入库时间代码
        self.level = level # level 瓦片等级
        self.start_x = start_x # start_x瓦片地图起始编号x
        self.start_y = start_y # start_y瓦片地图起始编号y
        self.end_x = end_x  # end_x瓦片地图结束编号x
        self.end_y = end_y  # end_y瓦片地图结束编号y
        #self.size = size
        if size==-1:
            # 设置了结束编号
            self.rows = self.end_x - self.start_x
            self.cols = self.end_y - self.start_y
        else:
            #未设置结束编号，长宽都为size
            self.rows = size
            self.cols = size
        self.outName = outName # 保存的文件名  ***.tiff
        self.save_root = "./tile/" + time_code + "/" # 瓦片地图临时存放路径  ***.tiff
        self.pool = ThreadPoolExecutor(max_workers=80) # 线程池
        self.deleteTiles = deleteTiles #是否删除瓦片地图


    def __download(self, url, name_):
        if not os.path.exists(self.save_root + name_):
            resp = requests.get(url=url, timeout=8).content
            with open(self.save_root + name_, "wb") as fp:
                fp.write(resp)
            print(name_)


    def __createTiles(self, base_url):
        for i in range(self.rows):
            for j in range(self.cols):
                name_ = str(i) + "-" + str(j) + ".png"
                url = base_url + (str(self.start_x + i) + "/" + str(self.start_y + j))
                img_name = self.save_root + name_
                if not os.path.exists(img_name):
                    self.pool.submit(self.__download, url, name_)
                else:
                    print("done " + name_)



    def crawlWayback(self):
        save_root = "./tile/" + self.time_code + "/"
        if not os.path.exists(save_root):
            os.mkdir(save_root)

        base_url = "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/" + self.time_code + "/" + self.level + "/"
        #pool = ThreadPoolExecutor(max_workers=80)

        if "404 " in str(requests.get(url=base_url + str(self.start_x) + "/" + str(self.start_y), timeout=8).content):
            print("Image Not Found ")
            return

        rows = []
        cols = []

        count = 0

        self.__createTiles(base_url)




        while count != self.rows * self.cols:
            count = len(os.listdir(save_root))
            print(count)
            time.sleep(5)
            if count == len(os.listdir(save_root)) and count != self.rows * self.cols:
                self.__createTiles(base_url)


        for i in range(self.rows):
            for j in range(self.cols):
                name = str(i) + "-" + str(j) + ".png"
                image = cv2.imread(save_root + name)
                rows.append(image)
            cols.append(np.hstack(rows))
            rows = []
        final = np.vstack(cols)
        cv2.imwrite('./out/' + self.outName, final)
        if self.deleteTiles:
            shutil.rmtree(save_root)


