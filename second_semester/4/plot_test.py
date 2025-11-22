# matplotlib のインポート
import matplotlib.pyplot as plt

# プロットする点の定義
X = [1,2,3]
Y = [1,1,2]

### 折れ線グラフの表示
plt.plot(X, Y)

# ラベル設定
plt.xlabel(' label')
plt.ylabel('y label')
plt.title('pyplot interface')
# 表示
plt.show()

### オブジェクト指向インターフェースでの散布図の表示
## より複雑なグラフの描画に対応

# 1.figureオブジェクト(グラフ全体を表すオブジェクト)を生成する 
fig = plt.figure()

# 2.axesオブジェクトをfigureオブジェクトに対して設定する
ax = fig.add_subplot(1, 1, 1)

# 3.axesオブジェクトに対して散布図のメソッドを設定する
# 折れ線、棒グラフ、散布図など様々なグラフを描画可能
#ax.scatter(X, Y)  # 散布図
#ax.plot(X, Y)   # 折れ線グラフ
#ax.bar(X, Y)   # 棒グラフ
#ax.hist(Y)    # ヒストグラム
#ax.boxplot(Y) # 箱ひげ図
ax.pie(Y)     # 円グラフ

# 4.出力
# 4-1 表示
plt.show()

# 4-2 画像ファイルとして保存
# .png, .jpg, .svg など様々な形式で保存可能
plt.savefig('scatter_plot.png')
