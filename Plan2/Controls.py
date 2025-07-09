import serial
import keyboard
import time
import math

ser = serial.Serial('/dev/ttyUSB0', 115200)
speed = 1.0  # scale factor (0.0 - 1.0)

def compute_motor_speeds(vx, vy, wz):
    R = 1
    v1 = -0.5 * vx + (math.sqrt(3)/2) * vy + R * wz
    v2 = -0.5 * vx - (math.sqrt(3)/2) * vy + R * wz
    v3 = vx + R * wz
    scale = 255
    return [int(scale * v * speed) for v in [v1, v2, v3]]

while True:
    vx = vy = wz = 0
    if keyboard.is_pressed('w'): vy = 1
    if keyboard.is_pressed('s'): vy = -1
    if keyboard.is_pressed('a'): vx = -1
    if keyboard.is_pressed('d'): vx = 1
    if keyboard.is_pressed('q'): wz = -1
    if keyboard.is_pressed('e'): wz = 1
    if keyboard.is_pressed('space'): vx = vy = wz = 0

    m1, m2, m3 = compute_motor_speeds(vx, vy, wz)
    cmd = f"M{m1},{m2},{m3}\n"
    ser.write(cmd.encode())

    if keyboard.is_pressed('k'):
        ser.write(b'K1\n')
        time.sleep(0.1)
        ser.write(b'K0\n')

    time.sleep(0.05)
