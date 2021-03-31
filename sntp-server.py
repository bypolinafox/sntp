import socket
import struct
import sys
import errno

offset = int(sys.argv[1])
server = 'time.windows.com'


def getNormalTime(server):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = '\x1b' + 47 * '\0'
    client.settimeout(5)
    try:
        client.sendto(data.encode('utf-8'), (server, 123))
        data, address = client.recvfrom(1024)
        t_secs = struct.unpack('!12I', data)[10]
        return (t_secs, data[36:40])
    except socket.error as error:
        if error.errno == errno.ECONNREFUSED:
            print("Не самолет, не птица — летит и матерится. "
                  "Знаешь, про кого это? Про техника ростелекома, "
                  "который, возможно, где-то накосячил и ты так и не "
                  "смог узнать время с разницей в " + offset + " секунд")

        elif error.errno == errno.ETIMEDOUT:
            print("https://shutniki.club/wp-content/uploads/2019/12/hatiko_mem_19_05120800-600x325.png")

        elif error.errno == errno.EADDRNOTAVAIL:
            print("Адрес, с которого запрашивается время, временно недоступен")

        else:
            print("Что-то пошло не так. "
                  "Можешь пока поиграть в "
                  "https://www.geoguessr.com/ ")

        sys.exit(0)



def getNTPResponse(req: bytes, offset: int, server: str):
    secs, msecs = getNormalTime(server)
    secs += offset
    res = bytearray(48)
    res[0] = (req[0] & 0x38) + 4
    res[1] = 1
    res[2] = req[2]
    res[3] = 0xEC
    res[12] = 0x4E
    res[13] = 0x49
    res[14] = 0x43
    res[15] = 0x53
    res[16:20] = secs.to_bytes(4, 'big')
    res[24:32] = req[40:48]
    res[32:36] = secs.to_bytes(4, 'big')
    res[36:40] = msecs
    res[40:48] = res[32:40]
    return res

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('', 123))
    while True:
        data, addr = s.recvfrom(1024)
        s.sendto(getNTPResponse(data, offset, server), addr)
