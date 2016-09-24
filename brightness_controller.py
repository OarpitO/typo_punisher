import subprocess
import os
import sys
import time

user_brightness_value = 0
keylogger_process = 0

def start_keylogger():
  args = ("./lib/keylogger")
  return subprocess.Popen(args, stdout=subprocess.PIPE)

def clear_logger():
  os.system('rm keystroke.log')

def get_current_brightness():
  args = ("./lib/brightness", "-l")
  popen = subprocess.Popen(args, stdout=subprocess.PIPE)
  popen.wait()
  return float(popen.stdout.read().rsplit(None, 1)[-1])

def set_brightness( brightness_value ):
  cmd = './lib/brightness -m ' + str(brightness_value)
  os.system(cmd)

def get_logger_lines_count():
  args = ("wc", "-l", "keystroke.log")
  popen = subprocess.Popen(args, stdout=subprocess.PIPE)
  popen.wait()
  return popen.stdout.read().split(" ")[-2]

def get_logger_last_line():
  args = ("tail", "-n", "1", "keystroke.log")
  popen = subprocess.Popen(args, stdout=subprocess.PIPE)
  popen.wait()
  return popen.stdout.read()

last_key = ""
last_key_timestamp = 0
none_del_counter = 0
brightness_step_size = 0.05

def process_key(key, timestamp):
  print key
  global last_key, last_key_timestamp, none_del_counter, brightness_step_size, user_brightness_value
  time_diff = timestamp - last_key_timestamp
  current_brightness = get_current_brightness()

  if key == "[del]" and time_diff < 1 and last_key != "[del]":
    set_brightness(max((current_brightness - brightness_step_size),0.0))
    none_del_counter = 0
  elif key != "[del]":
    none_del_counter += 1

  if none_del_counter !=0 and none_del_counter%10 == 0:
      set_brightness(min((current_brightness + brightness_step_size),user_brightness_value))

  last_key, last_key_timestamp = key, timestamp

user_brightness_value = get_current_brightness()
clear_logger()
keylogger_process = start_keylogger()
time.sleep(2)

num_of_lines = get_logger_lines_count()
while True:
  current_lines = get_logger_lines_count()
  if num_of_lines != current_lines:
    process_key(get_logger_last_line().rstrip(), time.time())
    num_of_lines = current_lines
  time.sleep(0.1)
