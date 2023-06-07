from datetime import datetime , timedelta
from math import floor

# userAssign = [
#     {
#         'subject': "",
#         'assignment': "",
#         'due': "",
#     }
# ]

def str_to_datetime(strdate):
    return datetime.strptime(strdate, "%Y-%m-%d %H:%M:%S")

def str_to_date(strdate):
    return datetime.strptime(strdate, "%Y-%m-%d")

def subtract_date(d1,d2):
    return d1 - d2

def subdate(d1):
    if (d1 - datetime.now()).seconds < 43200:
        return True
    return False
    # return then.date() <= datetime.now().date() 

def toRemove(due):
    return str_to_date(due).date() < datetime.now().date()

dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
d1 = str_to_date('2023-05-09')
now = str_to_datetime(dt_string)
time_left = subtract_date(d1,now)

print(subdate(d1))



def sec_to_hrs(secs):
    m = secs/60
    return floor(m/60)



# date_time = 'Apr 20 2023 11:51PM'

# then = str_to_date(date_time)

# now = datetime.now()
# due_date = now.strftime("%b %d %Y %H:%M%p")

# year = now.strftime("%Y")
# print("year:", year)

# month = now.strftime("%m")
# print("month:", month)

# day = now.strftime("%d")
# print("day:", day)

# time = now.strftime("%H:%M:%S")
# print("time:", time)

# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
# print("date and time:",date_time)

# then = then - timedelta(days=5)

# # year = then.strftime("%Y")
# # print("year:", year)

# # month = then.strftime("%m")
# # print("month:", month)

# # day = then.strftime("%d")
# # print("day:", day)

# # time = then.strftime("%H:%M:%S")
# # print("time:", time)

# # date_time = then.strftime("%m/%d/%Y, %H:%M:%S")
# # print("date and time:",date_time)

# if then.strftime("%d")==now.strftime("%d"):
#     print("yes")



