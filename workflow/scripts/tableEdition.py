from datetime import  datetime

class TableEdition:

    def date2datetime(date_input):
        # print(date_input)
        date = datetime. strptime(date_input, '%Y-%m-%d')
        time = datetime.min.time()
        datetime_final = datetime.combine(date, time)
        # print(datetime_final)
        return datetime_final