from rest_framework import serializers

from uf_app.models import UFValue


class UFValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = UFValue
        fields = (
            'value', 'date'
        )


class UFPriceSerializer(serializers.Serializer):
    value = serializers.DecimalField(decimal_places=3, max_digits=12)
    date = serializers.DateField()
    price = serializers.DecimalField(decimal_places=3, max_digits=12, required=False)
