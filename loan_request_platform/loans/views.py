from django.shortcuts import render
from .models import Loan
from .serializers import CreateLoanRequestSerializer, LoanRequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging
import requests

# Create your views here.

#view loans/id
class ViewLoanRequest(APIView):
    def get(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanRequestSerializer(loan)
        return Response(serializer.data)


#create a new loan request for a user

logger = logging.getLogger(__name__)

class CreateLoanRequestView(APIView):
    def post(self, request):
        serializer = CreateLoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save()

            # Prepare request_data for credit scoring API
            request_data = {
                'loan_id': loan.id,
                'amount': float(loan.amount),
                'user': {'name': loan.user.name, 'email_address': loan.user.email_address},
                'callback_url': f"{settings.SITE_URL}/webhook/credit-score"
            }

            try:
                response = requests.post(settings.CREDIT_API_URL, json=request_data, timeout=5)
                logger.info(f"Sent scoring request for loan {loan.id} with status {response.status_code}")
            except Exception:
                logger.exception(f"Failed to send scoring request for loan {loan.id}")

            return Response(LoanRequestSerializer(loan).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#delete loan request
class LoanDeleteView(APIView):
    def delete(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            return Response({'detail': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        loan.delete()
        return Response({'detail': f'Loan {pk} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CreditScoreWebhookView(APIView):
    def post(self, request):
        data = request.data
        loan_id = data.get('loan_id')
        status_ = data.get('status')
        reason = data.get('reason', '')

        if not loan_id or not status_:
            return Response({'detail': 'loan_id and loan status are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            logger.warning(f"Webhook has been received with an unknown loan_id: {loan_id}")
            return Response({'detail': 'Unknown loan_id'}, status=status.HTTP_400_BAD_REQUEST)

        loan.status = status_
        loan.reason = reason
        loan.save()

        logger.info(f"Loan {loan_id} updated via webhook to status {status_}")
        return Response({'detail': 'Loan status updated!'})