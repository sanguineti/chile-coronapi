from coronapi.constants import INE_CHILEAN_HABITANTS


def _per_million(number):
    return round(number * 1000000 / INE_CHILEAN_HABITANTS, 1)


def get_per_one_million(confirmed, deaths):
    return (_per_million(confirmed), _per_million(deaths))


def undotter(string_number):
    return int(string_number.replace(".", ""))
