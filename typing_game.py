from game import game
from game.user import User

from materials.drawer import StateDraw, FocusSelector
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
    selector_max_length = {
        States.TITLE: 2,
        States.USER: 0,
        States.TYPE: 2,
        States.MODE: 3,
        States.PLAY: 0,
        States.RESULT: 0,
    }
    while True:
        state.transition()  # キーダウンに応じて状態遷
        if not state.is_running:
            if not state.selector:
                state.selector = FocusSelector(selector_max_length[state.state])
            if state.state == States.TITLE:
                draw.title(state.selector.position)  # タイトル画面の描画
            elif state.state == States.USER:
                user_name = draw.register()
                user.name = user_name  # ユーザーインスタンスのnameに名前をセットする
            elif state.state == States.TYPE:
                draw.choose_type(state.selector.position)  # ゲームタイプの描画
            elif state.state == States.MODE:
                cls = getattr(game, game_types[state.game_type_key])  # 選択された方のクラス
                game_instance = cls()  # インスタンス化
                game_modes = game_instance.get_mode()
                draw.choose_mode(game_modes, state.selector.position)  # ゲームモードの描画
            elif state.state == States.PLAY:
                mode = game_modes[state.game_mode_key]
                game_instance.set_mode(mode)
                draw.play(game_instance)  # プレイ画面の描画
                user.add_score(game_instance.score)  # ユーザーにスコアを追加する
            elif state.state == States.RESULT:
                draw.result(user)
            state.is_running = True # 描画済みであることをstateに知らせる

if __name__ == "__main__":
    main()
