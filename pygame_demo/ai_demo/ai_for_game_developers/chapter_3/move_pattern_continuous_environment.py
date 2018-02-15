#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
from random import randint
from time import ctime,sleep
import math
from gameobjects.vector2 import Vector2
import time



# 600 * 600
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# 定义一些颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DEEP_SKY_BLUE = (0, 191, 255)
RED = (255, 0, 0)

# 定义下船转向的速度
ANGLE_SPEED = 10

# pygame初始化相关内容
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


# 定义一些类及相关方法
class Boat(object):
    def __init__(self, x, y, direction, boat_length, boat_width, speed=20, color=DEEP_SKY_BLUE):
        self.center_x = x
        self.center_y = y
        self.direction = direction
        self.boat_length = boat_length
        self.boat_width = boat_width
        self.color = color
        self.border_width = 1
        self.speed = speed


def format_boat_direction(direction):
    if math.fmod(direction, 360) >= 180:
        direction = -360 + math.fmod(direction, 360)
    elif math.fmod(direction, 360) <= 180 and math.fmod(direction, 360) > -180:
        direction = math.fmod(direction, 360)
    elif math.fmod(direction, 360) <= -180:
        direction = 360 + math.fmod(direction, 360)
    else:
        direction = math.fmod(direction, 360)
    return direction


def draw_boat(screen, boat):
    # 绘制多边形
    center_x = boat.center_x
    center_y = boat.center_y
    boat_length = boat.boat_length
    boat_width = boat.boat_width

    width = 1
    color = boat.color

    #boat_length边与x轴的夹角
    angle_degrees = boat.direction

    #对角线
    diagonal = math.sqrt(boat_length ** 2 + boat_width ** 2)
    #对角线与boat_length边的夹角
    #弧度
    angle1_radians = math.atan(boat_width * 1.0/boat_length)
    angle1_degrees = math.degrees(angle1_radians)
    #对角线与x轴夹角
    angle2_degrees = angle_degrees - angle1_degrees

    p4 = {}
    p4['x'] = center_x + diagonal * 0.5 * math.cos(math.radians(angle2_degrees))
    p4['y'] = center_y + diagonal * 0.5 * math.sin(math.radians(angle2_degrees))

    angle3_degrees = angle_degrees + angle1_degrees
    p2 = {}
    p2['x'] = center_x + diagonal * 0.5 * math.cos(math.radians(angle3_degrees))
    p2['y'] = center_y + diagonal * 0.5 * math.sin(math.radians(angle3_degrees))

    p3 = {}
    p3['x'] = center_x + (boat_length + boat_width) * 0.5 * math.cos(math.radians(angle_degrees))
    p3['y'] = center_y + (boat_length + boat_width) * 0.5 * math.sin(math.radians(angle_degrees))

    # 对称性
    p1 = {}
    p1['x'] = center_x * 2 - p4['x']
    p1['y'] = center_y * 2 - p4['y']

    p5 = {}
    p5['x'] = center_x * 2 - p2['x']
    p5['y'] = center_y * 2 - p2['y']

    pygame.draw.aalines(screen, color, True, [(p1['x'], p1['y']), (p2['x'], p2['y']), (p3['x'], p3['y']), (p4['x'], p4['y']), (p5['x'], p5['y'])], 1)
    # 画出中心
    pygame.draw.aaline(screen, color, (center_x, center_y), (center_x, center_y), 1)



class ControlData(object):

    def __init__(self, delta_heading_degrees_limit, delta_position_limit,
                 limit_heading_change, limit_position_change):
        # 载具的方向变化，正数表示；负数表示
        self.delta_heading_degrees_limit = delta_heading_degrees_limit
        # 载具的位置变化
        self.delta_position_limit = delta_position_limit
        # limit_heading_change 为 True，则每轮仿真循环中载具的相对位置变化
        # 会以 delta_heading_degrees_limit 来判断，是否进行下一个运动模式
        self.limit_heading_change = limit_heading_change
        # limit_position_change 为 True，则每轮仿真循环中载具的相对位置变化
        # 会以 delta_position_limit 来判断，是否进行下一个运动模式
        self.limit_position_change = limit_position_change


# 记录状态改变的结构体
class StateChangeData(object):

    def __init__(self, initial_heading_degrees, initial_position,
                 delta_heading_degress, delta_position, current_control_index):
        self.initial_heading = initial_heading_degrees
        # Vector2
        self.initial_position = initial_position
        self.delta_heading_degress = delta_heading_degress
        self.delta_position = delta_position
        self.current_control_index = current_control_index


