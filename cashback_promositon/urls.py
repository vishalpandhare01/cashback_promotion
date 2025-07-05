from django.urls import path
from .views import CashRuleView ,CashbackTransactionView , CashbackAnalyticsView

urlpatterns = [
    path('cashback-rules', CashRuleView.as_view()),
    path('cashback-rules/<int:pk>', CashRuleView.as_view()),
    path('transactions', CashbackTransactionView.as_view()),
    path('analytics', CashbackAnalyticsView.as_view()),
]



