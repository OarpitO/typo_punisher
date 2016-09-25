import subprocess
import os
import sys
import time
import signal
from sh import tail

user_brightness_value = 0
keylogger_process = 0
keylogger_bin = "./lib/keylogger/bin/keylogger"
brightness_bin = "./lib/brightness/bin/brightness"

log_file = "/tmp/keystroke.log" # recompile keylogger binary if you change this.

print "Accepts an integer as a parameter to set the difficulty if this is too easy for you"

def start_keylogger():
  global keylogger_bin
  args = (keylogger_bin)
  return subprocess.Popen(args, stdout=subprocess.PIPE)

def clear_logger():
  global log_file
  os.system('rm ' + log_file)

def get_current_brightness():
  global brightness_bin
  args = (brightness_bin, "-l")
  popen = subprocess.Popen(args, stdout=subprocess.PIPE)
  popen.wait()
  return float(popen.stdout.read().rsplit(None, 1)[-1])

def set_brightness( brightness_value ):
  global brightness_bin
  cmd = brightness_bin + ' -m ' + str(brightness_value)
  os.system(cmd)

last_key = ""
last_key_timestamp = 0
none_del_counter = 0
brightness_step_size = 0.05 if len(sys.argv) <= 1 else (float(sys.argv[1])*5)/100

def process_key(key, timestamp):
  # print key
  global last_key, last_key_timestamp, none_del_counter, brightness_step_size, user_brightness_value
  time_diff = timestamp - last_key_timestamp
  current_brightness = get_current_brightness()

  if key == "[del]" and time_diff < 1 and last_key != "[del]":
    set_brightness(max((current_brightness - brightness_step_size),0.0))
    none_del_counter = 0
  elif key != "[del]" and key != last_key:
    none_del_counter += 1

  if none_del_counter !=0 and none_del_counter%10 == 0:
      set_brightness(min((current_brightness + 0.05),user_brightness_value))

  last_key, last_key_timestamp = key, timestamp

user_brightness_value = get_current_brightness()
keylogger_process = start_keylogger()
time.sleep(2)
print "typo_punisher started ! , you can proceed to do your work.\n(CTRl + C to exit gracefully)"

def signal_handler(signal, frame):
  global keylogger_process
  clear_logger()
  keylogger_process.kill()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


for key in tail("-f", log_file, _iter=True):
    process_key(key.rstrip(),time.time())

