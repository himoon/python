from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_date_start_end(rows=100):
    dt_end = datetime.now() - relativedelta(days=1)
    dt_start = dt_end - relativedelta(days=rows)
    return dt_start.strftime("%Y%m%d"), dt_end.strftime("%Y%m%d")


print(get_date_start_end(rows=1))
print(get_date_start_end(rows=100))
