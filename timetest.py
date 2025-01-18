import time

str_time = "18/01/25"
day,month,year = str_time.split("/")

that_time = time.localtime(time.mktime(time.struct_time((int("20"+year),int(month),int(day),23,59,59,-1,-1,-1))))
print(time.asctime(that_time))

print(round(abs(time.mktime(that_time) - time.mktime(time.localtime()))/86400))