#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
import time
from gameobjects.vector2 import Vector2
import math

# 600 * 600
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 650

# 定义一些颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DEEP_SKY_BLUE = (0, 191, 255)
RED = (255, 0, 0)

# 定义下船转向的速度
ANGLE_SPEED = 10
# 定义下船的加速度
ACCELERATED_SPEED = 10

# 单位的长度和宽度
UNIT_WIDTH = 20
UNIT_LENGTH = 40

WIDE_VIEW = True
LIMITED_VIEW = False
NARROW_VIEW = False


# 视野角度
WIDE_VIEW_FIELD_ANGLE_DEGREES = 270
LIMITED_VIEW_FIELD_ANGLE_DEGREES = 180
NARROW_VIEW_FIELD_ANGLE_DEGREES = 90

# 视野半径因子
# 视野半径 = 视野半径因子 × 单位长度
WIDE_VIEW_FIELD_REDIUS_FACTOR = 5
LIMITED_VIEW_FIELD_REDIUS_FACTOR = 10
NARROW_VIEW_FIELD_REDIUS_FACTOR = 15

# 分隔距离因子
# 安全距离 = 分隔距离因子 × 单位长度
SEPARATION_FACTOR = 3.0

# 为了调整单位的转向和前进后退，施加在单位上的一个力。真正施加在单位上的力是参考这个力进行调整的
STREERING_FORCE = 10


# pygame初始化相关内容
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


# 将目标的位置转换为相对于追击者局部坐标的位置（局部坐标以追击者中心为原点，前进方向为y轴方向）
# boat1 目标，boat2追击者
# 坐标系旋转变换公式
# angle_a_degrees 表示绝对坐标系x轴到相对坐标系x轴的角度
def v_rotate_2d(delta_vector, angle_a_degrees):

    # 全局坐标系下，相对位置的向量
    x1 = delta_vector.x
    y1 = delta_vector.y

    x2 = x1 * math.cos(math.radians(angle_a_degrees)) + y1 * math.sin(math.radians(angle_a_degrees))
    y2 = -1.0 * x1 * math.sin(math.radians(angle_a_degrees)) + y1 * math.cos(math.radians(angle_a_degrees))
    return Vector2(x2, y2)


# 定义一些类及相关方法
class Boat(object):
    def __init__(self, x, y, direction, boat_length, boat_width, speed=20, is_leader=False, color=DEEP_SKY_BLUE):
        self.center_x = x
        self.center_y = y
        self.direction = direction
        self.boat_length = boat_length
        self.boat_width = boat_width
        self.color = color
        self.border_width = 1
        self.speed = speed
        self.is_leader = is_leader


# 对单个单位施加力之后，更新单个单位的速度和转向
# unit是受力单位
# force是施加的力，force.x表示转向方面的力，force.y表示前进后退方向的力
def update_single_unit(boat, force):
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0
    # print force
    # 转向方面的力
    if force.x > 0:
        boat.direction -= ANGLE_SPEED * (math.fabs(force.x / STREERING_FORCE)) * time_passed_seconds
    elif force.x == 0:
        pass
    else:
        boat.direction += ANGLE_SPEED * (math.fabs(force.x / STREERING_FORCE)) * time_passed_seconds

    # 前进后退方向的力
    if force.y > 0:
        boat.speed -= ACCELERATED_SPEED * (math.fabs(force.y / STREERING_FORCE)) * time_passed_seconds
    elif force.y == 0:
        pass
    else:
        boat.speed += ACCELERATED_SPEED * (math.fabs(force.y / STREERING_FORCE)) * time_passed_seconds


