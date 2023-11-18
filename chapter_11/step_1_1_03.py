from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_date_start_end(intv="D", rows=100):
    dt_end = datetime.now() - relativedelta(days=1)
    if intv == "D":
        dt_start = dt_end - relativedelta(days=rows)
        return dt_start.strftime("%Y%m%d"), dt_end.strftime("%Y%m%d")
    elif intv == "M":
        dt_start = dt_end - relativedelta(months=rows)
        return dt_start.strftime("%Y%m"), dt_end.strftime("%Y%m")


print(get_date_start_end(intv="D", rows=1))
print(get_date_start_end(intv="D", rows=100))

print(get_date_start_end(intv="M", rows=1))
print(get_date_start_end(intv="M", rows=100))
