from game.game import Report, Shiritori


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
    print("終了")
    print("制限時間に正解すべき問題:", game.score.game_info.mode.number_of_words)
    print("正解数:", game.score.number_of_corrects)
    print("不正解数:", game.score.number_of_incorrects)


if __name__ == "__main__":
    main()
