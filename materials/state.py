"""
主要な状態における処理をまとめたモジュール
インスタンス作成後、順次メソッドを呼び出すことにより処理を行っていく
"""


import textwrap
import pygame
from enum import Enum
from pygame.locals import *  # 定数読み込み
from .colors import Color  # 色に関するモジュール
from .align import Align  # オブジェクトの配置に関するモジュール
from . import events  # イベント処理に関するモジュール
import sys
sys.path.append('../')
from game import game

class States(Enum):
    """状態の定義"""
    TITLE = 0
    TYPE = 1
    MODE = 2
    PLAY = 3
    RESULT = 4


class State:
    def __init__(self):
        self.state = None
        self.type = None
        self.modes = None

    def transition(self):
        """現在時の状態とキーの押下に応じて状態を更新するメソッド"""
        for event in pygame.event.get():
            if self.state is None: # 初期状態のNoneであれば
                self.state = States.TITLE
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = States.TITLE
                # 状態がTITLEでキーの押下があったとき
                elif self.state == States.TITLE:
                    #if event.key == K_SPACE:
                    self.state = States.TYPE  # 次の状態CHOOSEに遷移する
                # 状態がCHOOSEでキーの押下があったとき
                elif self.state == States.TYPE:
                    if event.key in [K_f, K_j]:
                        self.state = States.MODE  # 次の状態MODEに遷移する
                        if event.key == K_f:
                            self.type = game.Report() # typeをレポートゲームにする
                        else:
                            self.type = game.Shiritori() # typeをしりとりゲームにする
                        self.modes = self.type.get_mode()
                elif self.state == States.MODE:
                    if event.key in [K_0, K_1, K_2]:
                        self.state = States.MODE  # 次の状態MODEに遷移する
                        self.type.set_mode(self.type.get_mode()[int(pygame.key.name(event.key))])
                        self.state = States.PLAY
                # 状態がPLAYでキーの押下があったとき
                elif self.state == States.PLAY:
                    if event.key == K_SPACE:
                        self.state = States.RESULT  # 次の状態RESULTに遷移する
                # 状態がRESULTでキーの押下があったとき
                elif self.state == States.RESULT:
                    if event.key == K_SPACE:
                        self.state = States.TITLE  # 次の状態TITLEにする
            if event.type == QUIT:
                events.quit_game(event.type)  # 閉じるボタン押下で終了


"""
各画面を状態として捉えて処理を行うクラス
インスタンス作成後、title→choose→play→resultメソッドを順次呼び出していく
"""