def initial_pattern(boat, pattern_tracking):
    initial_pattern_tracking(boat, pattern_tracking)


def initial_pattern_tracking(boat, pattern_tracking):
    pattern_tracking.current_control_index = 0
    pattern_tracking.delta_heading_degress = 0
    pattern_tracking.delta_position = 0

    pattern_tracking.initial_heading = boat.direction
    pattern_tracking.initial_position = Vector2(boat.center_x, boat.center_y)


def do_pattern(boat, move_pattern, pattern_tracking):
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0

    current_control_index = pattern_tracking.current_control_index
    current_control_data = move_pattern[current_control_index]
    if current_control_data.limit_heading_change \
            and ( math.fabs(pattern_tracking.delta_heading_degress) >= math.fabs(current_control_data.delta_heading_degrees_limit)) \
            or current_control_data.limit_position_change\
                    and (pattern_tracking.delta_position >= current_control_data.delta_position_limit):
        initial_pattern_tracking(boat, pattern_tracking)
        current_control_index += 1
        pattern_tracking.current_control_index = current_control_index
        if pattern_tracking.current_control_index >= len(move_pattern):
            return False

    # 计算运动

    # 施加转向力
    if current_control_data.delta_heading_degrees_limit > 0:
        boat.direction += ANGLE_SPEED * time_passed_seconds

    elif current_control_data.delta_heading_degrees_limit < 0:
        boat.direction -= ANGLE_SPEED * time_passed_seconds

    # 计算boat的前进
    speed = boat.speed
    angle_degrees = boat.direction
    speed_x = speed * math.cos(math.radians(angle_degrees))
    speed_y = speed * math.sin(math.radians(angle_degrees))
    boat.center_x = boat.center_x + speed_x * time_passed_seconds
    boat.center_y = boat.center_y + speed_y * time_passed_seconds

    # 计算这组指令开始后，方向上的变化
    delta_heading = boat.direction - pattern_tracking.initial_heading
    pattern_tracking.delta_heading_degress = delta_heading
    # 计算这组指令开始后，位置上的变化
    delta_position_vector = Vector2(boat.center_x - pattern_tracking.initial_position.x,
                                    boat.center_y - pattern_tracking.initial_position.y)
    delta_position = delta_position_vector.length
    pattern_tracking.delta_position = delta_position

    return True


def update_simulation(boat, move_pattern, pattern_tracking, patrol, zigzag):
    if patrol:
        if not do_pattern(boat, move_pattern, pattern_tracking):
            initial_pattern_tracking(boat, pattern_tracking)

    if zigzag:
        if not do_pattern(boat, move_pattern, pattern_tracking):
            initial_pattern_tracking(boat, pattern_tracking)


# 定义一些变量
# 目标
boat1 = Boat(150, 100, 0, 40, 20, 20)

PATROL_ARRAY_SIZE = 8
ZIGZAG_ARRAY_SIZE = 4

# 巡逻模式
patrol_patterns = []
# 蛇形模式
zigzag_patterns = []

# 数据类型为StateChangeData，用于记录这些模式在执行时位置和方向上的变化
# self, initial_heading_degrees, initial_position, delta_heading_degress, delta_position, current_control_index
pattern_tracking = StateChangeData(0, Vector2(0, 0), 0, 0, 0)

# 前进200
control_data = ControlData(delta_heading_degrees_limit=0, delta_position_limit=200, limit_heading_change=False, limit_position_change=True)
patrol_patterns.append(control_data)
# 右转90度
control_data = ControlData(delta_heading_degrees_limit=90, delta_position_limit=0, limit_heading_change=True, limit_position_change=False)
patrol_patterns.append(control_data)
# 前进200
control_data = ControlData(delta_heading_degrees_limit=0, delta_position_limit=200, limit_heading_change=False, limit_position_change=True)
patrol_patterns.append(control_data)
# 右转90度
control_data = ControlData(delta_heading_degrees_limit=90, delta_position_limit=0, limit_heading_change=True, limit_position_change=False)
patrol_patterns.append(control_data)
# 前进200
control_data = ControlData(delta_heading_degrees_limit=0, delta_position_limit=200, limit_heading_change=False, limit_position_change=True)
patrol_patterns.append(control_data)
# 右转90度
control_data = ControlData(delta_heading_degrees_limit=90, delta_position_limit=0, limit_heading_change=True, limit_position_change=False)
patrol_patterns.append(control_data)
# 前进200
control_data = ControlData(delta_heading_degrees_limit=0, delta_position_limit=200, limit_heading_change=False, limit_position_change=True)
patrol_patterns.append(control_data)
# 右转90度
control_data = ControlData(delta_heading_degrees_limit=90, delta_position_limit=0, limit_heading_change=True, limit_position_change=False)
patrol_patterns.append(control_data)


