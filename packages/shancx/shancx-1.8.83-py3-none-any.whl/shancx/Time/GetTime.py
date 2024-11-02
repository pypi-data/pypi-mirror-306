import datetime
def UTC10minDiff():    
    now_utc = datetime.datetime.utcnow() 
    rounded_minute = round(now_utc.minute / 10) * 10
    if rounded_minute == 60:
        rounded_minute = 0
        now_utc += datetime.timedelta(hours=1)
    adjusted_time = now_utc.replace(minute=rounded_minute, second=0, microsecond=0)
    formatted_time = adjusted_time.strftime('%Y%m%d%H%M')
    return formatted_time

def UTCStr():    
    now_utc = datetime.datetime.utcnow() 
    now_utcstr = now_utc.strftime('%Y%m%d%H%M%S')
    return now_utcstr

def UTCStr():    
    now_cst = datetime.datetime.now() 
    now_cststr = now_cst.strftime('%Y%m%d%H%M%S')
    return now_cststr