from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    '''
    Serializes Comment model data.
    Adds three extra fields when returning a list of Comment instances.
    '''
    owner = serializers.ReadOnlyField(source='owner.proile.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.proile.id')
    profile_image = serializers.ReadOnlyField(source='owner.proile.image.url')

    def get_is_owner(self, obj):
        '''
        Return data if requester = owner
        '''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        '''
        What fields to return from Post model
        '''
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'post', 'created_at', 'updated_at', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):
    '''
    Serializer for the Comment model used in Detail view
    Post is a read only field so that we dont have to set it on each update
    '''
    post = serializers.ReadOnlyField(source='post.id')
