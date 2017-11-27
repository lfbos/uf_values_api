import pendulum
from django.db import IntegrityError
from django.test import TestCase

from uf_app.models import UFValue


class UFValueModelTest(TestCase):
    def test_cannot_save_empty_uf_value(self):
        with self.assertRaises(IntegrityError):
            UFValue.objects.create()

    def test_create_valid_uf_value(self):
        value = 26348.83
        date = pendulum.date.create(2017, 1, 1)

        uf_value = UFValue.objects.create(
            value=value,
            date=date
        )

        self.assertEqual(value, uf_value.value)
        self.assertEqual(date, uf_value.date)

    def test_cannot_create_equal_values(self):
        value = 26348.83
        date = pendulum.date.create(2017, 1, 1)

        with self.assertRaises(IntegrityError):
            uf_values = [
                UFValue(value=value, date=date),
                UFValue(value=value, date=date)
            ]

            UFValue.objects.bulk_create(uf_values)

    def test_cannot_create_equal_dates(self):
        value1 = 26348.83
        date = pendulum.date.create(2017, 1, 1)
        value2 = 27348.83

        with self.assertRaises(IntegrityError):
            uf_values = [
                UFValue(value=value1, date=date),
                UFValue(value=value2, date=date)
            ]

            UFValue.objects.bulk_create(uf_values)

    def test_can_create_different_values(self):
        value1 = 26348.83
        date1 = pendulum.date.create(2017, 1, 1)

        value2 = 26349.68
        date2 = pendulum.date.create(2017, 1, 2)

        uf_values = [
            UFValue(value=value1, date=date1),
            UFValue(value=value2, date=date2)
        ]

        uf_objects = UFValue.objects.bulk_create(uf_values)

        self.assertEqual(len(uf_objects), 2)
