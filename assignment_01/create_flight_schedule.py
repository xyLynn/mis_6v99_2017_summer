# -*- coding: utf-8 -*-
"""
Created on Sat Jul  1 10:48:31 2017

@author: Lynn
"""


t1 = [['T1','AUS','HOU','360']]
t2 = [['T2','DAL','HOU','360']]
t3 = [['T3','DAL','HOU','360']]
t4 = [['T4','HOU','AUS','360']] 
t5 = [['T5','HOU','DAL','360']]
t6 = [['T6','HOU','DAL','360']]
T = [t1, t2, t3, t4, t5, t6]

aus_dal = 50
aus_hou = 45
dal_hou = 65
gdtime = {'HOU':35, 'AUS':25, 'DAL':30}


def flight(j):
    for i in range(0,6):
        if T[i][j][2] == T[i][j][1]:
            nextone = T[i][j]
            nextone.insert(4, '0')
            nextone.insert(5, '0')
            
            T[i].append(nextone)
            
        elif T[i][j][2] == 'HOU':
            if T[i][j][1] == 'AUS':
                arrtime = aus_hou + int(T[i][j][3])
                time = gdtime[T[i][j][2]] + arrtime
                T[i][j].insert(4, str(arrtime))
                T[i][j].insert(5, str(time))
                
                nextone = T[i][j][:]
                nextone[1] = 'HOU'
                nextone[2] = 'AUS'
                nextone[3] = T[i][j][5]
                nearrtime = aus_hou + time
                netime = gdtime[T[i][j][1]] + nearrtime
                nextone[4] = str(nearrtime)
                nextone[5] = str(netime)
                
                T[i].append(nextone)
            
            elif T[i][j][1] == 'DAL':
                arrtime = dal_hou + int(T[i][j][3])
                time = gdtime[T[i][j][2]] + arrtime
                T[i][j].insert(4, str(arrtime))
                T[i][j].insert(5, str(time))

                nextone = T[i][j][:]
                nextone[1] = 'HOU'
                nextone[2] = 'DAL'
                nextone[3] = T[i][j][5]
                nearrtime = dal_hou + time
                netime = gdtime[T[i][j][1]] + nearrtime
                nextone[4] = str(nearrtime)
                nextone[5] = str(netime)

                T[i].append(nextone)
                
            else:
                continue
        
        elif T[i][j][2] == 'DAL':
            if T[i][j][1] == 'AUS':
                arrtime = aus_dal + int(T[i][j][3])
                time = gdtime[T[i][j][2]] + arrtime
                T[i][j].insert(4, str(arrtime))
                T[i][j].insert(5, str(time))

                nextone = T[i][j][:]
                nextone[1] = 'DAL'
                nextone[2] = 'AUS'
                nextone[3] = T[i][j][5]
                nearrtime = aus_dal + time
                netime = gdtime[T[i][j][1]] + nearrtime
                nextone[4] = str(nearrtime)
                nextone[5] = str(netime)

                T[i].append(nextone)
                
            elif T[i][j][1] == 'HOU':
                arrtime = dal_hou + int(T[i][j][3])
                time = gdtime[T[i][j][2]] + arrtime
                T[i][j].insert(4, str(arrtime))
                T[i][j].insert(5, str(time))

                nextone = T[i][j][:]
                nextone[1] = 'DAL'
                nextone[2] = 'HOU'
                nextone[3] = T[i][j][5]
                nearrtime = dal_hou + time
                netime = gdtime[T[i][j][1]] + nearrtime
                nextone[4] = str(nearrtime)
                nextone[5] = str(netime)

                T[i].append(nextone)
                
            else:
                continue
                
                
        elif T[i][j][2] == 'AUS':
            if T[i][j][1] == 'HOU':
                arrtime = aus_hou + int(T[i][j][3])
                time = gdtime[T[i][j][2]] + arrtime
                T[i][j].insert(4, str(arrtime))
                T[i][j].insert(5, str(time))

                nextone = T[i][j][:]
                nextone[1] = 'AUS'
                nextone[2] = 'HOU'
                nextone[3] = T[i][j][5]
                nearrtime = aus_hou + time
                netime = gdtime[T[i][j][1]] + nearrtime
                nextone[4] = str(nearrtime)
                nextone[5] = str(netime)

                T[i].append(nextone)
                
            elif T[i][j][1] == 'DAL':
                arrtime = aus_dal + int(T[i][j][3])
                time = gdtime[T[i][j][2]] + arrtime
                T[i][j].insert(4, str(arrtime))
                T[i][j].insert(5, str(time))

                nextone = T[i][j][:]
                nextone[1] = 'AUS'
                nextone[2] = 'DAL'
                nextone[3] = T[i][j][5]
                nearrtime = aus_dal + time
                netime = gdtime[T[i][j][1]] + nearrtime
                nextone[4] = str(nearrtime)
                nextone[5] = str(netime)

                T[i].append(nextone)
                
            else:
                continue
                
        
                
    return(T)

