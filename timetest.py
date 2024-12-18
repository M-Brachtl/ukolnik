import time

str_time = "28/12/24"
day,month,year = str_time.split("/")

that_time = time.localtime(time.mktime(time.struct_time((int("20"+year),int(month),int(day),23,59,59,-1,-1,-1))))
print(time.asctime(that_time))