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
# data = b'Hello, World!'
# print("1 - Entered data in binary format :",data)


# input_string = input("Enter data you want to send->")
# data1 =(''.join(format(ord(x), 'b') for x in input_string))
# print("Entered data in binary format :",data1)


# String for CRC calculation: 0x04A8 0x17C0 0x0000 0xED80 0x0000
# Transmission order: 0xA8 0x02 0xC0 0x17 0x00 0x00 0x80 0xED 0x00 0x00 0x0B 0x96

# CRC-CCITT (16-bit) of 'b'\x04\xa8\x17\xc0\x00\x00\xed\x80\x00\x00'' is: 0x960B

# maxon crc OK
# msg = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xB0, 0x30, 0x00, 0x2E, 0x62])
# crc data 0260B0010030 -> 0x622E

# Hex data
# hex_data = "04A817C00000ED800000"
msg = bytearray([0x90, 0x02, 0x60, 0x02, 0x01, 0xB0, 0x30, 0x00, 0x2E, 0x62])
# hex_data = "9002600201B030000000"
hex_data = "0260B0010030"

# hex_data = "0260600101E4"

read_data = b'\x90\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x005\xad'
# Convert hex data to bytes
data = bytes.fromhex(hex_data)


crc_ccitt_16 = crc_ccitt_16(data)

print(f"CRC-CCITT (16-bit) of '{data}' is: 0x{crc_ccitt_16:04X}")

print(F"crc is: 0x{crc_ccitt_16:04X}")
print("crc is:", crc_ccitt_16)

if crc_ccitt_16 == 38411:
    print("crc OK")
else:
    print("crc Not OK")

msg = bytearray([0x04, 0xa8, 0x17, 0xc0,  0x00,  0x00, 0xed, 0x80, 0x00, 0x00])
print("1 - message:",msg)
msg[8] = 0x0B
msg[9] = 0x96
print("2 - Tx message with crc:",msg)




def hex_to_little_endian(hex_string):
    little_endian_hex = bytearray.fromhex(hex_string)[::-1]
    return little_endian_hex

print(hex_to_little_endian('aabbccdd'))
# bytearray(b'\xdd\xcc\xbb\xaa')




# data = "F324658951425AF3EB00112233"
data = "00112233445566778899121314151617"
# bits = [16, 8, 8, 32, 8, 16]
bits = [16, 16, 16, 16, 16, 16, 16, 16]


bs = [data[i:i+2] for i in range(0, len(data), 2)] # get individual bytes
# ['F3', '24', '65', '89', '51', '42', '5A', 'F3', 'EB', '00', '11']

iterator = iter(bs)
result = []
for n in bits:
     chunk = [next(iterator) for _ in range(n//8)]
     result.extend(reversed(chunk))

print("".join(result))
# 24F36589F35A4251EB1100
# 11003322554477669988131215141716





# basic message   0      1     2      3      4      5     6         7
#               start, len,  ack, bills,escrow,resv'd,  end, checksum
# msg = bytearray([0x02, 0x08, 0x10, 0x7F,  0x00,  0x00, 0x03,     0x00])
# https://github.com/PyramidTechnologies/Python-RS-232/blob/master/host.py


# check crc online
# https://crccalc.com/?crc=04A817C00000ED800000&method=CRC-16/XMODEM&datatype=hex&outtype=hex
