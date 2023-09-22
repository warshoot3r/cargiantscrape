import datetime
import sys


scheduled_time_start_hour = 20
scheduled_time_end_hour = 21

print(f"Scheduled time is {scheduled_time_start_hour}:00 to {scheduled_time_end_hour}:00. Machine time -> {datetime.datetime.now().strftime('%H:%M')}")
while True:
        current_time = datetime.datetime.now()
        # Calculate the time difference between local time and GM
        time_str = current_time.strftime('%H:%M')
        if  scheduled_time_start_hour <= current_time.hour < scheduled_time_end_hour:

            print(f"It's time {time_str}", flush=True)
            break

        else:
            print(f"Not time. Cancelling {time_str}", flush=True)
            sys.exit()
