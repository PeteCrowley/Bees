import datetime


YEAR_0, MONTH_0, DAY_0 = (2022, 1, 1)
start_date = datetime.datetime(YEAR_0, MONTH_0, DAY_0)


def day_to_date(day: int) -> datetime.datetime:
    return start_date + datetime.timedelta(days=day)


def date_to_day(date) -> int:
    if type(date).__name__ == "tuple":
        return (datetime.datetime(date[0], date[1], date[2]) - start_date).days
    else:
        return (date - start_date).days



