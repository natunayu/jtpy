from PIL import Image, ImageDraw, ImageFont
import os

# 文字列の配列
c1 = [
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['あ', 'い', 'う', 'え', 'お'],
    ['か', 'き', 'く', 'け', 'こ'],
    ['さ', 'し', 'す', 'せ', 'そ'],
    ['は', 'ひ', 'ふ', 'へ', 'ほ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['や', 'わ', 'ゆ', 'を', 'よ', 'ん'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['た', 'ち', 'つ', 'て', 'と'],
]

c2 = [
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ'],
    ['が', 'ぎ', 'ぐ', 'げ', 'ご'],
    ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'],
    ['ば', 'び', 'ぶ', 'べ', 'ぼ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['ゃ', 'わ', 'ゅ', 'を', 'ょ', 'ん'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['だ', 'ぢ', 'づ', 'で', 'ど'],
]

c3 = [
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['あ', 'い', 'う', 'え', 'お'],
    ['が', 'ぎ', 'ぐ', 'げ', 'ご'],
    ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'],
    ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['ゃ', 'わ', 'ゅ', 'を', 'ょ', 'ん'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['た', 'ち', 'っ', 'て', 'と'],
]


# 画像のサイズとフォントの設定
image_size = 50
font_path = r"C:/Windows/Fonts/YuGothR"  # デフォルトのフォントパス
font_size = 20

# フォントのロード
font = ImageFont.truetype(font_path, font_size)

# 出力ディレクトリの作成
output_dir = r"resource/"
os.makedirs(output_dir, exist_ok=True)

# 画像を生成する関数

# 画像を生成する関数
def create_image(char, position, file_name):
    image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # テキストのバウンディングボックスを取得
    bbox = draw.textbbox((0, 0), char, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # テキストの位置を決定
    if position == 0:  # 中央
        x = (image_size - text_width) // 2
        y = (image_size - text_height) // 2
    elif position == 1:  # 右寄せ
        x = image_size - text_width
        y = (image_size - text_height) // 2
    elif position == 2:  # 下寄せ
        x = (image_size - text_width) // 2
        y = image_size - text_height * 2.5
    elif position == 3:  # 左寄せ
        x = 0
        y = (image_size - text_height) // 2
    elif position == 4:  # 上寄せ
        x = (image_size - text_width) // 2
        y = 0
    elif position == 5:  # 左上寄せ
        x = 0
        y = 0

    # テキストを描画
    draw.text((x, y), char, fill="black", font=font)
    image.save(f"{output_dir}/{file_name}.png")

coo = "ー"
# 画像を生成
create_image(coo, 0, coo)
#for i, row in enumerate(c3):
#    for j, char in enumerate(row):
#        create_image(char, 0, char)

