import sys
from story import DIALOGUES, GIFT_EFFECTS, Character
from manage import SaveManager


class Game:
    def __init__(self) -> None:
        self.characters = {
            "学姐": Character("学姐", "社团里的艺术少女"),
            "小白": Character("小白", "课堂上的元气同学"),
            "姐姐": Character("姐姐", "食堂里的温柔姐姐"),
            "None": Character("None", "无"),
        }
        self.current_target = self.characters["None"]
        self.save_manager = SaveManager("save_data.json")
        self.scene_index = 1

    def save_game(self) -> None:
        """保存当前剧情进度和所有角色的好感度。"""
        data = {
            "scene_index": self.scene_index,
            "current_target": self.current_target.name,
            "affinity": {name: character.affinity for name, character in self.characters.items() if name != "None"},
        }
        self.save_manager.save(data)
        print("游戏已保存。")

    def load_game(self) -> bool:
        """读取存档；读取成功返回 True。"""
        data = self.save_manager.load()
        if data is None:
            print("没有找到存档。")
            return False

        self.scene_index = int(data.get("scene_index", 1))

        for name, affinity in data.get("affinity", {}).items():
            if name in self.characters:
                self.characters[name].affinity = int(affinity)

        target_name = data.get("current_target", "None")
        if target_name in self.characters:
            self.current_target = self.characters[target_name]
        else:
            self.current_target = self.characters["None"]

        print("存档读取成功。")
        return True

    def start(self) -> None:
        print("========== 游戏开始：校园 if·恋 ==========")
        print("你是一名刚刚踏入大学校园的新生。")
        print("在开学典礼上，拿下压倒性成绩第一的你被选为新生代表发言。")
        print("在全场上千人的注视下，你气质非凡，发言流畅，很快成为焦点人物。")
        print("消息迅速传开，关于‘神秘新生代表’的讨论充斥着整个校园。")
        print("于是，在这个新的舞台上，你与三位不同的女生产生了交集……")

        save_data = self.save_manager.load()
        if save_data is not None:
            choice = input("检测到存档，是否读取？1. 是  2. 否：")
            if choice == "1":
                self.load_game()
                if self.current_target != self.characters["None"]:
                    self.story_loop()
                    return

        if self.scene_index <= 1:
            if self.scene_senpai():
                return
            self.scene_index = 2
            self.save_game()

        if self.scene_index <= 2:
            if self.scene_xiaobai():
                return
            self.scene_index = 3
            self.save_game()

        if self.scene_index <= 3:
            if self.scene_jiejie():
                return
            self.scene_index = 4
            self.save_game()
            print("\n啥，眼前三妹子都不要？？死现充别玩 galgame")

    def scene_senpai(self) -> bool:
        print("\n【场景一：社团学姐】")
        print("你路过社团活动室，学姐正拿着画板注意到你。")
        print("学姐：『这位新生？要不要来试试？』")

        choice = input("1. 主动表现兴趣，拿起一只笔作画\n2. 表示抱歉，没兴趣，转身离开\n请选择：")
        if choice == "1":
            print("\n你随手挑起一只笔，在纸上几笔勾勒出惊艳的图案，引得周围阵阵惊呼。")
            print("学姐目光一震，眼神变得格外认真。你进入【学姐线】！")
            self.current_target = self.characters["学姐"]
            self.save_game()
            self.story_loop()
            return True
        else:
            print("在纵目睽睽下，你扬长而去。")
            return False

    def scene_xiaobai(self) -> bool:
        print("\n【场景二：小白】")
        print("你走进图书馆，发现小白正在奋笔疾书，却被一道算法题难住了。")
        print("小白：『呜呜……这题到底该怎么写呀？』")

        choice = input("1. 主动帮她解题\n2. 敷衍几句，转身离开\n请选择：")
        if choice == "1":
            print("\n你耐心地为小白讲解算法思路，她的眼睛闪烁着光芒。")
            print("小白感激地看着你，决定与你一起学习。你进入【小白线】！")
            self.current_target = self.characters["小白"]
            self.save_game()
            self.story_loop()
            return True
        else:
            print("小白失望地看着你离开，继续埋头苦读。")
            return False

        # TODO 两种选择 如果选择了 1 则进入该位角色的故事线 并返回 True 如果选择了 2 则进入下一位角色的选择 并且返回 False
        # 注意 除了判断外 你可以同时输出角色的反应
        # 比如在上一位角色的判断中 选择了 1 时 输出了 print("\n你随手挑起一只笔，在纸上几笔勾勒出惊艳的图案，引得周围阵阵惊呼。")
        # 写法可以借鉴学姐线

    def scene_jiejie(self) -> bool:
        print("\n【场景三：姐姐】")
        print("你偶然在校外的咖啡店敲代码，一位看起来成熟知性的姐姐似乎对你感兴趣，缓缓朝你走了过来...")
        print("姐姐：『你的代码思路很有趣呢，能给我讲讲你的实现方法吗？』")

        choice = input("1. 缓缓低眉，毫不在意的开始解释\n2. 头也不抬，保持敲代码的状态\n请选择：")
        if choice == "1":
            print("\n你耐心地为姐姐讲解代码实现，她的内心受到触动。")
            print("姐姐微笑着点头，决定与你一起探讨更多编程问题。你进入【姐姐线】！")
            self.current_target = self.characters["姐姐"]
            self.save_game()
            self.story_loop()
            return True
        else:
            print("姐姐嫌弃地看着你，轻轻叹了口气离开。")
            return False
        # TODO 两种选择 如果选择了 1 则进入该位角色的故事线 并返回 True 如果选择了 2 则进入下一位角色的选择 并且返回 False
        # 要求同上

    def story_loop(self) -> None:
        """角色线主循环"""
        while True:
            print("\n你要做什么？")
            print("1. 和她聊天")
            print("2. 送她礼物")
            print("3. 查看好感度")
            print("4. 离开（退出游戏）")
            print("5. 保存游戏")
            print("6. 读取游戏")

            choice = input("请输入选项：")
            if choice == "1":
                self.current_target.talk()
                self.save_game()
            elif choice == "2":
                gift = input("请输入你要送的礼物（鲜花、编程笔记、奶茶、奇怪的石头、精致的钢笔、可爱玩偶、夜宵外卖）：")
                self.current_target.give_gift(gift)
                self.save_game()
            elif choice == "3":
                print(f"{self.current_target.name} 的当前好感度：{self.current_target.affinity}")  # 类的调用 直接调用属性
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                self.load_game()
            elif choice == "4":
                print("你选择离开，游戏结束。")
                sys.exit(0)

            else:
                print("无效输入，请重新选择。")

            if self.current_target == self.characters["None"] or self.current_target.check_ending():
                break


if __name__ == "__main__":
    game = Game()
    game.start()
