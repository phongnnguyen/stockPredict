import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks,peak_widths,find_peaks_cwt
data = pd.read_csv('vnindex.csv',names=['Ticker','Date','Open','High','Low','Close','Volume'],skiprows=1)
data=data.loc[data['Ticker']=='VNINDEX']
vnindex_data = data.iloc[::-1]
vnindex_data.reset_index(inplace=True)
final_data=vnindex_data.reset_index(inplace=False)
final_data.drop(['index'],axis=1)
# Add all ta features filling nans values
close = final_data['Close']
peaks,_ = find_peaks(close,height=1000)
plt.plot(close)
plt.plot(peaks, close[peaks], "x")