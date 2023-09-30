import os
import sys
import requests

from urllib.parse import unquote
from time import sleep
from math import floor as fl
from datetime import datetime as dt
from utils.time import getNowTime,getNowTimeWithOffset
import hashlib,base64

sys.path.append(os.getcwd())
from config.config import ConfigParser



class Master:
    def __init__(self):
        # room map
        self.roomMap = {
            '1':'自习室',
            '2':'教师休息室',
            '3':'阅览室',
            '4':'讨论室'
        }
        self.rooms = None
    
    def init(self, configFile):
        self.loadConfig(configFile)
        self.__initSession()
    
    def loadConfig(self, configFile):
        self.configParser = ConfigParser(configFile)
        if not os.path.exists(configFile):
            self.configParser.createConfig()
        self.cfg = self.configParser.parseConfig()
        self.sessionCfg = self.cfg['session']
        self.urls = self.cfg['urls']
        self.planCode = self.cfg["planCode"]
        self.data = self.cfg["data"]
        self.userInfo = self.cfg["user_info"]
        self.plans = self.cfg["plans"]
        self.job= self.cfg["job"]
        
        if self.userInfo['login_name'] is None or self.job['maxTrials'] is None:
            self.env2conf()
    
    def env2conf(self):
        env_userid = os.environ.get("HLMUSERID")
        env_password = os.environ.get("HLMPASSWORD")
        env_planCode = os.environ.get("HLMPLANCODE")
        env_max_trials = os.environ.get("HLMMAXTRIALS")
        env_delay = os.environ.get("HLMDELAY")
        env_logDetails = os.environ.get("HLMLOGDETAILS")
        env_executeTime = os.environ.get("HLMEXECUTETIME")
        env_preExeTime = os.environ.get("HLMPREEXETIME")
        
        if env_userid is not None and env_password is not None and env_planCode is not None:
            self.userInfo["login_name"] = env_userid
            self.userInfo["password"] = env_password
            self.planCode = env_planCode.split(",")
        else:
            print("未设置环境变量，无法自动登录")
            self.configParser.delConfigFile()
            exit(0)
            
        # default job config
        if env_max_trials is None or env_max_trials == '':
            self.job["maxTrials"] = 1  # default max trials
        else:
            self.job["maxTrials"] = int(env_max_trials)
        if env_delay is None or env_delay == '' or int(env_delay) > 10 or int(env_delay) < 1:
            self.job["delay"] = 2   # default delay
        else:
            self.job["delay"] = int(env_delay)
        if env_logDetails == 'true':
            self.job["logDetails"] = True
        else:
            self.job["logDetails"] = False
        if env_preExeTime is None or env_preExeTime == '':
            self.job["preExeTime"] = "00:00:00"
        if env_executeTime is None or env_executeTime == '':
            self.job["executeTime"] = "20:00:00"
        else:
            try:
                exeTime=dt.strptime(env_executeTime,"%H:%M:%S")
                if exeTime.hour==20 and exeTime.minute==0:
                    pass
                elif exeTime.hour>=19 and exeTime.hour<20:
                    self.job["executeTime"] = env_executeTime
                else:
                    raise Exception("任务时间应控制在19:00:00-20:00:00之间")
            except Exception as e:
                print(f"环境变量[HLMEXECUTETIME]格式错误，应为HH:MM:SS且不应不晚于19:00:00\n将使用默认值'20:00:00'\n[Exception]{e}")
                self.job["executeTime"] = "20:00:00"
            
     
    def delConfigFile(self):
        self.configParser.delConfigFile()
        
    def saveConfig(self):
        self.cfg['planCode'] = self.planCode
        self.cfg['user_info'] = self.userInfo
        self.cfg['plans'] = self.plans
        self.configParser.saveConfig(self.cfg)
    
    def __initSession(self):
        import urllib3
        urllib3.disable_warnings()
        self.session = requests.Session()
        self.session.headers = self.sessionCfg['headers']
        self.session.trust_env = self.sessionCfg['trust_env']
        self.session.verify = self.sessionCfg['verify']
        self.session.params = self.sessionCfg['params']
    
    def login(self):
        url = self.urls["login"]
        loginRes = self.session.post(url=url, data=self.userInfo)
        if loginRes.status_code != 200:
            print(f"登录失败，错误代码{loginRes.status_code}")
            return False
        _json=loginRes.json()
        if _json["CODE"] == "ok":
            self.uid = _json["DATA"]["uid"]
            self.name = _json["DATA"]["user_info"]["name"]
        return _json["CODE"] == "ok"

    def __queryRooms(self):
        # 查询所有可用的房间类型，返回一个字典，键为房间名，值为房间对应的请求参数
        url = self.urls["query_rooms"]
        queryRoomsRes = self.session.get(url=url).json()
        rawRooms = queryRoomsRes["content"]["children"][1]["defaultItems"]
        rooms = {x["name"]: unquote(x["link"]["url"]).split('?')[1] for x in rawRooms}
        for room in rooms.keys():
            rooms[room] = self.session.get(url=self.urls["query_seats"] + "?" + rooms[room]).json()["data"]
            sleep(self.job["delay"]) # minimal interval is unknown
        return rooms
    
    def __querySeats(self):
        # 查询每个房间的座位信息（并非目标任务时间段的座位信息）
        _time = getNowTime()
        if _time.hour >= 22:
            _time = getNowTimeWithOffset(days=1,hours=0).replace(hour=8, minute=0)
        elif _time.hour < 7:
            _time = getNowTimeWithOffset(days=0,hours=0).replace(hour=8, minute=0)
        for room in self.rooms.keys():
            data = {
                "beginTime": _time.timestamp(),
                "duration": 3600,
                "num": 1,
                "space_category[category_id]": self.rooms[room]["space_category"]["category_id"],
                "space_category[content_id]": self.rooms[room]["space_category"]["content_id"],
            }
            resp = self.session.post(url=self.urls["query_seats"], data=data).json()
            self.rooms[room]["floors"] = {x["roomName"]:x for x in resp["allContent"]["children"][2]["children"]["children"]}
            for floor in self.rooms[room]["floors"].keys():
                self.rooms[room]["floors"][floor]["seats"] = self.rooms[room]["floors"][floor]["seatMap"]["POIs"]
            sleep(self.job["delay"])
    def updateRooms(self):
        self.rooms = self.__queryRooms()
        self.__querySeats()
        return list(self.rooms.keys())
    
    def getRoomNameByIndex(self,index):
        if index<0 or index>=len(self.rooms):
            return None
        return self.roomMap[str(index)]
    
    def getFloorNamesByRoom(self, roomName):
        floors = self.rooms[roomName]["floors"]
        return list(floors.keys())
    
    def getFloorNameByRoomAndId(self,room,id):
        for floor in self.rooms[room]['floors']:
            thisFloor=self.rooms[room]['floors'][floor]
            if thisFloor['seatMap']['info']['id'] == str(id):
                return floor
        return None
    
    def getSeatsByRoomAndFloor(self, roomName, floorName):
        seats = self.rooms[roomName]["floors"][floorName]["seats"]
        return seats
    
    def getRoomDetails(self):
        details={}
        for room in self.rooms:
            details[room]={}
            for floor in self.rooms[room]['floors']:
                thisFloor=self.rooms[room]['floors'][floor]
                details[room][floor]=thisFloor['seatMap']['info']['id']
        return details
    
    def addPlan(self, roomName, beginTime, duration, seatsInfo, seatBookers):
        self.plans.append({
            "roomName": roomName,
            "beginTime": beginTime,
            "duration": duration,
            "seatsInfo": list(seatsInfo),
            "seatBookers": list(seatBookers),
        })
    
    def plan2data(self, plan):
        data = {}
        data["beginTime"] = int(plan["beginTime"].timestamp())
        data["duration"] = plan["duration"]*3600
        data["is_recommend"] = 1
        data["api_time"]= fl(getNowTimeWithOffset(days=0, hours=0).timestamp());
        for i in range(len(plan["seatsInfo"])):
            data[f"seats[{i}]"] = plan["seatsInfo"][i]["seatId"]
            data[f"seatBookers[{i}]"] = plan["seatBookers"][i]
        return data
    
    def run(self, plan):
            data = self.plan2data(plan)
            url = self.urls["book_seat"]
            
            _g=f"post&/Seat/Index/bookSeats?LAB_JSON=1&api_time{str(data['api_time'])}&beginTime{str(data['beginTime'])}&duration{str(data['duration'])}&is_recommend{str(data['is_recommend'])}&seatBookers[0]{str(data['seatBookers[0]'])}&seats[0]{str(data['seats[0]'])}"
            md5=hashlib.md5(_g.encode('utf-8')).hexdigest()
            str_g=base64.b64encode(md5.encode('utf-8')).decode('utf-8')
            self.session.headers["Api-Token"]=str_g
            
            res = None
            
            try:
                res = self.session.post(url=url, data=data).json()
            except requests.exceptions.JSONDecodeError as e:
                print(e)
                return None
            
            return res

if __name__ == "__main__":
    pass
