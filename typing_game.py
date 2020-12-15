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
    # gameモジュールでAGameを継承しているクラスのリスト
    game_types = ["Report", "Shiritori"]
    game_instance = None  # ゲームのインスタンスを格納する変数
    while True:
        state.event()  # キーダウンに応じて状態遷移
        if not state.is_running:  # 再描画(描画の更新)をする必要があるなら
            if state.state.name == States.TITLE:
                draw.title(state.selector.position)  # タイトル画面の描画
            elif state.state.name == States.USER:
                user_name = draw.register()  # ユーザー名入力画面の描写
                user.name = user_name  # ユーザーインスタンスのnameに名前をセットする
                state.has_user_name = True  # ユーザー名の登録が完了したことを知らせる
            elif state.state.name == States.TYPE:
                draw.choose_type(state.selector.position)  # ゲームタイプの描画
                cls = getattr(game, game_types[state.selector.position])  # 選択された方のクラス
                game_instance = cls()  # そのクラスのインスタンス化
            elif state.state.name == States.MODE:
                game_modes = game_instance.get_mode()  # そのゲームのモード(難易度)取得
                draw.choose_mode(game_modes, state.selector.position)  # ゲームモードの描画
                # ゲームモードのセット
                game_instance.set_mode(game_modes[state.selector.position])
            elif state.state.name == States.PLAY:
                draw.play(game_instance)  # プレイ画面の描画
                user.add_score(game_instance.score)  # ユーザーにスコアを追加する
            elif state.state.name == States.RESULT:
                draw.result(user)  # リザルト画面の描画
            state.is_running = True  # 描画済みであることをstateに知らせる


if __name__ == "__main__":
    main()
