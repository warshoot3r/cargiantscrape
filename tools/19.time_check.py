import datetime
import sys


scheduled_time = datetime.time(20)# 8 PM
print(f"Scheduled time at {scheduled_time}")
print(f"Machine time at {datetime.datetime.now()}")
while True:
        current_time = datetime.datetime.now()
        # Calculate the time difference between local time and GMT
        time_difference = current_time - datetime.datetime.utcnow()

        # Subtract the time difference to get the GMT time
        gmt_time = current_time - time_difference

        converted_current_time = gmt_time.time()
        if converted_current_time < scheduled_time:
            print(f"Not time yet {converted_current_time}")
            sys.exit()

        else:
            print("Its time")
            print(current_time)
            break
