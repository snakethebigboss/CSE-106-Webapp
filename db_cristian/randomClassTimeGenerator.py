import random
# from randomtimestamp import random_time
from datetime import time



def addTime(a:time, b:int) -> time:
    m = a.minute + b
    h = a.hour

    if m >= 60:
        h += int(m/60)
        if h > 12:
            h -= 12
        m %= 60
        m = int(m)
    
    result = time(h,m)
    return result


def adjustMinute(minute:int) -> int:
    if minute < 30:
        minute = 0
    elif minute >= 30 and minute < 45:
        minute = 30
    else:
        minute = 45
    return minute


def randomDateGen():
    weekdays = ['M', 'T', 'W', 'R', 'F']
    
    date = weekdays[random.randint(0,len(weekdays)-1)]
    

    if date == 'M' or date == 'W':
        return 'MW'
    elif date == 'T' or date == 'R':
        return 'TR'
    else:
        return 'MWF'


def genClassTime() -> str:
    date = randomDateGen()
    ti = ['AM', 'PM']   #ti = time indicators

    start_time = time(random.randint(1,12), adjustMinute(random.randint(0,59)))
    end_time = addTime(start_time, start_time.minute+50)
    time_shift = ti[random.randint(0,1)]

    while time_shift == 'AM' and start_time.hour >= 1 and start_time.hour <= 6 or start_time.hour == 12:
        start_time = time(random.randint(1,12), adjustMinute(random.randint(0,59)))
        end_time = addTime(start_time, start_time.minute+50)

    while time_shift == 'PM' and start_time.hour >= 9 and start_time.hour <= 11:
        start_time = time(random.randint(1,12), adjustMinute(random.randint(0,59)))
        end_time = addTime(start_time, start_time.minute+50)

    if end_time.hour == 12 and time_shift == 'AM':
        time_shift = 'PM'
    
    
    start_time = start_time.strftime("%I:%M")
    end_time = end_time.strftime("%I:%M")

    
    result = date + " " + start_time + " - " + end_time + time_shift
    return result


# def genClassTime():
#     date = getClassTime()
#     print(date)


# if __name__ == '__main__':
#     main()