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
        date_in_seconds = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
        print date_in_seconds
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

now = time.strptime(str(datetime.datetime.now()).split(".")[0], '%Y-%m-%d %H:%M:%S')
date_in_seconds_now = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=int(x.tm_sec)).total_seconds()
total_awake_time = total_awake_time + date_in_seconds_now

print "{0:.2f}".format(total_awake_time/3600.0), "hours"

