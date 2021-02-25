from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'crypto', 'ceiling', 'alert_on_fall', 'alert_on_rise', 'added_by', 'created_date']
