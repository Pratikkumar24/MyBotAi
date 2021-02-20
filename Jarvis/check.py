from datetime import datetime

# now = datetime.now()
hour = datetime.now().hour
minute = datetime.now().minute
second = datetime.now().second

print("current hour: "+ str(hour))
print("current minute: "+ str(minute))
print("current second: "+ str(second))