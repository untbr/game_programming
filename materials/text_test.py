import sys
import pygame
from pygame.locals import *
from text import Text


class Draw:
    """テキストを表示するためのクラス(= TextクラスとUI処理を分離するための別のクラス)"""

    def __init__(self, win_size):
        self.font = pygame.font.SysFont("yumincho", 25)
        self.screen = pygame.display.set_mode(win_size)
        self.is_editing = False

    def draw(self, text):
        """
        入力文字を表示するためのメソッド
        """
        self.screen.fill((0, 0, 0))  # 黒画面
        text_ = self.font.render(text, True, (255, 255, 255))  # 白フォント
        self.screen.blit(text_, [320 - (text_.get_width() // 2), 240])


if __name__ == "__main__":
    win_size = (640, 480)  # ウィンドウサイズ
    pygame.init()
    text = Text()  # Textクラスのインスタンス化
    drawer = Draw(win_size)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not text.is_editing:  # 編集中(全角の変換前)でないとき
                    if event.key == K_BACKSPACE:  # BS時
                        drawer.draw(text.delete())  # 確定した方から削除する
                    if event.key == K_LEFT:
                        drawer.draw(text.move_cursor_left())  # 文字のカーソルを左に動かす
                    if event.key == K_RIGHT:
                        drawer.draw(text.move_cursor_right())  # 文字のカーソルを右に動かす
                if len(event.unicode) == 0:  # 確定時
                    if event.key == K_RETURN:
                        print(text.enter())  # 確定した文字の取得
                        drawer.draw("|")  # テキストボックスを空にする
            elif event.type == TEXTEDITING:  # 全角入力するときに必ず真
                drawer.draw(text.edit(event.text))
            elif event.type == TEXTINPUT:  # 半角入力するときに必ず使う(もしくは全角時enter)
                drawer.draw(text.input(event.text))
        pygame.display.update()
