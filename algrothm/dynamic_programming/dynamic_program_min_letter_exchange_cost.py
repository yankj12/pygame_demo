#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 案例六 字符替换最小代价问题
'''
给定两个字符串str1，str2，在给定三个整数ic,dc,rc，分别代表插入，删除和替换一个字符的代价。返回将str1
编辑成str2的代价，比如，str1="abc",str2="adc",ic=5,dc=3,rc=2,从str1到str2，将'b'换成'd'代价最小，所以返回2.

分析：
在构建出动态规划表的时候，关键是搞清楚每个位置上数值的来源。
首先我们生成dp[M+1][N+1]的动态规划表，M代表str1的长度，N代表str2的长度，
那么dp[i][j]就是str1[0..i-1]变成str2[0...j-1]的最小代价，则dp[i][j]的来源分别来自以下四种情况：
a、首先将str1[i-1]删除，变成str1[0...i-2],
  然后将str1[0...i-2]变成str2[0...j-1],
  那么dp[i-1][j]就代表从str1[0..i-2]到str2[0...j-1]的最小代价，
  所以：dp[i][j] = dp[i-1][j]+dc;
b、同理也可以是从str1[0...i-1]变成str2[0...j-2]，
  然后再插入str2[j-1],dp[i][j-1]就代表从str1[0...i-1]变成str2[0...j-2]的最小大家，
  所以：dp[i][j] = dp[i][j-1]+ic;
c、如果str[i-1] == str2[j-1],则只需要将str1[0...i-2]变成str2[0...j-2]，此时dp[i][j] = dp[i-1][j-1];
d、如果str1[i-1]!=str2[j-1],则我们只需要将str1[i-1]替换成str2[j-1],此时dp[i][j] = dp[i-1][j-1]+rc;
在这四种情况当中，我们选取最小的一个，即为最小代价。
'''

# 为什么只有上面四种情况？
# 因为操作只有三种：删除、增加、替换。
# 那么两个字符串变成相等，我们只考虑变成最后相等的前一步，
# 只可能是：删除一个字母、添加一个字母、替换一个字母、最后一个字母不需要替换
# 如下：
# str1比str2多了最后一个字母，删除最后一个字母即可，就是上面的a
# str1比str2少了最后一个字母，增加最后一个字母即可，就是上面的b
# 两个字符串最后一个字母相等，不需要替换
# 两个字符串最后一个字母不相等，需要替换

# 单个字符替换的代价
ic = 5
dc = 3
rc = 2

str1 = "ab12cd3"
str2 = "abcdf"

m = len(str1)
n = len(str2)


# 获取两个值中最小值的方法
def min(a, b):
    return a if a < b else b


# 动态规划表
dp = []

# 动态表初始化
# dp[i][j]就是str1[0..i-1]变成str2[0...j-1]的最小代价
for i in range(0, m+1, 1):
    ary = []
    for j in range(0, n+1, 1):
        ary.append(0)
    dp.append(ary)

for i in range(1, m+1, 1):
    # j的位置为0，说明str2为空，也就是说str1都是进行的删除操作
    dp[i][0] = dc * i

for j in range(1, n+1, 1):
    # i的位置为0，说明str1为空，也就是说str1变为str2进行的都是插入字符操作
    dp[0][j] = ic * i



for i in range(0, m, 1):
    for j in range(0, n, 1):
        # 我们在此处要获得dp[i+1][j+1]
        x = min(dp[i+1][j] + dc, dp[i][j+1] + ic)
        if str1[i] == str2[j]:
            x = min(x, dp[i][j])
        else:
            x = min(x, dp[i][j] + rc)
        dp[i+1][j+1] = x

print dp[m][n]
