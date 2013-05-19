import serial
import sdo

ser = serial.Serial("COM19", 115200)
sdo.dev = ser
sdo.logf = open('tlist.log', 'wb')

if __name__ == '__main__':
    t4 = sdo.proc()
    t4.write("list()\n")
    t4.wait_line("\t0, 0x00000000")
    t4.success("Test list")

    sdo.loop(10)

