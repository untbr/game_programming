"""
主要な状態における処理をまとめたモジュール
インスタンス作成後、順次メソッドを呼び出すことにより処理を行っていく
"""


import textwrap
from time import sleep
import typing
import pygame
from pygame.locals import *  # 定数読み込み
from .colors import Color  # 色に関するモジュール
from .align import Align  # オブジェクトの配置に関するモジュール
from . import events  # イベント処理に関するモジュール
from .game import Report, Shiritori
from .user import User


class State:
    """
    各画面を状態として捉えて処理を行うクラス
    インスタンス作成後、title→mode→...とメソッドを順次呼び出していく
    """

    def __init__(self, width: int, height: int) -> None:
        """
        コンストラクタ
        width: ウィンドウの横幅, height: ウィンドウの縦幅
        """
        self.user = User("test_user")  # ユーザー定義
        self.game = None  # ReportもしくはShiritoriのインスタンスを格納する変数
        self.game_mode = None
        self.width = width  # ウィンドウ横幅
        self.height = height  # ウィンドウ縦幅
        self.is_running = True  # ゲームループの判定
        pygame.init()  # Pygame初期化
        self.screen = pygame.display.set_mode((self.width, self.height))  # ウィンドウ生成(横, 縦)
        self.font_S = pygame.font.SysFont('yumincho', 15)  # テキスト：小
        self.font_M = pygame.font.SysFont('yumincho', 30)  # テキスト：中
        self.font_L = pygame.font.SysFont('yumincho', 60)  # テキスト：大

    def title(self) -> None:
        """タイトル画面"""
        pygame.display.set_caption('タイピングゲーム(仮) | Title')  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render('タイピングゲーム(仮)', True, Color.WHITE.rgb)  # タイトル
        align = Align(text_h, self.width, self.height)
        self.screen.blit(text_h, [align.center(), align.middle() - text_h.get_height()*2])
        text_p1 = self.font_M.render('開始: " 1 "を入力してください', True, Color.WHITE.rgb)  # 開始
        align = Align(text_p1, self.width, self.height)
        self.screen.blit(text_p1, [align.center(), align.middle()])
        text_p2 = self.font_M.render('終了: " 2 "を入力してください', True, Color.WHITE.rgb)  # 終了
        align = Align(text_p2, self.width, self.height)
        self.screen.blit(text_p2, [align.center(), align.middle() + text_p2.get_height()*2])
        pygame.display.update()  # 画面更新
        self.is_running = True
        while(self.is_running):
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:  # 閉じるボタン押下
                    events.quit_game()  # 終了
                if event.type == KEYDOWN:
                    if events.input_key(event.key) == '1':  # 開始
                        self.is_running = False  #次の画面へ
                    if events.input_key(event.key) == '2':  # 終了
                        events.quit_game()  # 終了

    def mode(self) -> None:
        """ゲーム選択画面"""
        pygame.display.set_caption('タイピングゲーム(仮) | Mode')  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render('ゲーム選択', True, Color.WHITE.rgb)  # タイトル
        align = Align(text_h, self.width, self.height)
        self.screen.blit(text_h, [align.center(), align.middle() - text_h.get_height()*2])
        text_p1 = self.font_M.render('レポートゲーム(仮): " 1 "を入力してください', True, Color.WHITE.rgb)
        align = Align(text_p1, self.width, self.height)
        self.screen.blit(text_p1, [align.center(), align.middle()])
        text_p2 = self.font_M.render('しりとりゲーム(仮): " 2 "を入力してください', True, Color.WHITE.rgb)
        align = Align(text_p2, self.width, self.height)
        self.screen.blit(text_p2, [align.center(), align.middle() + text_p2.get_height()])
        pygame.display.update()  # 画面更新
        self.is_running = True
        while(self.is_running):
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                if event.type == KEYDOWN:
                    if events.input_key(event.key) == '1':  # 「レポートゲーム(仮)」を選択
                        self.game = Report()
                        self.is_running = False
                    elif events.input_key(event.key) == '2':  # 「しりとりゲーム(仮)」を選択
                        self.game = Shiritori()
                        self.is_running = False
        self.game_mode = self.game.get_mode()  # 難易度(品詞)を取得

    def choose(self) -> None:
        """モード選択画面"""
        pygame.display.set_caption('タイピングゲーム(仮) | Choose')  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render('モード選択', True, Color.WHITE.rgb)  # タイトル
        align = Align(text_h, self.width, self.height)
        self.screen.blit(text_h, [align.center(), align.middle() - text_h.get_height()*2])
        for i in self.game_mode:
            text_p = self.font_M.render('{0}: " {1} "を入力してください'.format(i.value, i.id), True, Color.WHITE.rgb)
            align = Align(text_p, self.width, self.height)
            self.screen.blit(text_p, [align.center(), align.middle() + text_p.get_height()*i.id])
        pygame.display.update()  # 画面更新
        self.is_running = True
        while(self.is_running):
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                if event.type == KEYDOWN:
                    if events.input_key(event.key) == '0':  # 「かんたん/名詞」を選択
                        self.game.set_mode(self.game_mode[int(0)])  # 難易度/品詞の設定
                        self.is_running = False
                    elif events.input_key(event.key) == '1':  # 「ふつう/動詞」を選択
                        self.game.set_mode(self.game_mode[int(1)])  # 難易度/品詞の設定
                        self.is_running = False
                    elif events.input_key(event.key) == '2':  # 「むずかしい/形容詞」を選択
                        self.game.set_mode(self.game_mode[int(2)])  # 難易度/品詞の設定
                        self.is_running = False

    def play(self) -> None:
        """ゲームプレイ画面"""
        pygame.display.set_caption('タイピングゲーム(仮) | Play')  # キャプション設定
        while not self.game.is_finish():
            self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
            # 画面に表示するテキストの設定
            text_h = self.font_M.render('時間内に入力せよ！', True, Color.WHITE.rgb)  # 小見出し
            align = Align(text_h, self.width, self.height)
            self.screen.blit(text_h, [align.left() + 10, align.top() + 10])
            text_time = self.font_M.render('00:00', True, Color.WHITE.rgb)  # 残り時間 ダミー
            align = Align(text_time, self.width, self.height)
            self.screen.blit(text_time, [align.right() - 10, align.top() + 10])
            text_input = self.font_M.render('|', True, Color.WHITE.rgb)  # 入力文字
            align = Align(text_input, self.width, self.height)
            self.screen.blit(text_input, [align.center(), align.bottom() - text_input.get_height()])
            word = self.game.get_word()  # 出題をしてもらう
            text_word = self.font_L.render(word.word, True, Color.WHITE.rgb)  # 単語
            align = Align(text_word, self.width, self.height)
            self.screen.blit(text_word, [align.center(), align.top() + text_h.get_height()*2])
            for i, desc in enumerate(textwrap.wrap(word.describe, 18)):
                text_desc = self.font_M.render(desc, True, Color.WHITE.rgb)  #説明
                align = Align(text_desc, self.width, self.height)
                self.screen.blit(text_desc, [align.center(), align.top() + text_desc.get_height()*(i + 1) + text_h.get_height()*3])
            pygame.display.update()  # 画面更新
            # 文字入力に必要な変数
            txt_give = ''  # 最終的に正誤処理へ渡す文字列を保持する変数
            txt_words = []  # 入力された文字を保持するリスト
            txt_tmp = ''  # 入力された1文字を一時的に保持する変数
            self.is_running = True
            while(self.is_running):
                # イベント処理
                for event in pygame.event.get():
                    if event.type == QUIT:
                        events.quit_game()  # 閉じるボタン押下で終了
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:  # Enter押下時
                            txt_give = ''.join(txt_words)  # 文字列に直す
                            txt_words = []  # 初期化
                            self.is_running = False
                        elif event.key == K_BACKSPACE:  # BackSpace押下時
                            if not len(txt_words) == 0:
                                txt_words.pop()  # 最後の文字を取り出す(削除)
                        else:  # 上記以外のキーが押された時
                            txt_tmp = events.input_key(event.key)
                            if not txt_tmp == None:  # 入力受取の可否判断
                                txt_words.append(txt_tmp)
                        # 上書き(塗りつぶし) rect値(x, y, width, height)
                        self.screen.fill(Color.BLACK.rgb, (float(align.center()), float(align.bottom() - text_input.get_height()), float(self.width), float(text_input.get_height())))
                        pygame.display.update()  # 画面更新
                        if not len(txt_words) == 0:  # 表示するテキストが存在するかの判断
                            text_input = self.font_M.render(''.join(txt_words) + '|', True, Color.WHITE.rgb)
                        else:
                            if not self.is_running == False:  # Enterが押された後か判断
                                text_input = self.font_M.render('|', True, Color.WHITE.rgb)
                            else:
                                text_input = self.font_M.render(txt_give, True, Color.WHITE.rgb)
                        align = Align(text_input, self.width, self.height)
                        self.screen.blit(text_input, [align.center(), align.bottom() - text_input.get_height()])
                        pygame.display.update()  # 画面更新
            judge = self.game.judge_word(txt_give)  # 正誤判定
            if not judge.correct:  # 不正解時
                # 上書き(塗りつぶし) rect値(x, y, width, height)
                self.screen.fill(Color.BLACK.rgb, (float(align.center()), float(align.bottom() - text_input.get_height()), float(self.width), float(text_input.get_height())))
                pygame.display.update()  # 画面更新
                text_jud = self.font_M.render(judge.message, True, Color.RED.rgb)  # 入力文字
                align = Align(text_jud, self.width, self.height)
                self.screen.blit(text_jud, [align.center(), align.bottom() - text_jud.get_height()])
                pygame.display.update()  # 画面更新
                sleep(2)  # 不正解時のメッセージを見せるために2秒待機
        self.user.add_score(self.game.score)  # ユーザーの情報にスコアを追加

    def result(self):
        """リザルト画面"""
        pygame.display.set_caption('タイピングゲーム(仮) | Result')  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render('リザルト', True, Color.WHITE.rgb)  # ヘッダー
        align = Align(text_h, self.width, self.height)
        self.screen.blit(text_h, [align.center(), align.middle() - text_h.get_height()*2])
        result = self.user.__str__().split('\n')  # ちょっと無理に処理
        for i, val in enumerate(result):
            text_p = self.font_M.render(val, True, Color.WHITE.rgb)  # リザルト
            align = Align(text_p, self.width, self.height)
            self.screen.blit(text_p, [align.center(), align.middle() + text_p.get_height()*i])
        text_next = self.font_M.render('Please press any key...'.format(0), True, Color.WHITE.rgb)  # 操作の促し
        align = Align(text_next, self.width, self.height)
        self.screen.blit(text_next, [align.center(), align.middle() + text_next.get_height()*5])
        pygame.display.update()  # 画面更新
        self.is_running = True
        while(self.is_running):
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                if event.type == KEYDOWN:
                    self.is_running = False  #キー入力検知で次の画面へ