import sys
import tkinter as tk
import csv
from tkinter import StringVar, ttk, messagebox
import os
import datetime
import time
import pygame
import threading


# ローマ字変換辞書
romaji_dict = {
    'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お',
    'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ',
    'sa': 'さ', 'si': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ',
    'ta': 'た', 'ti': 'ち', 'tu': 'つ', 'te': 'て', 'to': 'と', 'xtu': 'っ',
    'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の',
    'ha': 'は', 'hi': 'ひ', 'fu': 'ふ', 'he': 'へ', 'ho': 'ほ',
    'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も',
    'ya': 'や', 'yu': 'ゆ', 'yo': 'よ', 'wa': 'わ', 'wo': 'を', 'nn': 'ん',
    'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ',
    'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご',
    'za': 'ざ', 'zi': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ',
    'da': 'だ', 'di': 'ぢ', 'du': 'づ', 'de': 'で', 'do': 'ど',
    'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ',
    'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ',
    'xya': 'ゃ', 'xyu': 'ゅ', 'xyo': 'ょ',
    'xa': 'ぁ', 'xi': 'ぃ', 'xu': 'ぅ', 'xe': 'ぇ', 'xo': 'ぉ', '-': 'ー'
}


typings = []
start_time = None


# pygameのミキサーの初期化はプログラムの開始時に一度だけ行う
pygame.mixer.init()


class FileManager:
    """ CSVファイルを読み込んで問題を管理するクラス """
    def __init__(self, filepath):
        self.filepath = filepath
        self.questions = self.load_questions()


    def load_questions(self):
        """ CSVファイルから問題を読み込む """
        questions = []
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # 空行を無視
                    questions.append(row[0])
        return questions



class TypingLogic:
    """ タイピングロジックを管理するクラス """
    def __init__(self, question):
        global romaji_dict
        global typings
        self.question = question
        self.current_index = 0  # 現在タイプされている文字の位置
        self.romaji_dict = romaji_dict
        self.start_index = len(typings)  # 新しい変数を追加
        self.last_key_time = start_time
        self.miss_count = 0


    def update_current_index(self, input_text):
        global typings
        global start_time

        missFlag = False

        """ 入力されたテキストに基づいてcurrent_indexを更新し、ひらがなの誤入力を削除 """
        i_text = self.convert_romaji_to_hiragana(input_text)
        new_input_text = ''

        # ひらがなのみの場合
        if self.is_hiragana_only(i_text):
            current_time = time.time()
            # 正しい入力が続いているかどうか確認

            # タイムスタンプを4桁の小数点で記録
            elapsed_time = round(current_time - start_time, 4)

            # 最初の誤りが見つかった時点でループを終了
            #print(i_text)
            for i in range(min(len(i_text), len(self.question))):
                if i_text[i] != self.question[i]:
                    # ミスしたひらがなを記録
                    mistake = ["miss", i_text[i], elapsed_time]
                    typings.append(mistake)
                    play_mp3(0)
                    missFlag = True
                    self.miss_count += 1
                    break
                new_input_text += i_text[i]
                self.current_index = i + 1

                print(self.current_index)

            if not missFlag:
                if new_input_text and self.current_index + self.start_index + self.miss_count > len(typings):
                    e_t = ["ok", new_input_text[-1], elapsed_time]
                    typings.append(e_t)
                    print("ok", new_input_text[-1])

            self.last_key_time = current_time
            return new_input_text

        return i_text


    def convert_romaji_to_hiragana(self, romaji_input):
        """ ローマ字入力をひらがなに変換する関数 """
        hiragana_output = ""
        i = 0
        while i < len(romaji_input):
            # 最大3文字分のローマ字をチェックして変換
            for length in range(3, 0, -1):
                if i + length > len(romaji_input):
                    continue  # 入力の長さを超える場合はスキップ
                romaji_chunk = romaji_input[i:i + length]
                if romaji_chunk in self.romaji_dict:
                    hiragana_output += self.romaji_dict[romaji_chunk]
                    i += length
                    break
            else:
                # 変換できない場合はそのまま残す
                hiragana_output += romaji_input[i]
                i += 1
        return hiragana_output


    def is_hiragana_only(self, text):
        """ テキストがひらがなのみで構成されているかどうかを判定する """
        return all('ぁ' <= char <= 'ん' or char == 'ー' for char in text)



