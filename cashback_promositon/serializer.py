from rest_framework.serializers import Serializer , ModelSerializer
from .models import CashbackRule ,CashbackTransaction 
class CashbackRuleSerializer(ModelSerializer):
    class Meta:
        model = CashbackRule
        fields = '__all__'

class CashbackTransactionSerializer(ModelSerializer):
    class Meta:
        model = CashbackTransaction
        fields = '__all__'
