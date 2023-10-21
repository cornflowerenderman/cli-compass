import datetime

try:
    import pytz
except:
    raise Exception("Missing dependency: pytz")

def convertNewsEntryTime(timestamp): #Converts bugged news entry time to unix time
    d = datetime.datetime.strptime(timestamp, "%d/%m/%Y - %I:%M %p")
    d = d.astimezone(pytz.timezone("UTC"))
    d = datetime.datetime(d.year,d.month,d.day,d.hour,d.minute)
    return int(d.timestamp())

def convertAttendanceTime(timestamp): #Converts attendance timestamp to unix time
    d = datetime.datetime.strptime(timestamp, "%d/%m - %I:%M %p")
    year = datetime.datetime.now().year
    d = datetime.datetime(year, d.month, d.day, d.hour, d.minute)
    return int(d.timestamp())

def convertScheduleTime(timestamp): #Converts schedule timestamp to unix time
    return int(datetime.datetime.strptime(timestamp, "%d/%m/%Y - %I:%M %p").timestamp())


def findNextWeekday(day):     #Accepts a datetime object
    next_day = day + datetime.timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += datetime.timedelta(days=1)
    return next_day         #Returns the next weekday as a datetime object

def unixToShortTime(unix): #Accepts unix time and returns the time in format "HH:MM AM"
    return datetime.datetime.fromtimestamp(unix).strftime('%I:%M %p')

def unixToTime(unix): #Accepts unix time and returns the time in format "DD Mmm HH:MM AM"
    return datetime.datetime.fromtimestamp(unix).strftime('%d %b, %I:%M %p')

