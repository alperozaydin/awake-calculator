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

for index, line in enumerate(dates):
    if "Wake" in line:
        date = None
        matches = datefinder.find_dates(line)
        for match in matches:
            try:
                if "+" in str(match):
                    date = str(match).split(" ")[1].split("+")[0]
                elif "-" in str(match):
                    date = str(match).split(" ")[1].split("-")[0]
            except Exception as e:
                print e
            print date
            x = time.strptime(date.split(',')[0],'%H:%M:%S')
            date_in_seconds = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            print date_in_seconds
            break
