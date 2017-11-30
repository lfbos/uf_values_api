import logging
from decimal import Decimal

import scrapy
from scrapy import FormRequest

from uf_app.models import UFValue
from uf_app.utils import get_valid_date

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
        only_current_year = getattr(self, 'only_current_year', False)

        years = response.css('#DrDwnFechas option::text').extract()

        selected_year = response.css(
            '#DrDwnFechas option[selected="selected"]::text'
        ).extract_first()

        previous_year = str(int(selected_year) - 1)

        last_year = years[0]

        current_uf_values = UFValue.objects.values('value', 'date')

        self._iterate_and_validate_columns(selected_year, current_uf_values, response)

        if int(previous_year) >= int(last_year) and not only_current_year:
            yield FormRequest.from_response(
                response,
                formname="form1",
                formdata={
                    "DrDwnFechas": previous_year
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

    def _iterate_and_validate_columns(self, selected_year, current_uf_values, response):
        only_current_year = getattr(self, 'only_current_year', False)

        day = None
        month = None

        current_dates = list(map(lambda uf_value: uf_value.get('date'), current_uf_values))

        for td in response.css('.Grid tr td'):
            cell = td.css('::text').extract_first()

            if cell in MONTH_DAYS:
                day = int(cell)  # Day of month
                month = 1
                continue
            else:
                uf_value = cell  # UF Value

                date = get_valid_date(int(selected_year), month, day)

                if uf_value is not None and date is not None:
                    uf_value = Decimal(uf_value.replace('.', '').replace(',', '.'))

                    if date not in current_dates:
                        self.uf_values.append(
                            UFValue(
                                value=uf_value,
                                date=date
                            )
                        )
                    elif only_current_year:
                        uf = list(
                            filter(
                                lambda uf_value: uf_value.get('date') == date,
                                current_uf_values
                            )
                        )[0]

                        current_value = uf.get('value')

                        if uf_value != current_value:
                            UFValue.objects.filter(
                                date=date
                            ).update(
                                value=uf_value
                            )

                            logger.info(
                                'Value for the date {} updated: {}'.format(
                                    date,
                                    uf_value
                                )
                            )

                month += 1
