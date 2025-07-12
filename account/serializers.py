from rest_framework import serializers
from account.models import User


class EmailPasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Эта почта уже используется")
        return data

class EmailCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField(write_only=True)

    def validate(self, data):
        if len(str(data['code'])) < 6:
            raise serializers.ValidationError("Неверная длина кода")

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)

    def validate(self, data):
        if len(data['username']) < 3:
            raise serializers.ValidationError("Слишком короткое имя")
        if len(data['username']) > 30:
            raise serializers.ValidationError("Слишком длинное имя")