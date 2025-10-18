###8-1

#1．センサの取得値を温度に変換 
#　	以下の計算を追加し，取得値valueを温度c_temiperatureに変換する

①
volt = (r_termistorを使った式) #取得値を電圧値に変換する式
r_thermistor = (voltを使った式) #抵抗値の計算[Ω]:分圧の法則 
abs_temperature = （r_thermistorを使った式） #絶対温度の計算[Ｋ]: Ｂ定数の式
c_temperature = abs_temperature - 273.15 #セ氏温度の計算[℃]

#2．下の３つの処理をプログラムに追加する
①
HEATER = 21#ピン番号の指定（好きなピンを使ってよい）

②
GPIO.output(HEATER,GPIO.HIGH)#ヒーターをオンにする処理を最初に追加する．

③
finally:
	GPIO.output(HEATER,GPIO.HIGH)#ヒーターをオンにする処理をfinallyの中に追加する


###8-2

#3．そのままadc_data_save.pyを使う
#グラフの軸ラベルをvaluesからtemperatureに変更してもよい

#4．移動平均法を以下の配列にデータを保存することで実現する
①
temperatures = [0,0,0,0,0]#初期化の時に配列を用意しておく

②
temperatures[4]=temperatures[3]
temperatures[3]=temperatures[2]
temperatures[2]=temperatures[1]
temperatures[1]=temperatures[0]
temperatures[0]=c_temperature
ave_temps = sum(temperatures)/5
#これで，valueと同じようにave_tempsを扱える
