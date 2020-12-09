import pygame


class Text:
    def __init__(self):
        self.text = ["|"]  # 入力されたテキストを格納していく変数
        self.editing = []  # 全角の文字編集中(変換前)の文字を格納するための変数
        pygame.key.start_text_input()
        self.is_editing = False  # 編集中文字列の有無(全角入力時に使用)
        self.cursor_pos = 0  # 文字入力のカーソル(パイプ|)の位置

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
        # カーソルの位置で区切って文字を結合する
        return (
            format(self)[0 : self.cursor_pos] + disp + format(self)[self.cursor_pos :]
        )

    def input(self, text):
        """
        半角文字が打たれたとき、もしくは全角で変換が確定したときに呼ばれるメソッド
        """
        self.editing = []
        for x in text:
            self.text.insert(self.cursor_pos, x)
            self.cursor_pos += 1
        self.is_editing = False
        return format(self)

    def delete(self):
        """
        確定している文字(半角なら文字入力後、全角なら変換確定後)を削除するためのメソッド
        """
        if len(self.text) > 1:
            self.text.pop(self.cursor_pos - 1)
            self.cursor_pos -= 1
        return format(self)

    def enter(self):
        """入力文字が確定したときに呼ばれるメソッド"""
        # カーソルを読み飛ばす
        entered = (
            format(self)[0 : self.cursor_pos] + format(self)[self.cursor_pos + 1 :]
        )
        self.text = ["|"]  # 次回の入力で使うためにself.textを空にする
        self.cursor_pos = 0
        return entered

    def move_cursor_left(self):
        """inputされた文字のカーソル(パイプ|)の位置を左に動かすメソッド"""
        if self.cursor_pos > 0:
            # カーソル位置をカーソル位置の前の文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos - 1] = (
                self.text[self.cursor_pos - 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos -= 1  # カーソルが1つ前に行ったのでデクリメント
        return format(self)

    def move_cursor_right(self):
        """inputされた文字のカーソル(パイプ|)の位置を右に動かすメソッド"""
        if len(self.text) - 1 > self.cursor_pos:
            # カーソル位置をカーソル位置の後ろの文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos + 1] = (
                self.text[self.cursor_pos + 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos += 1  # カーソルが1つ後ろに行ったのでインクリメント
        return format(self)


class Draw:
    """テキストを表示するためのクラス(= TextクラスとUI処理を分離するための別のクラス)"""

    def __init__(self, win_size, screen):
        self.font = pygame.font.SysFont("yumincho", 30)
        self.screen = screen
        self.is_editing = False

    def draw(self, text):
        """
        入力文字を表示するためのメソッド
        """
        text_ = self.font.render(text, True, (255, 255, 255))  # 白フォント
        self.screen.fill(
            (0, 0, 0),
            (0, (600 - text_.get_height() * 2), float(800), float(text_.get_height())),
        )  # 黒画面
        self.screen.blit(
            text_,
            [((800 / 2) - (text_.get_width() / 2)), (600 - text_.get_height() * 2)],
        )
