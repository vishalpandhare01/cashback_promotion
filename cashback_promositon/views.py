from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status , response 
from django.shortcuts import get_object_or_404
from .serializer import CashbackRuleSerializer , CashbackTransactionSerializer
from .models import CashbackRule ,CashbackTransaction
from datetime import date ,datetime
from django.db.models import Sum
from .utils import parse_float

# Cashback rules view
class CashRuleView(APIView):
    def post(self , request):
        serializer = CashbackRuleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request):
        data = CashbackRule.objects.all()
        serializer = CashbackRuleSerializer(data,many=True)
        return response.Response(data= serializer.data, status=status.HTTP_200_OK)
       
        
    def put(self, request, pk):
        rule = get_object_or_404(CashbackRule, pk=pk)
        serializer = CashbackRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CashbackTransactionView(APIView):
    def post(self, request):
        order_amount = request.data.get("order_amount")
        rule_id = request.data.get("cashback_rule")
        customer_id = request.data.get("customer_id")
        order_id = request.data.get("order_id")

        # Validate required fields
        if not customer_id:
            return response.Response({"error": "customer_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not order_amount:
            return response.Response({"error": "order_amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not rule_id:
            return response.Response({"error": "cashback_rule is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if customer already has a transaction
        existing_tx = CashbackTransaction.objects.filter(customer_id=customer_id).first()
        if existing_tx:
            return response.Response({"error": "Customer transaction already done"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse and validate amount
        order_amount = parse_float(order_amount, "order_amount")

        # Fetch rule
        rule_data = CashbackRule.objects.filter(id=rule_id).first()
        if not rule_data:
            return response.Response({"error": "Invalid cashback_rule"}, status=status.HTTP_400_BAD_REQUEST)

        today = date.today()
        is_active = rule_data.status == "active"
        is_within_dates = rule_data.valid_from <= today <= rule_data.valid_to
        is_min_amount = order_amount >= rule_data.min_order_value

        if is_active and is_within_dates and is_min_amount:
            cashback_percentage = float(rule_data.cashback_percentage)
            calculated_cashback = (cashback_percentage / 100) * order_amount

            payload = {
                "order_id":order_id,
                "customer_id": customer_id,
                "order_amount": order_amount,
                "cashback_amount": calculated_cashback,
                "cashback_rule": rule_id,
            }

            serializer = CashbackTransactionSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response.Response(
            {"error": "Rule not applicable: inactive, expired, or minimum order not met"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        transactions = CashbackTransaction.objects.all()
        serializer = CashbackTransactionSerializer(transactions, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
   
# Cashback Analytics
class CashbackAnalyticsView(APIView):
    def get( self , request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
            
        transactions = CashbackTransaction.objects.all()

        if start_date:
            transactions = transactions.filter(created_at__gte=start_date)
        if end_date:
            transactions = transactions.filter(created_at__lte=end_date)
            
        total_issued = transactions.filter(status='issued').aggregate(Sum('cashback_amount'))['cashback_amount__sum'] or 0
        total_pending = transactions.filter(status='pending').aggregate(Sum('cashback_amount'))['cashback_amount__sum'] or 0
        total_redeemed = transactions.filter(status='redeemed').aggregate(Sum('cashback_amount'))['cashback_amount__sum'] or 0
            
        recent_transactions = CashbackTransactionSerializer(transactions.order_by('-created_at')[:10], many=True).data
            
        data = {
            "total_cashback_issued": total_issued,
            "total_cashback_pending": total_pending,
            "total_cashback_redeemed": total_redeemed,
            "recent_transactions": recent_transactions
        }

        return response.Response(data, status=status.HTTP_200_OK)
        
    
        
        