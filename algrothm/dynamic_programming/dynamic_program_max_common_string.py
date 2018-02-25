#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 案例四
'''
给定两个字符串str1和str2，返回两个字符串的最长公共子序列，
例如：str1="1A2C3D4B56",str2="B1D23CA45B6A",
"123456"和"12C4B6"都是最长公共子序列，返回哪一个都行。

分析：本题是非常经典的动态规划问题，
假设str1的长度为M，str2的长度为N，则生成M*N的二维数组dp，
dp[i][j]的含义是str1[0..i]与str2[0..j]的最长公共子序列的长度。

dp值的求法如下：
dp[i][j]的值必然和dp[i-1][j],dp[i][j-1],dp[i-1][j-1]相关，
结合下面的代码来看，我们实际上是从第1行和第1列开始计算的，而把第0行和第0列都初始化为0，
这是为了后面的取最大值在代码实现上的方便，dp[i][j]取三者之间的最大值。
'''


str1 = "1A2C3D4B56"
str2 = "B1D23CA45B6A"



# 计算动态表
def find_max_common_str(str1, str2):
    m = len(str1)
    n = len(str2)

    # 动态表
    dp = []
    # 初始化动态表
    # dp[i][j]的含义是str1[0..i]与str2[0..j]的最长公共子序列的长度，
    # str1[0...i]是含头不含尾的，所以整个字符串应该是str1[0,n+1]
    # 也就是dp应该是(m+1)*(n+1)
    for i in range(0, m+1, 1):
        ary = []
        for j in range(0, n+1, 1):
            ary.append(0)
        dp.append(ary)

    # print dp

    # 计算动态表
    for i in range(0, m, 1):
        for j in range(0, n, 1):
            if str1[i] == str2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                tmp_max = dp[i][j+1]
                if tmp_max < dp[i+1][j]:
                    tmp_max = dp[i+1][j]
                # dp[i+1][j+1] = max(dp[i+1][j],dp[i][j+1])
                dp[i+1][j+1] = tmp_max

    return dp[m][n]

print find_max_common_str(str1, str2)

