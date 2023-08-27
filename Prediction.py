import numpy
import pandas as pd
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def Predict_Out_Time(Time,size,state):
    df = pd.read_csv('Past In and Out.csv')

    def Milli(X):
        given_date_time = X
        epoch = datetime(1970, 1, 1)
        time_difference = given_date_time - epoch
        total_seconds = time_difference.total_seconds()
        milliseconds = int(total_seconds * 1000)
        return milliseconds

    def Date_Time(X):
        seconds = X / 1000
        date_time = datetime.fromtimestamp(seconds)
        date_time1= date_time.strftime('%d-%m-%y %H:%M:%S')
        return date_time1

    IN_Time = []
    OUT_Time = []
    for i in range(df.shape[0]):
        x1 = datetime.strptime(df['IN_TIME'][i], '%d-%m-%y %H:%M:%S')
        x1m = Milli(x1)
        IN_Time.append(x1m)
        y1 = datetime.strptime(df['OUT_TIME'][i], '%d-%m-%y %H:%M:%S')
        y1m = Milli(y1)
        IN_Time.append(x1m)
        OUT_Time.append(y1m)
    In = pd.DataFrame(IN_Time)
    Out = pd.DataFrame(OUT_Time)
    df.drop(columns='REF_ID', axis=1, inplace=True)
    df.drop(columns='VALIDITY', axis=1, inplace=True)
    df.drop(columns='CON_NUM', axis=1, inplace=True)
    df.drop(columns='IN_TIME', axis=1, inplace=True)
    df.drop(columns='OUT_TIME', axis=1, inplace=True)
    df['In_time'] = In
    df['Out_time'] = Out
    df.dropna(axis=0, inplace=True)
    df.reset_index(inplace=True)
    df1 = pd.get_dummies(data=df['STATUS'], drop_first=True)
    df['L'] = df1
    df.drop(['STATUS'], axis=1, inplace=True)
    df.drop(columns='index',axis=1,inplace=True)
    Time_diff = []
    for i in range(df.shape[0]):
        Time_diff.append(df['Out_time'][i]-df['In_time'][i])
        
    df['Time_Diff'] = Time_diff
    def find_outliers(df,col):
        q1=df[col].quantile(0.25)
        q3=df[col].quantile(0.75)
        IQR=q3-q1
        lv=q1-1.5*IQR
        hv=q3+1.5*IQR
        df=df[(df[col]<=hv) | (df[col]>=lv)]
        return df
    find_outliers(df,'Time_Diff')
    df.drop(columns='Time_Diff',axis=1,inplace=True)
    x = df.drop('Out_time', axis=1)
    y = df['Out_time']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    # print(x_train.shape)
    # print(x_test.shape)
    # print(y_train.shape)
    # print(y_test.shape)
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    # print(lr.coef_)
    # print(lr.intercept_)
    y_pred = lr.predict(x_test)
    # print(y_pred)
    # print(y_test)
    mse = mean_squared_error(y_pred, y_test)
    # mse
    df = pd.read_csv('Insert data.csv')
    x = Time
    x1 = datetime.strptime(x, '%d-%m-%y %H:%M:%S')
    x1m = Milli(x1)
    Out = [[size, x1m, state]]
    x1=lr.predict(Out)
    Outtime = datetime.strptime(Date_Time(int(x1)),'%d-%m-%y %H:%M:%S')
    return Outtime


pre = Predict_Out_Time('14-03-22 15:46:44',20,1)
print(pre)
