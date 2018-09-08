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
for index, line in enumerate(dates):
    print line
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

print "========"

total_awake_time = 0.0
total_sleep_time = 0.0
total_time = 0.0

for i in range(0, len(wake_and_sleep)):
    try:
        if wake_and_sleep[i][0] == "Wake" and wake_and_sleep[i + 1][0] == "Sleep":
            if wake_and_sleep[i + 1][1] > wake_and_sleep[i][1]:
                total_awake_time = total_awake_time + (wake_and_sleep[i + 1][1] - wake_and_sleep[i][1])
            else:
                total_awake_time = total_awake_time + (86400.0 - wake_and_sleep[i][1])
    except:
        pass

if len(wake_and_sleep) > 1 and wake_and_sleep[-1][0] == "Wake":
    now = time.strptime(str(datetime.datetime.now()).split(".")[0], '%Y-%m-%d %H:%M:%S')
    date_in_seconds_now = datetime.timedelta(days=now.tm_yday, hours=now.tm_hour, minutes=now.tm_min, seconds=int(now.tm_sec)).total_seconds()
    total_awake_time = total_awake_time + date_in_seconds_now - wake_and_sleep[-1][1]
    print "{0:.2f}".format(total_awake_time/3600.0), "hours"
else:
    print "No data!"


# date1 = "29/11/2015 21:38:02"
# date2 = "30/11/2015 00:45:14"
# newdate1 = time.strptime(date1, "%d/%m/%Y %H:%M:%S")
# newdate2 = time.strptime(date2, "%d/%m/%Y %H:%M:%S")
#
# print newdate1
# print newdate2
#
# date_in_seconds_now = datetime.timedelta(days=newdate1.tm_yday, hours=newdate1.tm_hour, minutes=newdate1.tm_min, seconds=int(newdate1.tm_sec)).total_seconds()
# date_in_seconds_now2 = datetime.timedelta(days=newdate2.tm_yday, hours=newdate2.tm_hour, minutes=newdate2.tm_min, seconds=int(newdate2.tm_sec)).total_seconds()
#
# print date_in_seconds_now
# print date_in_seconds_now2 - date_in_seconds_now