import sys
from typing import Optional

from client.shiritori import Any, ShiritoriClient


class ShiritoriGame:
    def __init__(self) -> None:
        self.client = ShiritoriClient()

    def select_mode(self) -> Any:
        modes = self.client.get_modes()
        if modes is None:
            return None
        for k, v in dict(modes).items():
            print(k, v)
        mode = input("プレイするモードの番号を入力してください: ")
        set_mode = self.client.set_mode(mode)
        if set_mode:
            return modes[mode]
        print("番号が正しくありません")
        return self.select_mode()

    def start(self) -> None:
        mode_name = self.select_mode()
        get_next_head = self.client.get_head_word()
        if mode_name is None or get_next_head is None:
            print("通信に失敗しました")
            return None
        next_head = get_next_head["next_head"]
        while 1:
            input_word = input("「{}」で始まる{}を入力してください: ".format(next_head, mode_name)).strip()
            result = self.client.shiritori(input_word, next_head)
            if result is None:
                print("通信に失敗しました")
                return None
            if result["is_correct"] is False:
                print(result["message"])
            next_head = result["next_head"]
            if next_head == "ん":
                print("「ん」を使いました")
                break
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ShiritoriClient.host = sys.argv[1]
    game = ShiritoriGame()
    game.start()
