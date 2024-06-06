import pyautogui as pyautogui
import pygame
import math
import tkinter as tk
from threading import Thread
from tkinter import PhotoImage, Label
import io
import time

"""0=PS5R, 1=switch-R 2=switch-L"""
c = 1

"""0-右スティックx, 1-右スティックy, 2-R押し込み, 3-Rバンパー, 4-1〇, 5-0×, 6-Rトリガー"""
controller_settings = [[2, 3, 8, 10, 1, 0, 5], [1, 0, 7, 16, 1, 3, 18], [1, 0, 7, 17, 1, 0, 19]]

flag = 0

section = 0

section_pie = None

# デッドゾーンのしきい値を設定
DEADZONE = 0.5

list_layer0_hiragana = [
    "な", "あ", "か",
    "さ", "は", "ら",
    "や", "ま", "た"
]

list_layer1_hiragana = [
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['あ', 'い', 'う', 'え', 'お'],
    ['か', 'き', 'く', 'け', 'こ'],
    ['さ', 'し', 'す', 'せ', 'そ'],
    ['は', 'ひ', 'ふ', 'へ', 'ほ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['や', 'わ', 'ゆ', 'を', 'よ', "ん", '-'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['た', 'ち', 'つ', 'て', 'と'],
]

list_modeb_hiragana = [
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ'],
    ['が', 'ぎ', 'ぐ', 'げ', 'ご'],
    ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'],
    ['ば', 'び', 'ぶ', 'べ', 'ぼ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['ゃ', 'わ', 'ゅ', 'を', 'ょ', 'ん', '-'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['だ', 'ぢ', 'づ', 'で', 'ど'],
]

list_modep_hiragana = [
    ['な', 'に', 'ぬ', 'ね', 'の'],
    ['あ', 'い', 'う', 'え', 'お'],
    ['が', 'ぎ', 'ぐ', 'げ', 'ご'],
    ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'],
    ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'],
    ['ら', 'り', 'る', 'れ', 'ろ'],
    ['ゃ', 'わ', 'ゅ', 'を', 'ょ', 'ん', '-'],
    ['ま', 'み', 'む', 'め', 'も'],
    ['た', 'ち', 'っ', 'て', 'と'],
]

hiragana_to_romaji = {
    'あ': 'a  ', 'い': 'i  ', 'う': 'u  ', 'え': 'e  ', 'お': 'o  ',
    'か': 'ka ', 'き': 'ki ', 'く': 'ku ', 'け': 'ke ', 'こ': 'ko ',
    'さ': 'sa ', 'し': 'si ', 'す': 'su ', 'せ': 'se ', 'そ': 'so ',
    'た': 'ta ', 'ち': 'ti ', 'つ': 'tu ', 'て': 'te ', 'と': 'to ', 'っ': 'xtu',
    'な': 'na ', 'に': 'ni ', 'ぬ': 'nu ', 'ね': 'ne ', 'の': 'no ',
    'は': 'ha ', 'ひ': 'hi ', 'ふ': 'fu ', 'へ': 'he ', 'ほ': 'ho ',
    'ま': 'ma ', 'み': 'mi ', 'む': 'mu ', 'め': 'me ', 'も': 'mo ',
    'や': 'ya ', 'ゆ': 'yu ', 'よ': 'yo ', 'わ': 'wa ', 'を': 'wo ', 'ん': 'nn ',
    'ら': 'ra ', 'り': 'ri ', 'る': 'ru ', 'れ': 're ', 'ろ': 'ro ',
    'が': 'ga ', 'ぎ': 'gi ', 'ぐ': 'gu ', 'げ': 'ge ', 'ご': 'go ',
    'ざ': 'za ', 'じ': 'zi ', 'ず': 'zu ', 'ぜ': 'ze ', 'ぞ': 'zo ',
    'だ': 'da ', 'ぢ': 'di ', 'づ': 'du ', 'で': 'de ', 'ど': 'do ',
    'ば': 'ba ', 'び': 'bi ', 'ぶ': 'bu ', 'べ': 'be ', 'ぼ': 'bo ',
    'ぱ': 'pa ', 'ぴ': 'pi ', 'ぷ': 'pu ', 'ぺ': 'pe ', 'ぽ': 'po ',
    'ゃ': 'xya', 'ゅ': 'xyu', 'ょ': 'xyo',
    'ぁ': 'xa ', 'ぃ': 'xi ', 'ぅ': 'xu ', 'ぇ': 'xe ', 'ぉ': 'xo ', '-': '-  '
}

# n, b, p
mode = "n"

# レイヤー0の画像を保存
imgList_r_l0 = []
imgList_b_l0 = []

# 二次元配列で画像データを保持
imgList_r_l1 = []
imgList_b_l1 = []

# モードB
imgList_r_mb = []
imgList_b_mb = []

# モードP
imgList_r_mp = []
imgList_b_mp = []

# 透明な画像
img_none = None

# 画像とテキストのラベルの参照を保持するグローバル変数
labels = []
text_label = None

# 音声の読み込み
sounds = []

# pygameのミキサーの初期化はプログラムの開始時に一度だけ行う
pygame.mixer.init()


def R1_button_down(layer):
    global section_pie
    global mode

    if mode == "n":
        mode = "b"
        if layer == 1 and section_pie == 6:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     6, 4, 5]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    labels[index].config(image=imgList_b_mb[section_pie][image_number])
                else:
                    labels[index].config(image=imgList_r_mb[section_pie][image_number])

        elif layer == 1:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     9, 4, 9]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    labels[index].config(image=imgList_b_mb[section_pie][image_number])
                else:
                    labels[index].config(image=imgList_r_mb[section_pie][image_number])

    elif mode == "b" and (section_pie == 4 or section_pie == 8):
        mode = "p"
        if layer == 1 and section_pie == 6:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     6, 4, 5]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    labels[index].config(image=imgList_b_mp[section_pie][image_number])
                else:
                    labels[index].config(image=imgList_r_mp[section_pie][image_number])

        elif layer == 1:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     9, 4, 9]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    labels[index].config(image=imgList_b_mp[section_pie][image_number])
                else:
                    labels[index].config(image=imgList_r_mp[section_pie][image_number])
    else:
        mode = "n"
        if layer == 1 and section_pie == 6:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     6, 4, 5]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    labels[index].config(image=imgList_b_l1[section_pie][image_number])
                else:
                    labels[index].config(image=imgList_r_l1[section_pie][image_number])

        elif layer == 1:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     9, 4, 9]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    labels[index].config(image=imgList_b_l1[section_pie][image_number])
                else:
                    labels[index].config(image=imgList_r_l1[section_pie][image_number])


