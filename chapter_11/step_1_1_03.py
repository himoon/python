from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_date_start_end(intv="D", rows=100):
    if intv == "D":
        dt_end = datetime.now() - relativedelta(days=1)
        dt_start = dt_end - relativedelta(days=rows - 1)
        return dt_start.strftime("%Y%m%d"), dt_end.strftime("%Y%m%d")
    elif intv == "M":
        dt_end = datetime.now() - relativedelta(months=1)
        dt_start = dt_end - relativedelta(months=rows - 1)
        return dt_start.strftime("%Y%m"), dt_end.strftime("%Y%m")


print(get_date_start_end(intv="D", rows=1))
print(get_date_start_end(intv="D", rows=100))

print(get_date_start_end(intv="M", rows=1))
print(get_date_start_end(intv="M", rows=100))
