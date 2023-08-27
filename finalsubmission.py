# /////////////////////////////Predicting Outtime on bases of Intime,Container size and status////////////////////////////

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
    x = Time
    x1 = datetime.strptime(x, '%d-%m-%y %H:%M:%S')
    x1m = Milli(x1)
    Out = [[size, x1m, state]]
    x1=lr.predict(Out)
    Outtime = datetime.strptime(Date_Time(int(x1)),'%d-%m-%y %H:%M:%S')
    return Outtime


# ////////////////////////////////////////////Adding Outtime data in Csv////////////////////////////////////////


# df = pd.read_csv('Insert data.csv')
# OutTime=[]
# s=0
# for i in range(df.shape[0]):
#     if df['STATUS'][i] == 'L':
#         s=1
#     else:
#         s=0
#     pre = Predict_Out_Time(df['IN_TIME'][i],df['CON_SIZE'][i],s)
#     OutTime.append(pre)
# df['Out_Time'] = OutTime


area={}

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
    date_time1= date_time.strftime('%d-%m-%Y %H:%M:%S')
    return date_time1
# /////////////////////////////grid created//////////////////////////////////////////////////

def create_grid(are,lev,col,row):
    global area
    if(are not in area):
        shape = (lev, col, row)
        #       val=how many days for exporting container       
        myList = [[[{'val':0,'id':'','below_container_export_days':0,'container_size':0} for r in range(row)] for c in range(col)]for l in range(lev)]   
        area[are] = {'shape':myList,'container_type':' ','size':row*col*lev,'full':False}
        print('grid created!')
    else:
        print('Area already present!')



# /////////////////////////////grid created//////////////////////////////////////////////////
# /////////////////////////////Finding and placing container/////////////////////////////////
def placement(id,container_type,container_return_days,container_size):
    global area
    newinsert=True
    for i in area:
        if(container_type==area[i]['container_type']):
            newinsert=False
    
    if(newinsert==True):
        maxavailableareasize=0
        maxavailablearea=''
        is_space_available_flag=False
        for i in area:
            if area[i]['container_type']==' ' and area[i]['size']>maxavailableareasize :
                maxavailableareasize=area[i]['size']
                maxavailablearea=i
                is_space_available_flag=True
        if(is_space_available_flag==False):
            print('no more space left')
            return 0
        area[maxavailablearea]['container_type']=container_type
        placement(id,container_type,container_return_days,container_size)
        return 0
    else:
        insert_into_yard(id,container_type,container_return_days,container_size)

#///////////////////////////////insertion logic///////////////////////////////////////////////// 

def insert_into_yard(id,container_type,container_return_days,container_size):
            global area
            port_area=''
            for i in area:
                if(area[i]['container_type']==container_type and area[i]['full']==False):
                    port_area=i
                    break
            shapee=np.shape(area[port_area]['shape'])
            final_placement=''
            zero_flag=False
            for lev in range(shapee[0]):
                for col in range(shapee[1]):
                    for row in range(shapee[2]):
                            # if(lev!=3):
                                # print(lev,col,row,'below:',area[port_area]['shape'][lev+1][col][row]['below_container_export_days'],area[port_area]['shape'][lev][col][row]['val'])
                            # code for placement of size 20 container
                            if (container_size==20):
                                if(lev!=shapee[0]-1 and (area[port_area]['shape'][lev][col][row]['container_size']==0 or area[port_area]['shape'][lev][col][row]['container_size']==20)):
