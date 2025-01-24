from rest_framework import serializers
from followers.models import Follower
from .models import Profile

# A serializer in Django REST Framework (DRF) is responsible
# for converting complex data types (like Django model instances)
# into Python data types that can be easily rendered into JSON
# or other content types. It also handles deserialization,
# meaning it converts incoming JSON data into Django model instances.


class ProfileSerializer(serializers.ModelSerializer):
    ''' Serializes Profile Data from model '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # id field is created automatically with (model.Model).

    def get_following_id(self, obj):
        '''
        Assigns an id when following a user.
        '''
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # print(following)
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'content', 'image', 'is_owner', 'following_id'
        ]
