#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 案例三
'''
给定数组arr，返回arr的最长递增子序列的长度，
比如arr=[2,1,5,3,6,4,8,9,7]，最长递增子序列为[1,3,4,8,9]返回其长度为5.

分析：
首先生成dp[n]的数组，dp[i]表示以必须arr[i]这个数结束的情况下产生的最大递增子序列的长度。
对于第一个数来说，很明显dp[0]为1，当我们计算dp[i]的时候，我们去考察i位置之前的所有位置，
找到i位置之前的最大的dp值，记为dp[j](0=<j<i),dp[j]代表以arr[j]结尾的最长递增序列，
而dp[j]又是之前计算过的最大的那个值，我们在来判断arr[i]是否大于arr[j],
如果大于dp[i]=dp[j]+1.计算完dp之后，我们找出dp中的最大值，即为这个串的最长递增序列。
'''

arr = [2, 1, 5, 3, 6, 4, 8, 9, 7]
n = len(arr)
dp = [0] * n
#print dp

dp[0] = 1
for i in range(1, n, 1):
    tmp_max = 0
    for j in range(0, i, 1):
        if dp[j] > tmp_max and arr[i] > arr[j]:
            tmp_max = dp[j]
    dp[i] = tmp_max + 1


max = dp[0]
for i in range(0,n,1):
    if max < dp[i]:
        max = dp[i]

print max