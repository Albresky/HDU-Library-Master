from utils.master import Master
from utils.time import getNowTime, getNowTimeWithOffset
from UserInterface import UserInterface
from time import sleep

def getInfo(trial,plan,resp):
    info=plan['seatsInfo'][0]
    print(f"[{getNowTime()}][try={trial}] MSG={resp['MESSAGE']} | {info['roomName']},{info['floorName']},{info['seatNum']}座,{plan['beginTime'].strftime('%Y-%m-%d %H:%M')},{plan['duration']}小时")

def run():
    api = UserInterface()
    master = api.master
    if api.run():
        planIndex = 0
        for plan in master.plans:
            planCode=master.planCode[planIndex]
            planIndex+=1
            beginTime = plan["beginTime"]
            # plan["beginTime"] = getTime(beginTime.hour)+dt.timedelta(days=2)
            plan["beginTime"] = getNowTimeWithOffset(days=2,hours=0).replace(hour=beginTime.hour, minute=0)
            maxTrials = master.job["maxTrials"]
            delay = master.job["delay"]
            isSuccess=False
            tryTimes=0
            while tryTimes<maxTrials and not isSuccess:
                res=master.run(plan)
                if api.master.job["logDetails"]:
                    getInfo(tryTimes+1,plan,res)
                if res['DATA']['result'] != 'fail':
                    isSuccess=True
                else:
                    sleep(delay)
                tryTimes+=1
            if isSuccess:
                print(f"[{getNowTime()}][plan={planCode}] 预约成功")
            else:   
                print(f"[{getNowTime()}][plan={planCode}] 预约失败")
            
             
if __name__ == "__main__":
    run()
