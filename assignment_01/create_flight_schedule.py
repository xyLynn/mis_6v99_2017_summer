csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
file_name = 'flight_schedule.csv'

def print_flight_schedule(fn, csv_hdr, flt_sched):
    with open(fn,'wt') as f:
        print(csv_hdr, file=f)
        for s in flt_sched:
            print(','.join(s), file=f)

flight_schedule = [['T1','AUS','DAL','0600','0650'],
 ['T2','DAL','HOU','0600','0705'],
['T3','DAL','HOU','0600','0705']]
addition = [['T4','HOU','AUS','0600','0645'],['T5','HOU','DAL','0600','0705'],['T6','HOU','DAL','0600','0705']]
flight_schedule.extend(addition)
print(flight_schedule)

print_flight_schedule(file_name, csv_header, flight_schedule)


