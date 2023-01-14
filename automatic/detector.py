# -*-coding:UTF-8 -*-
# import aircv as ac
from aircv import find_template
from loguru import logger


class Detector:
    def __init__(self):
        self.threshold = 0.99
        logger.info("init detector, threshold: {}".format(self.threshold))

    # aircv相关操作
    # 找到图片A在图片B的位置
    def find_location(self, image_src, image_search):
        result = find_template(image_src, image_search, self.threshold)
        if (result != None):
            # logger.info(result)
            x = result['result'][0]
            y = result['result'][1]
            # logger.info('找到目标，中点位于：({},{})'.format(x, y))
            return True, x, y
        else:
            # logger.info("模板图片未找到！")
            return False, 0, 0
