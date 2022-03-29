# DMAI-HW1-Operating-Reserve-Prediction

## OVERVIEW
In this HW, we will implement an algorithm to predict the operating reserve (備轉容量) of electrical power. Given a time series electricity data to predict the value of the operating reserve value of each day during 2022/03/30 ~ 2022/04/13. 


## 資料集
使用的資料集是來自台電所提供的:
1.本年度每日尖峰備轉容量率("https://data.gov.tw/dataset/25850")
2.近三年每日尖峰備轉容量率("https://data.gov.tw/dataset/24945")
3.過去電力供需資訊("https://data.gov.tw/dataset/19995")。

## 資料前處理
將檔案讀取後，將格式統一並進行合併，去除掉不需要的欄位，透過關係圖得知，每年夏季跟春秋季的備轉容量有顯著差異，而我們要預測3/30-4/13的台電備轉容量，因此我只使用了2019-2022年中每年的1-4月做模型的訓練。

## 程式執行
有測試過的模型包含LSTM、ARIMA、以及Prophet 三種模型，LSTM以及ARIMA經測試後的效果不佳，因此最後採用FACEBOOK所開發的Prophet model作為訓練模型，程式直接執行hw1_Prophet.ipynb即可，結果會輸出到answer.csv。