class Drawer(State):
    def __init__(self, width: int, height: int) -> None:
        """
        コンストラクタ
        width: ウィンドウの横幅, height: ウィンドウの縦幅
        """
        super().__init__()
        self.width = width  # ウィンドウ横幅
        self.height = height  # ウィンドウ縦幅
        pygame.init()  # Pygame初期化
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # ウィンドウ生成(横, 縦)
        self.font_S = pygame.font.SysFont("yumincho", 15)  # テキスト：小
        self.font_M = pygame.font.SysFont("yumincho", 30)  # テキスト：中
        self.font_L = pygame.font.SysFont("yumincho", 60)  # テキスト：大

    def title(self) -> None:
        """タイトル画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Title")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render("タイピングゲーム(仮)", True, Color.WHITE.rgb)  # タイトル
        align = Align(text_h, self.width, self.height)
        self.screen.blit(
            text_h, [align.center(), align.middle() - text_h.get_height() * 2]
        )
        text_p = self.font_M.render(
            "Please press any key...", True, Color.WHITE.rgb
        )  # 操作の促し
        align = Align(text_p, self.width, self.height)
        self.screen.blit(text_p, [align.center(), align.middle()])
        pygame.display.update()  # 画面更新

    def choose_type(self) -> None:
        """難易度選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Choose")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render("難易度選択", True, Color.WHITE.rgb)  # タイトル
        align = Align(text_h, self.width, self.height)
        self.screen.blit(
            text_h, [align.center(), align.middle() - text_h.get_height() * 2]
        )
        text_p1 = self.font_M.render('レポート: Input " f "', True, Color.WHITE.rgb)  # 難易度1
        align = Align(text_p1, self.width, self.height)
        self.screen.blit(text_p1, [align.center(), align.middle()])
        text_p2 = self.font_M.render(
            'しりとり: Input " j "', True, Color.WHITE.rgb
        )  # 難易度2
        align = Align(text_p2, self.width, self.height)
        self.screen.blit(
            text_p2, [align.center(), align.middle() + text_p2.get_height()]
        )
        pygame.display.update()  # 画面更新

    def mode(self) -> None:
        """難易度選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Choose")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render("難易度選択", True, Color.WHITE.rgb)  # タイトル
        align = Align(text_h, self.width, self.height)
        self.screen.blit(
            text_h, [align.center(), align.middle() - text_h.get_height() * 2]
        )
        m = 0
        for  x in self.modes:
            text_p1 = self.font_M.render("{}: {}".format(x.value,x.id), True, Color.WHITE.rgb)  # 難易度1
            align = Align(text_p1, self.width, self.height)
            self.screen.blit(text_p1, [align.center(), align.middle()+m])
            m += 30
        pygame.display.update()  # 画面更新

    def play(self) -> None:
        """ゲームプレイ画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Play")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_M.render("時間内に入力せよ！", True, Color.WHITE.rgb)  # 小見出し
        align = Align(text_h, self.width, self.height)
        self.screen.blit(text_h, [align.left() + 10, align.top() + 10])
        text_time = self.font_M.render("00:00", True, Color.WHITE.rgb)  # 残り時間
        align = Align(text_time, self.width, self.height)
        self.screen.blit(text_time, [align.right() - 10, align.top() + 10])

        #text_word = self.font_L.render("オブ○ェクト", True, Color.WHITE.rgb)  # 単語
        #align = Align(text_word, self.width, self.height)
        #self.screen.blit(
        #    text_word, [align.center(), align.middle() - text_h.get_height() * 3]
        #)
        #text = "オブジェクトとは、物、物体、目標物、対象、目的語、客体、などの意味を持つ英単語。"
        #for i, desc in enumerate(textwrap.wrap(text, 18)):
        #    text_desc = self.font_M.render(desc, True, Color.WHITE.rgb)  # 説明
        #    align = Align(text_desc, self.width, self.height)
        #    self.screen.blit(
        #        text_desc,
        #        [
        #            align.center(),
        #            align.middle()
        #            + text_desc.get_height() * i
        #            - text_desc.get_height(),
        #        ],
        #    )
        pygame.display.update()  # 画面更新

    def result(self):
        """リザルト画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Result")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        text_h = self.font_L.render("リザルト", True, Color.WHITE.rgb)  # ヘッダー
        align = Align(text_h, self.width, self.height)
        self.screen.blit(
            text_h, [align.center(), align.middle() - text_h.get_height() * 2]
        )
        text_p1 = self.font_M.render("正解：{0}".format(0), True, Color.WHITE.rgb)  # 正解
        align = Align(text_p1, self.width, self.height)
        self.screen.blit(text_p1, [align.center(), align.middle()])
        text_p2 = self.font_M.render("不正解：{0}".format(0), True, Color.WHITE.rgb)  # 不正解
        align = Align(text_p2, self.width, self.height)
        self.screen.blit(
            text_p2, [align.center(), align.middle() + text_p2.get_height()]
        )
        text_p3 = self.font_M.render(
            "Please press any key...".format(0), True, Color.WHITE.rgb
        )  # 操作の促し
        align = Align(text_p3, self.width, self.height)
        self.screen.blit(
            text_p3, [align.center(), align.middle() + text_p3.get_height() * 3]
        )
        pygame.display.update()  # 画面更新