flight(0)


def maxvalue(k):
    lst1 = [item[k] for item in T]
    lst2 = [item[5] for item in lst1]
    detime = max(lst2)
    return detime


t11 = ['T1', 'AUS', 'DAL', maxvalue(1)]
t21 = ['T2', 'DAL', 'HOU', maxvalue(1)]
t31 = ['T3', 'DAL', 'HOU', maxvalue(1)]
t41 = ['T4', 'HOU', 'DAL', maxvalue(1)] 
t51 = ['T5', 'HOU', 'AUS', maxvalue(1)]
t61 = ['T6', 'HOU', 'HOU', maxvalue(1)]
T[0].append(t11)
T[1].append(t21)
T[2].append(t31)
T[3].append(t41)
T[4].append(t51)
T[5].append(t61)

flight(2)


t12 = ['T1', 'AUS', 'DAL', maxvalue(3)]
t22 = ['T2', 'DAL', 'HOU', maxvalue(3)]
t32 = ['T3', 'DAL', 'HOU', maxvalue(3)]
t42 = ['T4', 'HOU', 'DAL', maxvalue(3)] 
t62 = ['T6', 'HOU', 'AUS', maxvalue(3)]
t52 = ['T5', 'HOU', 'HOU', maxvalue(3)]
T[0].append(t12)
T[1].append(t22)
T[2].append(t32)
T[3].append(t42)
T[4].append(t52)
T[5].append(t62)

flight(4)


t13 = ['T1', 'AUS', 'DAL', maxvalue(5)]
t23 = ['T2', 'DAL', 'HOU', maxvalue(5)]
t33 = ['T3', 'DAL', 'HOU', maxvalue(5)]
t53 = ['T5', 'HOU', 'DAL', maxvalue(5)] 
t63 = ['T6', 'HOU', 'AUS', maxvalue(5)]
t43 = ['T4', 'HOU', 'HOU', maxvalue(5)]
T[0].append(t13)
T[1].append(t23)
T[2].append(t33)
T[3].append(t43)
T[4].append(t53)
T[5].append(t63)

flight(6)


t14 = ['T1', 'AUS', 'HOU', maxvalue(7)]
t24 = ['T2', 'DAL', 'HOU', maxvalue(7)]
t34 = ['T3', 'DAL', 'HOU', maxvalue(7)]
t44 = ['T4', 'HOU', 'AUS', maxvalue(7)] 
t54 = ['T5', 'HOU', 'DAL', maxvalue(7)]
t64 = ['T6', 'HOU', 'DAL', maxvalue(7)]
T[0].append(t14)
T[1].append(t24)
T[2].append(t34)
T[3].append(t44)
T[4].append(t54)
T[5].append(t64)

flight(8)

for i in range(0,6):
    for j in range(0,10):
        T[i][j][4] = str(int(int(T[i][j][4])/60)*100+int(int(T[i][j][4])%60)).zfill(4)
        T[i][j][3] = str(int(int(T[i][j][3])/60)*100+int(int(T[i][j][3])%60)).zfill(4)
        del T[i][j][-1] 
    del T[i][-1] 

del T[5][2:4]
del T[4][4:6]
del T[3][6:8]
 
flight_schedule = sum(T, [])

print(flight_schedule)

csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
file_name = 'flight_schedule.csv'
def print_flight_schedule(fn, csv_hdr, flt_sched):
    with open(fn,'wt') as f:
        print(csv_hdr, file=f)
        for s in flt_sched:
            print(','.join(s), file=f)

print_flight_schedule(file_name, csv_header, flight_schedule)        

        