from materials.state import State, StateDraw, States  # 状態


def main():
    """
    ゲームのサンプル
    """
    draw = StateDraw()
    state = State()  # インスタンス作成
    while True:
        state.transition()  # キーダウンに応じて状態遷
        if not state.is_running:
            if state.state == States.TITLE:
                draw.title()  # タイトル画面の描画
            elif state.state == States.TYPE:
                draw.choose_type()  # ゲームタイプの描画
            elif state.state == States.MODE:
                draw.choose_mode(state.game_modes)  # ゲームモードの描画
            elif state.state == States.PLAY:
                draw.play(state.game_instance)  # プレイ画面の描画
                state.is_finish = True
            elif state.state == States.RESULT:
                draw.result()


if __name__ == "__main__":
    main()
