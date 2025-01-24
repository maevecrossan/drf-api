from django.db import IntegrityError
from rest_framework import serializers
from followers.models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Follower model
    Create method handles the unique constraint on 'owner' and 'followed'
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        '''
        What fields to return from Like model
        '''
        model = Follower
        fields = [
            'id', 'owner', 'created_at',
            'followed', 'followed_name'
        ]

    def create(self, validated_data):
        '''
        Raise error for duplicate like attempts
        '''
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'posible duplicate'
            })
