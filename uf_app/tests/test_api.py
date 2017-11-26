import pendulum
from django.test import TestCase

from uf_app.api.views import (
    INVALID_DATE_ERROR_MESSAGE, INVALID_VALUE_ERROR_MESSAGE
)
from uf_app.models import UFValue


class UFValueListAPITest(TestCase):
    base_url = '/uf/list/'

    def test_get_returns_json_200(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_items_for_correct_uf_values(self):
        value = 26348.83
        date = pendulum.date.create(2017, 1, 1)

        UFValue.objects.create(value=value, date=date)

        response = self.client.get(self.base_url)
        self.assertEqual(
            response.json(),
            [{
                "value": value,
                "date": date.to_date_string()
            }]
        )

    def test_filter_by_year(self):
        value1 = 26348.83
        date1 = pendulum.date.create(2017, 1, 1)

        value2 = 26347.7
        date2 = pendulum.date.create(2017, 1, 2)

        uf_values = [
            UFValue(value=value1, date=date1),
            UFValue(value=value2, date=date2)
        ]

        UFValue.objects.bulk_create(uf_values)

        response = self.client.get('{}?year=2017'.format(self.base_url))

        self.assertEqual(
            response.json(),
            [
                {
                    "value": value2,
                    "date": date2.to_date_string()
                },
                {
                    "value": value1,
                    "date": date1.to_date_string()
                }
            ]
        )

    def test_filter_by_date(self):
        value1 = 26348.83
        date1 = pendulum.date.create(2017, 1, 1)

        value2 = 26347.7
        date2 = pendulum.date.create(2017, 1, 2)

        uf_values = [
            UFValue(value=value1, date=date1),
            UFValue(value=value2, date=date2)
        ]

        UFValue.objects.bulk_create(uf_values)

        response = self.client.get(
            '{}?date={}'.format(
                self.base_url, date1.to_date_string()
            )
        )

        self.assertEqual(
            response.json(),
            [
                {
                    "value": value1,
                    "date": date1.to_date_string()
                }
            ]
        )


class UFPriceAPITest(TestCase):
    base_url = '/uf/price/'

    def test_get_empty_response_if_url_does_not_have_parameters(self):
        response = self.client.get(self.base_url)

        self.assertEqual(
            response.json(),
            {}
        )

    def test_error_with_invalid_date_parameter(self):
        value = 200000
        date = 'date'
        response = self.client.get(
            '{}?value={}&date={}'.format(
                self.base_url,
                value,
                date
            )
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json().get('detail'), INVALID_DATE_ERROR_MESSAGE)

    def test_error_with_invalid_value_parameter(self):
        value = '1212412f'
        date = '20170101'

        response = self.client.get(
            '{}?value={}&date={}'.format(
                self.base_url,
                value,
                date
            )
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json().get('detail'), INVALID_VALUE_ERROR_MESSAGE)

    def test_error_uf_not_found(self):
        value = 20000.124
        date = '20170101'

        response = self.client.get(
            '{}?value={}&date={}'.format(
                self.base_url,
                value,
                date
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_valid_uf_price_response(self):
        chilean_pesos = 30000
        value = 26348.83
        date = pendulum.date.create(2017, 1, 1)

        UFValue.objects.create(value=value, date=date)

        response = self.client.get(
            '{}?value={}&date={}'.format(
                self.base_url,
                chilean_pesos,
                date.strftime('%Y%m%d')
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json().get('price'))
