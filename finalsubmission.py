import numpy as np
area={}

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
                                if(area[port_area]['shape'][lev][col][row]['container_size']==0 or area[port_area]['shape'][lev][col][row]['container_size']==20):
                                    if(lev!=3):
                                        print('idharhe::',lev,col,row,area[port_area]['shape'][lev][col][row]['val'],'=',container_return_days,area[port_area]['shape'][lev+1][col][row]['below_container_export_days'],'=',area[port_area]['shape'][lev][col][row]['val'],zero_flag)
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
                                if((area[port_area]['shape'][lev][col][row]['container_size']==0 and row!=shapee[2]-1) or (area[port_area]['shape'][lev][col][row]['container_size']==40 and row!=shapee[2]-1)):  
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
                insert_into_yard(id,container_type,container_return_days,container_size)
                return 0
            else:
                if (container_size==20 and final_placement[0]+1!=shapee[0]):
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['val']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['id']=id
                    area[port_area]['shape'][final_placement[0]+1][final_placement[1]][final_placement[2]]['below_container_export_days']=container_return_days
                    area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['container_size']=container_size
                elif (container_size==20 and final_placement[0]==shapee[0]):
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
                return 0
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

import pandas as pd
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

# to understand better uncomment 181-184 and comment 188-190 and 196-213
# for i in dict:
# #              name,  level  ,    col    ,    row
#     create_grid(i,dict[i]['maxlev'],dict[i]['maxcol'],dict[i]['maxrow'])
# display()

# example for creating manually/////////////////////
    #   name,level,col,row
create_grid('A',4,4,6)
create_grid('B',4,4,6)
display()

# ////////////////////////////////////////////creating grid ends////////////////////////////////////////

# ///////////////////////////////////some examples for entry of containers//////////////////////////////

placement('001','Empty',5,20)
display()
placement('002','Empty',4,40)
display()

placement('004','Empty',4,40)
display()
placement('003','Empty',5,20)
display()
placement('005','Empty',4,40)
display()
placement('006','Empty',4,40)
display()

placement('004','Filled',4,40)
display()
placement('003','Filled',5,20)
display()

# ///////////////////////////////////some examples for entry of containers ends//////////////////////////////

# basic description:
#  by running the code you will see placement of some containers.
#  if size is 40 than 2 index is filled for one container while for 20 only 1 index is filled
#  display will be as follows: Name of area-->info of area-->level(height index)-->row and col(row and col index)|
#                                                          /\                                                    |
#                                                          |                                                     \/
#                                                          |<-----------------------------------------------------
