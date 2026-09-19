"""Campus IF Love —— I_love_ 拼接模拟。

题目来源: west2-online learn-AI / tasks(2026) / foundation / task0 / 作业 4 (OI) 第 5 题

规则:
    编号 u 的学长喜欢上编号 v 的学长后, u 立刻把名字更新为
        name[u] = "I_love_" + name[v]     # v 此刻的名字, 可能已被改过

    按输入顺序执行 m 条记录, 最后输出 1 号学长的名字。

解法:
    按顺序直接模拟。name[v] 存的就是它当前的值, 所以链式更新
    (v 之前被别人改过) 天然正确, 不需要建图或递归。
"""

import sys


def solve(data):
    """data 是已按空白切分好的输入 token 列表, 返回 1 号学长最后的名字。"""
    it = iter(data)

    n = int(next(it))

    # 学长编号从 1 开始, 多开一格让下标直接等于学号
    name = [""] * (n + 1)
    for i in range(1, n + 1):
        name[i] = next(it)

    m = int(next(it))
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        name[u] = "I_love_" + name[v]

    return name[1]


def main():
    print(solve(sys.stdin.read().split()))


if __name__ == "__main__":
    main()
