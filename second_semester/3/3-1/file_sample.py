# -*- coding: utf-8 -*-
# ファイルに書き込むサンプル関数
def file_write(text, path):
    with open(path, "w") as file:  # ファイルを書き込みモードで開く
        file.write(text)            # ファイルにデータを書き込む
    print(f"ファイル '{path}' にデータを書き込みました。")


# ファイルから読み込むサンプル関数
def file_read(path):
    with open(path, "r") as file:   # ファイルを読み取りモードで開く
        data_read = file.read()     # ファイルからデータを読み込む
    print(f"ファイル '{path}' から読み取ったデータ:\n{data_read}")
    return data_read


if __name__ == "__main__":
    # データの保存
    data_to_write = input("保存する文字を入力してください: ")
    file_path = 'text_example.txt'
    file_write(data_to_write, file_path)

    # データの読み込み処理（コメントアウト解除で実行可能）
    # data_read = file_read(file_path)
    # print(data_read)
