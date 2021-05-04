import datetime
def get_hrs(d1,d2,t1,t2):
    d1_t1 = d1+' '+t1
    d2_t2 = d2+' '+t2
    do1 = datetime.datetime.strptime(d1_t1, '%Y-%m-%d %H:%M:%S')
    do2 = datetime.datetime.strptime(d2_t2, '%Y-%m-%d %H:%M:%S')

    total_hrs = ((do2-do1).total_seconds())/(60*60)

    return total_hrs