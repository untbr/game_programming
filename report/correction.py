import sys
import random


def main():
    """
    データセットの先頭3行を取り出し問題として表示する
    """
    words = [['' for j in range(3)] for i in range(3)]  # 単語を保持する2次元配列
    with open('words.csv', mode = 'r', encoding = 'shift_jis') as f:
        for i in range(3):
            # "と\nを取り除きながら,の位置で要素を分割してリストで返す
            words[i] = f.readline().replace('"', '').replace('\n', '').split(',', maxsplit = 2)
            words[i][2] = words[i][2].strip(',')  # 末尾の要素に,が1つ残るので取り除く
    for i in range(3):
        print('-------------------------')
        print('>> Question')
        print('-', hole(words[i][0]))  # 単語(穴抜きした状態)
        print(words[i][2])  # 説明
        print('')
        print('>> Input your answer')
        ans = sys.stdin.readline().strip()
        print('->', ans == words[i][1])  # True or False
        print('Correct answer:', words[i][1])
    return 0


def hole(text: str):
    """
    文字列に対してランダムで一文字を○で置換する関数
    複数同じ文字がある場合は最初に現れる文字に対して置換を行う
    例) remenber →eを置換→ r○menber
    """
    tmp = text[random.randrange(len(text))]
    text = text.replace(tmp, '○', 1)
    return text


if __name__ == '__main__':
    main()