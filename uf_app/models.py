import pendulum
from django.db import models

from django.utils.translation import ugettext as _


class UFValue(models.Model):
    value = models.FloatField(verbose_name=_('Value in Chilean pesos'))
    date = models.DateField(unique=True, verbose_name=_('Value date'))

    def __str__(self):
        date = pendulum.date.instance(self.date)
        return '{}: {} CLP.'.format(
            date.to_formatted_date_string(),
            self.value
        )

    class Meta:
        verbose_name = _('UF value')
        verbose_name_plural = _('UF values')
        ordering = ['-date']
