from rest_framework import serializers
from models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ['id', 'username', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
        )
        user.is_active = True
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)