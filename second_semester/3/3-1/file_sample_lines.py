# -*- coding: utf-8 -*-

# 複数行をファイルに書き込む関数
def file_write_lines(lines, path):
    # ファイルを「新規書き込み」モードで開く（UTF-8）
    with open(path, "w", encoding="utf-8", newline="\n") as file:
        for line in lines:
            file.write(line + "\n")  # 各行をファイルに書き込む
    print(f"ファイル '{path}' にデータを書き込みました。")

# 複数行をファイルから読み込む関数
def file_read_lines(path):
    # ファイルを「読み取り」モードで開く（UTF-8）
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()  # 各行をリストとして取得
    lines = [line.strip() for line in lines]  # 改行などを除去
    print(f"ファイル '{path}' から読み込んだデータ:\n{lines}")
    return lines

# メインプログラム
if __name__ == "__main__":
    # 保存先ファイル
    file_path = "text_example.txt"
    data_to_write = []

    print("保存したい複数行のテキストを入力してください（空行で終了）:")
    while True:
        line = input()  # 入力を受け取る
        if line == "":  # 空行で終了
            break
        data_to_write.append(line)  # 入力行を追加

    # 入力内容を書き込み
    file_write_lines(data_to_write, file_path)

    
    # 読み込みテスト
    data_read = file_read_lines(file_path)
    print("読み込んだデータ:")
    for line in data_read:
        print(line)
    

