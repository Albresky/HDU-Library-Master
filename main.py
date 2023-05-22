from utils.master import Master
from UserInterface import UserInterface
from time import sleep

import datetime as dt

def getTime(hour):
    str_timeToday = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    timeToday=dt.datetime.strptime(str_timeToday, "%Y-%m-%d %H:%M")
    return timeToday.replace(hour=hour, minute=0)

def getInfo(trial,plan,resp):
    info=plan['seatsInfo'][0]
    print(f"[try={trial}] MSG={resp['MESSAGE']} | {info['roomName']},{info['floorName']},{info['seatNum']}座,{plan['beginTime'].strftime('%Y-%m-%d %H:%M')}")

def run():
    api = UserInterface()
    master = api.master
    if api.run():
        planIndex = 0
        for plan in master.plans:
            planCode=master.planCode[planIndex]
            planIndex+=1
            beginTime = plan["beginTime"]
            plan["beginTime"] = getTime(beginTime.hour)+dt.timedelta(days=2)
            maxTrials = master.job["maxTrials"]
            delay = master.job["delay"]
            isSuccess=False
            tryTimes=0
            while tryTimes<maxTrials and not isSuccess:
                res=master.run(plan)
                getInfo(tryTimes+1,plan,res)
                if res['DATA']['result'] != 'fail':
                    isSuccess=True
                else:
                    sleep(delay)
                tryTimes+=1
            if isSuccess:
                print(f"[plan={planCode}] 预约成功")
            else:   
                print(f"[plan={planCode}] 预约失败")
            
             
if __name__ == "__main__":
    run()