def handle_button_down(button, layer):
    """ボタンが押された時の処理を行う関数"""

    global section
    global imgList_r_l0
    global imgList_b_l0
    global imgList_r_l1
    global imgList_b_l1
    global labels
    global section_pie
    global img_none

    print(f"Button {button} pressed")

    if layer == 1 and section_pie == 6:
        section_pie = section
        # 画像の番号に従って配置する順序
        # 9の時はパス
        order = [9, 2, 9,
                 1, 0, 3,
                 6, 4, 5]

        # 3x3グリッドに画像を配置
        for index, image_number in enumerate(order):
            if image_number == 9:
                labels[index].config(image=img_none)
                continue
            if image_number == section:
                labels[index].config(image=imgList_b_l1[section_pie][image_number])
            else:
                labels[index].config(image=imgList_r_l1[section_pie][image_number])


    elif layer == 0:
        layer = 1
        section_pie = section

        # 画像の番号に従って配置する順序
        # 9の時はパス
        order = [9, 2, 9,
                 1, 0, 3,
                 9, 4, 9]

        # 3x3グリッドに画像を配置
        for index, image_number in enumerate(order):
            if image_number == 9:
                labels[index].config(image=img_none)
                continue
            if image_number == section:
                labels[index].config(image=imgList_b_l1[section_pie][image_number])
            else:
                labels[index].config(image=imgList_r_l1[section_pie][image_number])

    else:
        layer = 0
        section_pie = None

    print(layer)
    return layer


def handle_button_up(button, layer):
    """ボタンが離された時の処理を行う関数"""
    global section
    global section_pie
    global imgList_r_l0
    global imgList_b_l0
    global mode

    print(f"Button {button} released")

    if layer == 1:
        layer = 0

        # 画像の番号に従って配置する順序
        order = [1, 2, 3,
                 8, 0, 4,
                 7, 6, 5]

        # 3x3グリッドに画像を配置
        for index, image_number in enumerate(order):
            if image_number == section:
                labels[index].config(image=imgList_b_l0[image_number])
            else:
                labels[index].config(image=imgList_r_l0[image_number])

    print(layer)
    play_mp3(1)
    # 入力呼び出し関数
    input_character_with_ime(section_pie, section)

    # リセット
    section_pie = None
    mode = "n"
    return layer


