# /////////////////////////////Predicting Outtime on bases of Intime,Container size and status////////////////////////////
import os
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def Predict_Out_Time(Time,size,state):
    df = pd.read_csv('Past In and Out.csv')

    def hr_diff(time1, time2):
        date_time1 = datetime.strptime(time1, "%d-%m-%y %H:%M:%S")
        date_time2 = datetime.strptime(time2, "%d-%m-%y %H:%M:%S")
        diff = date_time2 - date_time1
        difference_in_hours = int(diff.total_seconds() / 3600)
        return difference_in_hours
    def strdate_to_timestamp(date):
        date_time = datetime.strptime(date, "%d-%m-%y %H:%M:%S")
        return int(date_time.timestamp())


    IN_Time=[]
    OUT_Time=[]
    for i in range(df.shape[0]):
        IN_Time.append(strdate_to_timestamp(df['IN_TIME'][i]))
        OUT_Time.append(strdate_to_timestamp(df['OUT_TIME'][i]))
    In = pd.DataFrame(IN_Time)
    Out = pd.DataFrame(OUT_Time)
    df.drop(columns='REF_ID', axis=1, inplace=True)
    df.drop(columns='VALIDITY', axis=1, inplace=True)
    df.drop(columns='CON_NUM', axis=1, inplace=True)
    df["In_Time"] = In
    df["Out_Time"] = Out
    df.dropna(axis=0, inplace=True)
    df.reset_index(inplace=True)
   
    df1 = pd.get_dummies(data=df['STATUS'], drop_first=True)
    df1 = df1.astype(int)
    df['L'] = df1
    
    df.drop(columns='STATUS',axis=1,inplace=True)
    df.drop(columns='index',axis=1,inplace=True)
    
    Time_diff = []
    for i in range(df.shape[0]):
        Time_diff.append(hr_diff(df["IN_TIME"][i],df["OUT_TIME"][i]))
    
    df["Time_Diff"] = Time_diff
    def find_outliers(df,col):
        q1=df[col].quantile(0.25)
        q3=df[col].quantile(0.75)
        IQR=q3-q1
        lv=q1-1.5*IQR
        hv=q3+1.5*IQR
        df=df[(df[col]<=hv) | (df[col]>=lv)]
        return df
    find_outliers(df,'Time_Diff')

    df.drop(columns='IN_TIME',axis=1,inplace=True)
    df.drop(columns='OUT_TIME',axis=1,inplace=True)
    df.drop(columns='Time_Diff',axis=1,inplace=True)

    x=df.drop(columns='Out_Time')
    y=df['Out_Time']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)

    x = Time
    x1 = datetime.strptime(x, '%d-%m-%y %H:%M:%S')
    x1m=x1.timestamp()
    Out = [[size, int(x1m), state]]
    x1=lr.predict(Out)
    Outtime = datetime.fromtimestamp(int(x1)).strftime("%d-%m-%Y %H:%M:%S")
    return Outtime




area={}

def strdate_to_timestamp(date):
    date_time = datetime.strptime(date, "%d-%m-%y %H:%M:%S")
    return int(date_time.timestamp())

# /////////////////////////////grid created//////////////////////////////////////////////////

def create_grid(are,lev,col,row):
    global area
    if(are not in area):
        shape = (lev, col, row)
        myList = [[[{'val':0,'id':'','below_container_export_days':0,'container_size':0} for r in range(row)] for c in range(col)]for l in range(lev)]   
        area[are] = {'shape':myList,'container_type':' ','size':row*col*lev,'full':False}

        print('grid created!')
    else:
        print('Area already present!')


print(area)
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
                            if (container_size==20):
                                if(lev!=shapee[0]-1 and (area[port_area]['shape'][lev][col][row]['container_size']==0 or area[port_area]['shape'][lev][col][row]['container_size']==20)):
                                    if(area[port_area]['shape'][lev][col][row]['val']>=container_return_days and area[port_area]['shape'][lev+1][col][row]['below_container_export_days']>=area[port_area]['shape'][lev][col][row]['val']):
                                        i=0
                                        flag=True
                                        for level in range(shapee[0]):
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

display()
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

for i in dict:
#              name         level             col              row
    create_grid(i,dict[i]['maxlev'],dict[i]['maxcol'],dict[i]['maxrow'])
print(dict)

df = pd.read_csv('Insert data.csv')
output_df = pd.DataFrame(columns=["ID", "IN_TIME","REF_ID","CON_NUM","CON_SIZE", "STATUS", "Out_Time","Location"])

OutTime=[]
list=[]
s=0
for i in range(3):
    if df['STATUS'][i] == 'L':
        s=1
    else:
        s=0
    pre = Predict_Out_Time(df['IN_TIME'][i],df['CON_SIZE'][i],s)
    x1 = pre
    D = datetime.strptime(x1, "%d-%m-%Y %H:%M:%S")
    d = D.timestamp()
    placement(str(df['CON_NUM'][i]),str(df['STATUS'][i]),int(d),int(df['CON_SIZE'][i]))
    print(i,'Number of set inserted!!')
    data = {'ID':df['ID'][i],'IN_TIME':df['IN_TIME'][i],'REF_ID':df['REF_ID'][i],'CON_NUM':df['CON_NUM'][i],'CON_SIZE':df['CON_SIZE'][i],'STATUS':df['STATUS'][i],'Out_Time':pre}
    output_df = output_df._append(data,ignore_index=True)

output_df['Location']=list
if not os.path.isfile('Result.csv'):
    output_df.to_csv('Result.csv',index=False)
else:
    os.remove('Result.csv')
    output_df.to_csv('Result.csv',index=False)

print(area)

# display()
# ///////////////////////////////////some examples for entry of containers ends//////////////////////////////

# basic description:
#  by running the code you will see placement of some containers.
#  if size is 40 than 2 index is filled for one container while for 20 only 1 index is filled
#  display will be as follows: Name of area-->info of area-->level(height index)-->row and col(row and col index)|
#                                                          /\                                                    |
#                                                          |                                                     \/
#                                                          |<-----------------------------------------------------
