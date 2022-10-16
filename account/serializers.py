from rest_framework import serializers
from api.models import *
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields = '__all__' #['id', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_active']