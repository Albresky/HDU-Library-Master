import os

from time import sleep
from datetime import datetime
from utils.master import Master
from threading import Thread
from utils.time import getNowTime

class UserInterface:
    def __init__(self):
        self.configFile = "./config/config.yaml"
        self.master = Master()
        self.th = None
        
    def init(self):
        if not os.path.exists(self.configFile):
            print(f"未检测到配置文件，将在config目录下创建配置文件: {self.configFile}")
            self.master.init(self.configFile)
        else:
            try:
                self.master.init(self.configFile)              
            except Exception as e:
                print(f"配置文件解析失败，请检查配置文件是否正确。错误为：")
                print(e)
                print(f"若无法解决，请尝试删除{self.configFile}，重新运行程序。")
                self.exit()
            print(f"配置文件解析成功。")
            sleep(1)

    
    def login(self):
        flag = False
        while not flag:
            if self.master.userInfo["login_name"]  and self.master.userInfo["password"] :
                if self.master.login():
                    print("登录成功")
                    self.master.saveConfig()
                    self.th = Thread(target=self.master.updateRooms)
                    self.th.start()
                    flag = True
                else:
                    print("环境变量中账号密码错误")
                    self.master.delConfigFile()
                    self.exit()
            else:
                self.exit()
        return flag
    
    
    def exit(self):
        if self.th and self.th.is_alive():
            for _ in "请等待其他线程结束...":
                    print(_, end="", flush=True)
                    sleep(0.5 if self.th.is_alive() else 0.1)
            while self.th.is_alive():
                print(".", end="", flush=True)
                sleep(0.5)
        exit(0)
        
    def run(self):
        self.init()
        state = self.login()
        if len(self.master.plans) == 0:
            print("初始化预约方案...")
            if self.addPlan():
                self.master.saveConfig()
                print("预约方案初始化成功")
            else:
                print("预约方案初始化失败")
                self.exit()
        return state

    def planParser(self, plan:list):
        return [list(map(int, x.split(":"))) for x in plan]

    def addPlan(self):
        try:
            num = 0
            mPlans = self.planParser(self.master.planCode)
            if self.th.is_alive():
                print("正在初始化楼层和座位信息...")
                while self.th.is_alive():
                    sleep(0.1)
            numRooms = len(self.master.rooms)
            
            for _plan in mPlans:
                roomName = _plan[0] # roomType
                if roomName < 1 or roomName > numRooms:
                    raise Exception("房间类型不合法")
                roomName = self.master.getRoomNameByIndex(roomName)
                room = self.master.rooms[roomName]
                
                retries = self.master.job["maxTrials"] + 5
                delay = self.master.job['delay']
                floor = None
                floorName = None
                while retries >= 0:
                    retries -= 1
                    floor = self.master.getFloorNamesByRoom(roomName)
                    if len(floor) > 0:
                        floorName = self.master.getFloorNameByRoomAndId(roomName, _plan[1]) # floorId2floorName
                        if floorName is None:
                            if retries == 0:
                                raise Exception(f"{roomName}中楼层{_plan[1]}不存在")
                            else:
                                sleep(delay)
                                self.th = Thread(target=self.master.updateRooms)
                                self.th.start()
                                self.th.join()
                        else:
                            break
                    elif len(floor) == 0 and retries != 0:
                        sleep(delay)
                        self.th = Thread(target=self.master.updateRooms)
                        self.th.start()
                        self.th.join()
                    else:
                        raise Exception(f"{roomName}没有开放楼层")
                    
                time = getNowTime().replace(hour=_plan[3],minute=0,second=0) # hour
                if time.hour < room["range"]["minBeginTime"] or time.hour > room["range"]["maxEndTime"]:
                    raise Exception("开始时间不在房间开放时间内")
                leftTime = room["range"]["maxEndTime"] - time.hour
                hours = _plan[4] # duration
                if hours < 1 or hours > leftTime:
                    raise Exception("使用时长不合法")
                seatsInfo = self.master.getSeatsByRoomAndFloor(roomName, floorName)
                seats = _plan[2] # seatType
                seats = eval(f"({seats})")
                seatsDictList = []
                seat = str(seats)
                seatInfo = [x for x in seatsInfo if x["title"] == seat]
                if len(seatInfo) == 0:
                    raise Exception(f"{floorName}中座位{seat}不存在")
                if len(seatInfo) > 1:
                    raise Exception(f"程序错误，{floorName}中座位{seat}存在多个\n"+str(seatInfo))
                seatsDictList.append({
                    "roomName": roomName,
                    "floorName": floorName,
                    "seatId": seatInfo[0]["id"],
                    "seatNum": seatInfo[0]["title"],
                    "booker": self.master.uid,
                    "bookerName": self.master.name,
                })
                seatBookers = (self.master.uid, )
                self.master.addPlan(roomName, time, hours, seatsDictList, seatBookers)
                print(f"plan[{num}]添加成功")
                num += 1
            self.master.saveConfig()
            return True
        except Exception as e:
            print(f"{e}\n环境变量错误，取消操作..")
            self.master.delConfigFile()
            return False


if __name__ == "__main__":
    pass
