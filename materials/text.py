import pygame


class Text:
    def __init__(self):
        self.text = []  # 入力されたテキストを格納していく変数
        self.editing = []  # 全角の文字編集中(変換前)の文字を格納するための変数
        pygame.key.start_text_input()
        self.is_editing = False

    def __str__(self):
        return "".join(self.text)

    def edit(self, text):
        """
        edit(編集中)であるときに呼ばれるメソッド
        全角かつ漢字変換前の確定していないときに呼ばれる
        """
        if text:
            self.is_editing = True  # テキストがあるときはTrue
            for x in text:
                self.editing.append(x)  # 編集中の文字列を文字として格納していく
            disp = "[" + "".join(self.editing) + "]"
        else:
            self.is_editing = False  # テキストが空の時はFalse
            disp = ""
        self.editing = []  # 次のeditで使うために空にする
        return format(self) + disp

    def input(self, text):
        """
        半角文字が打たれたとき、もしくは全角で変換が確定したときに呼ばれるメソッド
        """
        self.editing = []
        for x in text:
            self.text.append(x)
        self.is_editing = False
        return format(self)

    def delete(self):
        """
        確定している文字(半角なら文字入力後、全角なら変換確定後)を削除するためのメソッド
        """
        print("a")
        if self.text:
            self.text.pop()
        return format(self)

    def enter(self):
        entered = format(self)
        self.text = []  # 次回の入力で使うためにself.textを空にする
        return entered