class TypingApp:
    """ タイピング練習アプリのメインクラス """

    def __init__(self, selected_file, username):
        self.root = tk.Tk()
        set_center_window(self.root, 1200, 200)
        self.username = username
        self.file_manager = FileManager(f"questions/{selected_file}")
        self.is_first_question = True  # 最初の問題かどうかを追跡するフラグ
        self.setup_ui()


    def setup_ui(self):
        """ UIのセットアップ """
        self.root.title("タイピング練習")

        # 問題文の表示
        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 40), bg="white", width=60, wraplength=1200)
        self.question_label.pack(pady=20)

        # 入力ボックス
        self.input_var = StringVar()
        self.input_box = tk.Entry(self.root, textvariable=self.input_var, font=("Helvetica", 16), width=50)
        self.input_box.pack()
        self.input_box.bind("<KeyRelease>", self.on_key_release)

        # 残り問題数の表示
        self.remaining_questions_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.remaining_questions_label.pack()

        # 問題の読み込みと表示
        self.load_new_question()


    def load_new_question(self):
        """ 新しい問題を読み込み、表示を更新 """
        if hasattr(self, 'file_manager') and self.file_manager.questions:
            if self.is_first_question:
                # 最初の問題の場合のみカウントダウン
                self.countdown_before_start()
                self.is_first_question = False

            question = self.file_manager.questions.pop(0)
            self.typing_logic = TypingLogic(question)
            self.question_label.config(text=question)
            self.input_var.set('')

            # 残り問題数の更新
            remaining = len(self.file_manager.questions)
            self.remaining_questions_label.config(text=f"残り問題数: {remaining}")

            # Input boxにフォーカスを設定
            self.input_box.focus_set()

        else:
            # 全ての問題が終わった後の処理
            self.remaining_questions_label.config(text="")
            self.save_results()
            self.root.destroy()  # 練習ウィンドウを閉じる
            messagebox.showinfo("完了", "問題は以上です。")  # メッセージボックスを表示


    def countdown_before_start(self):
        """ ゲーム開始前のカウントダウン """
        global start_time
        for i in range(5, 0, -1):
            self.question_label.config(text=str(i))
            self.root.update()
            time.sleep(1)

        start_time = time.time()


    def on_key_release(self, event):
        """ キーリリースイベント """
        input_text = self.input_var.get()
        processed_text = self.typing_logic.update_current_index(input_text)
        self.input_var.set(processed_text)  # 更新されたテキストを入力ボックスに設定
        self.update_display(processed_text)

        # 問題が完全にタイプされた場合、次の問題に進む
        if self.typing_logic.current_index == len(self.typing_logic.question):
            self.load_new_question()


    def update_display(self, input_text):
        """ 表示を更新 """
        question = self.typing_logic.question
        current_index = self.typing_logic.current_index
        displayed_text = question[:current_index] + '\u0336'.join(question[current_index:] + ' ')
        self.question_label.config(text=displayed_text)


    def get_question_files(self):
        """ 'questions' ディレクトリ内のファイル名をリストアップする """
        directory = "questions"
        return os.listdir(directory)


    def load_selected_file(self):
        """ 選択されたファイルから問題を読み込む """
        selected_file = self.file_var.get()
        filepath = f"questions/{selected_file}"
        self.file_manager = FileManager(filepath)
        self.load_new_question()


    def save_results(self):
        global typings
        global start_time

        end_time = time.time()
        total_time = end_time - start_time

        print(typings)

        # インターバル計算
        for i in range(len(typings)):
            if i == 0:
                typings[i].append(0)
            else:
                interval = round(typings[i][2] - typings[i-1][2], 4)
                typings[i].append(interval)

        # char毎CPM計算
        correct_count = 0
        error_count = 0
        for i in range(len(typings)):
            if typings[i][0] == "ok":
                correct_count += 1
                cpm = round(60 / typings[i][2] * correct_count, 2)
                typings[i].append(cpm)
            else:
                error_count += 1

        # 総合CPM計算
        cpm = round(60 / total_time * correct_count, 2)

        # トータルエラー率
        toe = round(error_count/correct_count*100, 2)

        results_dir = f"results/{self.username}"
        os.makedirs(results_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

        filename = f"{results_dir}/{datetime.datetime.now().strftime('%Y-%m-%d-%H%M')}_{self.file_manager.filepath.split('/')[-1]}_{self.username}.csv"
        with open(filename, 'w', newline='', encoding='utf_8_sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["result", "Character", "Time Elapsed", "Interval", f"CPM={cpm}", f"={toe}%"])
            #print(typings)
            if typings:
                for typing in typings:
                    writer.writerow(list(typing))

        sys.exit()


""""ファイル選択ウィンドウ関数"""
def select_file_window():
    def on_select():
        selected_file = file_var.get()
        username = username_var.get()
        if not username:
            # ユーザーネームが入力されていない場合は警告を表示
            tk.messagebox.showwarning("警告", "ユーザーネームを入力してください。")
            return
        file_select_window.destroy()
        app = TypingApp(selected_file, username)
        app.root.mainloop()

    file_select_window = tk.Tk()
    file_select_window.title("ファイルを選択")

    set_center_window(file_select_window, 300, 150)

    file_var = StringVar(file_select_window)
    file_dropdown = ttk.OptionMenu(file_select_window, file_var, '選択してください', *get_question_files())
    file_dropdown.pack(pady=10)

    username_var = StringVar(file_select_window)
    username_entry = tk.Entry(file_select_window, textvariable=username_var)
    username_entry.pack(pady=10)

    select_button = tk.Button(file_select_window, text="決定", command=on_select)
    select_button.pack(pady=5)

    file_select_window.mainloop()


def get_question_files():
    directory = "questions"
    return os.listdir(directory)


def set_center_window(root, width=350, height=250):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height / 4 - 100)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y)) # 渡されたオブジェクトのジオメトリーに設定


def play_mp3(i):
    """
    リスト内のMP3ファイルを非同期で再生

    :param i: 再生するMP3ファイルのインデックス。
    """

    def play_sound():
        mp3_list = ["resource/sounds/buzzer.mp3"]
        mp3 = mp3_list[i]
        try:
            # MP3ファイルをロード
            pygame.mixer.music.load(mp3)
            # MP3ファイルを再生
            pygame.mixer.music.play()
        except Exception as e:
            print(f"{mp3}の再生中にエラーが発生しました: {e}")

    # 音楽の再生を別スレッドで実行
    thread = threading.Thread(target=play_sound)
    thread.start()


select_file_window()

