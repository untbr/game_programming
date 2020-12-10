from materials.state import State, Draw, States  # 状態


def main():
    """
    ゲームのサンプル
    """
    draw = Draw()
    state = State()  # インスタンス作成
    while True:
        state.transition()
        if not state.is_running:
            if state.state == States.TITLE:
                draw.title()  # タイトル画面の描画
            if state.state == States.TYPE:
                draw.choose_type()  # ゲームタイプの描画
            elif state.state == States.MODE:
                draw.game = state.game_instance
                draw.game_mode = state.game_modes
                draw.choose_mode()  # ゲームモードの描画
            elif state.state == States.PLAY:
                draw.game.set_mode(state.mode)
                draw.play()  # プレイ画面の描画
                state.is_finish = True
            elif state.state == States.RESULT:
                draw.result()


if __name__ == "__main__":
    main()
