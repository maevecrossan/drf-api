from rest_framework import serializers
from posts.models import Post

class PostSerializer(serializers.PostSerializer):
    ''' Serializes Profile Data from model '''

    owner = serializers.ReadOnlyField(source='owner.proile.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.proile.id')
    profile_image = serializers.ReadOnlyField(source='owner.proile.image.url')

    def validate_image(self, value):
        '''Check imported image dimensions'''
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        '''Return data if requested in owner'''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        '''What fields to return from Post model'''
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image', 'image_filter'
        ]
