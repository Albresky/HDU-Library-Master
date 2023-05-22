from datetime import datetime,timedelta
import pytz

# UTC+8 timezone name
timezone_name = 'Asia/Shanghai'

def getNowTime():
    utc_now = datetime.utcnow()
    timezoneCN = pytz.timezone(timezone_name)
    local_now = utc_now.replace(tzinfo=pytz.timezone('UTC')).astimezone(timezoneCN)
    return local_now

'''
get now time with offset(days,hours), precision: hour
'''
def getNowTimeWithOffset(days=0,hours=0):
    timeNow = getNowTime()
    timeNow=timeNow.strftime("%Y-%m-%d %H:%M") # # str(datetime)
    timeNow = datetime.strptime(timeNow, "%Y-%m-%d %H:%M")
    if days != 0:
        timeNow += timedelta(days=days)
    if hours != 0:
        timeNow += timedelta(hours=hours)
    return timeNow # datetime
    
if __name__ == '__main__':
    pass