def update_display(layer, nex_s):
    global section
    global imgList_r_l0
    global imgList_b_l0
    global imgList_r_l1
    global imgList_b_l1
    global labels
    global section_pie

    # セクションの遷移判定
    if nex_s == section:
        return 0

    else:
        play_mp3(0)
        print("更新")
        section = nex_s

        if layer == 0:
            # 画像の番号に従って配置する順序
            order = [1, 2, 3,
                     8, 0, 4,
                     7, 6, 5]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == section:
                    labels[index].config(image=imgList_b_l0[image_number])
                else:
                    labels[index].config(image=imgList_r_l0[image_number])

        elif layer == 1 and section_pie == 6:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     6, 4, 5]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    if mode == "n":
                        labels[index].config(image=imgList_b_l1[section_pie][image_number])
                    elif mode == "b":
                        labels[index].config(image=imgList_b_mb[section_pie][image_number])
                    else:
                        labels[index].config(image=imgList_b_mp[section_pie][image_number])
                else:
                    if mode == "n":
                        labels[index].config(image=imgList_r_l1[section_pie][image_number])
                    elif mode == "b":
                        labels[index].config(image=imgList_r_mb[section_pie][image_number])
                    else:
                        labels[index].config(image=imgList_r_mp[section_pie][image_number])


        elif layer == 1:
            # 画像の番号に従って配置する順序
            # 9の時はパス
            order = [9, 2, 9,
                     1, 0, 3,
                     9, 4, 9]

            # 3x3グリッドに画像を配置
            for index, image_number in enumerate(order):
                if image_number == 9:
                    labels[index].config(image=img_none)
                    continue
                if image_number == section:
                    if mode == "n":
                        labels[index].config(image=imgList_b_l1[section_pie][image_number])
                    elif mode == "b":
                        labels[index].config(image=imgList_b_mb[section_pie][image_number])
                    else:
                        labels[index].config(image=imgList_b_mp[section_pie][image_number])
                else:
                    if mode == "n":
                        labels[index].config(image=imgList_r_l1[section_pie][image_number])
                    elif mode == "b":
                        labels[index].config(image=imgList_r_mb[section_pie][image_number])
                    else:
                        labels[index].config(image=imgList_r_mp[section_pie][image_number])

        # play_sound(1)


# ジョイスティックのイベントを処理するための関数
def joystick_event_handling(labels):
    global running
    global controller_settings
    global c
    global DEADZONE
    layer = 0

    while running:
        # イベントキューを処理する

        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.JOYBUTTONDOWN:
                print("Button pressed:", event.button)

            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == controller_settings[c][6] and event.value > 0.5:  # 軸の値が一定値を超えたらトリガーが押されたと判断
                    print("トリガーボタン（R1）が押されました。", event.axis)
                    pyautogui.press('TAB')

            if event.type == pygame.JOYBUTTONDOWN and event.button == controller_settings[c][1]:
                pyautogui.press('enter')

            elif event.type == pygame.JOYBUTTONDOWN and (event.button == controller_settings[c][5]):
                pyautogui.press('backspace')

            elif event.type == pygame.JOYBUTTONDOWN and event.button == controller_settings[c][2]:
                if layer != 1 or section_pie in [0, 5, 7]:
                    pass
                else:
                    # ボタンが押された時のイベントを処理
                    R1_button_down(layer)

            elif event.type == pygame.JOYBUTTONDOWN and event.button == controller_settings[c][3]:
                # ボタンが押された時のイベントを処理
                layer = handle_button_down(event.button, layer)

            elif event.type == pygame.JOYBUTTONUP and event.button == controller_settings[c][3]:
                # ボタンが離された時のイベントを処理
                layer = handle_button_up(event.button, layer)

        # 右のジョイスティックの入力を取得
        right_x_axis = joystick.get_axis(controller_settings[c][0])  # 通常、右のジョイスティックのX軸はインデックス2
        right_y_axis = joystick.get_axis(controller_settings[c][1])  # 通常、右のジョイスティックのY軸はインデックス3
        if c == 1:
            right_y_axis = right_y_axis * -1

        elif c == 2:
            right_x_axis = right_x_axis * -1

        # 右のジョイスティックの表示テキストを更新
        display_text, nex_s = get_section_num(right_x_axis, right_y_axis, DEADZONE, layer)
        update_text(display_text)

        update_display(layer, nex_s)

        pygame.time.wait(100)


