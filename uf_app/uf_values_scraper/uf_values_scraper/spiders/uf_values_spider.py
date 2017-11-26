import pendulum
import scrapy
from scrapy import FormRequest

from uf_app.models import UFValue

MONTH_DAYS = list(map(str, range(1, 32)))


class UFValuesSpider(scrapy.Spider):
    name = "uf_values"
    start_urls = [
        'http://si3.bcentral.cl/'
        'Indicadoressiete/secure/Serie.aspx?gcode=UF'
        '&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNA'
        'GgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQ'
        'QBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLA'
        'F8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAe'
        'gBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhA'
        'EEAOABkAHkAZwAxAEEARAA=',
    ]
    uf_values = []

    def parse(self, response):
        years = response.css('#DrDwnFechas option::text').extract()

        selected_year = response.css(
            '#DrDwnFechas option[selected="selected"]::text'
        ).extract_first()

        next_year = str(int(selected_year) - 1)

        last_year = years[0]

        day = None
        month = None

        current_uf_values = UFValue.objects.values_list('value', 'date')

        for td in response.css('.Grid tr td'):
            text = td.css('::text').extract_first()

            if text in MONTH_DAYS:  # If cell is day of month
                day = int(text)  # Saved it
                month = 1  # Reboot year
                continue  # Continue in the next iteration
            else:
                value = text  # UF Value

                try:
                    date = pendulum.date.create(
                        int(selected_year),
                        month,
                        day
                    )
                except ValueError:
                    date = None

                if value is not None and date is not None:
                    value = float(value.replace('.', '').replace(',', '.'))

                    if (value, date) not in current_uf_values:
                        self.uf_values.append(
                            UFValue(
                                value=value,
                                date=date
                            )
                        )
                        yield {
                            "value": value,
                            "date": date
                        }

                month += 1  # Continue to the next month

        if int(next_year) >= int(last_year):
            yield FormRequest.from_response(
                response,
                formname="form1",
                formdata={
                    "DrDwnFechas": next_year
                }
            )

    def closed(self, reason):
        if self.uf_values:
            UFValue.objects.bulk_create(self.uf_values)
