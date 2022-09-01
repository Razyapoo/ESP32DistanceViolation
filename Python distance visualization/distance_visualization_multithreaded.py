from sqlite3 import connect
import time
import turtle
import cmath
import socket
import json
from _thread import *
import threading

# hostname = socket.gethostname()
# UDP_IP = socket.gethostbyname(hostname)
# print("***Local ip: " + str(UDP_IP) + "***")
UDP_PORT = 30002
# print_lock = threading.Lock()
# data, addr = sock.accept()
# global data;
# global addr;
a1_range = 0.0
a2_range = 0.0
distance_a1_a2 = 3.0
meter2pixel = 100
range_offset = 0.9


def screen_init(width=1200, height=800, t=turtle):
    t.setup(width, height)
    t.tracer(False)
    t.hideturtle()
    t.speed(0)


def turtle_init(t=turtle):
    t.hideturtle()
    t.speed(0)


def draw_line(x0, y0, x1, y1, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x0, y0)
    t.down()
    t.goto(x1, y1)
    t.up()


def draw_fastU(x, y, length, color="black", t=turtle):
    draw_line(x, y, x, y + length, color, t)


def draw_fastV(x, y, length, color="black", t=turtle):
    draw_line(x, y, x + length, y, color, t)


def draw_cycle(x, y, r, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x, y - r)
    t.setheading(0)
    t.down()
    t.circle(r)
    t.up()


def fill_cycle(x, y, r, color="black", t=turtle):
    t.up()
    t.goto(x, y)
    t.down()
    t.dot(r, color)
    t.up()


def write_txt(x, y, txt, color="black", t=turtle, f=('Arial', 12, 'normal')):

    t.pencolor(color)
    t.up()
    t.goto(x, y)
    t.down()
    t.write(txt, move=False, align='left', font=f)
    t.up()


def draw_rect(x, y, w, h, color="black", t=turtle):
    t.pencolor(color)

    t.up()
    t.goto(x, y)
    t.down()
    t.goto(x + w, y)
    t.goto(x + w, y + h)
    t.goto(x, y + h)
    t.goto(x, y)
    t.up()


def fill_rect(x, y, w, h, color=("black", "black"), t=turtle):
    t.begin_fill()
    draw_rect(x, y, w, h, color, t)
    t.end_fill()
    pass


def clean(t=turtle):
    t.clear()


def draw_ui(t):
    write_txt(-300, 250, "UWB Position", "black",  t, f=('Arial', 32, 'normal'))
    fill_rect(-400, 200, 800, 40, "black", t)
    write_txt(-50, 205, "WALL", "yellow",  t, f=('Arial', 24, 'normal'))


def draw_uwb_anchor(x, y, txt, range, t):
    r = 20
    fill_cycle(x, y, r, "green", t)
    write_txt(x + r, y, txt + ": " + str(range) + "M",
              "black",  t, f=('Arial', 16, 'normal'))


def draw_uwb_tag(x, y, txt, t):
    pos_x = -250 + int(x * meter2pixel)
    pos_y = 150 - int(y * meter2pixel)
    r = 20
    fill_cycle(pos_x, pos_y, r, "blue", t)
    write_txt(pos_x, pos_y, txt + ": (" + str(x) + "," + str(y) + ")",
              "black",  t, f=('Arial', 16, 'normal'))


def read_data():

    line = data.recv(1024).decode('UTF-8')

    uwb_list = []

    try:
        uwb_data = json.loads(line)
        print(uwb_data)

        uwb_list = uwb_data["links"]
        for uwb_archor in uwb_list:
            print(uwb_archor)

    except:
        print(line)
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

def on_new_tag(data, addr):
    node_count = 0
    list = read_data()
    tagID = "";
    for one in list:
        if one["A"] == "101":
            tagID = one["T"];
            # clean(t_a1)
            # a1_range = uwb_range_offset(float(one["R"]))
            # draw_uwb_anchor(-250, 150, "A-1(0,0)", a1_range, t_a1)
            node_count += 1

        if one["A"] == "102":
            tagID = one["T"];
            # clean(t_a2)
            # a2_range = uwb_range_offset(float(one["R"]))
            # draw_uwb_anchor(-250 + meter2pixel * distance_a1_a2,
            #                 150, "A-2(" + str(distance_a1_a2)+")", a2_range, t_a2)
            node_count += 1

    if node_count == 2:
    #     x, y = tag_pos(a2_range, a1_range, distance_a1_a2)
    #     print(x, y)
    #     clean(t_a3)
    #     draw_uwb_tag(x, y, "TAG-1", t_a3)
        if tagID == "1":
            if a1_range == 0:
                x = -250;
                y = 150;
            else:
                x, y = tag_pos(a2_range, a1_range, distance_a1_a2)
            print(tagID, ": x: " ,x, "y: ",y)
            # clean(t_a3)
            # draw_uwb_tag(x, y, "TAG-1", t_a3)
            # sock.close();
        
        if tagID == "2":
            if a1_range == 0:
                x = -250;
                y = 150;
            else:
                x, y = tag_pos(a2_range, a1_range, distance_a1_a2)
            print(tagID, ": x: " ,x, "y: ",y)
            # clean(t_a4)
            # draw_uwb_tag(x, y, "TAG-2", t_a4)
            # sock.close();
    # time.sleep(0.3)
    data.close()
    # print_lock.release()

if __name__ == '__main__':
    # global t_ui, t_a1, t_a2, t_a3, t_a4;
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', UDP_PORT))
    sock.listen(1)
    
    # t_ui = turtle.Turtle()
    # t_a1 = turtle.Turtle()
    # t_a2 = turtle.Turtle()
    # t_a3 = turtle.Turtle()
    # t_a4 = turtle.Turtle()
    # turtle_init(t_ui)
    # turtle_init(t_a1)
    # turtle_init(t_a2)
    # turtle_init(t_a3)
    # turtle_init(t_a4)

    # draw_ui(t_ui)

    while True:
        global data;
        global addr;
        data, addr = sock.accept()
        # print_lock.acquire()
        start_new_thread(on_new_tag,(data,addr))
        

    # turtle.mainloop()