# units是群聚中所有单位的数组
# force是施加在群聚中leader上的力
def update_simulation(units, force):
    dt = time.time()
    # 初始化后端缓冲区

    # 更新玩家控制的单位units[0]
    # 玩家通过左右键控制方向
    leader = units[0]
    update_single_unit(leader, force)

    # 单位移动到屏幕边界的时候从另外一侧的屏幕出现
    if leader.center_x == SCREEN_WIDTH:
        leader.center_x = 0
    elif leader.center_x == 0:
        leader.center_x = SCREEN_WIDTH

    if leader.center_y == SCREEN_HEIGHT:
        leader.center_y = 0
    elif leader.center_y == 0:
        leader.center_y = SCREEN_HEIGHT

    # 更新计算机控制的单位
    for i in range(0, len(units), 1):
        unit = units[i]
        do_unit_ai(units, i)

        # 单位移动到屏幕边界的时候从另外一侧的屏幕出现
        if unit.center_x == SCREEN_WIDTH:
            unit.center_x = 0
        elif unit.center_x == 0:
            unit.center_x = SCREEN_WIDTH

        if unit.center_y == SCREEN_HEIGHT:
            unit.center_y = 0
        elif unit.center_y == 0:
            unit.center_y = SCREEN_HEIGHT

        # 根据单位不同的角色定位（leader, interceptor），给单位绘制不同的颜色
    # 把后端缓冲区复制到屏幕上