def get_section_num(x_axis, y_axis, dead_zone, layer):
    global mode
    section = None  # ここでデフォルト値を設定

    if abs(x_axis) < dead_zone:
        x_axis = 0
    if abs(y_axis) < dead_zone:
        y_axis = 0

    # ジョイスティックがデッドゾーン外にある場合のみ角度を計算
    if x_axis != 0 or y_axis != 0:
        # ジョイスティックの角度を計算（ラジアンから度に変換）
        angle = int(math.atan2(y_axis, x_axis) * (180 / math.pi))

        # 角度を正の範囲に変換（-180～180から0～360度）
        if angle < 0:
            angle += 360

        # レイヤー0の時
        if layer == 0:

            # 水平垂直
            if angle == 270:
                section = 2

            elif angle == 0:
                section = 4

            elif angle == 90:
                section = 6

            elif angle == 180:
                section = 8

            # 対角
            elif 270 > angle > 180:
                section = 1

            elif 180 > angle > 90:
                section = 7

            elif 90 > angle > 0:
                section = 5

            elif angle > 270:
                section = 3

        # やゆよ・わをんの行
        # up: 1 left:2 right: down
        if layer == 1 and section_pie == 6:

            # up
            if 225 <= angle < 315:
                section = 2

            # left
            elif 180 < angle < 225 or angle == 180:
                section = 1

            # right
            elif 315 <= angle <= 360 or angle == 0:
                section = 3

            # ななめ右した
            elif 0 < angle < 90:
                section = 5

            # ななめ左した
            elif 90 < angle < 180:
                section = 6

            # down
            elif 90:
                section = 4



        # up: 1 left:2 right: down
        elif layer == 1:
            # up
            if 225 <= angle < 315:
                section = 2

            # right
            elif 315 <= angle < 360 or 0 <= angle < 45:
                section = 3

            # down
            elif 45 <= angle < 135:
                section = 4

            # left
            elif 135 <= angle < 225:
                section = 1

        # section = int(angle // (360 // cut_into))
        return f"A: {angle:.2f} , S: {section}, L: {layer}, M: {mode}", section
    else:
        return f"A: -1, S: 0, L: {layer}, M: {mode}", 0


def on_close():
    global running
    running = False
    thread.join()
    pygame.joystick.quit()
    pygame.quit()
    root.destroy()


def create_image_grid(root):
    global labels
    global imgList_b_l0
    global imgList_r_l0
    image_frame = tk.Frame(root)
    image_frame.pack()

    # 画像の番号に従って配置する順序
    order = [1, 2, 3,
             8, 0, 4,
             7, 6, 5]

    # 3x3グリッドに画像を配置
    for index, image_number in enumerate(order):
        row = index // 3
        col = index % 3
        if image_number == 0:
            img_label = Label(image_frame, image=imgList_b_l0[image_number])
        else:
            img_label = Label(image_frame, image=imgList_r_l0[image_number])
        img_label.image = imgList_r_l1[image_number]  # ガベージコレクションを防ぐための参照の保持
        img_label.grid(row=row, column=col, padx=5, pady=5)
        labels.append(img_label)

    print(labels)


def create_text_area(root):
    global text_label

    text_frame = tk.Frame(root)
    text_frame.pack()

    text_label = Label(text_frame, text="Joystick")
    text_label.pack()


