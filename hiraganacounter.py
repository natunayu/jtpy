from collections import Counter
import re

def count_hiragana_and_sort(text):
    # ひらがな全体のリスト
    hiragana_list = [chr(i) for i in range(ord('あ'), ord('ん') + 1)] + ['ー']

    # テキストからひらがなと伸ばし棒を抽出
    extracted = re.findall(r'[あ-んー]', text)

    # 文字ごとの出現回数をカウント
    count = Counter(extracted)

    # 出現しなかったひらがなもカウントに含める
    for hiragana in hiragana_list:
        if hiragana not in count:
            count[hiragana] = 0

    # 出現回数が多い順に並べ替え
    sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True)

    return sorted_count


# テスト用の文字列
test_text = """はんかちをおとす
かんさいべんこうざ
ちゅらうみすいぞくかん
しょくちゅうしょくぶつ
ぴぽっとてーぶる
ちょすいそうてんけん
ばれんたいんでい
ぜんにんしゃへわたす
ぎょふのりをする
あしたのてんきははれのちくもり
ぬらりひょん
ありがたいことば
べっぴんなぼうず
ぺたんこなあしでゆっくりあるく
こうがくとうせんしゃ
えねるぎーびーむ
おもてじょうのかんけい
ほうりつそうだんじむしょ
ぱんぷきんぱい
"""

# 関数を実行して結果を表示
print(count_hiragana_and_sort(test_text))
