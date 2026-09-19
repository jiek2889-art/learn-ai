"""把样例逐步骤打出来, 用于理解「当前的名字」是怎么传递的。

    python trace.py
"""

NAMES = [None, "anonymous", "natalia", "LeBron", "Tanya_Romanova", "MikeMirzayanov"]
OPS = [(1, 2), (3, 4), (2, 1), (4, 3), (1, 4), (3, 2)]


def main():
    name = NAMES[:]
    print(f"start      : #1={name[1]}  #2={name[2]}  #3={name[3]}  #4={name[4]}")
    for step, (u, v) in enumerate(OPS, 1):
        name[u] = "I_love_" + name[v]
        print(f"step{step}: #{u} loves #{v}  ->  #{u} = I_love_ + name[{v}] = {name[u]}")
    print(f"answer     : {name[1]}")


if __name__ == "__main__":
    main()
