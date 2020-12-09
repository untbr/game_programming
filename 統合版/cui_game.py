from game.game import Report, Shiritori
from game.user import User


def main():
    game = None  # ReportもしくはShiritoriのインスタンスを格納する変数
    input_type = input("report: 1\nshiritori: 2\n")
    if input_type == "1":
        game = Report()
    elif input_type == "2":
        game = Shiritori()
    else:
        return
    game_mode = game.get_mode()  # 難易度(品詞)を取得
    for i in game_mode:
        print("{}:{}".format(i.value, i.id))
    idx = input("モードを入力してください: ")
    game.set_mode(game_mode[int(idx)])  # 難易度(品詞)の設定
    while not game.is_finish():
        word = game.get_word()  # 出題をしてもらう
        print("{}\n{}".format(word.word, word.describe))
        answer = input("answer: ")
        judge = game.judge_word(answer)  # 正誤判定
        if not judge.correct:  # 不正解時
            print(judge.message)
    user.add_score(game.score)  # ユーザーの情報にスコアを追加
    print("終了")
    print(user)
    share = input("ツイッターで結果をシェアしますか？ y/n: ")
    if share == "y":
        user.share()


if __name__ == "__main__":
    # ゲーム起動中Userインスタンスは同じものを使う
    # クリア次第、UserのscoresにScoreインスタンスを追加していく
    user = User("test_user")
    main()
