import numpy as np
area={}

# /////////////////////////////grid created//////////////////////////////////////////////////

def create_grid(are,lev,col,row):
    global area
    if(are not in area):
        shape = (lev, col, row)
        myList = [[[{'val':0,'id':'','below_container_export_days':0} for r in range(row)] for c in range(col)]for l in range(lev)]   
        area[are] = {'shape':myList,'container_type':' ','size':row*col*lev,'full':False}
        print('grid created!')
    else:
        print('Area already present!')



# /////////////////////////////grid created//////////////////////////////////////////////////
# /////////////////////////////Finding and placing container/////////////////////////////////
def placement(id,container_type,container_return_days):
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
        placement(id,container_type,container_return_days)
        return 0
    else:
       insert_into_yard(id,container_type,container_return_days)

def insert_into_yard(id,container_type,container_return_days):
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
                            if(area[port_area]['shape'][lev][col][row]['val']>=container_return_days and area[port_area]['shape'][lev+1][col][row]['below_container_export_days']>=area[port_area]['shape'][lev][col][row]['val']):
                                i=0
                                flag=True
                                for level in range(shapee[0]-1):
                                    # print(area[port_area]['shape'][level][col][row]['val'])
                                    if(area[port_area]['shape'][level][col][row]['val']==0):
                                        i=level
                                        flag=False
                                        break
                                else:
                                    pass
                                if(flag==False):
                                    final_placement=(i,col,row)
                                    zero_flag=True

                            elif(area[port_area]['shape'][lev][col][row]['val']==0 and zero_flag==False):
                                # print('idharr:',lev,col,row,area[port_area]['shape'][lev][col][row]['val'],zero_flag)
                                final_placement=(lev,col,row)
                                zero_flag=True
                            elif(area[port_area]['shape'][lev][col][row]['val']<container_return_days):
                                pass
            if(final_placement==''):
                area[port_area]['full']=True
                insert_into_yard(id,container_type,container_return_days)
                return 0
            else:
                area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['val']=container_return_days
                area[port_area]['shape'][final_placement[0]][final_placement[1]][final_placement[2]]['id']=id
                area[port_area]['shape'][final_placement[0]+1][final_placement[1]][final_placement[2]]['below_container_export_days']=container_return_days
                return 0
            
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
                    print('days:',area[i]['shape'][lev][col][row]['val'],'id:',area[i]['shape'][lev][col][row]['id'],end=', ')
                print()
            print()
# /////////////////////////////Displaying our array or containers ends////////////////////////////

#       name,level,col,row
create_grid('A',4,4,6)
display()
placement('001','Empty',5)
display()
placement('002','Empty',4)
display()
placement('003','Empty',3)
display()
placement('004','Empty',5)
display()
placement('005','Empty',5)
display()
placement('006','Empty',6)
display()
placement('007','Empty',7)
display()
placement('008','Empty',8)
display()
placement('009','Empty',9)
display()
placement('010','Empty',10)
display()