# units是群聚中所有单位的数组
# i为当前所处理的单位在units中的索引下标
def do_unit_ai(units, i):

    # 临近单位数量
    neighbors = 0
    do_block = WIDE_VIEW or LIMITED_VIEW or NARROW_VIEW

    # 初始化
    average_position = Vector2(0, 0)
    average_speed = Vector2(0, 0)
    # force是指，为了调整单位，而施加在单位上的力，既包括转向的力，也包括加减速的力
    force = Vector2(0, 0)

    # 检查并收集临近单位的信息
    for j in range(0, len(units), 1):
        if j != i:
            in_view = False
            delta = Vector2(units[j].center_x, units[j].center_y) - Vector2(units[i].center_x, units[i].center_y)
            # units[j]在units[i]的相对坐标系中的位置
            w = v_rotate_2d(delta, 90 - units[i].direction)
            if w.y == 0:
                angle_b_degrees = 90
                view_field_degrees = angle_b_degrees
            elif w.y > 0:
                angle_b_degrees = math.degrees(math.atan(math.fabs(w.x / w.y)))
                view_field_degrees = angle_b_degrees
            else:
                angle_b_degrees = math.degrees(math.atan(math.fabs(w.x / w.y)))
                view_field_degrees = 180 - angle_b_degrees

            if WIDE_VIEW:
                if view_field_degrees <= WIDE_VIEW_FIELD_ANGLE_DEGREES / 2.0:
                    in_view = True
                else:
                    in_view = False
                view_field_redius = WIDE_VIEW_FIELD_REDIUS_FACTOR * UNIT_LENGTH
            if LIMITED_VIEW:
                if view_field_degrees <= LIMITED_VIEW_FIELD_ANGLE_DEGREES / 2.0:
                    in_view = True
                else:
                    in_view = False
                view_field_redius = LIMITED_VIEW_FIELD_REDIUS_FACTOR * UNIT_LENGTH
            if NARROW_VIEW:
                if view_field_degrees <= NARROW_VIEW_FIELD_ANGLE_DEGREES / 2.0:
                    in_view = True
                else:
                    in_view = False
                view_field_redius = NARROW_VIEW_FIELD_REDIUS_FACTOR * UNIT_LENGTH
            if in_view:
                # 如果在视野内，并且距离小于安全距离，那么应该远离
                if delta.length <= view_field_redius:
                    # TODO
                    average_position += Vector2(units[j].center_x, units[j].center_y)
                    speed_x = units[j].speed * math.cos(math.radians(units[j].direction))
                    speed_y = units[j].speed * math.sin(math.radians(units[j].direction))
                    average_speed += Vector2(speed_x, speed_y)
                    neighbors += 1

            # 分隔
            # 分隔意指我们想让每个单位彼此间保持最小距离。
            # 即，根据凝聚和对齐规则，他们会试着靠近一点。我们不想让这些单位撞在一起，或者更糟的是，在某个时刻重叠在一起。
            # 因此，我们采用分隔手段，让每个单位和其视野内的单位保持某一预定的最小间隔距离
            if in_view:
                if delta.length <= SEPARATION_FACTOR * UNIT_LENGTH:
                    # 因为此处是计算分隔，所以m和计算凝聚和对齐时不同
                    if w.x < 0:
                        # 如果w的x值小于0，则必须右转（左侧）
                        m = 1
                    elif w.x > 0:
                        # 如果w的x值大于0，则表示临近单位的平均位置位于units[i]的右侧，units[i]需要左转
                        m = -1
                    # delta是units[j]和units[i]的距离
                    force.x += m * STREERING_FORCE * SEPARATION_FACTOR * UNIT_LENGTH / delta.length

    # 凝聚规则
    # 凝聚意指，我们想让所有单位待在同一个群体当中。
    # 为了满足这条规则，每隔单位都应该朝其临近单位的平均位置前进
    if do_block and neighbors > 0:
        average_position = average_position / neighbors

        speed_x = units[i].speed * math.cos(math.radians(units[i].direction))
        speed_y = units[i].speed * math.sin(math.radians(units[i].direction))
        v = Vector2(speed_x, speed_y)
        v.normalise()
        u = average_position - Vector2(units[i].center_x, units[i].center_y)
        u.normalise()
        w = v_rotate_2d(u, 90 - units[i].direction)

        # 确定和转向力有关的乘数m
        if w.x < 0:
            # 如果w的x值小于0，则必须右转（左侧）
            m = -1
        elif w.x > 0:
            # 如果w的x值大于0，则表示临近单位的平均位置位于units[i]的右侧，units[i]需要左转
            m = 1

        # 最后，做一个快速检查，以得知v和u的内积是否大于-1且小于1。这一定要做，因为这个内积要在计算两向量夹角的时候用到，
        # 而反余弦函数的自变量范围在-1到1之间
        if math.fabs(v * u) < 1:
            # 实际计算满足凝聚规则的转向力。
            # 上面的m实际上已经计算出应该向左还是向右转，现在自己算的是转向的力度大小
            # fs.x += m * 一个系数 * math.degrees(math.acos(v*u))
            # 平均位置向量和速度向量夹角，也就是平均位置向量与units[i]的方向的夹角，夹角越大，也就是所需要的转向力越大
            force.x += m * STREERING_FORCE * math.degrees(math.acos(v*u))


    # 对齐规则
    # 对齐，意指我们想让群聚中所有的单位都朝大概的方位运动。
    # 为了实现这条规则，每隔单位都应该在行进时，试着以等同于临近单位行进方向的方向前进。
    if do_block and neighbors > 0:
        average_speed = average_speed / neighbors
        u = average_speed
        u.normalise()

        speed_x = units[i].speed * math.cos(math.radians(units[i].direction))
        speed_y = units[i].speed * math.sin(math.radians(units[i].direction))
        v = Vector2(speed_x, speed_y)
        v.normalise()

        # 平均速度的向量相对于units[i]的的局部坐标系中的表示
        w = v_rotate_2d(u, 90 - units[i].direction)

        # 确定和转向力有关的乘数m
        if w.x < 0:
            # 如果w的x值小于0，则必须右转（左侧）
            m = -1
        elif w.x > 0:
            # 如果w的x值大于0，则表示临近单位的平均位置位于units[i]的右侧，units[i]需要左转
            m = 1

        # 最后，做一个快速检查，以得知v和u的内积是否大于-1且小于1。这一定要做，因为这个内积要在计算两向量夹角的时候用到，
        # 而反余弦函数的自变量范围在-1到1之间
        if math.fabs(v * u) < 1:
            # 实际计算满足凝聚规则的转向力。
            # 上面的m实际上已经计算出应该向左还是向右转，现在自己算的是转向的力度大小
            # fs.x += m * 一个系数 * math.degrees(math.acos(v*u))
            # 平均速度向量和速度向量夹角，也就是平均位置向量与units[i]的方向的夹角，夹角越大，也就是所需要的转向力越大
            force.x += m * STREERING_FORCE * math.degrees(math.acos(v * u))


    # 处理转向力对units[i]的影响
    update_single_unit(units[i], force)