#                                     if(lev!=3):
#                                         print('idharhe::',lev,col,row,area[port_area]['shape'][lev][col][row]['val'],'=',container_return_days,area[port_area]['shape'][lev+1][col][row]['below_container_export_days'],'=',area[port_area]['shape'][lev][col][row]['val'],zero_flag)
                                    if(area[port_area]['shape'][lev][col][row]['val']>=container_return_days and area[port_area]['shape'][lev+1][col][row]['below_container_export_days']>=area[port_area]['shape'][lev][col][row]['val']):
                                        i=0
                                        flag=True
                                        for level in range(shapee[0]):
                                            # print(area[port_area]['shape'][level][col][row]['val'])
                                            if(area[port_area]['shape'][level][col][row]['val']==0):
                                                i=level
                                                flag=False
                                                break
                                        if(flag==False):
                                            final_placement=(i,col,row)
                                            zero_flag=True
                                    elif(area[port_area]['shape'][lev][col][row]['val']==0 and zero_flag==False):
                                        # print('idharr:',lev,col,row,area[port_area]['shape'][lev][col][row]['val'],zero_flag)
                                        final_placement=(lev,col,row)
                                        zero_flag=True
                                    elif(area[port_area]['shape'][lev][col][row]['val']<container_return_days):
                                        pass
                            # code for placement of size 40 container
                            else:
                                if(lev!=shapee[0]-1 and ((area[port_area]['shape'][lev][col][row]['container_size']==0 and row!=shapee[2]-1) or (area[port_area]['shape'][lev][col][row]['container_size']==40 and row!=shapee[2]-1))):  
                                    if(area[port_area]['shape'][lev][col][row]['val']>=container_return_days and area[port_area]['shape'][lev][col][row+1]['val']>=container_return_days and area[port_area]['shape'][lev+1][col][row]['below_container_export_days']>=area[port_area]['shape'][lev][col][row]['val'] and area[port_area]['shape'][lev+1][col][row+1]['below_container_export_days']>=area[port_area]['shape'][lev][col][row+1]['val']):
                                        i=0
                                        flag=True
                                        for level in range(shapee[0]):
                                            # print(area[port_area]['shape'][level][col][row]['val'])
                                            if(area[port_area]['shape'][level][col][row]['val']==0 and area[port_area]['shape'][level][col][row+1]['val']==0):
                                                i=level
                                                flag=False
                                                break
                                        if(flag==False):
                                            final_placement=(i,col,row)
                                            zero_flag=True
                                    elif(area[port_area]['shape'][lev][col][row]['val']==0 and area[port_area]['shape'][lev][col][row+1]['val']==0 and zero_flag==False):
                                            # print('idharr:',lev,col,row,area[port_area]['shape'][lev][col][row]['val'],zero_flag)
                                            final_placement=(lev,col,row)
                                            zero_flag=True
                                    elif(area[port_area]['shape'][lev][col][row]['val']<container_return_days):
                                        pass
            if(final_placement==''):
                area[port_area]['full']=True
                placement(id,container_type,container_return_days,container_size)
                return 0
            else:
                if (container_size==20 and final_placement[0]+1!=shapee[0]):
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['id']=id
                    area[port_area]['shape'][final_placement[0]+1][final_placement[1]][final_placement[2]]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['container_size']=container_size
                elif (container_size==20 and final_placement[0]==shapee[0]-1):
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['id']=id
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['container_size']=container_size
                elif(container_size==40 and final_placement[0]+1!=shapee[0]):
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['id']=id
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['id']=id
                    area[port_area]['shape'][final_placement[0]+1][final_placement[1]][final_placement[2]]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]+1][final_placement[1]][final_placement[2]+1]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['container_size']=container_size
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['container_size']=container_size
                else:
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['id']=id
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['id']=id
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['container_size']=container_size
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]+1]['container_size']=container_size
                if(container_size==20 and len(str(final_placement[2]))==1):
                    list.append(str(port_area)+'0'+str(final_placement[2])+str(final_placement[1])+str(final_placement[0]))
                elif(container_size==20 and len(str(final_placement[2]))!=1):
                    list.append(str(port_area)+str(final_placement[2])+str(final_placement[1])+str(final_placement[0]))
                elif(container_size==40 and (len(str(final_placement[2]))==1 or final_placement[2]<9)):
                    list.append(str(port_area)+'0'+str(final_placement[2]+1)+str(final_placement[1])+str(final_placement[0]))
                else:
                    list.append(str(port_area)+str(final_placement[2]+1)+str(final_placement[1])+str(final_placement[0]))
                    
#///////////////////////////////insertion logic ends////////////////////////////////////////// 
# /////////////////////////////Finding and placing container ends////////////////////////////
# /////////////////////////////Displaying our array or containers////////////////////////////
def display():
    for i in area:
        print(i)
        print('container_type:',area[i]['container_type'],'size:',area[i]['size'],'full:',area[i]['full'])
        print()
        shapee=np.shape(area[i]['shape'])
        for lev in range(shapee[0]):
            print('Level',lev+1)
            for col in range(shapee[1]):
                for row in range(shapee[2]):
                    print('days:',area[i]['shape'][lev][col][row]['val'],' id:',area[i]['shape'][lev][col][row]['id'],' container size:',area[i]['shape'][lev][col][row]['container_size'],end=', ')
                print()
            print()
# /////////////////////////////Displaying our array or containers ends////////////////////////////
# ////////////////////////////////////////////creating grid/////////////////////////////////////////////

data = pd.read_csv("Yard locations.csv")
dict={}
loc = data['Location']
for i in loc:
    areaaa = i[0:1]
    row = int(i[1:3])
    col = ord(str(i[3:4]))-64
    lev = int(i[4:5])

    if (areaaa not in dict.keys()):
        dict[areaaa] = {'maxrow': row,'maxcol': col,'maxlev':lev}
    else:
        if (dict[areaaa]['maxrow'] < row):
            dict[areaaa]['maxrow'] = row
        if (dict[areaaa]['maxcol'] < col):
            dict[areaaa]['maxcol'] = col
        if (dict[areaaa]['maxlev'] < lev):
            dict[areaaa]['maxlev'] = lev

# create_grid('A',4,4,6)
# create_grid('B',4,4,6)
# display()
for i in dict:
#              name,  level  ,    col    ,    row
    create_grid(i,dict[i]['maxlev'],dict[i]['maxcol'],dict[i]['maxrow'])

df = pd.read_csv('Predicted_Data.csv')
list=[]
for i in range(df.shape[0]):
    x1 = datetime.strptime(df['Out_Time'][i], '%Y-%m-%d %H:%M:%S')
    D=Milli(x1)
    placement(str(df['CON_NUM'][i]),str(df['STATUS'][i]),int(D),int(df['CON_SIZE'][i]))
    print(i,'Number of set inserted!!')
display()

# x1 = datetime.strptime(df['Out_Time'][0],'%Y-%m-%d %H:%M:%S')
# D=Milli(x1)
# placement(str(df['CON_NUM'][0]),str(df['STATUS'][0]),int(D),int(df['CON_SIZE'][0]))
# x1 = datetime.strptime(df['Out_Time'][3],'%Y-%m-%d %H:%M:%S')
# D=Milli(x1)
# placement(str(df['CON_NUM'][3]),str(df['STATUS'][3]),int(D),int(df['CON_SIZE'][3]))
# print(list)

# placement('001','Empty',5,20)

# display()
# ///////////////////////////////////some examples for entry of containers ends//////////////////////////////

# basic description:
#  by running the code you will see placement of some containers.
#  if size is 40 than 2 index is filled for one container while for 20 only 1 index is filled
#  display will be as follows: Name of area-->info of area-->level(height index)-->row and col(row and col index)|
#                                                          /\                                                    |
#                                                          |                                                     \/
#                                                          |<-----------------------------------------------------
