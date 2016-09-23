import subprocess
import os
import sys
import time
brightness_value = 0.5
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
  return popen.stdout.read().rsplit(None, 1)[-1]

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

clear_logger()
keylogger_process = start_keylogger()
time.sleep(2)

num_of_lines = get_logger_lines_count()
while True:
    current_lines = get_logger_lines_count()
    if num_of_lines != current_lines:
      print get_logger_last_line()
      num_of_lines = current_lines
