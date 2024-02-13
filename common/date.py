
def handle_day_out_of_range(date_str):
    year=date_str.split("-")[-3]
    month=date_str.split("-")[-2]
    day=date_str.split("-")[-1]

    day=int(day)-1
    date_str=year+"-"+month+"-"+str(day)
    return date_str
