from rest_framework import serializers
from .models import Loan
from users.models import User
from users.serializers import UserSerializer

class LoanRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'status', 'reason', 'created_at', 'updated_at']

#creating loan requests serializer
#User must exist, Amount > 0 and < 1,000,000, no duplicate pending requests

class CreateLoanRequestSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user_id', 'amount']

    def validate_amount(self, value):
       # print("Validating amount:", value)
        if value <= 0 or value >= 1_000_000:
            raise serializers.ValidationError("Amount should be > 0 and < 1,000,000")
        return value

    def validate(self, data):
        user_id = data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if Loan.objects.filter(user_id=user_id, status="PENDING").exists():
            raise serializers.ValidationError("User has a pending loan")

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data.pop('user')
        loan = Loan.objects.create(user=user, **validated_data)
        return loan
