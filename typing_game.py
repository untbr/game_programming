from game.game import Report, Shiritori
from game.user import User
from materials.drawer import StateDraw
from materials.state import State, States


def main():
    # 描画を担当するクラス(ここでpygameの初期化を行う)
    draw = StateDraw()
    state = State()  # 状態を管理するクラス
    user = User()  # ユーザー情報(スコアや名前)を管理するクラス
    # gameモジュールでAGameを継承しているクラスのリスト
    game_types = [Report, Shiritori]
    game = None  # ゲームのインスタンスを格納する変数
    while True:
        state.event()  # キーダウンに応じて状態遷移
        if not state.is_running:  # 再描画(描画の更新)をする必要があるなら
            if state.state.name == States.TITLE:
                draw.title(state.selector.position)  # タイトル画面の描画
            elif state.state.name == States.USER:
                if len(user.name) > 0:  # 既にユーザー名が登録されているなら
                    state.transition()  # ゲームモード選択画面に遷移
                    continue
                user_name = draw.register()  # ユーザー名入力画面の描写
                user.name = user_name  # ユーザーインスタンスのnameに名前をセットする
            elif state.state.name == States.TYPE:
                draw.choose_type(state.selector.position)  # ゲームタイプの描画
                game = game_types[state.selector.position]()  # 選択された方をインスタンス化
            elif state.state.name == States.MODE:
                game_modes = game.get_mode()  # そのゲームのモード(難易度)取得
                game_modes_list = [str(i.value) for i in game_modes]
                draw.choose_mode(game_modes_list, state.selector.position)  # ゲームモードの描画
                # ゲームモードのセット
                game.set_mode(game_modes[state.selector.position])
            elif state.state.name == States.PLAY:
                while not game.is_finish:
                    # プレイ画面の描画
                    play = draw.play(format(game), game.progress)
                    next(play)
                    # draw.play、左辺値questionに出題ワードを渡す
                    input_text = play.send(game.get_word())
                    try:
                        # draw.play、左辺値judgeに判定結果を渡す
                        play.send(game.judge_word(input_text))
                    except StopIteration:
                        pass
                user.add_score(game.score)  # ユーザーにスコアを追加する
                state.transition()  # ゲームプレイが終わると自動で結果画面に遷移させる
                continue
            elif state.state.name == States.RESULT:
                draw.result(format(user).split("\n"))  # リザルト画面の描画
            state.is_running = True  # 描画済みであることをstateに知らせる


if __name__ == "__main__":
    main()
