import subprocess
import os
import sys
import time

user_brightness_value = 0
keylogger_process = 0
last_key = ""
last_key_timestamp = 0
none_del_counter = 0


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

def process_key(key, timestamp):
  print key
  global last_key, last_key_timestamp, none_del_counter
  time_diff = timestamp - last_key_timestamp
  if key == "[del]\n" and time_diff < 3 and last_key != "[del]\n":
    current_brightness = get_current_brightness()
    set_brightness(current_brightness*0.80)
    none_del_counter = 0
  elif key != "[del]\n":
    none_del_counter += 1
  last_key, last_key_timestamp = key, timestamp

user_brightness_value = get_current_brightness()
clear_logger()
keylogger_process = start_keylogger()
time.sleep(2)

num_of_lines = get_logger_lines_count()
while True:
  current_lines = get_logger_lines_count()
  if num_of_lines != current_lines:
    process_key(get_logger_last_line(), time.time())
    num_of_lines = current_lines
  time.sleep(0.1)