# 蛇形模式
# 前进100
control_data = ControlData(delta_heading_degrees_limit=0, delta_position_limit=100, limit_heading_change=False, limit_position_change=True)
zigzag_patterns.append(control_data)
# 右转60度
control_data = ControlData(delta_heading_degrees_limit=60, delta_position_limit=0, limit_heading_change=True, limit_position_change=False)
zigzag_patterns.append(control_data)
# 前进100
control_data = ControlData(delta_heading_degrees_limit=0, delta_position_limit=100, limit_heading_change=False, limit_position_change=True)
zigzag_patterns.append(control_data)
# 左转60度
control_data = ControlData(delta_heading_degrees_limit=-60, delta_position_limit=0, limit_heading_change=True, limit_position_change=False)
zigzag_patterns.append(control_data)


# 上一秒时候的毫秒数
last_second = time.time()
# boat1的路径
path_boat1 = []
path_boat1.append(Vector2(boat1.center_x, boat1.center_y))


# 显示boat1的速度和角度
font = pygame.font.SysFont("simsunnsimsun", 15)
text_surface = font.render(u"Boat1, position:(" + str(round(boat1.center_x,2)) + "," + str(round(boat1.center_y,2)) + "), speed:" + str(boat1.speed) + ", direction:" + str(format_boat_direction(boat1.direction)), True, (0, 0, 255))


#
initial_pattern(boat1, pattern_tracking)

# 游戏主循环
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                # 船的角度
                boat1.direction -= ANGLE_SPEED

            elif event.key == K_RIGHT:
                # 船的角度
                boat1.direction += ANGLE_SPEED

            elif event.key == K_UP:
                boat1.speed += 1

            elif event.key == K_DOWN:
                boat1.speed -= 1

        elif event.type == KEYUP:
            # 如果用户放开了键盘，图就不要动了
            move = (0, 0)

    # 计算运动
    # 巡逻运动
    patrol = True
    zigzag = False
    update_simulation(boat1, patrol_patterns, pattern_tracking, patrol, zigzag)
    # 蛇形运行
    #patrol = True
    #zigzag = False
    #update_simulation(boat1, zigzag_patterns, pattern_tracking, patrol, zigzag)

    # 记录当前boat1和boat2的路径
    # 单位是秒
    current_second = time.time()
    # 以1秒为时间间隔取小船的点
    if current_second - last_second >= 1:
        # 如果连续3个点在一条直线上，那么中间点不保存
        # 当前点
        current_point = Vector2(boat1.center_x, boat1.center_y)
        if len(path_boat1) >= 2:
            # 上一个点
            last_1_point = path_boat1[-1]
            # 上上个点
            last_2_point = path_boat1[-2]
            vector_1 = Vector2(last_1_point.x - last_2_point.x, last_1_point.y - last_2_point.y)
            vector_2 = Vector2(current_point.x - last_2_point.x, current_point.y - last_2_point.y)

            if vector_1.x == 0 and vector_2 == 0 \
                    or vector_1.y / vector_1.x == vector_2.y / vector_2.x:
                # 在一条直线上，弹出上一个点
                pop_point = path_boat1.pop()
                #print pop_point.x, ',', pop_point.y
        # 获取当前boat1和boat2的点，放入到路径中
        path_boat1.append(current_point)
        # 将当前毫秒数赋值给上一秒毫秒数
        last_second = current_second

    # 绘制白色背景色
    screen.fill(WHITE)
    # 绘制boat1
    draw_boat(screen, boat1)

    # 绘制boat1的路径
    if len(path_boat1) > 1:
        pygame.draw.lines(screen, BLACK, False, path_boat1)
    elif len(path_boat1) == 1:
        pygame.draw.aaline(screen, BLACK, path_boat1[0], path_boat1[0] )

    # 显示boat1的速度和角度
    text_surface = font.render(u"Boat1, position:(" + str(round(boat1.center_x,2)) + "," + str(round(boat1.center_y,2)) + "), speed:" + str(boat1.speed) + ", direction:" + str(format_boat_direction(boat1.direction)), True, (0, 0, 255))

    screen.blit(text_surface, (0, 0))

    pygame.display.update()
