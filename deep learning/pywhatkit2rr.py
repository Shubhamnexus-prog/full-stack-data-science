import pywhatkit
from datetime import datetime, timedelta

# Current time + 2 minutes
send_time = datetime.now() + timedelta(minutes=2)

hour = send_time.hour
minute = send_time.minute

print("WhatsApp opening at:", hour, minute)

pywhatkit.sendwhatmsg(
    "+919279610872",
    "Hello! Testing WhatsApp automation.",
    hour,
    minute,
    wait_time=20,
    tab_close=False
)