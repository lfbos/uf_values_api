import pendulum


def string_to_date(date_string):
    year = int(date_string[:4])
    month = int(date_string[4:6])
    day = int(date_string[6:])

    return pendulum.date.create(year, month, day)


def pesos_to_uf(pesos, uf_value):
    return pesos / uf_value
