from rest_framework.serializers import ModelSerializer

from .models import User, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
