import numpy as np

a = np.array([[1.2, 3.4, 5.6],
              [7.8, 9.0, 1.2]])

np.savetxt("data.csv", a, delimiter=",")
print("配列を保存しました。")

b = np.loadtxt("data.csv", delimiter=",")
print(b)
print("配列を読み込みました。")