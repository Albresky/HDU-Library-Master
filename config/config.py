import yaml
import os

class ConfigParser():
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = None
        self.template = """
data:
  query_data:
    beginTime: null
    duration: null
    num: '1'
    space_category[category_id]: '591'
    space_category[content_id]: '3'
planCode: []
session:
  headers:
    Accept-Encoding: gzip, deflate, br, zstd
    Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
    Connection: keep-alive
    Host: hdu.huitu.zhishulib.com
    Origin: https://hdu.huitu.zhishulib.com
    Referer: https://hdu.huitu.zhishulib.com/
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-origin
    User-Agent: Mozilla/5.0 (Linux; Android 12; Pixel 3 Build/SP1A.210812.016.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4375 MMWEBSDK/20221011 Mobile Safari/537.36 MMWEBID/2340 MicroMessenger/8.0.30.2244(0x28001E44) WeChat/arm64 Weixin GPVersion/1 NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android
    Accept: application/json, text/plain, */*
    Content-type: application/x-www-form-urlencoded;charset=UTF-8
    Sec-ch-ua: ""
    Sec-ch-ua-mobile: ?1
    Sec-ch-ua-platform: ""
  params:
    LAB_JSON: '1'
  trust_env: false
  verify: false
urls:
  book_seat: https://hdu.huitu.zhishulib.com/Seat/Index/bookSeats
  login: https://hdu.huitu.zhishulib.com/User/Index/login
  query_seats: https://hdu.huitu.zhishulib.com/Seat/Index/searchSeats
  query_rooms: https://hdu.huitu.zhishulib.com/Space/Category/list
  index: https://hdu.huitu.zhishulib.com/
  index: https://hdu.huitu.zhishulib.com/
user_info:
  login_name: 
  org_id: '104'
  password: 
plans: []
job:
  maxTrials:
  delay:
  logDetails:
  executeTime:
  preExeTime:
  checkPoint:
"""
    
    def createConfig(self):
        with open(self.configFile, 'w+', encoding="utf-8") as f:
            self.config = yaml.load(self.template, Loader=yaml.FullLoader)
            yaml.dump(self.config, f, encoding="utf-8", allow_unicode=True)
    
    def parseConfig(self):
        with open(self.configFile, 'r', encoding="utf-8") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        return self.config
      
    def saveConfig(self, config):
        with open(self.configFile, 'w', encoding="utf-8") as f:
            yaml.dump(config, f, encoding="utf-8", allow_unicode=True)
    
    def delConfigFile(self):
        os.remove(self.configFile)


if __name__ == "__main__":
    config = ConfigParser("config.yaml")
    config.createConfig(config)
