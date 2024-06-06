
import csv
import tkinter as tk
from tkinter import filedialog



def read_csv_to_list(file_path):
    data_list = []
    with open(file_path, mode='r', encoding='utf-8_sig', newline='') as csvfile:  # UTF-8でエンコーディング指定
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            data_list.append(row)
    return data_list



def select_file_and_read():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しない
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:  # ファイルが選択された場合
        data = read_csv_to_list(file_path)
        print(data)
        main(data)
    root.destroy()



def main(datas):
    miss = 0
    ok = 0
    for d in datas:
        if d[0] == "miss":
            miss += 1
        else:
            ok += 1
    print("miss数=", miss, ", ok数=", ok, ", TOE=", round(miss/(ok+miss), 4))



# 例: 'example.csv' というファイルを読み込む
select_file_and_read()