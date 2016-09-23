import subprocess
import os
import sys
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

keylogger_process = start_keylogger()

# clear_logger()
# keylogger_process.kill()

def get_logger_lines_count():
  num_lines = sum(1 for line in open('keystroke.log'))
  print num_lines

def get_logger_last_line():
  args = ("tail", "-n", "1", "keystroke.log")
  popen = subprocess.Popen(args, stdout=subprocess.PIPE)
  print popen.stdout.read()
