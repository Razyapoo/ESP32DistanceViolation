from sqlite3 import connect
import sys
import time
# import turtle
import cmath
import socket
import json

hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
path = '/home/oskar/Documents/Master Thesis/ESP32/Python distance visualization/experiment.txt'
sys.stdout = open(path, 'w')
UDP_PORT_1 = 30001
UDP_PORT_2 = 30002
UDP_PORT_3 = 30003

sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_1.bind(('', UDP_PORT_1))
sock_2.bind(('', UDP_PORT_2))
sock_3.bind(('', UDP_PORT_3))

sock_1.listen(1)
sock_2.listen(1)
sock_3.listen(1)

data_1, addr_1 = sock_1.accept()
data_2, addr_2 = sock_2.accept()
data_3, addr_3 = sock_3.accept()

distance_a1_a2 = 9.0
meter2pixel = 100
# range_offset = 0.9

def read_data():
    if data_1:
        line_1 = data_1.recv(1024).decode('UTF-8')
    
    if data_2:
        line_2 = data_2.recv(1024).decode('UTF-8')
    
    if data_3:
        line_3 = data_3.recv(1024).decode('UTF-8')

    uwb_list = {}
    uwb_list_1 = []
    uwb_list_2 = []
    uwb_list_3 = []

    try:
        uwb_data_1 = json.loads(line_1)
        uwb_data_2 = json.loads(line_2)
        uwb_data_3 = json.loads(line_3)

        print(uwb_data_1)
        print(uwb_data_2)
        print(uwb_data_3)
        
        uwb_list_1 = uwb_data_1["links"]
        uwb_list_2 = uwb_data_2["links"]
        uwb_list_3 = uwb_data_3["links"]
        # for uwb_archor in uwb_list:
        #     print(uwb_archor)
        uwb_list = {'1': uwb_list_1, '2': uwb_list_2, '3': uwb_list_3};

    except:
        print(line_1)
        print(line_2)
        print(line_3)
    print("")

    return uwb_list


def tag_pos(a, b, c):
    # p = (a + b + c) / 2.0
    # s = cmath.sqrt(p * (p - a) * (p - b) * (p - c))
    # y = 2.0 * s / c
    # x = cmath.sqrt(b * b - y * y)
    # if (a > 0 and b > 0 and c > 0):
    cos_a = (b * b + c*c - a * a) / (2 * b * c)
    x = b * cos_a
    y = b * cmath.sqrt(1 - cos_a * cos_a)

    return round(x.real, 1), round(y.real, 1)


def uwb_range_offset(uwb_range):

    temp = uwb_range
    return temp


def main():

    a1_range = 0.0
    a2_range = 0.0

    while True:
        
        list = read_data()
        tagID = "";
        for tag in list:
            if list[tag]:
                node_count = 0  
                for one in list[tag]:
                    if one["A"] == "101":
                        tagID = one["T"];
                        a1_range = uwb_range_offset(float(one["R"]))
                        node_count += 1

                    if one["A"] == "102":
                        tagID = one["T"];
                        a2_range = uwb_range_offset(float(one["R"]))
                        node_count += 1

                if node_count == 2:
                    if a1_range == 0:
                        x = -250;
                        y = 150;
                    else:
                        x, y = tag_pos(a2_range, a1_range, distance_a1_a2)
                    print(x, y)
                    if tagID == "1": 
                        print("Tag 1", x, y)
                    elif tagID == "2": 
                        print("Tag 2", x, y)
                    elif tagID == "3": 
                        print("Tag 3", x, y)

    turtle.mainloop()


if __name__ == '__main__':
    main()
