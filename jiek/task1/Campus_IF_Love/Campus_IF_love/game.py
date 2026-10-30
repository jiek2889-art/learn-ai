import sys
from story import BLOCKS, DIALOGUES, GIFT_EFFECTS, Character
from manage import SaveManager


#     reference from chatgpy
#     根据chatgpt,进行了修改
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
        self.current_block = "prologue"
        self.current_line = 0

    def save_game(self, show_message: bool = True) -> None:
        """保存当前剧情进度和所有角色的好感度。"""
        data = {
            "scene_index": self.scene_index,
            "current_block": self.current_block,
            "current_line": self.current_line,
            "current_target": self.current_target.name,
            "affinity": {name: character.affinity for name, character in self.characters.items() if name != "None"},
        }
        self.save_manager.save(data)
        if show_message:
            print("游戏已保存。")

    def load_game(self) -> bool:
        """读取存档"""
        data = self.save_manager.load()
        if data is None:
            print("没有找到存档。")
            return False

        self.scene_index = int(data.get("scene_index", 1))

        saved_block = data.get("current_block")
        if saved_block in BLOCKS:
            self.current_block = saved_block
            saved_line = int(data.get("current_line", 0))
            self.current_line = max(0, min(saved_line, len(BLOCKS[saved_block])))
        else:
            legacy_blocks = {
                1: ("prologue", 0),
                2: ("scene_xiaobai", 0),
                3: ("scene_jiejie", 0),
                4: ("scene_jiejie", len(BLOCKS["scene_jiejie"])),
            }
            self.current_block, self.current_line = legacy_blocks.get(
                self.scene_index,
                ("prologue", 0),
            )

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

    def play_block(self, block_name: str) -> str | None:
        """执行一个 BLOCKS 剧情块，并返回选择后的下一个剧情块。"""
        if block_name not in BLOCKS:
            raise ValueError(f"不存在的剧情块：{block_name}")

        if self.current_block != block_name:
            self.current_block = block_name
            self.current_line = 0

        block = BLOCKS[block_name]

        while self.current_line < len(block):
            item = block[self.current_line]
            item_type = item.get("type")

            if item_type == "narration":
                print(item["text"])

            elif item_type == "dialogue":
                character = item.get("character")
                if character:
                    print(f"{character}：『{item['text']}』")
                else:
                    print(item["text"])

            elif item_type == "choice":
                options = item.get("options", [])
                for number, option in enumerate(options, start=1):
                    print(f"{number}. {option['text']}")

                while True:
                    choice = input("请选择：").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(options):
                        selected = options[int(choice) - 1]
                        break
                    print("无效输入，请重新选择。")

                next_block = selected.get("next_block")
                self.current_line += 1
                if next_block is not None:
                    self.current_block = next_block
                    self.current_line = 0
                    self.save_game(show_message=False)
                    return next_block

                self.save_game(show_message=False)
                continue

            elif item_type == "set_target":
                character_name = item.get("character")
                if character_name in self.characters:
                    self.current_target = self.characters[character_name]

            self.current_line += 1
            self.save_game(show_message=False)

        return None

    def run_scene_blocks(self, start_block: str, block_names: set[str]) -> None:
        """从当前存档位置继续执行指定场景相关的剧情块。"""
        if self.current_block in block_names:
            block_name = self.current_block
        else:
            block_name = start_block

        while block_name is not None:
            block_name = self.play_block(block_name)

    def start(self) -> None:
        print("========== 游戏开始：校园 if·恋 ==========")

        save_data = self.save_manager.load()
        if save_data is not None:
            choice = input("检测到存档，是否读取？1. 是  2. 否：")
            if choice == "1":
                self.load_game()
                if self.current_target != self.characters["None"]:
                    self.story_loop()
                    return

        if self.current_block == "prologue":
            self.play_block("prologue")

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
        self.run_scene_blocks(
            "scene_senpai",
            {"scene_senpai", "senpai_accept", "senpai_decline"},
        )

        if self.current_target != self.characters["None"]:
            self.story_loop()
            return True
        return False

    def scene_xiaobai(self) -> bool:
        print("\n【场景二：小白】")
        self.run_scene_blocks(
            "scene_xiaobai",
            {"scene_xiaobai", "xiaobai_accept", "xiaobai_decline"},
        )

        if self.current_target != self.characters["None"]:
            self.story_loop()
            return True
        return False

    def scene_jiejie(self) -> bool:
        print("\n【场景三：姐姐】")
        self.run_scene_blocks(
            "scene_jiejie",
            {"scene_jiejie", "jiejie_accept", "jiejie_decline"},
        )

        if self.current_target != self.characters["None"]:
            self.story_loop()
            return True
        return False

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