def input_character_with_ime(x, y):
    global list_layer1_hiragana
    global hiragana_to_romaji
    global mode

    hiragana = ""
    # 選択された文字を取得
    print(x, y)
    try:
        if mode == "n":
            hiragana = list_layer1_hiragana[x][y]
        elif mode == "b":
            hiragana = list_modeb_hiragana[x][y]
        elif mode == "p":
            hiragana = list_modep_hiragana[x][y]

        romaji = hiragana_to_romaji[hiragana]
        if romaji[1] == " " and romaji[2] == " ":
            s_1 = romaji[0]
            pyautogui.write(s_1)

        elif romaji[2] == " ":
            s_1, s_2 = romaji[0], romaji[1]
            pyautogui.write(s_1)
            pyautogui.write(s_2)

        else:
            s_1, s_2, s_3 = romaji[0], romaji[1], romaji[2]
            pyautogui.write(s_1)
            pyautogui.write(s_2)
            pyautogui.write(s_3)

    except IndexError:
        print("Error: 値抜け")
        pass


def update_text(new_text):
    global text_label
    text_label.config(text=new_text)


def play_sound(i):
    global sounds
    """ 音声を再生する """
    play_obj = sounds[i].play()
    play_obj.wait_done()


def set_center_window(r, width=350, height=250):
    screen_width = r.winfo_screenwidth()
    screen_height = r.winfo_screenheight()

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2)
    r.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 渡されたオブジェクトのジオメトリーに設定


def play_mp3(i):
    """
    リスト内のMP3ファイルを非同期で再生します。

    :param i: 再生するMP3ファイルのインデックス。
    """

    def play_sound():
        mp3_list = ["resource/sound/enter01.mp3", "resource/sound/enter02.mp3"]
        mp3 = mp3_list[i]
        try:
            # MP3ファイルをロード
            pygame.mixer.music.load(mp3)
            # MP3ファイルを再生
            pygame.mixer.music.play()
        except Exception as e:
            print(f"{mp3}の再生中にエラーが発生しました: {e}")

    # 音楽の再生を別スレッドで実行
    thread = Thread(target=play_sound)
    thread.start()


if __name__ == '__main__':
    # Pygameを初期化
    pygame.init()

    # ジョイスティックの初期化
    pygame.joystick.init()

    # 最初のジョイスティックを取得
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Tkinterウィンドウを設定
    root = tk.Tk()
    root.title('Joystick Status')
    set_center_window(root, 250, 250)
    # 透明な画像
    img_none = PhotoImage(file=f"resource/none.png")

    # レイヤー0の画像を保存
    imgList_r_l0 = [PhotoImage(file=f"resource/r/hiragana_{list_layer0_hiragana[i]}.png") for i in range(9)]
    imgList_b_l0 = [PhotoImage(file=f"resource/b/hiragana_{list_layer0_hiragana[i]}.png") for i in range(9)]

    # 二次元配列で画像データを保持
    imgList_r_l1 = [[PhotoImage(file=f"resource/r/hiragana_{hiragana}.png") if hiragana else None for hiragana in row]
                    for row in list_layer1_hiragana]

    # 二次元配列で画像データを保持
    imgList_b_l1 = [[PhotoImage(file=f"resource/b/hiragana_{hiragana}.png") if hiragana else None for hiragana in row]
                    for row in list_layer1_hiragana]

    # ModeB
    imgList_r_mb = [[PhotoImage(file=f"resource/r/hiragana_{hiragana}.png") if hiragana else None for hiragana in row]
                    for row in list_modeb_hiragana]

    imgList_b_mb = [[PhotoImage(file=f"resource/b/hiragana_{hiragana}.png") if hiragana else None for hiragana in row]
                    for row in list_modeb_hiragana]

    # ModeP
    imgList_r_mp = [[PhotoImage(file=f"resource/r/hiragana_{hiragana}.png") if hiragana else None for hiragana in row]
                    for row in list_modep_hiragana]

    imgList_b_mp = [[PhotoImage(file=f"resource/b/hiragana_{hiragana}.png") if hiragana else None for hiragana in row]
                    for row in list_modep_hiragana]

    print(imgList_b_l1)

    # サウンドロード
    # sounds_path = [f"resource/sound/enter01.mp3", f"resource/sound/enter02.mp3"]
    # sounds = load_mp3s(sounds_path)

    create_image_grid(root)
    create_text_area(root)

    # スレッドが動いているかのフラグ
    running = True

    # ジョイスティックイベントを処理するスレッドを開始
    thread = Thread(target=joystick_event_handling, args=(labels,))
    thread.daemon = True
    thread.start()

    # Tkinterのウィンドウが閉じられたときの処理

    root.protocol('WM_DELETE_WINDOW', on_close)

    root.mainloop()
