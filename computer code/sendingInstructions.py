import serial
import time
import ctypes
from sys import exit

serialAddress = '/dev/cu.usbmodem14121'

def binary(x):
    a = int(16*(x+2048))
    A=a>>8
    B=a-(A<<8)
    print(A, B)
    if A < 0 or A > 255 or B < 0 or B > 255:
            print("Error: angle is out of bounds")
            return [0,0]
    return [A, B]



def sendSteps(steps):
    def sendFloat(flt):
        ser.write(binary(flt))

    def sendInt(i):
        ser.write([i])

    def sendLongInt(i):
        a = i>>8
        b = i-(a<<8)
        ser.write([a, b])

    def sendPenup():
        sendInt(2)
        time.sleep(0.01)
        sendFloat(0)
        time.sleep(0.01)
        sendFloat(0)

    def sendPendown():
        sendInt(3)
        time.sleep(0.01)
        sendFloat(0)
        time.sleep(0.01)
        sendFloat(0)

    def sendMove(p):
        sendInt(4)
        time.sleep(0.01)
        sendFloat(p[0])
        time.sleep(0.01)
        sendFloat(p[1])
        time.sleep(0.01)
    n_inst = 0
    for i in steps:
        #penup, move to start of line, pendown
        n_inst += 3
        n_inst += len(i)-1

    ser = serial.Serial(serialAddress)
    print("Connected to Arduino")

    responded = False

    print("Sending the start instruction")
    while not(responded):
        if ser.in_waiting > 0:
            response = int(ser.readline())
            print("Message recieved:",response)
            if response == 1:
                print("Arduino recieved the start instruction")
                responded = True
            else:
                print("Arduino did not echo the correct instruction, exiting")
                exit()
        else:
            print("\twriting to arduino")
            
            sendInt(1)
            time.sleep(0.05)

    responded = False
    print("Sending n instructions")
    while not(responded):
        if ser.in_waiting > 0:
            response = int(ser.readline())
            print("Instruction Length recieved:", response)
            if response == n_inst:
                print("Arduino echoed the correct instruction length")
                responded = True
            else:
                print("Arduino did not echo correct instruction length, exiting")
                exit()
        else:
            print("\twriting to arduino")
            sendLongInt(n_inst)
            time.sleep(0.01)

    time.sleep(0.01)

    for curve in steps:
        sendPenup()
        sendMove(curve[0])
        sendPendown()
        for p in range(len(curve)-1):
            sendMove(curve[p+1])

    time.sleep(1)
    while ser.in_waiting > 0:
        print(ser.readline())

    loop = True
    while loop:
        while ser.in_waiting > 0:
            message = ser.readline().decode("utf-8")[:-1]
            print(message)
            if message.find("Finished") >= 0:
                loop = False
        time.sleep(0.5)



    ser.close()
    print("Connection Ended")