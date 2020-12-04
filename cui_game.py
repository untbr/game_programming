from game.game import Report, Shiritori


def main():
    game_instance = None
    input_type = input("report: 1\nshiritori: 2\n")
    if input_type == "1":
        game_instance = Report()
    elif input_type == "2":
        game_instance = Shiritori()
    else:
        return
    game_mode = game_instance.get_mode()
    for i in game_mode:
        print("{}:{}".format(i.value, i.id))
    idx = input("モードを入力してください: ")
    game_instance.set_mode(game_mode[int(idx)])
    while not game_instance.is_finish():
        word = game_instance.get_word()
        print("{}\n{}".format(word.word, word.describe))
        answer = input("answer: ")
        judge = game_instance.judge_word(answer)
        if not judge.correct:
            print(judge.message)
    print("終了")


if __name__ == "__main__":
    main()
