from typing import Optional

from fastapi import FastAPI, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from shiritori import Mode, Response, Shiritori

app = FastAPI()
shiritori = Shiritori()
word_classes = [i.value for i in Mode]

@app.get("/shiritori/")
def hello() -> str:
    return "Hello"

@app.get("/")
def default() -> RedirectResponse:
    return RedirectResponse("docs/")


@app.get("/shiritori/{mode}", response_model=Response)
def judge_valid_word(
    *,
    mode: int = Path(..., ge=0, lt=len(Mode)),
    text: str,
    head_word: str
) -> Response:
    """	
    入力された文字の品詞などが正しいのかを判定する関数	
    """
    mode_word_class: str = word_classes[mode].class_name
    response: Response = shiritori.is_correct_word(mode_word_class, text, head_word)
    return response

@app.get("/shiritori/head_word/", response_model=Response)
def get_initial_word() -> Response:
    """	
    ゲーム開始時に出題する頭文字を生成するメソッド	
    カタカナ、アスキーコードのァからンまでの間の値から一つ選び、	
    それをひらがなに直す(小文字を避けるため)	
    """
    return shiritori.make_initial_word()


@app.get("/shiritori/modes/")
def get_mode() -> dict:
    """	
    しりとりの品詞のモード一覧を返す関数	
    """
    return dict(word_classes)
