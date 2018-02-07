#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class PathPoint(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

# 定义路径变量
path = []

# 初始化路径
def initialize_path_array(k_max_path_length):
    for i in range(0, k_max_path_length, 1):
        # 初始化为(-1,-1)，是因为砖块环境下-1不是有效坐标
        point = PathPoint(-1, -1)
        path.append(point)


def build_path_segment(current_point, end_point):
    k_max_path_length = math.fabs(end_point.row - current_point.row) + math.fabs(end_point.col - current_point.col)

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

    for i in range(0, k_max_path_length, 1):
        if path[i].row == -1 and path[i].col == -1:
            current_step = i
            break

    step_row = -1 if delta_row < 0 else step_row = 1
    step_col = -1 if delta_col < 0 else step_col = 1

    delta_row = math.fabs(delta_row * 2)
    delta_col = math.fabs(delta_col * 2)

    path[current_step].row = next_row
    path[current_step].col = next_col
    current_step += 1

    if current_step >= k_max_path_length:
        return

    if delta_col > delta_row:
        fraction = delta_row * 2 - delta_col
        while next_col != end_col:
            if fraction >= 0:
                next_row += step_row
                fraction = fraction - delta_col

            next_col = next_col + step_col
            fraction = fraction + delta_row

            path[current_step].row = next_row
            path[current_step].col = next_col

            current_step += 1
            if current_step >= k_max_path_length:
                return
    else:
        fraction = delta_col * 2 - delta_row
        while next_row != end_row:
            if fraction >= 0:
                next_col += step_col
                fraction = fraction - delta_row

            next_row = next_row + step_row
            fraction = fraction + delta_col

            path[current_step].row = next_row
            path[current_step].col = next_col

            current_step += 1
            if current_step >= k_max_path_length:
                return

