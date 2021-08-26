a = "13:14"
temp = a.split(':')
res_start_time = int(temp[0])*100 + int(temp[1])
print(res_start_time)