from inspect import getinnerframes
import time
import datetime

def get_now():
    return time.time()

def get_interval(t1,t2):
    """
    获取两个时间戳的差值
    :return timedelta
    """
    bg = datetime.datetime.fromtimestamp(t1)
    ed = datetime.datetime.fromtimestamp(t2)
    interv = ed - bg
    return ed - bg
def timestamp_format(timestamp):
    """
    时间戳格式化
    """
    timelocal = time.localtime(float(timestamp))
    dt = time.strftime("%Y-%m-%d %H:%M:%S", timelocal)
    return dt

def interval_format(timedelta : datetime.timedelta):
    """
    使时间差可读
    :return (hour,minute,second)
    """
    seconds = int(timedelta.total_seconds())
    minutes = seconds // 60
    seconds -= minutes * 60
    hours = minutes // 60
    minutes -= hours * 60
    return (hours,minutes,seconds)

def calc_sum_running_time(timeline : list):
    sum = get_interval(0,0) 
    for per in timeline:
        bg,ed = per.split('-')
        sum += get_interval(float(bg),float(ed))
    return interval_format(sum)
def calc_last_running_time(timeline : list):
    if len(timeline) == 0:
        return '未曾运行过'
    last_run = timeline[-1].split('-')[0]
    return timestamp_format(last_run)



if __name__ == '__main__':
    a = get_now()
    time.sleep(3)
    b = get_now()
    interv = get_interval(a,b)
    interv += interv
    print(interval_format(interv))