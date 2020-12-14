from game import game
from game.user import User

from materials.drawer import StateDraw
from materials.state import State, States


def main():
    """
    ゲームのサンプル
    """
    draw = StateDraw()  # 描画を担当するクラス
    state = State()  # 状態を管理するクラス
    user = User()  # ユーザー情報を管理するクラス
    game_types = ["Report", "Shiritori"]
    game_instance = None
    # 小見出しを使った選択画面で使う変数
    while True:
        state.event()  # キーダウンに応じて状態遷
        if not state.is_running:
            if state.state.name == States.TITLE:
                draw.title(state.selector.position)  # タイトル画面の描画
            elif state.state.name == States.USER:
                user_name = draw.register()
                user.name = user_name  # ユーザーインスタンスのnameに名前をセットする
                state.exist_user = True
            elif state.state.name == States.TYPE:
                draw.choose_type(state.selector.position)  # ゲームタイプの描画
                cls = getattr(game, game_types[state.selector.position])  # 選択された方のクラス
                game_instance = cls()
            elif state.state.name == States.MODE:
                game_modes = game_instance.get_mode()
                draw.choose_mode(game_modes, state.selector.position)  # ゲームモードの描画
                mode = game_modes[state.selector.position]
                game_instance.set_mode(mode)
            elif state.state.name == States.PLAY:
                draw.play(game_instance)  # プレイ画面の描画
                user.add_score(game_instance.score)  # ユーザーにスコアを追加する
            elif state.state.name == States.RESULT:
                draw.result(user)
            state.is_running = True  # 描画済みであることをstateに知らせる


if __name__ == "__main__":
    main()
