from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

FloatValidator = RegexValidator(
    regex=r'^[0-9]+\.?[0-9]+$'
)

# Source:
# https://stackoverflow.com/questions/4766845/yyyymmdd-date-format-regular-expression-to-validate-a-date-in-c-sharp-net
DateValidator = RegexValidator(
    regex=r'^(?:(?:(?:(?:(?:[13579][26]|[2468][048])00)'
          r'|(?:[0-9]{2}(?:(?:[13579][26])|(?:[2468][048]|0[48]))))'
          r'(?:(?:(?:09|04|06|11)(?:0[1-9]|1[0-9]|2[0-9]|30))'
          r'|(?:(?:01|03|05|07|08|10|12)(?:0[1-9]|1[0-9]|2[0-9]|3[01]))'
          r'|(?:02(?:0[1-9]|1[0-9]|2[0-9]))))'
          r'|(?:[0-9]{4}(?:(?:(?:09|04|06|11)'
          r'(?:0[1-9]|1[0-9]|2[0-9]|30))'
          r'|(?:(?:01|03|05|07|08|10|12)'
          r'(?:0[1-9]|1[0-9]|2[0-9]|3[01]))|(?:02(?:[01][0-9]|2[0-8])))))$'
)


def is_valid_float(value):
    try:
        FloatValidator(value)
    except ValidationError:
        return False
    else:
        return True


def is_valid_date(value):
    try:
        DateValidator(value)
    except ValidationError:
        return False
    else:
        return True
