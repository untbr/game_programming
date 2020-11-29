class Align():
    """
    Surfaceオブジェクトに対して上下左右の配置をサポートするクラス
    Surface.blit()等でオブジェクトを画面上に描画するときに合わせて使用する
    """
    def __init__(self, surface_obj, win_w: int, win_h: int) -> None:
        """
        コンストラクタ
        surface_obj: Surfaceオブジェクト, win_w: ウィンドウの横幅, win_h: ウィンドウの縦幅
        """
        self.obj = surface_obj
        self.win_w = win_w
        self.win_h = win_h

    def align_left(self) -> int:
        """オブジェクトを水平方向に対して左寄せする関数"""
        return 0

    def align_right(self) -> int:
        """オブジェクトを水平方向に対して右寄せする関数"""
        return (self.win_w - self.obj.get_width())

    def align_center(self) -> int:
        """オブジェクトを水平方向に対して中央寄せする関数"""
        return int((self.win_w/2) - (self.obj.get_width()/2))

    def align_top(self) -> int:
        """オブジェクトを垂直方向に対して上寄せする関数"""
        return 0

    def align_bottom(self) -> int:
        """オブジェクトを垂直方向に対して下寄せする関数"""
        return (self.win_h - self.obj.get_height())

    def align_middle(self) -> int:
        """オブジェクトを垂直方向に対して中央寄せする関数"""
        return int((self.win_h/2) - (self.obj.get_height()/2))