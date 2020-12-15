import os
import sys
import unittest

sys.path.append(os.pardir)

from materials.text import Text


class TestText(unittest.TestCase):
    """Textの単体テストをするクラス"""

    def test_input(self):
        text = Text()
        self.assertEqual(format(text), "|")  # インスタンス化時はカーソルのみ
        self.assertEqual(text.input("HelloWorld"), "HelloWorld|")
        text.cursor_pos = 5
        self.assertEqual(text.input(" "), "Hello World|")  # カーソル自体はmove_cursorメソッドで動かす

    def test_edit(self):
        text = Text()
        input_text = "こんにちは"
        for i, x in enumerate(input_text):
            self.assertEqual(text.edit(x, i + 1), "[{}|]".format(x))

    def test_delete(self):
        text = Text()
        self.assertEqual(text.input("HelloWorld"), "HelloWorld|")
        for i in range(5):
            text.delete()
        self.assertEqual(format(text), "Hello|")

    def test_enter(self):
        text = Text()
        text.input("HelloWorld")
        self.assertEqual(text.enter(), "HelloWorld")

    def test_move_cursor_left(self):
        text = Text()
        input_text = "HelloWorld"
        text.input(input_text)
        self.assertEqual(text.cursor_pos, len(input_text))
        for i in range(len(input_text)):
            text.move_cursor_left()
            self.assertEqual(text.cursor_pos, len(input_text) - i - 1)

    def test_move_cursor_right(self):
        text = Text()
        input_text = "HelloWorld"
        text.input(input_text)
        self.assertEqual(text.cursor_pos, len(input_text))
        text.move_cursor_right()
        self.assertEqual(text.cursor_pos, len(input_text))  # カーソル位置は変わらないはず
        text.cursor_pos = 0
        for i in range(len(input_text)):
            text.move_cursor_right()
            self.assertEqual(text.cursor_pos, i + 1)


if __name__ == "__main__":
    unittest.main()
