import pandas as pd
data = pd.read_csv("Yardlocations.csv")
def area_size():
    def max_row():
        max_row_dict = {}
        loc = data['Location']
        for i in loc:

            area = i[0:1]
            row = int(i[1:3])
            if area not in max_row_dict:
                max_row_dict[area] = {'maxrow': row}
            else:
                if (max_row_dict[area]['maxrow'] < row):
                    max_row_dict[area]['maxrow'] = row

        print(max_row_dict)

    def determining_size():

        area = data['Area']
        dict = {}
        for i in area:
            if (i not in dict.keys()):
                dict[i] = 1
            else:
                dict[i] += 1
        print(dict)
        print(area)

    def determining_size():
        def Num(x):
            if x == 'A':
                return 1
            if x == 'B':
                return 2
            if x == 'C':
                return 3
            if x == 'D':
                return 4
            if x == 'E':
                return 5
            if x == 'F':
                return 6
        klst = list(dict.keys())
        for c in range(len(klst)):
            print(klst[c])
            print(max_row_dict[klst[c]])
            print(f"maxcol:{Num((max_col_dict[klst[c]])['maxcol'])}")
            print(max_lvl_dict[klst[c]])

    def max_col():
        max_col_dict = {}
        loc = data['Location']
        for i in loc:

            area = i[0:1]
            col = str(i[3:4])
            if area not in max_col_dict:
                max_col_dict[area] = {'maxcol': col}
            else:
                if (max_col_dict[area]['maxcol'] < col):
                    max_col_dict[area]['maxcol'] = col

        print(max_col_dict)
    def max_level():
        max_col_dict = {}
        loc = data['Location']
        for i in loc:

            area = i[0:1]
            col = str(i[3:4])
            if area not in max_col_dict:
                max_col_dict[area] = {'maxcol': col}
            else:
                if (max_col_dict[area]['maxcol'] < col):
                    max_col_dict[area]['maxcol'] = col

        print(max_col_dict)

