from django.urls import path
from .views import ViewLoanRequest, CreateLoanRequestView, LoanDeleteView, CreditScoreWebhookView

urlpatterns = [
    path('loan-request/', CreateLoanRequestView.as_view(), name='loan-create'),
    path('<int:pk>/', ViewLoanRequest.as_view(), name='view-loan'),
    path('<int:pk>/delete/', LoanDeleteView.as_view(), name='loan-delete'),
    path('webhook/credit-score/', CreditScoreWebhookView.as_view(), name='webhook-credit-score'),
]    
