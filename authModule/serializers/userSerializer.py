from authModule.models.user import User
from authModule.models.account import Account
from rest_framework import serializers
from authModule.serializers.accountSerializer import AccountSerializer

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'account']

    def create(self, validated_data):
        accountData = validated_data.pop('account')
        userInstance = User.objects.create(**validated_data)
        
        Account.objects.create(user=userInstance, **accountData)
        return userInstance

    def to_representation(self, instance):
        user = User.objects.get(id=instance.id)
        account = Account.objects.get(user=instance.id)
        return {
            'id': user.id,
            'username': user.username,
            'name' : user.name,
            'email' : user.email,
            'account': {
                'id' : account.id,
                'balance': account.balance,
                'lastChangeDate': account.lastChangeDate,
                'isActive': account.isActive
            }
        }