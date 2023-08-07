from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # This means that password information can be written to this field when creating a new user, but it will not be included in the serialization
        extra_kwargs = {'password':{'write_only':True}}
    #To hash the password
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
