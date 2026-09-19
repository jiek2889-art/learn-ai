heights = []
height = 0
num = 0
for i in range(10):
    height = int(input(f"请输入第{i + 1}个苹果的高度："))
    heights.append(height)
height_tao = int(input("请输入陶陶的身高："))
for i in heights:
    if i <= height_tao + 30:
        num += 1
print(num)
