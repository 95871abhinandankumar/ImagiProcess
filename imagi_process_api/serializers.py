from rest_framework import serializers
from .models import RequestStatus

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = ['request_id', 'status', 'result']
