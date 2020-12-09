from materials.state import State  # 状態


def main():
    """
    ゲームのサンプル
    """
    game = State()  # インスタンス作成
    while True:
        game.title()  # タイトル画面
        game.mode()  # ゲーム選択画面
        game.choose()  # モード選択
        game.play()  # ゲームプレイ画面
        game.result()  # リザルト画面


if __name__ == "__main__":
    main()
