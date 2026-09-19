x = int(input("请输入一个整数: "))
y = int(input("请输入一个整数: "))
num = []
for i in range(x, y + 1):
    if i % 400 == 0 or (i % 4 == 0 and i % 100 != 0):
        num.append(i)
print(len(num))
print(*num)
