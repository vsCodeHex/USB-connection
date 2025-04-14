# DARW connect to Epos4 via Rs232 and read object
# 2025.03

import struct
import serial, time
import serial.tools.list_ports

ser = serial.Serial()

def Search_ports():
    ports = serial.tools.list_ports.comports()
    print("********** searching serial ports ...")
    for p in ports:
        print(p.device)
        print(p.description)
    print('********* ports found :', len(ports))

def crc_ccitt_16(data):
    crc = 0x0000
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1

            crc &= 0xFFFF

    return crc

def Init_serial_comm():
    ser.port = "COM1"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = 0.5              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 0.5     #timeout for write


def crcCheck(data):
    # print("Rx crc -1: ", hex(data[-1]))
    # print("Rx crc -2: ", hex(data[-2]))

    Rxcrc = 0x0000
    Rxcrc = data[-1]
    Rxcrc = Rxcrc << 8
    Rxcrc |= data[-2]
    size = len(data)
    print(" /*** Rx crc = ", hex(Rxcrc), " Rx len = ", size)


def hex_to_little_endian(hex_string):
    little_endian_hex = bytearray.fromhex(hex_string)[::-1]
    return little_endian_hex

    # print(hex_to_little_endian('aabb'))
    # bytearray(b'\xbb\xaa')


def applyByteStuffing(flagbyte, escapebyte, payload):

    flagbyte = ("Z")
    escapebyte = ("A")


    x = payload.replace (escapebyte, escapebyte*2)
    y = x.replace (flagbyte, escapebyte+flagbyte)
    print (flagbyte + y + flagbyte)
    # return;


def byte_stuffing(data):
    # add bit stuffing 0x90 0x90
    print(" --> byte_array No stuffing:",[hex(x) for x in data])
    stuffed = bytearray()
    escapebyte = 0x90
    flagbyte = 0x90

    for byte in data:
        if byte == escapebyte:
            stuffed.append(escapebyte)
            stuffed.append(escapebyte)
        elif byte == flagbyte:
            stuffed.append(escapebyte)
            stuffed.append(flagbyte)
        else:
            stuffed.append(byte)
    print(" --> byte_array with Stuffing:",[hex(x) for x in stuffed])

    return stuffed



def composeTxMsg(data):
    # Prepare the word Data for CRC calculation (little endian):
    # CRC calculation includes all bytes of the data frame except synchronization bytes and byte stuffing

    msgCrc = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    # to little endian
    msgCrc[0] = data[3]
    msgCrc[1] = data[2]
    msgCrc[2] = data[5]
    msgCrc[3] = data[4]
    msgCrc[4] = data[7]
    msgCrc[5] = data[6]


    crc_16 = crc_ccitt_16(msgCrc)
    # print(F"crc is: 0x{crc_16:04X}")

    byte_array = crc_16.to_bytes(2, byteorder='big')
    byte_array = bytearray(byte_array)
    # print(" --> byte_array:",[hex(x) for x in byte_array])

    data[8] = byte_array[1]
    data[9] = byte_array[0]

    # data = byte_stuffing(data)

    return data




# read actual position (object 0x60E4-01)
# byte message        0     1      2       3      4       5 6      7       8 9
#                    DLE,  STX,  OpCode,  Len, Node-ID,  Index,  SubIdx,   Crc
# msg1 = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xE4, 0x60, 0x01, 0x20, 0xB4])
# msgToTransmit = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xE4, 0x60, 0x01, 0x00, 0x00])

# read home position (object 0x30B0-00)
# msgToTransmit = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xB0, 0x30, 0x00, 0x2E, 0x62])   # whole message with crc
# msgToTransmit = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xB0, 0x30, 0x00, 0x00, 0x00])   # message without crc
# msgCrc = bytearray([0x02, 0x60, 0xB0, 0x01, 0x00, 0x30])                                  # example of message data for calculating crc (with right order -> little endian)



#  Data to be transmit without crc (crc will be calculated)
msgToTransmit = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xE4, 0x60, 0x01, 0x00, 0x00])



try:
    # get the available serial ports on the PC
    # Search_ports()

    Init_serial_comm()
    ser.open()
    print("is opened", ser.name)


    try:
        ser.flushInput()
        ser.flushOutput()
        counterOfTxMsg = 0
        numOfTxMessages = 10

        TxMessage = composeTxMsg(msgToTransmit)

        while counterOfTxMsg < numOfTxMessages:
           counterOfTxMsg = counterOfTxMsg + 1
           print("Nr of Rx data: ", counterOfTxMsg)

           print(" --> Tx data:",[hex(x) for x in TxMessage])
           ser.write(TxMessage)

           RxMessage = ser.readline()
           print(" <-- Rx data:",[hex(x) for x in RxMessage])

           crcCheck(RxMessage)

    except Exception:
        print("No data recieved " )



except Exception:
    print ("error open serial port: ")
    exit()

finally:
    ser.close()
    print("com port closed")





