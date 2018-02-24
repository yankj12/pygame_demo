#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 案例二
'''
给定一个矩阵m，从左上角开始每次只能向右走或者向下走，最后达到右下角的位置，
路径中所有数字累加起来就是路径和，返回所有路径的最小路径和，
如果给定的m如下，那么路径1,3,1,0,6,1,0就是最小路径和，返回12.
1 3 5 9
8 1 3 4
5 0 6 1
8 8 4 0
分析：对于这个题目，假设m是m行n列的矩阵，那么我们用dp[m][n]来抽象这个问题，
dp[i][j]表示的是从原点到i,j位置的最短路径和。
我们首先计算第一行和第一列，直接累加即可，那么对于其他位置，要么是从它左边的位置达到，要么是从上边的位置达到，
我们取左边和上边的较小值，然后加上当前的路径值，就是达到当前点的最短路径。
然后从左到右，从上到下依次计算即可。
'''

#dp = [[0]*4]*4    # 这样的复制是浅层复制。dp[1][1] = 1,会导致很多dp[x][1]都变成1
dp = []
for i in range(0,4,1):
    a = []
    for j in range(0,4,1):
        a.append(0)
    dp.append(a)

#dp[1][1] = 1
#print dp

matrix = [[1,3,5,9],
     [8,1,3,4],
     [5,0,6,1],
     [8,8,4,0]]

#print matrix


def min_path_sum(matrix, i, j):
    if i == 0 and j == 0:
        return matrix[i][j]

    # 只有从左边或者上边才能达到i,j
    if i > 0:
        left_path_sum = min_path_sum(matrix, i-1, j)
    else:
        left_path_sum = None

    if j > 0:
        upper_path_sum = min_path_sum(matrix, i, j-1)
    else:
        upper_path_sum = None

    if left_path_sum == None:
        min_sum = upper_path_sum

    if upper_path_sum == None:
        min_sum = left_path_sum

    if left_path_sum != None and upper_path_sum != None:
        min_sum = left_path_sum
        if min_sum > upper_path_sum:
            min_sum = upper_path_sum

    min_sum += matrix[i][j]
    return min_sum

print min_path_sum(matrix, 3, 3)
