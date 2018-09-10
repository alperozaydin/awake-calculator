#!/usr/bin/python
import commands
import time
import datetime
import re

status, output = commands.getstatusoutput("pmset -g log|grep -e \" Sleep  \" -e \" Wake  \"")

output = output.split("\n")

output.sort(reverse=True)

dates =[]

for line in output:
    if "(Charge:100%)" in line and "Wake" in line:
        dates.append(line)
        break
    dates.append(line)

dates.sort(reverse=False)

wake_and_sleep = []
for line in dates:
    # print line
    date = None
    # matches = datefinder.find_dates(line)
    if " Wake" in line:
        day_and_time = line.split(" Wake")
    elif " Sleep" in line:
        day_and_time = line.split(" Sleep")
    date_in_seconds = None

    if "+" in str(day_and_time[0]):
        date_time = str(day_and_time[0]).split(" ")[1].split("+")[0]
    elif "-" in str(day_and_time[0]):
        date_time = str(day_and_time[0]).split(" ")[1].split("-")[0]
    date_day = str(day_and_time[0]).split(" ")[0]
    date_day_and_time = date_day + " " + date_time
    x = time.strptime(date_day_and_time, "%Y-%m-%d %H:%M:%S")
    date_in_seconds = datetime.timedelta(days=x.tm_yday, hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()

    if "Wake" in line:
        wake_and_sleep.append(("Wake", date_in_seconds))
    if "Sleep" in line:
        wake_and_sleep.append(("Sleep", date_in_seconds))

total_awake_time = 0.0
total_sleep_time = 0.0

for i in range(0, len(wake_and_sleep)):
    try:
        if wake_and_sleep[i][0] == "Wake" and wake_and_sleep[i + 1][0] == "Sleep":
            total_awake_time = total_awake_time + (wake_and_sleep[i + 1][1] - wake_and_sleep[i][1])
        else:
            total_sleep_time = total_sleep_time + (wake_and_sleep[i + 1][1] - wake_and_sleep[i][1])
    except:
        pass

status, output= commands.getstatusoutput("ioreg -l | awk '$3~/Capacity/'")

current_battery = map(int, re.findall(r'\d+', output.split("| |")[2].strip()))[0]
design_capacity =  map(int, re.findall(r'\d+', output.split("| |")[3].strip()))[0]
max_capacity = map(int, re.findall(r'\d+', output.split("| |")[1].strip()))[0]

battery_capacity_design = float(current_battery) / float(design_capacity) * 100.0
battery_capacity_real = float(-current_battery) / float(max_capacity - design_capacity - (design_capacity)) * 100.0

if battery_capacity_design < 100.0:
    now = time.strptime(str(datetime.datetime.now()).split(".")[0], '%Y-%m-%d %H:%M:%S')
    date_in_seconds_now = datetime.timedelta(days=now.tm_yday, hours=now.tm_hour, minutes=now.tm_min, seconds=int(now.tm_sec)).total_seconds()
    total_awake_time = total_awake_time + date_in_seconds_now - wake_and_sleep[-1][1]
    print "On use:", str(datetime.timedelta(seconds=total_awake_time)), "| On sleep:", str(datetime.timedelta(seconds=total_sleep_time)), "| Battery (Design):", '{0:.2f}'.format(battery_capacity_design), "| Battery (Capacity):", '{0:.2f}'.format(battery_capacity_real) 
else:
    print "No data!"











