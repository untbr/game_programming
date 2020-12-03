import sys
import textwrap
import pygame
from pygame.locals import *  # 定数読み込み
from materials import colors  # 色に関するモジュール
from materials import align  # オブジェクトの配置に関するモジュール
from materials import events  # イベント処理に関するモジュール


def main():
    """
    ゲーム起動画面のサンプル
    画面中央にタイトルを表示、その下にメニューが来る
    """
    pygame.init()  # モジュール初期化
    WIDTH = 800  # ウィンドウ横幅
    HEIGHT = 600  # ウィンドウ縦幅
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ウィンドウ生成(width, height)
    pygame.display.set_caption('タイピングゲーム(仮) | Top')  # キャプション設定
    # フォント設定(フォント種類, サイズ(px))
    font_title = pygame.font.SysFont('yumincho', 60)  # タイトル
    font_text = pygame.font.SysFont('yumincho', 30)  # 本文
    # タイトル画面 --------------------------------------------------------------------------------
    is_running = True
    screen.fill(colors.Color.BLACK.color())  # ウィンドウを塗りつぶす
    # 描画する文字を設定(文字列, アンチエイリアスの有無, 色)
    text_h = font_title.render('タイピングゲーム(仮)', True, colors.Color.WHITE.color())
    text_p = font_text.render('Please press any key...', True, colors.Color.WHITE.color())
    # 文字の表示位置を設定
    aling = align.Align(text_h, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_h, [aling.align_center(), aling.align_middle() - text_h.get_height()*2])
    aling = align.Align(text_p, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_p, [aling.align_center(), aling.align_middle()])
    pygame.display.update()  # ウィンドウ更新(変更結果を表示)
    while(is_running):
        # イベント処理
        for event in pygame.event.get():
            events.quit_game(event.type)  # 閉じるボタン押下で終了
            if event.type == KEYDOWN:
                is_running = False
    is_running = True
    level = ''
    # 難易度選択 --------------------------------------------------------------------------------
    screen.fill(colors.Color.BLACK.color())  # ウィンドウを塗りつぶす
    text_h = font_title.render('難易度選択', True, colors.Color.WHITE.color())
    text_p1 = font_text.render('やさしい: f', True, colors.Color.WHITE.color())
    text_p2 = font_text.render('むずかしい: j', True, colors.Color.WHITE.color())
    aling = align.Align(text_h, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_h, [aling.align_center(), aling.align_middle() - text_h.get_height()*2])
    aling = align.Align(text_p1, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_p1, [aling.align_center(), aling.align_middle()])
    aling = align.Align(text_p2, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_p2, [aling.align_center(), aling.align_middle() + text_p2.get_height()])
    pygame.display.update()  # ウィンドウ更新(変更結果を表示)
    while(is_running):
        # イベント処理
        for event in pygame.event.get():
            events.quit_game(event.type)  # 閉じるボタン押下で終了
            if event.type == KEYDOWN:
                if events.input_catch(event.key) == 'f':
                    level = 'f'
                    is_running = False
                elif events.input_catch(event.key) == 'j':
                    level = 'j'
                    is_running = False
    # プレイ画面 --------------------------------------------------------------------------------
    is_running = True
    # ここの辺でデータセットからの読み込みが発生する(？)
    screen.fill(colors.Color.BLACK.color())  # ウィンドウを塗りつぶす
    text_h = font_text.render('時間内に入力せよ！', True, colors.Color.WHITE.color())
    text_time = font_text.render('00:00', True, colors.Color.WHITE.color())
    text_word = font_text.render('オブ○ェクト', True, colors.Color.WHITE.color())
    # text_desc = font_text.render('オブジェクトとは、物、物体、目標物、対象、目的語、客体、などの意味を持つ英単語。', True, colors.Color.WHITE.color())  # 18文字ごとで区切った配列を作成→forで出力
    aling = align.Align(text_h, WIDTH, HEIGHT)
    screen.blit(text_h, [aling.align_left() + 10, aling.align_top() + 10])
    aling = align.Align(text_time, WIDTH, HEIGHT)
    screen.blit(text_time, [aling.align_right() - 10, aling.align_top() + 10])
    aling = align.Align(text_word, WIDTH, HEIGHT)
    screen.blit(text_word, [aling.align_center(), aling.align_middle() - text_h.get_height()*3])
    text = 'オブジェクトとは、物、物体、目標物、対象、目的語、客体、などの意味を持つ英単語。'
    for i, desc in enumerate(textwrap.wrap(text, 18)):
        text_desc = font_text.render(desc, True, colors.Color.WHITE.color())
        aling = align.Align(text_desc, WIDTH, HEIGHT)
        screen.blit(text_desc, [aling.align_center(), aling.align_middle() + text_desc.get_height()*i - text_desc.get_height()])
    pygame.display.update()
    while(is_running):
        # イベント処理
        for event in pygame.event.get():
            events.quit_game(event.type)  # 閉じるボタン押下で終了
            if event.type == KEYDOWN:
                is_running = False
    # リザルト画面 --------------------------------------------------------------------------------
    is_running = True
    screen.fill(colors.Color.BLACK.color())  # ウィンドウを塗りつぶす
    text_h = font_title.render('リザルト', True, colors.Color.WHITE.color())
    aling = align.Align(text_h, WIDTH, HEIGHT)
    screen.blit(text_h, [aling.align_center(), aling.align_middle() - text_h.get_height()*2])
    text_p1 = font_text.render('正解：{0}'.format(0), True, colors.Color.WHITE.color())
    aling = align.Align(text_p1, WIDTH, HEIGHT)
    screen.blit(text_p1, [aling.align_center(), aling.align_middle()])
    text_p2 = font_text.render('不正解：{0}'.format(0), True, colors.Color.WHITE.color())
    aling = align.Align(text_p2, WIDTH, HEIGHT)
    screen.blit(text_p2, [aling.align_center(), aling.align_middle() + text_p2.get_height()])
    text_p3 = font_text.render('Please press any key...'.format(0), True, colors.Color.WHITE.color())
    aling = align.Align(text_p3, WIDTH, HEIGHT)
    screen.blit(text_p3, [aling.align_center(), aling.align_middle() + text_p3.get_height()*3])
    pygame.display.update()
    while(is_running):
        # イベント処理
        for event in pygame.event.get():
            events.quit_game(event.type)  # 閉じるボタン押下で終了
            if event.type == KEYDOWN:
                is_running = False
    # タイトル画面 --------------------------------------------------------------------------------
    is_running = True
    screen.fill(colors.Color.BLACK.color())  # ウィンドウを塗りつぶす
    # 描画する文字を設定(文字列, アンチエイリアスの有無, 色)
    text_h = font_title.render('タイピングゲーム(仮)', True, colors.Color.WHITE.color())
    text_p = font_text.render('Please press any key...', True, colors.Color.WHITE.color())
    # 文字の表示位置を設定
    aling = align.Align(text_h, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_h, [aling.align_center(), aling.align_middle() - text_h.get_height()*2])
    aling = align.Align(text_p, WIDTH, HEIGHT)  # 表示位置を操作する準備
    screen.blit(text_p, [aling.align_center(), aling.align_middle()])
    pygame.display.update()  # ウィンドウ更新(変更結果を表示)
    while(is_running):
        # イベント処理
        for event in pygame.event.get():
            events.quit_game(event.type)  # 閉じるボタン押下で終了
            if event.type == KEYDOWN:
                is_running = False
                sys.exit(0)


if __name__ == '__main__':
    main()