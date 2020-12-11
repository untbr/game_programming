import asyncio

import pygame
from materials.state import State, StateDraw, States  # 状態

from game.user import User


def main():
    """
    ゲームのサンプル
    """
    draw = StateDraw()
    state = State()  # インスタンス作成
    user = User()
    user.name = "test"

    loop = asyncio.get_event_loop()
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
                pygame.key.start_text_input()
                while not state.game_instance.is_finish():
                    # 出題を取得する
                    question = loop.run_until_complete(state.game_instance.get_word())
                    input_text = draw.play(question)  # プレイ画面の描画
                    # 入力の判定をする
                    judge = loop.run_until_complete(
                        state.game_instance.judge_word(input_text)
                    )
                    if not judge.correct:  # 間違っていたら
                        draw.correct_answer(judge)  # 答えを表示する
                user.add_score(state.game_instance.score)  # ユーザーにスコアを追加する
                pygame.key.stop_text_input()
            elif state.state == States.RESULT:
                draw.result(user)


if __name__ == "__main__":
    main()
