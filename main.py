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
            if not api.master.job["logDetails"]:
                _planCode = '****'
            else:
                _planCode = planCode
            beginTime = plan["beginTime"]
            plan["beginTime"] = getNowTimeWithOffset(days=2, hours=0).replace(
                hour=beginTime.hour, minute=0
            )
            maxTrials = master.job["maxTrials"]
            delay = master.job["delay"]

            nowTime = getNowTime(precision="second")
            preExeTime_details = getNowTime().strptime(
                master.job["preExeTime"], "%H:%M:%S"
            )
            preExeTime =getNowTimeWithOffset(days=1).replace(
                hour=preExeTime_details.hour,
                minute=preExeTime_details.minute,
                second=preExeTime_details.second,
            )
            
            time_wait = (preExeTime - nowTime).seconds
            if time_wait < 7200:
                # checkpoint A: executeTime seats reservation at 00:00:01
                print(f"[{getNowTime()}][checkpoint A]未到任务执行时间，还差[{time_wait}]s，等待中...")
                sleep(time_wait)
            else:
                # checkpoint B: executeTime seats reservation at 20:00:01
                executeTime_details = getNowTime().strptime(
                    master.job["executeTime"], "%H:%M:%S"
                )
                executeTime = getNowTime().replace(
                    hour=executeTime_details.hour,
                    minute=executeTime_details.minute,
                    second=executeTime_details.second,
                )

                if nowTime < executeTime:
                    time_wait = (executeTime - nowTime).seconds
                    print(f"[{getNowTime()}][checkpoint B]未到任务执行时间，还差[{time_wait}]s，等待中...")
                    sleep(time_wait)

            print(f"[{getNowTime()}][plan[{planIndex}]={_planCode}] 开始预约...")
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
                    print(f"[{getNowTime()}]plan[{planIndex}]={_planCode}] 预约失败，原因：{e}")
                finally:
                    tryTimes += 1
            if isSuccess:
                print(f"[{getNowTime()}][plan[{planIndex}]={_planCode}] 预约成功")
            else:
                print(f"[{getNowTime()}]plan[{planIndex}]={_planCode}] 预约失败")
            planIndex += 1
        


if __name__ == "__main__":
    run()
