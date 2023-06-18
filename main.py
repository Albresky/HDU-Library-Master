from utils.master import Master
from utils.time import getNowTime, getNowTimeWithOffset
from utils.messages import *
from UserInterface import UserInterface
from time import sleep
from datetime import datetime as dt


def getInfo(trial, plan, resp):
    info = plan["seatsInfo"][0]
    print(f"[{getNowTime()}][try={trial}] MSG={resp['MESSAGE']} | {info['roomName']},{info['floorName']},{info['seatNum']}座,{plan['beginTime'].strftime('%Y-%m-%d %H:%M')},{plan['duration']}小时"
)


def run():
    api = UserInterface()
    master = api.master
    if api.run():
        planIndex = 0
        for plan in master.plans:
            planCode = master.planCode[planIndex]
            beginTime = plan["beginTime"]
            plan["beginTime"] = getNowTimeWithOffset(days=2, hours=0).replace(
                hour=beginTime.hour, minute=0
            )
            maxTrials = master.job["maxTrials"]
            delay = master.job["delay"]

            executeTime_details = getNowTime().strptime(
                master.job["executeTime"], "%H:%M:%S"
            )
            executeTime = getNowTime().replace(
                hour=executeTime_details.hour,
                minute=executeTime_details.minute,
                second=executeTime_details.second,
            )
            nowTime = getNowTime(precision="second")
            if nowTime < executeTime:
                time_wait = (executeTime - nowTime).seconds
                print(f"[{getNowTime()}]未到任务执行时间，还差[{time_wait}]s，等待中...")
                sleep(time_wait)

            print(f"[{getNowTime()}][plan[{planIndex}]={planCode}] 开始预约...")
            isSuccess = False
            tryTimes = 0
            while tryTimes < maxTrials and not isSuccess:
                res = master.run(plan)
                if api.master.job["logDetails"]:
                    getInfo(tryTimes + 1, plan, res)
                try:
                    if res["DATA"]["result"] != "fail":
                        isSuccess = True
                    elif str(res["MESSAGE"]).startswith(MSG_TIME_OUT_OF_RANGE):
                        sleep(delay)
                    elif str(res["MESSAGE"]).startswith(MSG_DUPLICATE):
                        isSuccess = False
                        break
                    elif str(res["MESSAGE"]).startswith(MSG_SEAT_UNAVAILABLE):
                        isSuccess = False
                        break
                except Exception as e:
                    print(f"[{getNowTime()}]plan[{planIndex}]={planCode}] 预约失败，原因：{e}")
                tryTimes += 1
            if isSuccess:
                print(f"[{getNowTime()}][plan[{planIndex}]={planCode}] 预约成功")
            else:
                print(f"[{getNowTime()}]plan[{planIndex}]={planCode}] 预约失败")
            planIndex += 1
        


if __name__ == "__main__":
    run()
