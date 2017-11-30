import pendulum


def pesos_to_uf(pesos, uf_value):
    return pesos / uf_value


def get_valid_date(year, month, day):
    date = None

    try:
        date = pendulum.date.create(
            year,
            month,
            day
        )
    except ValueError:
        pass

    return date
