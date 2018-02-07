#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


class PathPoint(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col


class AiEntity(object):

    def __init__(self, k_max_path_length):
        # 支持的最大模式segment数量
        self.k_max_path_length = k_max_path_length
        # 模式中实际segment的数量
        self.path_size = 0
        # 其实在python中k_max_path_length和path_size是非必要的，可以直接len(path)解决
        # 定义路径变量
        self.path = []
        # 设置偏移量
        self.pattern_offset


    # 初始化路径
    def initialize_path_array(self):
        for i in range(0, self.k_max_path_length, 1):
            # 初始化为(-1,-1)，是因为砖块环境下-1不是有效坐标
            point = PathPoint(-1, -1)
            self.path.append(point)


    # 向模式数组中添加环节，段落
    def build_path_segment(self, current_point, end_point):
        # k_max_path_length = math.fabs(end_point.row - current_point.row) + math.fabs(end_point.col - current_point.col)

        row = current_point.row
        col = current_point.col
        end_row = end_point.row
        end_col = end_point.col

        next_row = row
        next_col = col
        delta_row = end_row - row
        delta_col = end_col - col

        # 这一轮要走的row数
        step_row = None
        # 这一轮要走的col数
        step_col = None
        current_step = None
        fraction = None

        for i in range(0, self.k_max_path_length, 1):
            if self.path[i].row == -1 and self.path[i].col == -1:
                current_step = i
                break

        step_row = -1 if delta_row < 0 else step_row = 1
        step_col = -1 if delta_col < 0 else step_col = 1

        delta_row = math.fabs(delta_row * 2)
        delta_col = math.fabs(delta_col * 2)

        self.path[current_step].row = next_row
        self.path[current_step].col = next_col
        current_step += 1

        if current_step >= self.k_max_path_length:
            return

        if delta_col > delta_row:
            fraction = delta_row * 2 - delta_col
            while next_col != end_col:
                if fraction >= 0:
                    next_row += step_row
                    fraction = fraction - delta_col

                next_col = next_col + step_col
                fraction = fraction + delta_row

                self.path[current_step].row = next_row
                self.path[current_step].col = next_col

                current_step += 1
                if current_step >= self.k_max_path_length:
                    return
        else:
            fraction = delta_col * 2 - delta_row
            while next_row != end_row:
                if fraction >= 0:
                    next_col += step_col
                    fraction = fraction - delta_row

                next_row = next_row + step_row
                fraction = fraction + delta_col

                self.path[current_step].row = next_row
                self.path[current_step].col = next_col

                current_step += 1
                if current_step >= self.k_max_path_length:
                    return


    # 标准化函数
    # 将模式标准化，使其以相对坐标表示，而非绝对坐标。这样标准化的模式才不会在游戏领域里和特定的起点位置绑定在一起。
    # 一旦把模式建立起来并且标准化，就能在任何游戏中使用。
    def normalize_pattern(self):

        origin = self.path[0]
        for i in range(0, self.k_max_path_length, 1):
            if self.path[i].row == -1 and self.path[i].col == -1:
                self.path_size = i
                break
        for i in range(0, self.path_size, 1):
            self.path[i].row = self.path[i].row - origin.row
            self.path[i].col = self.path[i].col - origin.col

    # 设置偏移量
    def set_pattern_offset(self, pattern_offset=PathPoint(0,0)):
        self.pattern_offset = pattern_offset




# 准备一些数据
entity_list = []

entity = AiEntity(10)
entity.initialize_path_array()
entity.build_path_segment(PathPoint(2, 2), PathPoint(2, 10))
entity.build_path_segment(PathPoint(2, 10), PathPoint(10, 10))
entity.build_path_segment(PathPoint(10, 10), PathPoint(10, 2))
entity.build_path_segment(PathPoint(10, 2), PathPoint(2, 2))
entity.normalize_pattern()
entity.set_pattern_offset(PathPoint(3, 3))

entity_list.append(entity)

