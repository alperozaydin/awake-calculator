import commands
import datefinder
import time
import datetime



status, output = commands.getstatusoutput("pmset -g log|grep -e \" Sleep  \" -e \" Wake  \"")
# status2, output2= commands.getstatusoutput("ioreg -l | awk '$3~/Capacity/{c[$3]=$5}END{OFMT=\"%.3f\";max=c[\"\"MaxCapacity\"\"];print(max>0?100*c[\"\"CurrentCapacity\"\"]/max:\"?\")}'")
# status2, output2= commands.getstatusoutput("ioreg -l | awk '$3~/Capacity/{c[$3]=$5}END{OFMT=\"%.3f\";max=c['MaxCapacity'];print(max>0?100*c['CurrentCapacity']/max:\"?\")}'")


output = output.split("\n")

output.sort(reverse=True)

# print len(output)
# print output

dates =[]

for line in output:
    if "(Charge:100%)" in line and "Wake" in line:
        dates.append(line)
        break
    dates.append(line)

dates.sort(reverse=False)

wake_and_sleep = []
for line in dates:
    date = None
    matches = datefinder.find_dates(line)
    date_in_seconds = None
    for match in matches:
        if "+" in str(match):
            date_time = str(match).split(" ")[1].split("+")[0]
        elif "-" in str(match):
            date_time = str(match).split(" ")[1].split("-")[0]
        date_day = str(match).split(" ")[0]
        date_day_and_time = date_day + " " + date_time
        x = time.strptime(date_day_and_time, "%Y-%m-%d %H:%M:%S")
        date_in_seconds = datetime.timedelta(days=x.tm_yday, hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
        break
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

if len(wake_and_sleep) > 1 and wake_and_sleep[-1][0] == "Wake":
    now = time.strptime(str(datetime.datetime.now()).split(".")[0], '%Y-%m-%d %H:%M:%S')
    date_in_seconds_now = datetime.timedelta(days=now.tm_yday, hours=now.tm_hour, minutes=now.tm_min, seconds=int(now.tm_sec)).total_seconds()
    total_awake_time = total_awake_time + date_in_seconds_now - wake_and_sleep[-1][1]
    print "On use:", str(datetime.timedelta(seconds=total_awake_time)), "| On sleep:", str(datetime.timedelta(seconds=total_sleep_time))
else:
    print "No data!"