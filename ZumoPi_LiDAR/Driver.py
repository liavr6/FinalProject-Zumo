#!/usr/bin/python3
import threading
import serial
import time
import tty, sys, termios
from time import sleep
import KeyboardTeleoperate

global fwd_dist, right_dist, right_ang, status

fwd_dist = 10
right_dist = 0.1
right_ang = 0
status = -2

fwd = 0
front_wall = 1
fix_dist = 2
fix_ang = 3

min_fwd = 0.3
min_right_dist = 0.2
max_right_dist = 0.4
min_right_ang = -5
max_right_ang = 5

# serial connection
ser = serial.Serial('/dev/ttyACM0')  # open serial port

global joyX , joyY , speed

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

def TransmitThread(counter):
  while ser.isOpen:
    #print("send data")
    global joyX, joyY, speed, quit
    #print(f'joystick {joyX}\t{joyY}')
    #counter+=1
    #msg = 'test ' + str(counter) + '\r\n'
    if quit == True: return
    msg = ''
    msg = str(joyX*speed) + ',' +str(joyY*speed) +'\r\n'
    # msg+= ','
    # msg+= str(joyY)
    # msg+= '\r\n'
    ser.write(msg.encode('ascii'))
    time.sleep(0.1)

def QuitThread(t1, t2):
  global status
  status = -1
  while ser.isOpen:
    global joyX, joyY, speed, quit
    key = sys.stdin.read(1)[0]
    if key == 'q':
      print('quitting auto driving')
      quit = True
      joyX = 0
      joyY = 0
      speed = 0
      t1.join()
      t2.join()
      msg = ''
      msg = str(joyX*speed) + ',' +str(joyY*speed) +'\r\n'
      ser.write(msg.encode('ascii'))
      time.sleep(0.1)
      print('turning on manual driving')
      KeyboardTeleoperate.LoopbackTest()
      exit(0)

def ReceiveThread():
  global quit
  while ser.isOpen:
    if quit == True: return
    if ser.in_waiting > 0:
      #print("recived data")
      #c = ser.read(ser.in_waiting)
      c = ser.readline().decode("ascii")
      # print(c)
    else:
      time.sleep(0.05)

def LoopbackTest():
  sleep(3)
  global joyX, joyY, speed, joy_speed, quit
  global fwd_dist, right_dist, right_ang, status
  counter = 0
  quit = False
  joyX = 0
  joyY = 0
  speed = 2.5
  joy_speed = 100
  t1 = threading.Thread(target=TransmitThread,args=(counter,))
  t2 = threading.Thread(target=ReceiveThread)
  t3 = threading.Thread(target=QuitThread, args=(t1, t2,))
  t1.start()
  t2.start()
  t3.start()
  meas_num = 100
  try:
    while True:
      if quit == True: return
      i = 0
      j = 0
      k = 0
      # joyY = 0
      # joyX = 0
      # speed(1000000000)
      while i < meas_num:
        if going_2_crash():
          i += 1
        else: break
        if i == meas_num:
          status = 3
          do_not_crash()
      while j < meas_num:
        if i == meas_num: break
        if out_of_bounds():
          j += 1
        else: break
        if j == meas_num:
          status = 2
          distancer()
      while k < meas_num:
        if (i == meas_num) or (j == meas_num): break
        if not_straight():
          k += 1
        else: break
        if k == meas_num:
          status = 1
          angler()
      # check if the angle is 90 before fixing the distance
      if (i != meas_num) and (j != meas_num) and (k != meas_num):
        status = 0
        just_go()
      sleep(0.01)
  except:
    time.sleep(0.1)
    pass
  
def going_2_crash():
  if fwd_dist < min_fwd:
    # print(f'fwd_dist = {fwd_dist}')
    # sleep(0.01)
    return True
  
def out_of_bounds():
  if right_dist < min_right_dist:
    # print(f'righ_dist = {right_dist}')
    # sleep(0.01)
    return True
  elif right_dist > max_right_dist:
    # print(f'righ_dist = {right_dist}')
    # sleep(0.01)
    return True
  else:
    # sleep(0.01)
    return False
  
def not_straight():
  if right_ang < min_right_ang:
    # print(f'right_ang = {right_ang}')
    # sleep(0.01)
    return True
  elif right_ang > max_right_ang:
    # print(f'right_ang = {right_ang}')
    # sleep(0.01)
    return True
  else:
    # sleep(0.01)
    return False
  
def do_not_crash():
  global joyX, joyY, joy_speed
  joyX = 0
  joyY = 0
  sleep(1)
  # print(right_ang)
  # turn left
  while right_ang < 25:
    joyX = -joy_speed / 2
    joyY = 0
    # print(right_ang)
  # print(right_ang)
  while right_ang > 10:
    joyX = -joy_speed / 2
    joyY = 0
    # print(right_ang)
  # print(right_ang)
  joyX = 0
  joyY = 0
  sleep(1)
  # print('do not crash')

def distancer():
  global joyX, joyY, joy_speed
  joyY = joy_speed
  # joyX = pid_controller(right_dist, min_right_dist, max_right_dist)
  if right_dist < min_right_ang:
    joyX = joy_speed / 3
  elif right_dist > max_right_ang:
    joyX = -joy_speed / 3
  # print('distancer')

def angler():
  global joyX, joyY, joy_speed
  joyY = joy_speed
  # joyX = pid_controller(right_ang, min_right_ang, max_right_ang)
  sleep(0.01)
  if right_ang < min_right_ang:
    joyX = joy_speed / 3
  elif right_ang > max_right_ang:
    joyX = -joy_speed / 3
  # print('angler')

def just_go():
  global joyX, joyY, joy_speed
  joyX = 0
  joyY = joy_speed
  # print('just go')
    
import time

def pid_controller(var, range_start, range_end, Kp=0.5, Ki=0.2, Kd=0.1):
    # Initialize variables
    global joy_speed
    last_error = 0
    integral_error = 0
    last_time = time.time()
    pid_speed = 0

    # Calculate time difference
    current_time = time.time()
    dt = current_time - last_time

    # Calculate the error
    if range_start <= var <= range_end:
        error = 0
    else:
        error = range_start - var

    # Proportional term
    proportional = Kp * error

    # Integral term
    integral_error += error * dt
    integral = Ki * integral_error

    # Derivative term
    derivative = Kd * (error - last_error) / dt

    # Calculate PID output
    pid_output = proportional + integral + derivative

    # Limit output to joy_speed if it exceeds that value
    if abs(pid_output) > joy_speed / 3:
        pid_output = joy_speed / 3 * (pid_output / abs(pid_output))

    # Update pid_speed
    pid_speed = pid_output

    # Update variables for next iteration
    last_error = error
    last_time = current_time

    return pid_speed
