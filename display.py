# this code shows how it should be displayed logic is yet to be added.


import pandas as pd
data = pd.read_csv("Yard locations.csv")
dict={}
loc = data['Location']
for i in loc:
    area = i[0:1]
    row = int(i[1:3])
    col = ord(str(i[3:4]))-64
    lev = str(i[4:5])

    if (area not in dict.keys()):
        dict[area] = {'maxrow': row,'maxcol': col,'maxlev':lev}
    else:
        if (dict[area]['maxrow'] < row):
            dict[area]['maxrow'] = row
        if (dict[area]['maxcol'] < col):
            dict[area]['maxcol'] = col
        if (dict[area]['maxlev'] < lev):
            dict[area]['maxlev'] = lev
print(dict)
        

# //////////////////////////////////simple gui
dic_area=[]
for i in dict:
    dic_area+=[i]
dic_pointer=0
canvas_width=1200
canvas_height=700
# global varibales
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
pic=simplegui._load_local_image('images.jpeg')
def draw_handler(canvas):
    Frame.set_canvas_background('black')
    loop_count=0
    k=dic_area[dic_pointer]
    a=canvas_width/dict[k]['maxcol']
    b=canvas_height/dict[k]['maxrow']
    for i in range(dict[k]['maxrow']):
        for j in range(dict[k]['maxcol']):
            canvas.draw_text(str(dic_area[dic_pointer]),(canvas_width//2-30,canvas_height//6-60),50,'black')
            canvas.draw_image(pic,(pic.get_width()//2,pic.get_height()//2),(pic.get_width(),pic.get_height()),(((a/2)+(a*j)),((b/2)+(b*i))),(a,b))
            canvas.draw_text('days: 15,id: 001,container-size: 20',(((a/8)+(a*j)),((b/2)+(b*i))),8,'black')
def key_handler(val):
    global dic_pointer
    if(val==simplegui.KEY_MAP['right']):
        if(dic_pointer<len(dic_area)-1):
            dic_pointer+=1
    if(val==simplegui.KEY_MAP['left']):
        if(dic_pointer>0):
            dic_pointer-=1
    
Frame=simplegui.create_frame('dockyard',canvas_width,canvas_height)
Frame.set_draw_handler(draw_handler)
Frame.set_keyup_handler(key_handler)
Frame.start()

