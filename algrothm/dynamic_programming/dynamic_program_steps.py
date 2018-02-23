#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 案例一：
'''
有n级台阶，一个人每次上一级或者两级，问有多少种走完n级台阶的方法。
分析：动态规划的实现的关键在于能不能准确合理的用动态规划表来抽象出
实际问题。在这个问题上，我们让f(n)表示走上n级台阶的方法数。

那么当n为1时，f(n) = 1,n为2时，f(n) =2,
就是说当台阶只有一级的时候，方法数是一种，台阶有两级的时候，方法数为2。
那么当我们要走上n级台阶，必然是从n-1级台阶迈一步或者是从n-2级台阶迈两步，
所以到达n级台阶的方法数必然是到达n-1级台阶的方法数加上到达n-2级台阶的方法数之和。
即f(n) = f(n-1)+f(n-2)，我们用dp[n]来表示动态规划表，dp[i],i>0,i<=n,表示到达i级台阶的方法数。
'''

dp = []

def calculate_steps(n):

    if n == 1 or n == 2:
        if len(dp) < 1:
            dp.append(1)
        else:
            dp[n-1] = 1

        if len(dp) < 2:
            dp.append(2)
        else:
            dp[n - 1] = 2
        return n

    # 判断 n-1 的状态有没有被计算过
    if len(dp) < n or dp[n-1] == None:
        num = calculate_steps(n-1)
        if len(dp) < n:
            dp.append(num)
        if len(dp) >= n and dp[n-1] == None:
            dp[n-1] = num

    # 判断 n-2 的状态有没有被计算过
    if len(dp) < n-1 or dp[n-2] == None:
        num = calculate_steps(n-2)
        if len(dp) < n-1:
            dp.append(num)
        if len(dp) >= n-1 and dp[n-2] == None:
            dp[n-2] = num

    return dp[n-1] + dp[n-2]


print calculate_steps(10)