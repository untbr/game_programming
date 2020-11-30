import sys
import pygame
from pygame.locals import *  # 定数読み込み
from materials import colors  # 色に関するモジュール
from materials import align  # オブジェクトの配置に関するモジュール


def main():
    """
    ゲーム起動画面のサンプル
    画面中央にタイトルを表示、その下にメニューが来る
    """
    pygame.init()  # モジュール初期化
    WIDTH = 800  # ウィンドウ横幅
    HEIGHT = 600  # ウィンドウ縦幅
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ウィンドウ生成(width, height)
    pygame.display.set_caption('Sample | Top')  # キャプション設定
    font = pygame.font.Font(None, 60)  # フォント設定(フォント種類, サイズ(px))
    # 色設定(r, g, b)
    while(True):
        screen.fill(colors.Color.AQUA.color())  # ウィンドウを塗りつぶす
        # 描画する文字を設定(文字列, アンチエイリアスの有無, 色)
        text_title = font.render('Game Title', True, colors.comp_color(colors.Color.AQUA.color()))
        # 文字の表示位置を設定
        aling = align.Align(text_title, WIDTH, HEIGHT)  # タイトルの表示位置を操作する準備
        screen.blit(text_title, [aling.align_center(), aling.align_middle()])  # 表示
        pygame.display.update()  # ウィンドウ更新(変更結果を表示)
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタン押下
                pygame.quit()  # Pygame終了(ウィンドウを閉じる)
                sys.exit(0)  # 処理終了


if __name__ == '__main__':
    main()