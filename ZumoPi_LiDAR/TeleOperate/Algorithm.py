#!/usr/bin/python3
import threading
import serial
import time
import tty, sys, termios

fwd = 0
front_wall = 1
fix_dist = 2
fix_ang = 3

min_fwd = 0.5
min_right_dist = 0.1
max_right_dist = 0.3
min_right_ang = 10
max_right_ang = -10

# serial connection
ser = serial.Serial('/dev/ttyACM0')  # open serial port

global joyX , joyY , speed

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

def TransmitThread(counter):
  while ser.isOpen:
    #print("send data")
    global joyX, joyY, speed
    #print(f'joystick {joyX}\t{joyY}')
    #counter+=1
    #msg = 'test ' + str(counter) + '\r\n'
    msg = ''
    msg = str(joyX*speed) + ',' +str(joyY*speed) +'\r\n'
    # msg+= ','
    # msg+= str(joyY)
    # msg+= '\r\n'
    ser.write(msg.encode('ascii'))
    time.sleep(0.1)

def ReceiveThread():
  while ser.isOpen:
    if ser.in_waiting > 0:
      #print("recived data")
      #c = ser.read(ser.in_waiting)
      c = ser.readline().decode("ascii")
      print(c)
    else:
      time.sleep(0.05)

def LoopbackTest(right_dist, right_ang, state=fwd):
  global joyX, joyY, speed
  counter = 0
  joyX = 0
  joyY = 0
  speed = 1
  t1 = threading.Thread(target=TransmitThread,args=(counter,))
  t2 = threading.Thread(target=ReceiveThread)
  t1.start()
  t2.start()
  try:
    while True:
      key = sys.stdin.read(1)[0]
      print(key)
      if key == 'q':
        joyX = 0
        joyY = 0
      elif key == 'w':
        joyY = 50
        joyX = 0
      elif key == 'a':
        joyY = 0
        joyX = -50
      elif key == 'd':
        joyY = 0
        joyX = 50
      elif key == 's':
        joyY = -50
        joyX = 0
      elif key == '1':
        speed = 1 
      elif key == '2':
        speed = 2
      elif key == '3':
        speed = 3
      elif key == '4':
        speed = 4 
      elif key == '5':
        speed = 5              
      elif state == front_wall or key == 'f':
        joyX, joyY = do_not_crash()
      elif state == fix_dist or key == 'g':
        joyX, joyY = distancer(right_dist)
      elif state == fix_ang or key == 'h':
        joyX, joyY = angler(right_ang)
      elif state == fwd:
        joyX, joyY = just_go()
  except:
      pass
  
def going_2_crash(fwd_dist):
  if fwd_dist < min_fwd:
    return True
  
def out_of_bounds(right_dist):
  if right_dist < min_right_dist:
    return True
  elif right_dist > max_right_dist:
    return True
  else:
    return False
  
def not_straight(right_ang):
  if right_ang < min_right_ang:
    return True
  elif right_ang > max_right_ang:
    return True
  else:
    return False
  
def do_not_crash():
  #turn_left()///////////////////////////////
  joyX = 50
  joyY = 0
  return joyX, joyY

def distancer(right_dist):
  joyY = 50
  if right_dist < min_right_ang:
    joyX = 0.5
  elif right_dist > max_right_ang:
    joyX = -0.5
  return joyX, joyY

def angler(right_ang):
  joyY = 50
  if right_ang < min_right_ang:
    joyX = 0.5
  elif right_ang > max_right_ang:
    joyX = -0.5
  return joyX, joyY

def just_go():
  joyX = 0
  joyY = 50
  return joyX, joyY
    
if __name__ == "__main__":

  fwd_dist = 10
  right_dist = 0.1
  right_ang = 0

  if going_2_crash(fwd_dist):
    if going_2_crash(fwd_dist):
      state = front_wall
  elif out_of_bounds(right_dist):
    if out_of_bounds(right_dist):
      state = fix_dist
  elif not_straight(right_ang):
    if not_straight(right_ang):
      state = fix_ang
  else:
    state = fwd
  LoopbackTest(right_dist, right_ang, state)