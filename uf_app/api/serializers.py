from rest_framework import serializers

from uf_app.models import UFValue


class UFValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = UFValue
        fields = (
            'value', 'date'
        )
