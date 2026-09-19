# Campus IF Love —— I_love_ 拼接

> 来源：west2-online `learn-AI` → `tasks(2026)/foundation/task0.md` → **作业 4 (OI)** 第 5 题，
> 参考实现文件名 `Campus_IF_Love.py`。

## 题目

ACM 集训队共有 $n$ 位学长，编号 $1 \sim n$，每人初始有一个名字。

若编号 $u$ 的学长喜欢上编号 $v$ 的学长，$u$ 会**立刻**把名字更新为
`I_love_` 拼上学长 $v$ **当前的名字**。

给定 $m$ 次「移情别恋」记录，输出 1 号学长最后的名字。

### 输入

- 第 1 行：$n$
- 接下来 $n$ 行：每行一个由大小写英文字母和下划线组成的字符串，长度 $< 25$，依次为 $1 \sim n$ 号的名字
- 第 $n+2$ 行：$m$
- 接下来 $m$ 行：每行两个正整数 $u\ v$（$1 \le u, v \le n$）

### 输出

一行，1 号学长最后的名字。

## 样例

| # | 输入 | 输出 |
|---|---|---|
| 1 | `sample1.in` | `sample1.out` |
| 2 | `sample2.in` | `sample2.out` |

## 思路

按输入顺序**直接模拟**。核心只有一行：

```python
name[u] = "I_love_" + name[v]
```

两个要点：

1. **「当前的名字」= 直接读 `name[v]`。** 数组里存的就是 $v$ 此刻的值，
   所以 $v$ 之前被别人改过多少次都会自然带上，不需要预处理、建图或递归。
2. **改名是覆盖，不是追加。** `name[u]` 始终只保留最新的一次赋值，
   旧的直接被丢弃——这正是样例里 `natalia` 最终消失的原因。

复杂度 $O(m \cdot L)$，$L$ 为名字长度（每步最多加 7 个字符）。

## 易错点

- 误以为要「记录所有人的历史名字」或建依赖图 —— 不需要，顺序已在输入里给死。
- 下标从 1 开始，数组开 `n + 1` 格，直接用学号当下标可避免 `-1` 换算错误。

## 运行

```bash
python solution.py < sample1.in     # Windows PowerShell: Get-Content sample1.in | python solution.py
python verify.py                    # 跑两组样例
```
