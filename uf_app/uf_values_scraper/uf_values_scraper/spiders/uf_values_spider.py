import logging

import pendulum
import scrapy
from scrapy import FormRequest

from uf_app.models import UFValue

MONTH_DAYS = list(map(str, range(1, 32)))

logger = logging.getLogger(__name__)


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
        #  Tag to parse only current year
        only_current_year = getattr(self, 'only_current_year', False)

        #  Get all the years with data available
        years = response.css('#DrDwnFechas option::text').extract()

        #  First iteration always will be current year
        selected_year = response.css(
            '#DrDwnFechas option[selected="selected"]::text'
        ).extract_first()

        #  Save next year
        next_year = str(int(selected_year) - 1)

        #  Save last year
        last_year = years[0]

        day = None
        month = None

        #  Get saved values
        current_uf_values = UFValue.objects.values_list('date')

        #  Iterate over all columns
        for td in response.css('.Grid tr td'):
            #  Extract text
            text = td.css('::text').extract_first()

            if text in MONTH_DAYS:  # If cell is day of month
                day = int(text)  # Saved it
                month = 1  # Reboot year
                continue  # Continue in the next iteration
            else:
                value = text  # UF Value

                #  Parse the year
                #  Prevent exception parsing date values
                try:
                    date = pendulum.date.create(
                        int(selected_year),
                        month,
                        day
                    )
                except ValueError:
                    date = None

                if value is not None and date is not None:
                    #  Change uf value format
                    value = float(value.replace('.', '').replace(',', '.'))

                    #  If date not in current values
                    if date not in current_uf_values:
                        #  Insert new uf value
                        self.uf_values.append(
                            UFValue(
                                value=value,
                                date=date
                            )
                        )
                    elif only_current_year:
                        #  Check values for current year (some probably changed)
                        UFValue.objects.filter(
                            date=date  # Filter by date
                        ).exclude(
                            value=value  # Exclude the value if is equal than before
                        ).update(
                            value=value  # Update
                        )

                month += 1  # Continue to the next month

        # If next year is less greater or equal than last year
        # And is not only current year
        # Keep parsing
        if int(next_year) >= int(last_year) and not only_current_year:
            yield FormRequest.from_response(
                response,
                formname="form1",
                formdata={
                    "DrDwnFechas": next_year
                }
            )

    def closed(self, reason):
        if self.uf_values:
            uf_values_created = UFValue.objects.bulk_create(self.uf_values)
            logger.info(
                'UF Values created {}'.format(
                    len(uf_values_created)
                )
            )
