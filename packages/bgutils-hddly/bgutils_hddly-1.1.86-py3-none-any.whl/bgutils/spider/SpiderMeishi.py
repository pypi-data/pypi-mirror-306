from dataclasses import dataclass
from datetime import datetime

from bgutils.spider.BaseSpider import BaseSpider

@dataclass
class SpiderMeishi(BaseSpider):
    uid: str #商品ID
    author: str #作者
    title: str #商品标题
    mainingredient: str #原材料
    dateline :str #日期
    subject:str #主题
    url: str #商品url
    pic: str #商品的图片url,对应fcover

    def __init__(self, username, collector, rawurl, rawdata):
        self.username = username #采集者学号
        self.collector= collector #采集者姓名
        self.topic = "meishi_data" #采集题材
        self.rawurl= rawurl  #采集的原始url地址
        self.rawdata = rawdata #采集的原始数据，如记录行的json内容
        self.coll_time = datetime.now() #采集时间，实体初始方法自动填充
